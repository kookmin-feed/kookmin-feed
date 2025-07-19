import asyncio
import os
from contextlib import asynccontextmanager
import sys
import uvicorn
from pathlib import Path
from fastapi import FastAPI


from kakao_bot.api.v1.api import api_router

from kakao_bot.utils.data_server_conect import get_data_from_server
from kakao_bot.config.env_loader import ENV
from kakao_bot.config.logger_config import setup_logger
from kakao_bot.middleware.auth_middleware import UserAuthMiddleware
from kakao_bot.middleware.logging_middleware import LoggingMiddleware


logger = setup_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 시작/종료 시 실행될 로직"""
    # 시작 시 실행
    logger.info("카카오톡 봇을 시작합니다...")
    
    try:
        # data server connection 테스트
        logger.info("Data Server 연결 상태를 검사합니다...")
        await get_data_from_server(endpoint="api/v1/connect-check")

        logger.info("meta data를 초기화합니다.")

        # task = asyncio.create_task(check_notice())
        logger.info(f"알림 체크 작업 생성:")

        logger.info("초기화가 완료되었습니다.")
        
    except Exception as e:
        logger.error(f"초기화 중 오류 발생: {e}")
        raise
    
    yield  # 애플리케이션 실행
    
    # 종료 시 실행
    logger.info("애플리케이션을 종료합니다...")

# FastAPI 앱 인스턴스 생성 (전역 변수로 선언)
app = FastAPI(
    title="Kakao Bot API",
    description="카카오톡 봇 API",
    version="1.0.0",
    lifespan=lifespan
)

# 미들웨어 추가
app.add_middleware(UserAuthMiddleware)
app.add_middleware(LoggingMiddleware)



app.include_router(api_router, prefix="/api/v1")
        

# 개발 서버 실행용
if __name__ == "__main__":
    try:
        host = ENV.get("HOST", "0.0.0.0")
        port = int(ENV.get("PORT","8000"))
       
        uvicorn.run(
            "kakao_bot.main:app",
            host=host,
            port=port,
            reload=False,
            log_level= "info" if ENV.get("IS_PROD") else "debug",
            access_log=False
        )
    except Exception as e:
        logger.error(f"초기화 중 오류 발생: {e}")
        raise


