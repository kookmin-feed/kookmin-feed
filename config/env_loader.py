import os
import platform
from dotenv import load_dotenv
from pathlib import Path


def is_ubuntu() -> bool:
    """현재 OS가 Ubuntu인지 확인합니다."""
    try:
        # /etc/os-release 파일 확인
        if os.path.exists("/etc/os-release"):
            with open("/etc/os-release", "r") as f:
                content = f.read().lower()
                return "ubuntu" in content

        # platform 모듈을 통한 확인
        return "ubuntu" in platform.platform().lower()
    except Exception as e:
        return False


def load_env_file():
    """환경에 따라 적절한 .env 파일을 로드하고 환경 설정을 반환합니다."""
    # 프로젝트 루트 디렉토리 경로
    root_dir = Path(__file__).parent.parent

    # Ubuntu 환경이면 기본 .env, 아니면 .dev.env 로드
    is_prod = is_ubuntu()
    print("This is " + ("DEV ENV" if not is_prod else "PROD ENV"))
    env_file = root_dir / ".env" if is_prod else root_dir / "envs/.dev.env"

    if env_file.exists():
        load_dotenv(env_file)
        return {
            "IS_PROD": is_prod,
            "MONGODB_URI": os.getenv("MONGODB_URI"),
            "DB_NAME": os.getenv("DB_NAME"),
            "DISCORD_TOKEN": os.getenv("DISCORD_TOKEN"),
            "DISCORD_PORT": os.getenv("DISCORD_PORT"),
            "KAKAO_PORT": os.getenv("KAKAO_PORT"),
            "KAKAO_CHANNEL_ID": os.getenv("KAKAO_CHANNEL_ID"),
            "KAKAO_API_KEY": os.getenv("KAKAO_API_KEY"),
            "YOUTUBE_API_KEY": os.getenv("YOUTUBE_API_KEY"),
            # 필요한 다른 환경 변수들도 여기에 추가
        }
    else:
        raise FileNotFoundError("환경 변수 파일이 존재하지 않습니다!")


# 환경 설정을 전역 변수로 로드
ENV = load_env_file()
