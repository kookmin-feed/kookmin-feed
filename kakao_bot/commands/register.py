from config.env_loader import ENV
import requests
import logging
from api.models.common import isUnregisterUserResponse

logger = logging.getLogger(__name__)

from util.check import is_register_user

async def register_user(user_id: str) -> bool:
    try:
        if not user_id:
            raise ValueError("User ID is required")
        
        if is_register_user(user_id):
            raise isUnregisterUserResponse(message="User is already registered", login_url=f"{ENV['SERVER_URL']}/login")
        
        response = requests.post(f"{ENV['DATA_SERVER_URL']}/kakao/user", json={"user_id": user_id})

        if response.status_code == 200:
            return True
        else:
            raise response
        
    except Exception as e:
        logger.error(f"Error registering user: {e}")
        return False
