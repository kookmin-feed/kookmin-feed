from utils.data_server_conect import request_to_server
from template.notice_data import NoticeData
from datetime import datetime

async def get_all_notices(notice_type: str = None, list_size: int = 10):
    """모든 공지사항 리스트를 가져옵니다."""
    params = {"notice_type": notice_type, "list_size": list_size}
    response = await request_to_server("GET", "notices/all", params=params)
    return [
        NoticeData(
            title=item["title"],
            link=item["link"],
            published=datetime.fromisoformat(item["published"]),
            scraper_type=notice_type,
        )
        for item in response
    ]

async def get_new_notices(notice_type: str = None, last_notice_link: str = None):
    """새로운 공지사항을 가져옵니다."""
    params = {"notice_type": notice_type, "last_notice_link": last_notice_link}
    response = await request_to_server("GET", "notices/new", params=params)
    return [
        NoticeData(
            title=item["title"],
            link=item["link"],
            published=datetime.fromisoformat(item["published"]),
            scraper_type=notice_type,
        )
        for item in response
    ]

async def get_scraper_register_users(users : list[dict], scraper_type: str) -> list[dict]:
    """스크래퍼 등록 유저를 가져옵니다."""
    return [user for user in users if user["scraper_type"] == scraper_type]