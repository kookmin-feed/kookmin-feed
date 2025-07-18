from pydantic import BaseModel
from typing import Optional, List
from config.env_loader import ENV
from fastapi.responses import JSONResponse

# ===== Response Models =====

def BoardListResponse(scrapers: List[str]):
    """게시판 목록 응답 모델"""

    if not scrapers:
        text = "현재 구독중인 게시판이 없습니다."
    else:
        text = "구독중인 게시판 목록입니다:\n\n" + "\n".join(f"- {s}" for s in scrapers)

    kakao_response = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": text
                    }
                }
            ]
        }
    }

    

    return JSONResponse(
        status_code=200,
        content=kakao_response
    )

def BoardListErrorResponse():
    """게시판 목록 조회 에러 응답 모델"""
    kakao_response = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {  
                        "text": "게시판 목록 조회 중 오류가 발생했습니다. 개발자에게 문의 부탁드립니다."
                    }
                }
            ]
        }
    }

    return JSONResponse(
        status_code=200,
        content=kakao_response
    )
