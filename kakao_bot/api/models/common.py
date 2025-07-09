from pydantic import BaseModel
from config.env_loader import ENV

class isUnregisterUserResponse(BaseModel):
    message: str

    class Config:
        schema_extra = {
            "example": {
                "message": "User is already registered",
                "response": {
                    "version": "2.0",
                    "template": {
                        "outputs": [
                            {
                                "simpleText": {
                                    "text": "간단한 텍스트 요소입니다."
                                }
                            }
                        ]
                    }
                }
            }
        }