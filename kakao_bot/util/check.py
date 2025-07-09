import requests

import logging
from config.env_loader import ENV

logger = logging.getLogger(__name__)



def is_register_user(user_id: str):

    if not user_id:
        logger.info("function:is_register_user, User ID is required")
        return False

    try:
        response = requests.get(f"{ENV['DATA_SERVER_URL']}/kakao/user?user_id={user_id}")
        if response.status_code == 200:
            logger.debug(f"function:is_register_user, User ID: {user_id} is registered")
            return True
        else:
            logger.info(f"function:is_register_user, User ID: {user_id} is not registered")
            return False

    except Exception as e:
        logger.error(f"Error checking user registration: {e}")
        return False


    