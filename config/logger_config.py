import logging
import sys
import traceback
import json
# is_ubuntu 함수를 직접 임포트
from config.env_loader import is_ubuntu

# 환경 변수 로드는 ENV 객체를 통해 이루어지므로 여기서는 is_ubuntu만 사용
# environment = "DEV" if not ENV["IS_PROD"] else "PROD" # 이 줄 제거

# Filter to add default values for missing context keys
class ContextFilter(logging.Filter):
    DEFAULT_CONTEXT = {
        'status': '-', 'method': '-', 'host': '-', 'remoteIp': '-', 'userAgent': '-',
    }
    def filter(self, record):
        for key, value in self.DEFAULT_CONTEXT.items():
            if not hasattr(record, key):
                setattr(record, key, value)
        return True

# JSON 형식으로 로그를 출력하는 커스텀 포매터 (이전과 동일)
class JsonFormatter(logging.Formatter):
    default_time_format = '%Y-%m-%dT%H:%M:%S.%f'
    def __init__(self, fmt=None, datefmt=None, style='%', validate=True, *, defaults=None):
        super().__init__(fmt=fmt, datefmt=datefmt or self.default_time_format, style=style, validate=validate, defaults=defaults)
    def format(self, record):
        log_record = {
            'timestamp': self.formatTime(record, self.datefmt),
            'level': record.levelname,
            'name': record.name,
            'process': record.process,
            'message': record.getMessage(),
        }
        for key in ContextFilter.DEFAULT_CONTEXT:
            if hasattr(record, key):
                log_record[key] = getattr(record, key)
        if record.exc_info:
            log_record['traceback'] = self.formatException(record.exc_info)
        elif record.exc_text:
             log_record['traceback'] = record.exc_text
        return json.dumps(log_record, ensure_ascii=False)

# ERROR 레벨 이상일 때 자동으로 Traceback을 포함하는 커스텀 포매터 (재추가)
class ErrorTracebackFormatter(logging.Formatter):
    def format(self, record):
        if record.levelno >= logging.ERROR and not record.exc_info:
            exc_info = sys.exc_info()
            if exc_info and exc_info[0] is not None:
                record.exc_info = exc_info
        formatted_message = super().format(record)
        # record.exc_info = None # 필요시 주석 해제
        return formatted_message

# 개발/테스트 환경용 사람이 읽기 쉬운 로그 포맷 (재추가)
human_readable_log_format = (
    "[%(asctime)s] [%(levelname)s] [%(name)s] process=%(process)d\n"
    "    request={status=%(status)s method=%(method)s host=%(host)s remoteIp=%(remoteIp)s userAgent='%(userAgent)s'}\n"
    "    message=%(message)s"
)
# 개발/테스트 환경용 시간 포맷 (JsonFormatter와 다르게 설정 가능)
human_readable_datefmt = '%Y-%m-%d %H:%M:%S'


def setup_logger(name: str) -> logging.Logger:
    """로거를 설정하고 반환합니다."""
    logger = logging.getLogger(name)

    if logger.filters or logger.handlers:
        return logger

    context_filter = ContextFilter()
    logger.addFilter(context_filter)

    # --- 환경 감지 및 포매터 선택 ---
    is_prod = is_ubuntu()
    if is_prod:
        # 운영 환경: JsonFormatter 사용
        formatter = JsonFormatter()
    else:
        # 개발/테스트 환경: ErrorTracebackFormatter 사용 (사람이 읽기 쉬운 포맷)
        formatter = ErrorTracebackFormatter(
            fmt=human_readable_log_format,
            datefmt=human_readable_datefmt
        )
    # -----------------------------

    # stdout 핸들러 설정
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(formatter) # 선택된 포매터 적용

    # 환경에 따른 로그 레벨 설정
    if is_prod: # is_prod 변수 사용
        logger.setLevel(logging.INFO)
        stdout_handler.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.DEBUG)
        stdout_handler.setLevel(logging.DEBUG)

    # stderr 핸들러 설정 (ERROR 레벨)
    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.ERROR)
    stderr_handler.setFormatter(formatter) # 선택된 포매터 적용

    logger.addHandler(stdout_handler)
    logger.addHandler(stderr_handler)

    logger.propagate = False

    return logger
