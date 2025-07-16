from pydantic import BaseModel
from typing import Optional, List
from config.env_loader import ENV

# ===== Request Models =====

class BoardRegisterRequest(BaseModel):
    """게시판 등록 요청 모델"""
    user_id: str
    board_id: str

class BoardUnregisterRequest(BaseModel):
    """게시판 등록 해제 요청 모델"""
    user_id: str
    board_id: str

class BoardListRequest(BaseModel):
    """사용자 등록 게시판 목록 조회 요청 모델"""
    user_id: str
    page: int = 1
    limit: int = 10

class BoardSearchRequest(BaseModel):
    """게시판 검색 요청 모델"""
    query: str
    category: Optional[str] = None
    page: int = 1
    limit: int = 10

# ===== Response Models =====

class BoardRegisterResponse(BaseModel):
    """게시판 등록 성공 응답 모델"""
    user_id: str
    board_id: str
    message: str = "게시판 등록이 완료되었습니다."

class BoardUnregisterResponse(BaseModel):
    """게시판 등록 해제 성공 응답 모델"""
    user_id: str
    board_id: str
    message: str = "게시판 등록이 해제되었습니다."

class BoardInfo(BaseModel):
    """게시판 정보 모델"""
    board_id: str
    board_name: str
    description: Optional[str] = None
    category: Optional[str] = None

class BoardListResponse(BaseModel):
    """게시판 목록 응답 모델"""
    user_id: str
    boards: List[BoardInfo]
    total_count: int
    page: int
    limit: int

class BoardSearchResponse(BaseModel):
    """게시판 검색 응답 모델"""
    query: str
    boards: List[BoardInfo]
    total_count: int
    page: int
    limit: int

# ===== Error Response Models =====

class BoardErrorResponse(BaseModel):
    """게시판 관련 에러 응답 모델"""
    error: str
    message: str
    login_url: Optional[str] = None

# ===== Exception Classes =====

class BoardNotFoundException(Exception):
    """게시판을 찾을 수 없는 경우 발생하는 예외"""
    def __init__(self, board_id: str):
        self.message = f"게시판을 찾을 수 없습니다: {board_id}"
        super().__init__(self.message)

class DuplicateBoardRegistrationException(Exception):
    """이미 등록된 게시판에 중복 등록 시도 시 발생하는 예외"""
    def __init__(self, user_id: str, board_id: str):
        self.message = f"사용자 {user_id}는 이미 게시판 {board_id}에 등록되어 있습니다."
        super().__init__(self.message) 