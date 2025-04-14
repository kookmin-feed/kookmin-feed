from bs4 import BeautifulSoup
from datetime import datetime, date, time
from template.notice_data import NoticeData
from utils.scraper_type import ScraperType
from utils.web_scraper import WebScraper
from config.logger_config import setup_logger

logger = setup_logger(__name__)


class DesignCeramicsAcademicScraper(WebScraper):
    """도자공예학과 학사공지 스크래퍼"""

    def __init__(self, url: str):
        super().__init__(url, ScraperType.DESIGN_CERAMICS_ACADEMIC)
        self.base_url = "https://kmuceramics.com"

    def get_list_elements(self, soup: BeautifulSoup) -> list:
        """도자공예학과 학사공지 목록의 HTML 요소들을 가져옵니다."""
        # 테이블의 모든 행을 가져오지만 헤더 행은 제외
        table = soup.select_one("div.kboard-list table")
        if not table:
            self.logger.error("테이블을 찾을 수 없습니다")
            return []

        elements = table.select("tbody tr")
        self.logger.debug(f"총 {len(elements)}개의 공지사항 요소를 찾았습니다")
        return elements if elements else []

    async def parse_notice_from_element(self, element) -> NoticeData:
        """HTML 요소에서 도자공예학과 학사공지 정보를 추출합니다."""
        try:
            # 제목과 링크 추출
            title_td = element.select_one("td.kboard-list-title")
            if not title_td:
                return None

            a_tag = title_td.select_one("a")
            if not a_tag:
                return None

            # 카테고리가 있으면 제목에 포함
            category_span = title_td.select_one("span.category1")
            category_text = ""
            if category_span:
                category_text = category_span.text.strip()

            # 제목 텍스트 추출 (카테고리를 제외한 실제 제목)
            title_div = title_td.select_one("div.kboard-default-cut-strings")
            if title_div:
                # 카테고리 부분을 제외한 텍스트 추출
                title = title_div.get_text(strip=True)
                if category_span:
                    title = title.replace(category_text, "").strip()
            else:
                title = a_tag.get_text(strip=True)

            # 카테고리가 제목 앞에 있으면 그대로 사용
            if category_text:
                title = f"{category_text} {title}"

            # 링크 추출
            relative_link = a_tag.get("href", "")
            if relative_link.startswith("/"):
                link = f"{self.base_url}{relative_link}"
            else:
                link = relative_link

            # 날짜 추출 및 파싱
            date_td = element.select_one("td.kboard-list-date")
            published = None
            if date_td:
                date_str = date_td.text.strip()
                # 시도할 날짜 형식 리스트
                date_formats = ["%Y.%m.%d", "%Y-%m-%d", "%y.%m.%d", "%H:%M"]

                for fmt in date_formats:
                    try:
                        if fmt == "%H:%M":
                            # 시간 형식인 경우 오늘 날짜와 결합
                            time_obj = datetime.strptime(date_str, fmt).time()
                            today_date = date.today()
                            published = datetime.combine(today_date, time_obj).replace(tzinfo=self.kst)
                        else:
                            # 다른 날짜 형식 시도
                            published = datetime.strptime(date_str, fmt).replace(tzinfo=self.kst)

                        # 파싱 성공 시 반복 중단
                        break
                    except ValueError:
                        # 파싱 실패 시 다음 형식 시도
                        continue

                # 모든 형식이 실패한 경우
                if published is None:
                    self.logger.error(f"지원하지 않는 날짜 형식 또는 파싱 오류: {date_str}")
                    published = datetime.now(self.kst) # Fallback
            else:
                self.logger.warning("날짜 요소를 찾을 수 없음")
                published = datetime.now(self.kst) # Fallback

            return NoticeData(
                title=title,
                link=link,
                published=published,
                scraper_type=self.scraper_type,
            )
        except Exception as e:
            self.logger.error(f"공지사항 파싱 중 오류: {e}", exc_info=True)
            return None
