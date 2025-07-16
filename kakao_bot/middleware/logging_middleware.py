from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from kakao_bot.config.logger_config import setup_logger, set_request_context
import time

logger = setup_logger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """요청 로깅 미들웨어"""
    
    async def dispatch(self, request: Request, call_next):
        # 요청 시작 시간 기록
        start_time = time.time()
        
        # 클라이언트 IP 추출 (프록시 고려)
        client_ip = self.get_client_ip(request)
        
        # User-Agent 추출
        user_agent = request.headers.get("user-agent", "Unknown")
        
        # 요청 경로 추출
        request_path = request.url.path
        
        # 요청 컨텍스트 설정
        set_request_context(client_ip, user_agent, request_path)

        try:
            # 다음 미들웨어/핸들러 호출
            response = await call_next(request)
            
            # 처리 시간 계산
            process_time = time.time() - start_time
            
            return response
            
        except Exception as e:
            # 에러 발생 시 로그
            process_time = time.time() - start_time
            logger.error(
                f"요청 에러: {request.method} {request.url.path} "
                f"- 에러: {str(e)} "
                f"- 처리시간: {process_time:.3f}초"
            )
            raise
    
    def get_client_ip(self, request: Request) -> str:
        """클라이언트 IP를 추출합니다. 프록시 환경을 고려합니다."""
        # X-Forwarded-For 헤더 확인 (프록시/로드밸런서 환경)
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        # X-Real-IP 헤더 확인 (nginx 등)
        real_ip = request.headers.get("x-real-ip")
        if real_ip:
            return real_ip
        
        # 기본값: 직접 연결된 클라이언트 IP
        return request.client.host if request.client else "Unknown" 