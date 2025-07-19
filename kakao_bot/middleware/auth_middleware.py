from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from kakao_bot.config.logger_config import setup_logger
from services.register import is_register_user
from kakao_bot.config.env_loader import ENV
from api.models.user_models import create_login_response, create_error_response
import json

logger = setup_logger(__name__)

class UserAuthMiddleware(BaseHTTPMiddleware):
    """사용자 인증 미들웨어"""
    
    def __init__(self, app, protected_paths: list = None):
        super().__init__(app)
        # 보호된 경로들 (사용자 검증이 필요한 경로)
        self.protected_paths = protected_paths or [
            "/api/v1/board"
        ]
    
    async def dispatch(self, request: Request, call_next):
        # 보호된 경로인지 확인
        if not self.is_protected_path(request.url.path):
            return await call_next(request)
        
        try:
            # user_id 추출
            user_id = await self.extract_user_id(request)
            
            if not user_id:
                logger.info("user_id가 요청에 포함되지 않음")
                return create_error_response()
            
            # 사용자 등록 상태 확인
            is_registered = await is_register_user(user_id)
            
            if not is_registered:
                logger.info(f"미등록 사용자 접근: {user_id} 로그인 요청 블럭 리턴")
                return create_login_response()
            
            # 검증된 user_id를 request state에 저장
            request.state.verified_user_id = user_id

            logger.info(f"등록된 사용자 확인: {user_id}")
            
            return await call_next(request)
            
        except Exception as e:
            logger.error(f"사용자 인증 미들웨어 에러: {str(e)}")
            return create_error_response()
    
    def is_protected_path(self, path: str) -> bool:
        """보호된 경로인지 확인"""
        return any(path.startswith(protected) for protected in self.protected_paths)
    
    async def extract_user_id(self, request: Request) -> str:
        """Request에서 user_id를 추출"""
        try:
            body = await request.json()
            # 1. body에서 확인
            user_id = body['userRequest']['user']['properties']['app_user_id']
            if user_id:
                return user_id
            
        except Exception as e:
            logger.error(f"user_id 추출 중 오류: {str(e)}")
            return None
