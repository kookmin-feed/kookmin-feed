import pytz
from datetime import datetime
import requests
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import asyncio
from typing import List

from config.env_loader import ENV
from utils.scraper_factory import ScraperFactory
from utils.scraper_type import ScraperType
from config.logger_config import setup_logger
from template.notice_data import NoticeData

logger = setup_logger(__name__)

def is_working_hour():
    """현재 시간이 작동 시간(월~토 8시~20시)인지 확인합니다."""
    if not ENV["IS_PROD"]:
        return True

    now = datetime.now(pytz.timezone("Asia/Seoul"))

    # 일요일(6) 체크
    if now.weekday() == 6:
        return False

    # 시간 체크 (8시~20시)
    if now.hour < 8 or now.hour >= 21:
        return False

    return True

async def check_all_notices():
    """모든 스크래퍼를 실행하고 새로운 공지사항을 처리합니다."""
    try:
        # 작동 시간이 아니면 스킵
        if not is_working_hour():
            current_time = datetime.now(pytz.timezone("Asia/Seoul")).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            logger.info(f"작동 시간이 아닙니다. (현재 시각: {current_time})")
            return
            
        # 활성화된 모든 스크래퍼 실행
        for scraper_type in ScraperType.get_active_scrapers():
            try:
                # 스크래퍼 생성
                scraper = ScraperFactory().create_scraper(scraper_type)
                if not scraper:
                    logger.error(f"지원하지 않는 스크래퍼 타입: {scraper_type.name}")
                    continue

                # 공지사항 확인 및 처리
                notices = await scraper.check_updates()
                await process_new_notices(notices, scraper_type)

            except Exception as e:
                logger.error(
                    f"{scraper_type.get_korean_name()} 스크래핑 중 오류 발생: {e}"
                )
                continue

    except Exception as e:
        logger.error(f"스크래핑 작업 중 오류 발생: {e}")

async def process_new_notices(notices: List[NoticeData], scraper_type: ScraperType):
    requests.post(f"localhost:{ENV['DISCORD_PORT']}/notices", {
        "notices": notices,
        "scraper_type": scraper_type
    }, {}) # discord 서버에 메세지 전송 요청

    requests.post(f"localhost:{ENV['KAKAO_PORT']}/notices", {
        "notices": notices,
        "scraper_type": scraper_type
    }, {}) # 카카오톡 메세지 전송 요청
    # 필요시 코드 추가

def setup_scheduler(interval: int):
    """스케줄러를 설정하고 시작합니다."""
    scheduler = AsyncIOScheduler()
    
    scheduler.add_job(
        check_all_notices,
        CronTrigger(minute=f'*/{interval}'),  # 매 5분마다 실행 (0, 5, 10, 15, ..., 55분)
        id='check_notices',
        name='공지사항 체크',
        misfire_grace_time=50
    )
    
    scheduler.start()
    logger.info("스케줄러가 시작되었습니다.")
    return scheduler

if __name__ == "__main__":
    scheduler = setup_scheduler()
    # 스케줄러가 계속 실행되도록 메인 스레드 유지
    asyncio.get_event_loop().run_forever()