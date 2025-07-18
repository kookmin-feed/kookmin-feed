from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from kakao_bot.config.env_loader import ENV
from starlette.responses import JSONResponse


# ===== Response Creation Functions =====

def create_login_response() -> JSONResponse:
    """미들웨어에서 로그인 링크가 포함된 카카오톡 응답 생성"""
    login_url = f"https://kauth.kakao.com/oauth/authorize?client_id={ENV.get('KAKAO_CLIENT_ID')}&redirect_uri={ENV.get('KAKAO_REDIRECT_URL')}&response_type=code&scope=talk_message"
    
    kakao_response = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "textCard": {
                        "title": "로그인 필요합니다",
                        "description": "로그인이 필요합니다",
                        "buttons": [
                            {
                                "action": "webLink",
                                "label": "로그인하기",
                                "webLinkUrl": f"{login_url}"
                            }
                        ]
                    }
                }
            ]
        }
    }
    
    return JSONResponse(
        status_code=200,
        content=kakao_response
    )

def create_error_response() -> JSONResponse:
    """미들웨어에서 에러 응답 생성"""
    kakao_response = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": f"로그인 오류가 발생했습니다. 개발자에게 문의 부탁드립니다."
                    }
                }
            ]
        }
    }
    
    return JSONResponse(
        status_code=200,
        content=kakao_response
    )


# ===== Response Models =====

class LoginRequiredResponse(BaseModel):
    version: str = "2.0"
    template: dict
    
    @classmethod
    def create(cls) -> "LoginRequiredResponse":
        login_url = f"{ENV.get('SERVER_URL', 'http://localhost:8000')}/api/v1/login"
        template = {
            "outputs": [{
                "basicCard": {
                    "title": "로그인이 필요합니다",
                    "description": "로그인 후 이용해주세요.",
                    "buttons": [{
                        "action": "webLink",
                        "label": "로그인하기", 
                        "webLinkUrl": f"{login_url}"
                    }]
                }
            }]
        }
        return cls(template=template)

# ===== Request Models =====

class KakaoCreateUser(BaseModel):
    user_id: str
    scrapers: List[str]
    access_token: str
    refresh_token: str
    expires_in: int
    refresh_token_expires_in: int

# ===== Exception Models =====

class UserAlreadyExists(Exception):
    status_code: int = 409
    detail: str = "User already exists"
    