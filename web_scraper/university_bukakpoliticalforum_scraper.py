import re
from bs4 import BeautifulSoup
from datetime import datetime
from utils.web_scraper import WebScraper
from utils.scraper_type import ScraperType
from template.notice_data import NoticeData
from config.logger_config import setup_logger

logger = setup_logger(__name__)


class UniversityBukakpoliticalforumScraper(WebScraper):
    """북악정치포럼 스크래퍼"""

    def __init__(self, url: str):
        super().__init__(url, ScraperType.UNIVERSITY_BUKAKPOLITICALFORUM)

    def get_list_elements(self, soup: BeautifulSoup) -> list:
        """공지사항 목록의 HTML 요소들을 가져옵니다."""
        return soup.select(".board_list ul li")

    async def parse_notice_from_element(self, element) -> NoticeData:
        """HTML 요소에서 공지사항 정보를 추출합니다."""
        try:
            # 제목 추출
            title_tag = element.select_one(".title")
            if not title_tag:
                logger.warning("제목 요소를 찾을 수 없습니다.")
                return None

            title = title_tag.text.strip()

            # 작성자 추출
            author_element = element.select_one(".desc")
            author = author_element.text.strip() if author_element else ""
            if author:
                title = f"[{author}] {title}"

            # 날짜와 장소 추출
            board_etc = element.select_one(".board_etc")
            if board_etc:
                spans = board_etc.select("span")
                if spans:
                    # 날짜 추출 및 변환
                    date_text = spans[0].text.strip().replace("일시 및 기간: ", "")
                    try:
                        # "2025.04.29 (18:45~20:15)" 형식에서 날짜 부분만 추출
                        date_match = re.search(r"(\d{4})\.(\d{2})\.(\d{2})", date_text)
                        if date_match:
                            year, month, day = date_match.groups()
                            published = datetime.strptime(
                                f"{year}-{month}-{day}", "%Y-%m-%d"
                            )
                            published = self.kst.localize(published)
                        else:
                            logger.warning(f"날짜 형식 변환 실패: {date_text}")
                            published = datetime.now(self.kst)
                    except ValueError as e:
                        logger.error(f"날짜 파싱 오류: {e}")
                        published = datetime.now(self.kst)

                    # 장소 정보 추출
                    location = spans[1].text.strip() if len(spans) > 1 else ""
            else:
                published = datetime.now(self.kst)
                location = ""

            # 회차 정보 추출
            category_element = element.select_one(".ctg_name em")
            category = category_element.text.strip() if category_element else ""

            # 링크 추출
            onclick = element.select_one("a").get("onclick", "")
            if "global.write(" in onclick:
                post_id = onclick.split("'")[1]
                link = f"https://www.kookmin.ac.kr/user/kmuNews/specBbs/bugAgForum/view.do?dataSeq={post_id}"
            else:
                link = self.url

            # 로깅
            logger.debug(f"공지사항 파싱: {title}")

            return NoticeData(
                title=title,
                link=link,
                published=published,
                scraper_type=self.scraper_type,
            )

        except Exception as e:
            logger.error(f"공지사항 파싱 중 오류: {e}")
            return None
