import json
from typing import Dict, Any, Optional
from kakao_bot.config.logger_config import setup_logger
from kakao_bot.utils.kakao_server_connect import post_data_to_server

logger = setup_logger(__name__)

class KakaoMessageService:
    """카카오 메시지 전송 관련 서비스"""
    
    @staticmethod
    async def send_text_message(access_token: str, text: str, web_url: Optional[str] = None) -> Dict[str, Any]:
        """
        카카오톡 나에게 보내기로 텍스트 메시지를 전송합니다.
        
        Args:
            access_token (str): 카카오 액세스 토큰
            text (str): 전송할 메시지 텍스트
            web_url (Optional[str]): 클릭 시 이동할 웹 URL
            
        Returns:
            Dict[str, Any]: API 응답 결과
            
        Raises:
            Exception: API 호출 실패 시
        """
        try:
            headers = {
                "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
                "Authorization": f"Bearer {access_token}"
            }
            
            template_object = {
                "object_type": "text",
                "text": text
            }
            
            # 웹 URL이 제공된 경우 링크 추가
            if web_url:
                template_object["link"] = {
                    "web_url": web_url
                }
            
            data = {
                "template_object": json.dumps(template_object)
            }
            
            response = await post_data_to_server(
                url="https://kapi.kakao.com/v2/api/talk/memo/default/send",
                data=data,
                headers=headers
            )
            
            logger.info(f"카카오 메시지 전송 성공: {text}")
            return response
            
        except Exception as e:
            logger.error(f"카카오 메시지 전송 실패: {str(e)}")
            raise
    
    @staticmethod
    async def send_login_complete_message(access_token: str, service_url: str = "https://kookmin-feed.com") -> Dict[str, Any]:
        """
        로그인 완료 메시지를 전송합니다.
        
        Args:
            access_token (str): 카카오 액세스 토큰
            service_url (str): 서비스 URL (기본값: https://kookmin-feed.com)
            
        Returns:
            Dict[str, Any]: API 응답 결과
        """
        return await KakaoMessageService.send_text_message(
            access_token=access_token,
            text="로그인 완료",
            web_url=service_url
        )