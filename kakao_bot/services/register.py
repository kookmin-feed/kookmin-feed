import sys
from pathlib import Path

# 상위 디렉토리를 Python path에 추가
sys.path.append(str(Path(__file__).parent.parent.parent))

from kakao_bot.config.env_loader import ENV
import requests
from kakao_bot.config.logger_config import setup_logger
from utils.data_server_conect import post_data_to_server, get_data_from_server
from fastapi import HTTPException
from api.models.user_models import KakaoCreateUser, UserAlreadyExists
logger = setup_logger(__name__)


async def register_user(kakao_create_user: KakaoCreateUser) -> bool:
    try:    
        response = await post_data_to_server(f"api/v1/kakao/user", data=kakao_create_user.model_dump())
        if response.get("status_code") == "409":
            raise UserAlreadyExists()
        return True

    except UserAlreadyExists as e:
        raise e
    except Exception as e:
        logger.error(f"Error registering user: {e}")
        raise e

async def is_register_user(user_id: str) -> bool:

    try:
        response = await get_data_from_server("api/v1/kakao/user", params={"user_id": user_id})
    
        if response['status_code'] == '200':  # 200은 성공, 404는 사용자 없음
            return True
        elif response['status_code'] == '404':
            return False
        else:
            raise Exception(response['status_code'], response['text'])

    except Exception as e:
        logger.error(f"Error checking user registration: {e}")
        return False
