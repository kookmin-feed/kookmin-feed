from fastapi import APIRouter
from api.v1 import board

api_router = APIRouter()


api_router.include_router(board.router, prefix="/board", tags=["board"])



