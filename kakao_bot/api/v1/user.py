from fastapi import APIRouter, HTTPException
from commands.register import register_user
from api.models.common import isUnregisterUserResponse
from config.logger_config import setup_logger

logger = setup_logger(__name__)

router = APIRouter()


@router.post("/")
async def user_register(user_id: str):

    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")

    try:
        response = await register_user(user_id)

        if response.status_code == 200:
            return True
    except isUnregisterUserResponse as e:
        logger.info(e.message)
        return e.response
    except Exception as e:
        logger.error(f"Error registering user: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "Hello, World!"}