import json
from typing import Dict, Any
from kakao_bot.config.env_loader import ENV
from kakao_bot.config.logger_config import setup_logger
from kakao_bot.utils.kakao_server_connect import post_data_to_server, get_data_from_server

logger = setup_logger(__name__)

class KakaoAuthService:
    """카카오 OAuth 인증 관련 서비스"""
    
    @staticmethod
    async def get_access_token(authorization_code: str) -> Dict[str, Any]:
        """
        카카오 인가 코드로 액세스 토큰을 가져옵니다.
        
        Args:
            authorization_code (str): 카카오에서 받은 인가 코드
            
        Returns:
            Dict[str, Any]: 토큰 정보 (access_token, refresh_token, expires_in 등)
            
        Raises:
            Exception: API 호출 실패 시
        """
        try:
            data = {
                "grant_type": "authorization_code",
                "client_id": ENV["KAKAO_CLIENT_ID"],
                "redirect_uri": ENV["KAKAO_REDIRECT_URL"], 
                "code": authorization_code
            }
            
            headers = {
                "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"
            }
            
            response = await post_data_to_server(
                url="https://kauth.kakao.com/oauth/token", 
                data=data,
                headers=headers
            )
            
            return response
            
        except Exception as e:
            logger.error(f"카카오 액세스 토큰 발급 실패: {str(e)}")
            raise
    
    @staticmethod
    async def refresh_access_token(refresh_token: str) -> Dict[str, Any]:
        """
        리프레시 토큰으로 액세스 토큰을 갱신합니다.
        
        Args:
            refresh_token (str): 리프레시 토큰
            
        Returns:
            Dict[str, Any]: 갱신된 토큰 정보
            
        Raises:
            Exception: API 호출 실패 시
        """
        try:
            data = {
                "grant_type": "refresh_token",
                "client_id": ENV["KAKAO_CLIENT_ID"],
                "refresh_token": refresh_token
            }
            
            headers = {
                "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"
            }
            
            response = await post_data_to_server(
                url="https://kauth.kakao.com/oauth/token",
                data=data,
                headers=headers
            )
            
            logger.info("카카오 액세스 토큰 갱신 성공")
            return response
            
        except Exception as e:
            logger.error(f"카카오 액세스 토큰 갱신 실패: {str(e)}")
            raise
    
    @staticmethod
    async def get_access_token_info(access_token: str) -> str:
        """
        액세스 토큰으로 토큰 정보를 가져옵니다.
        """
        try:
            headers = {
                "Authorization": f"Bearer {access_token}"
            }

            response = await get_data_from_server(
                url="https://kapi.kakao.com/v1/user/access_token_info",
                headers=headers
            )
            return str(response.get("id"))
        except Exception as e:
            logger.error(f"카카오 액세스 토큰 정보 가져오기 실패: {str(e)}")
            raise

