import sys
from pathlib import Path

# 상위 디렉토리를 Python path에 추가
sys.path.append(str(Path(__file__).parent.parent.parent))

from kakao_bot.config.env_loader import ENV
import requests
from kakao_bot.config.logger_config import setup_logger
from utils.data_server_conect import post_data_to_server, get_data_from_server
from pydantic import BaseModel
from fastapi import HTTPException

logger = setup_logger(__name__)

# 기존 함수 (필요시 다른 곳에서 사용)
async def register_user(user_id: str) -> BaseModel or bool:
    try:    
        response = await post_data_to_server(f"{ENV['DATA_SERVER_URL']}/kakao/user", json={"user_id": user_id})

        if response.status == 200:
            return True
        else:
            raise Exception(response.status, response.text)
        
    except Exception as e:
        logger.error(f"Error registering user: {e}")
        return False

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
