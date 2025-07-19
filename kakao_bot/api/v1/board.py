from fastapi import APIRouter, HTTPException, Depends, Request, Query
from services.register import register_user
from services.board_service import get_board_list, add_board
from kakao_bot.config.logger_config import setup_logger
from kakao_bot.api.deps import get_api_key
from kakao_bot.config.env_loader import ENV
from kakao_bot.api.models.board_models import BoardListResponse, BoardErrorResponse, BoardRegisterResponse, BoardAlreadyExists

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
    request: Request,
    board_name: str = Query(description="게시판 이름"),
    api_key: str = Depends(get_api_key)
):
    try:
        data = await request.json()
        user_id = data.get('userRequest').get('user').get('properties').get('app_user_id')
        await add_board(user_id, board_name)
        
        logger.info(f"게시판 등록 성공: {user_id}, {board_name}")
        return BoardRegisterResponse(board_name, already_registered=False)
    except BoardAlreadyExists as e:
        logger.info(f"이미 등록된 게시판: {e}")
        return BoardRegisterResponse(board_name, already_registered=True)
    except Exception as e:
        logger.error(f"게시판 등록 중 오류: {e}")
        return BoardErrorResponse()


@router.post("/list")
async def board_list(
    request: Request,
    api_key: str = Depends(get_api_key)
):
    try:
        data = await request.json()
        user_id = data.get('userRequest').get('user').get('properties').get('app_user_id')
        
        board_list = await get_board_list(user_id)
        logger.info(f"게시판 목록 조회 성공: {board_list}")
        return BoardListResponse(board_list)
    except Exception as e:
        logger.error(f"게시판 목록 조회 중 오류: {e}")
        return BoardErrorResponse()