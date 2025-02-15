import asyncio
import logging
import sys
import os
from dotenv import load_dotenv
from discord_bot.discord_bot import client, send_notice
from template.scrapper_type import ScrapperType
from web_scrapper.academic_notice_scrapper import AcademicNoticeScrapper
from web_scrapper.sw_notice_scrapper import SWNoticeScrapper
from web_scrapper.rss_notice_scrapper import RSSNoticeScrapper
from discord.ext import tasks
from config.logger_config import setup_logger
from config.db_config import get_database, close_database, save_notice

# .env 파일에서 환경 변수 로드
load_dotenv()

class MaxLevelFilter(logging.Filter):
    """특정 레벨 미만의 로그만 통과시키는 필터"""
    def __init__(self, max_level):
        super().__init__()
        self.max_level = max_level

    def filter(self, record):
        return record.levelno < self.max_level

async def process_new_notices(notices, scrapper_type: ScrapperType):
    """새로운 공지사항을 처리합니다."""
    for notice in notices:
        # DB에 저장
        await save_notice(notice, scrapper_type)
        # 디스코드로 전송
        await send_notice(notice, scrapper_type)

@tasks.loop(minutes=5)
async def check_all_notices():
    """모든 스크래퍼를 실행하고 새로운 공지사항을 처리합니다."""
    try:
        # 학사공지 스크래퍼
        academic_url = os.getenv('CS_ACADEMIC_NOTICE_URL')
        academic_scrapper = AcademicNoticeScrapper(academic_url)
        academic_notices = await academic_scrapper.check_updates()
        await process_new_notices(academic_notices, ScrapperType.CS_ACADEMIC_NOTICE)

        # SW중심대학 스크래퍼
        sw_url = os.getenv('SOFTWARE_NOTICE_URL')
        sw_scrapper = SWNoticeScrapper(sw_url)
        sw_notices = await sw_scrapper.check_updates()
        await process_new_notices(sw_notices, ScrapperType.SOFTWARE_NOTICE)
        
        # RSS 피드 스크래퍼
        rss_url = os.getenv('CS_SW_NOTICE_RSS_URL')
        rss_scrapper = RSSNoticeScrapper(rss_url, ScrapperType.CS_SW_NOTICE_RSS)
        rss_notices = await rss_scrapper.check_updates()
        await process_new_notices(rss_notices, ScrapperType.CS_SW_NOTICE_RSS)
            
    except Exception as e:
        logger.error(f"스크래핑 중 오류 발생: {e}")

@check_all_notices.before_loop
async def before_check():
    """크롤링 시작 전 봇이 준비될 때까지 대기"""
    await client.wait_until_ready()

async def main():
    logger.info("국민대학교 공지사항 알리미 봇을 시작합니다...")
    #logger.debug("환경: " + os.getenv('ENVIRONMENT'))
    
    try:
        # 환경 변수 검증
        discord_token = os.getenv('DISCORD_TOKEN')
        if not discord_token:
            raise ValueError("DISCORD_TOKEN이 설정되지 않았습니다. .env 파일을 확인해주세요.")
        
        # MongoDB 연결 초기화
        db = get_database()
        logger.info("MongoDB 연결이 성공적으로 설정되었습니다.")
        
        # 크롤링 태스크 시작
        check_all_notices.start()
        logger.info("크롤링 작업이 시작되었습니다.")
        
        logger.info("디스코드 봇을 시작합니다...")
        await client.start(discord_token)
        
    except ValueError as e:
        logger.error(str(e))
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("\n프로그램을 종료합니다...")
    except Exception as e:
        logger.error(f"오류 발생: {e}")
    finally:
        check_all_notices.cancel()
        await client.close()
        close_database()
        await asyncio.get_event_loop().shutdown_asyncgens()

@client.event
async def on_ready():
    """봇이 시작될 때 실행되는 이벤트"""
    logger.info(f'봇이 시작되었습니다: {client.user.name}')
    
    try:
        logger.info("슬래시 커맨드를 전역으로 등록합니다...")
        await client.tree.sync()
        logger.info("슬래시 커맨드 등록이 완료되었습니다.")
    except Exception as e:
        logger.error(f"슬래시 커맨드 등록 중 오류 발생: {e}")

    logger.info("봇이 준비되었습니다!")

@client.event
async def on_guild_join(guild):
    """봇이 새로운 서버에 참여했을 때 실행됩니다."""
    logger.info(f'새로운 서버 [{guild.name}]에 참여했습니다.')
    try:
        await client.tree.sync(guild=guild)
        logger.info(f'서버 [{guild.name}]에 슬래시 커맨드를 등록했습니다.')
    except Exception as e:
        logger.error(f'서버 [{guild.name}]에 슬래시 커맨드 등록 실패: {e}')

if __name__ == "__main__":
    
    logger = setup_logger(__name__)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("프로그램이 안전하게 종료되었습니다.") 