from fastapi import APIRouter, Query
from kakao_bot.config.logger_config import setup_logger
from kakao_bot.config.env_loader import ENV
from kakao_bot.utils.kakao_server_connect import post_data_to_server
import requests
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
        
        data = {
            "grant_type": "authorization_code",
            "client_id": ENV["KAKAO_CLIENT_ID"],
            "redirect_uri": ENV["KAKAO_REDIRECT_URL"], 
            "code": code
        }
    
        headers = {
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"
        }
        response = await post_data_to_server(url="https://kauth.kakao.com/oauth/token", 
                                data=data,
                                headers=headers)
        logger.info(response)
        logger.info(f"카카오 토큰 응답: {response}")


    except Exception as e:
        logger.error(f"카카오 로그인 실패: {e}")
        return {"message": "redirect"}

    return {"message": "redirect"}