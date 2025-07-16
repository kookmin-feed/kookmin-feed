from fastapi import APIRouter, HTTPException, Depends, Request
from commands.register import register_user
from config.logger_config import setup_logger
from api.deps import get_api_key
from kakao_bot.config.env_loader import ENV
from starlette.responses import JSONResponse
logger = setup_logger(__name__)

router = APIRouter()


@router.post("/",
summary="게시판 등록",
description="게시판 등록",
tags=["board"],
responses={
    200: {"description": "게시판 등록 성공"},
    403: {"description": "이미 등록된 사용자"},
    422: {"description": "클라이언트의 잘못된 요청"}
}
)
async def board_register(
    board_id: str,
    api_key: str = Depends(get_api_key)
):
    try:
        
        # 게시판 등록 로직 (실제 구현 필요)
        
        
        return {
            "message": "Board registration successful", 
            
        }
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"게시판 등록 중 오류: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/test")
async def test(
    user_id: str,
):

    login_url = ENV.get('SERVER_URL', 'http://localhost:8000')
    response = {
    "version": "2.0",
    "template": {
        "outputs": [
            {
                    "textCard": {
                        "title": "로그인이 필요합니다",
                        "description": "로그인이 필요합니다",
                        "buttons": [
                            {
                                "action": "webLink",
                                "label": "로그인하기",
                                "webLinkUrl": f"{login_url}/login"
                            }
                        ]
                    }
                }
        ]
    }
}
    return JSONResponse(
        status_code=200,
        content=response
    )