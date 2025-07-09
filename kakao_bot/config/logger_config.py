import logging
import sys
from config.env_loader import ENV

environment = "DEV" if not ENV["IS_PROD"] else "PROD"  # 기본값은 DEV


def setup_logger(name: str) -> logging.Logger:
    """로거를 설정하고 반환합니다."""
    logger = logging.getLogger(name)

    # 이미 핸들러가 설정되어 있다면 추가 설정하지 않음
    if logger.handlers:
        return logger

    # 로그 포맷 설정
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    formatter = logging.Formatter(log_format)

    # stdout 핸들러 (환경에 따라 DEBUG 또는 INFO 레벨)
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(formatter)

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
