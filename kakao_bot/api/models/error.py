from pydantic import BaseModel

class ErrorResponse(BaseModel):
    detail: str

    class Config:
        schema_extra = {
            "example": {
                "detail": "User is already registered"
            }
        }