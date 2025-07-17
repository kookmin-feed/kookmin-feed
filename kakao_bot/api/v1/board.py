from fastapi import APIRouter, HTTPException, Depends, Request
from commands.register import register_user
from kakao_bot.config.logger_config import setup_logger
from kakao_bot.api.deps import get_api_key
from kakao_bot.config.env_loader import ENV

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