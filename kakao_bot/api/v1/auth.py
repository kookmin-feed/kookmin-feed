from fastapi import APIRouter, Query
from kakao_bot.config.logger_config import setup_logger
from kakao_bot.config.env_loader import ENV
from kakao_bot.utils.kakao_server_connect import post_data_to_server
import requests
import json
from services.kakao_auth import KakaoAuthService
logger = setup_logger(__name__)

router = APIRouter()


@router.get("/redirect")
async def redirect(
    code: str = Query(None, description="카카오 로그인 인증 코드"),
    error: str = Query(None, description="카카오 로그인 취소"),
):
    try:
        if error:
            logger.error(f"카카오 로그인 취소: {error}")
            return {"message": "로그인이 취소되었습니다."}
        
        response = await KakaoAuthService.get_access_token(code)

        # 토큰 저장
        access_token = response["access_token"]
        refresh_token = response["refresh_token"]
        expires_in = response["expires_in"]
        refresh_token_expires_in = response["refresh_token_expires_in"]
    
        await KakaoMessageService.send_login_complete_message(access_token)
    
    except Exception as e:
        logger.error(f"카카오 로그인 실패: {e}")
        return {"message": "redirect"}

    return {"message": "redirect"}