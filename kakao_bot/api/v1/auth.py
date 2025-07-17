from fastapi import APIRouter, Query
from kakao_bot.config.logger_config import setup_logger
from kakao_bot.config.env_loader import ENV
from kakao_bot.utils.kakao_server_connect import post_data_to_server
import requests
import json
from services.kakao_auth import KakaoAuthService
from services.register import register_user
from api.models.user_models import KakaoCreateUser, UserAlreadyExists
from services.kakao_message import KakaoMessageService

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
        access_token = response.get("access_token")
        refresh_token = response.get("refresh_token")
        expires_in = response.get("expires_in")
        refresh_token_expires_in = response.get("refresh_token_expires_in")
        user_id = await KakaoAuthService.get_access_token_info(access_token)
        await register_user(KakaoCreateUser(user_id=user_id, scrapers=[], access_token=access_token, refresh_token=refresh_token, expires_in=expires_in, refresh_token_expires_in=refresh_token_expires_in))
        await KakaoMessageService.send_login_complete_message(access_token)
        
    except UserAlreadyExists as e:
        return {"message": "이미 로그인 되어있습니다."}
    except Exception as e:
        logger.error(f"카카오 로그인 실패: {e}")
        return {"message": "redirect"}

    logger.info("카카오 로그인 성공")
    return {"message": "redirect"}