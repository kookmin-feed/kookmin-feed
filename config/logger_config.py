import logging
import sys
import traceback  # traceback 모듈 임포트 (ErrorTracebackFormatter에서 사용 가능성 있음)
from config.env_loader import ENV

environment = "DEV" if not ENV["IS_PROD"] else "PROD"  # 기본값은 DEV


# Filter to add default values for missing context keys
class ContextFilter(logging.Filter):
    # 로그 포맷에서 사용하는 컨텍스트 키와 기본값 정의
    DEFAULT_CONTEXT = {
        'status': '-',
        'method': '-',
        'host': '-',
        'remoteIp': '-',
        'userAgent': '-',
    }

    def filter(self, record):
        # LogRecord에 기본 컨텍스트 값 설정 (없는 경우)
        for key, value in self.DEFAULT_CONTEXT.items():
            # record 객체에 해당 속성이 있는지 확인
            if not hasattr(record, key):
                # 없으면 기본값으로 설정
                setattr(record, key, value)
        # record.process는 logging이 자동으로 추가하므로 일반적으로 필요 없음
        # if not hasattr(record, 'process'):
        #     setattr(record, 'process', 0) # 예시: process ID가 없는 경우 0으로 설정
        return True  # 항상 로그 레코드를 처리하도록 True 반환


# ERROR 레벨 이상일 때 자동으로 Traceback을 포함하는 커스텀 포매터
class ErrorTracebackFormatter(logging.Formatter):
    def format(self, record):
        # 레벨이 ERROR 이상이고, exc_info가 명시적으로 설정되지 않았는지 확인
        if record.levelno >= logging.ERROR and not record.exc_info:
            # 현재 처리 중인 예외 정보가 있는지 확인
            exc_info = sys.exc_info()
            if exc_info and exc_info[0] is not None: # 유효한 예외 정보가 있다면
                # 로그 레코드에 예외 정보 설정
                # 이렇게 하면 이후 super().format() 호출 시 표준 포매터 로직이 Traceback을 처리함
                record.exc_info = exc_info

        # 부모 클래스의 format 메소드를 호출하여 최종 포맷팅 수행
        # record.exc_info가 설정되었다면 Traceback이 자동으로 추가됨
        formatted_message = super().format(record)

        # format() 메소드가 record.exc_info를 사용한 후에는 None으로 다시 설정하는 것이 좋습니다.
        # 그렇지 않으면 핸들러 체인에서 다른 포매터에 의해 중복 처리될 수 있습니다. (여기서는 핸들러가 분리되어 큰 문제는 아닐 수 있음)
        # 하지만 안전을 위해 None으로 되돌리는 것을 고려할 수 있습니다. (선택 사항)
        # record.exc_info = None # 필요시 주석 해제

        return formatted_message


def setup_logger(name: str) -> logging.Logger:
    """로거를 설정하고 반환합니다."""
    logger = logging.getLogger(name)

    # 이미 필터나 핸들러가 설정되어 있다면 추가 설정하지 않음 (중복 방지)
    if logger.filters or logger.handlers:
        return logger

    # --- 컨텍스트 필터 추가 ---
    context_filter = ContextFilter()
    logger.addFilter(context_filter)
    # ------------------------

    # 기본 로그 포맷 정의
    log_format = (
        "[%(asctime)s] [%(levelname)s] [%(name)s] process=%(process)d\n"
        "    request={status=%(status)s method=%(method)s host=%(host)s remoteIp=%(remoteIp)s userAgent='%(userAgent)s'}\n"
        "    message=%(message)s"
    )

    # stdout 핸들러용 표준 Formatter
    stdout_formatter = logging.Formatter(log_format)

    # stderr 핸들러용 커스텀 ErrorTracebackFormatter
    stderr_formatter = ErrorTracebackFormatter(log_format)

    # stdout 핸들러 (환경에 따라 DEBUG 또는 INFO 레벨)
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(stdout_formatter) # 표준 포매터 적용

    # 환경에 따라 로그 레벨 설정
    # 로거 레벨과 핸들러 레벨이 있기 때문에, 두개다 설정해야함.
    if environment.lower() == "prod":
        logger.setLevel(logging.INFO)
        stdout_handler.setLevel(logging.INFO)
    else:  # development
        logger.setLevel(logging.DEBUG)
        stdout_handler.setLevel(logging.DEBUG)

    # stderr 핸들러 (ERROR 레벨)
    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.ERROR)
    # stderr 핸들러에 커스텀 에러 포매터 적용
    stderr_handler.setFormatter(stderr_formatter)

    # 핸들러 추가
    logger.addHandler(stdout_handler)
    logger.addHandler(stderr_handler)

    # 로거가 상위 로거로 메시지를 전파하지 않도록 설정
    logger.propagate = False

    return logger
