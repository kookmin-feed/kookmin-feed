import asyncio
import os
from fastapi import FastAPI
from api.v1.api import api_router
from contextlib import asynccontextmanager
from config.env_loader import ENV

import sys
from pathlib import Path

# 상위 디렉토리를 Python path에 추가
sys.path.append(str(Path(__file__).parent.parent))

from utils.data_server_conect import get_data_from_server
from utils.enum_data_api import get_all_scraper_types, get_all_categories
from config.env_loader import ENV
from config.logger_config import setup_logger
from template.scraper_type_list import MetaData
import uvicorn

logger = setup_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 시작/종료 시 실행될 로직"""
    # 시작 시 실행
    logger.info("카카오톡 봇을 시작합니다...")
    
    try:
        # data server connection 테스트
        logger.info("Data Server 연결 상태를 검사합니다...")
        await get_data_from_server(endpoint="connect-check")

        logger.info("meta data를 초기화합니다.")
        
        MetaData.category_list = await get_all_categories()
        logger.info("카테고리 meta data 초기화 완료.")

        MetaData.scraper_type_list = await get_all_scraper_types()  
        logger.info("스크래퍼 타입 meta data를 초기화 완료.")
        
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
    # lifespan=lifespan
)

app.include_router(api_router, prefix="/api/v1")

# 개발 서버 실행용
if __name__ == "__main__":
    host = ENV.get("HOST", "0.0.0.0")
    port = int(ENV.get("PORT", 8000))
    kakao_bot_dir = Path(__file__).parent.resolve()
    os.chdir(kakao_bot_dir)
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=False, # 상위 디렉토리를 Python path에 추가하여  child process에서 참조하기 때문에, reload 불가
        log_level="info"
    )



