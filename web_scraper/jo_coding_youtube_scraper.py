import requests
from datetime import datetime
from bs4 import BeautifulSoup
from template.notice_data import NoticeData
from utils.scraper_type import ScraperType
from utils.web_scraper import WebScraper
from config.logger_config import setup_logger
from config.env_loader import ENV

logger = setup_logger(__name__)

class JoCodingYoutubeScraper(WebScraper):
    """조코딩 유튜브 스크래퍼 (YouTube Data API 사용)"""
    current_youtube_API_delay = 18
    YOUTUBE_API_DELAY = 18 # 18 * 10분 에 한번 실행 (3시간 간격)

    def __init__(self, url: str):
        super().__init__(url, ScraperType.JO_CODING_YOUTUBE)
        # YouTube Data API 키
        self.api_key = ENV['YOUTUBE_API_KEY']
        # 채널 ID (예: 조코딩 채널 ID)
        self.channel_id = 'UCQNE2JmbasNYbjGAcuBiRRg'  

    def get_list_elements(self, soup: BeautifulSoup) -> list:
        """유튜브 영상 목록의 HTML 요소들을 가져오는 대신, API로 데이터를 가져옵니다."""
        if JoCodingYoutubeScraper.current_youtube_API_delay < JoCodingYoutubeScraper.YOUTUBE_API_DELAY:
            JoCodingYoutubeScraper.current_youtube_API_delay += 1
            return []
        JoCodingYoutubeScraper.current_youtube_API_delay = 0

        url = f'https://www.googleapis.com/youtube/v3/search'
        params = {
            "part": "snippet",
            "channelId": self.channel_id,
            "maxResults": 5,  # 최신 3개 쇼츠 영상
            "key": self.api_key,
            "videoDuration": "short",  # 짧은 영상 (60초 이하)
            "type": "video"  # 오직 비디오만
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # HTTP 오류 발생 시 예외 처리

            videos = response.json().get('items', [])
            return videos
        except Exception as e:
            logger.error(f"유튜브 API 호출 중 오류: {e}")
            return []

    async def parse_notice_from_element(self, element) -> NoticeData:
        """API에서 받은 영상 데이터를 NoticeData 객체로 변환"""
        try:
            title = element['snippet']['title']
            video_id = element['id']['videoId']
            link = f'https://www.youtube.com/watch?v={video_id}'
            published_at = element['snippet']['publishedAt']
            published = datetime.strptime(published_at, '%Y-%m-%dT%H:%M:%S%z')

            return NoticeData(
                title=title,
                link=link,
                published=published,
                scraper_type=self.scraper_type
            )

        except Exception as e:
            logger.error(f"영상 정보 파싱 중 오류: {e}")
            return None
