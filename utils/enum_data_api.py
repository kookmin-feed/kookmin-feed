from utils.data_server_conect import request_to_server
from template.scraper_category import ScraperCategory
from template.scraper_type import ScraperType

async def get_all_categories():
    """모든 카테고리 리스트를 가져옵니다."""
    response = await request_to_server("GET", "api/v1/scraper/categories")
    return [ScraperCategory(category["name"], category["korean_name"], category["scraper_type_names"]) for category in response]

async def get_all_scraper_types():
    """모든 공지사항 타입을 가져옵니다."""
    response = await request_to_server("GET", "api/v1/scraper/types")
    return [ScraperType(scraper_type["korean_name"], scraper_type["collection_name"], scraper_type["type_name"]) for scraper_type in response]
