from fastapi import Header, HTTPException, Depends
from typing import Annotated
from kakao_bot.config.env_loader import ENV
from services.register import is_register_user
from kakao_bot.config.logger_config import setup_logger

logger = setup_logger(__name__)

def get_api_key(authorization: str = Header(None, description="Bearer 토큰 형식의 API 키")):
    """API 키 검증"""
    if authorization != f"Bearer {ENV.get('API_KEY')}" :
        raise HTTPException(status_code=403, detail="Forbidden: Invalid API Key")
    return authorization