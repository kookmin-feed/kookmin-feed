import logging
import sys
from contextvars import ContextVar
from kakao_bot.config.env_loader import ENV

# 요청 컨텍스트 변수들
client_ip_context: ContextVar[str] = ContextVar('client_ip', default='Unknown')
user_agent_context: ContextVar[str] = ContextVar('user_agent', default='Unknown')
request_path_context: ContextVar[str] = ContextVar('request_path', default='Unknown')

environment = "PROD" if ENV.get("IS_PROD") else "DEV"  # 기본값은 DEV


def set_request_context(client_ip: str, user_agent: str, request_path: str = 'Unknown') -> None:
    """요청 컨텍스트를 설정합니다."""
    client_ip_context.set(client_ip)
    user_agent_context.set(user_agent)
    request_path_context.set(request_path)


class CustomFormatter(logging.Formatter):
    """컨텍스트 정보를 포함한 커스텀 포맷터"""
    
    def get_client_ip(self) -> str:
        """현재 컨텍스트의 클라이언트 IP를 반환합니다."""
        return client_ip_context.get()

    def get_user_agent(self) -> str:
        """현재 컨텍스트의 User-Agent를 반환합니다."""
        return user_agent_context.get()

    def get_request_path(self) -> str:
        """현재 컨텍스트의 요청 경로를 반환합니다."""
        return request_path_context.get()
    
    def format(self, record):
        # 컨텍스트에서 정보 가져오기
        client_ip = self.get_client_ip()
        user_agent = self.get_user_agent()
        request_path = self.get_request_path()
        
        # 기본 포맷에 컨텍스트 정보 추가
        record.client_ip = client_ip
        record.user_agent = user_agent
        record.request_path = request_path
        
        return super().format(record)


def setup_logger(name: str) -> logging.Logger:
    """로거를 설정하고 반환합니다."""
    logger = logging.getLogger(name)

    # 이미 핸들러가 설정되어 있다면 추가 설정하지 않음
    if logger.handlers:
        return logger

    # 로그 포맷 설정 (컨텍스트 정보 포함)
    log_format = "%(asctime)s - %(name)s - %(levelname)s - [IP:%(client_ip)s] [Path:%(request_path)s] [UA:%(user_agent)s] - %(message)s"
    formatter = CustomFormatter(log_format)

    # stdout 핸들러 (환경에 따라 DEBUG 또는 INFO 레벨, ERROR 제외)
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(formatter)
    
    # ERROR 레벨 로그는 stderr_handler에서만 처리하도록 필터 추가
    stdout_handler.addFilter(lambda record: record.levelno < logging.ERROR)

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
    stderr_handler.setFormatter(formatter)

    # 핸들러 추가
    logger.addHandler(stdout_handler)
    logger.addHandler(stderr_handler)

    # 로거가 상위 로거로 메시지를 전파하지 않도록 설정
    logger.propagate = False

    return logger
