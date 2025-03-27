from fastapi import FastAPI, Request
from typing import List, Dict
import requests
import json
from config.env_loader import ENV
from utils.scraper_type import ScraperType
from config.logger_config import setup_logger
from pydantic import BaseModel

logger = setup_logger(__name__)
app = FastAPI()

# 카카오톡 API 설정
KAKAO_API_KEY = ENV['KAKAO_API_KEY']  # 카카오 REST API 키
KAKAO_CHANNEL_ID = ENV['KAKAO_CHANNEL_ID']  # 카카오톡 채널 ID

class NoticeData(BaseModel):
    title: str
    url: str
    date: str
    category: str = None

class NoticeRequest(BaseModel):
    notices: List[NoticeData]
    scraper_type: ScraperType

def send_kakao_message(text: str, web_url: str = None):
    """카카오톡 메시지를 전송합니다."""
    headers = {
        'Authorization': f"Bearer {KAKAO_API_KEY}",
        'Content-Type': 'application/json'
    }

    template = {
        "object_type": "text",
        "text": text,
        "link": {
            "web_url": web_url,
            "mobile_web_url": web_url
        },
        "button_title": "자세히 보기"
    }

    data = {
        "template_object": json.dumps(template)
    }

    response = requests.post(
        'https://kapi.kakao.com/v2/api/talk/memo/default/send',
        headers=headers,
        data=data
    )

    if response.status_code != 200:
        logger.error(f"카카오톡 메시지 전송 실패: {response.text}")
        return False
    return True

@app.post("/notices")
async def receive_notices(request: NoticeRequest):
    """새로운 공지사항을 받아서 카카오톡으로 전송합니다."""
    try:
        for notice in request.notices:
            message = (
                f"[{request.scraper_type.get_korean_name()}] 새로운 공지사항\n\n"
                f"제목: {notice.title}\n"
                f"날짜: {notice.date}\n"
            )
            if notice.category:
                message += f"분류: {notice.category}\n"

            send_kakao_message(message, notice.url)
            logger.info(f"카카오톡 메시지 전송 완료: {notice.title}")

        return {"status": "success", "message": "메시지가 성공적으로 전송되었습니다."}

    except Exception as e:
        logger.error(f"카카오톡 메시지 전송 중 오류 발생: {e}")
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    port = ENV.get('KAKAO_PORT', 8001)
    uvicorn.run(app, host="localhost", port=port)
