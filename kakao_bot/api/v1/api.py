from fastapi import APIRouter
from api.v1 import board
from api.v1 import auth
api_router = APIRouter()


api_router.include_router(board.router, prefix="/board", tags=["board"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])


