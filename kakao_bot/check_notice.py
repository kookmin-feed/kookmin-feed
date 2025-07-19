import asyncio
import sys
import os
from pathlib import Path

# # 현재 디렉토리와 상위 디렉토리를 Python path에 추가
# current_dir = Path(__file__).parent.resolve()
# parent_dir = current_dir.parent.resolve()
# sys.path.insert(0, str(current_dir))
# sys.path.insert(0, str(parent_dir))

from kakao_bot.config.logger_config import setup_logger
from kakao_bot.config.env_loader import ENV
from kakao_bot.services.kakao_auth import KakaoAuthService
from kakao_bot.services.kakao_message import KakaoMessageService
from kakao_bot.utils.enum_data_api import get_all_scraper_types, get_all_categories
from kakao_bot.template.scraper_type_list import MetaData
from kakao_bot.utils.scraper_data_api import get_all_notices, get_new_notices, get_scraper_register_users
from kakao_bot.utils.notice_cache import LastNoticeData
from datetime import datetime
import pytz

logger = setup_logger(__name__)


if ENV["IS_PROD"]:
    INTERVAL = 10
else:
    INTERVAL = 2

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

async def check_notice():  # async 함수로 변경
    while True:
        try:
            # if not is_working_hour():
            #     current_time = datetime.now(pytz.timezone("Asia/Seoul")).strftime(
            #         "%Y-%m-%d %H:%M:%S"
            #     )
            #     logger.info(f"작동 시간이 아닙니다. (현재 시각: {current_time})")
            #     await asyncio.sleep(INTERVAL * 60)  # 작동 시간이 아니면 더 길게 대기
            #     continue

            
            MetaData.category_list = await get_all_categories()
            MetaData.scraper_type_list = await get_all_scraper_types()
            users = await KakaoAuthService.get_all_users()

            for scraper_type in MetaData.scraper_type_list:
                register_users = await get_scraper_register_users(users, scraper_type.collection_name)
                type_name = scraper_type.collection_name
                
                # 최초 실행 또는 새로운 타입일 경우 메시지를 보내지 않고 최근 공지 캐싱
                if LastNoticeData.links.get(type_name) == None:
                    
                    
                    last_notice = (await get_all_notices(type_name, 1))[0]
                    LastNoticeData.links[type_name] = last_notice.link

                    logger.info(f"\"최초 실행\" {scraper_type.name}의 마지막 게시물 \"{last_notice.title}\"를 캐싱했습니다.")
                
                # 캐싱한 마지막 공지 기준으로 새로운 공지 발견시 메시지 보내기
                else:
                    new_notice_list = await get_new_notices(type_name, LastNoticeData.links[type_name])
                    logger.info(f"\"{scraper_type.name}\"의 새 게시물은 {len(new_notice_list)}개 입니다.")
                    
                    for new_notice in reversed(new_notice_list):
                        await KakaoMessageService.send_notice(new_notice, scraper_type, register_users)

                    if len(new_notice_list) != 0:
                        LastNoticeData.links[type_name] = new_notice_list[0].link
                        logger.info(f"\"{scraper_type.name}\"의 마지막 게시물 \"{new_notice_list[0].title}\"를 캐싱했습니다.")
            
            logger.info(f"다음 체크까지 {INTERVAL}초 대기합니다...")
            await asyncio.sleep(INTERVAL)
            
        except Exception as e:
            logger.error(f"알림 체크 중 오류 발생: {e}")
            await asyncio.sleep(INTERVAL)  # 오류 발생 시에도 대기


if __name__ == "__main__":
    kakao_bot_dir = Path(__file__).parent.resolve()
    os.chdir(kakao_bot_dir)
    asyncio.run(check_notice())