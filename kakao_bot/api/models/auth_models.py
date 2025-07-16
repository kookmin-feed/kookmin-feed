from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# ===== Request Models =====

class LoginRequest(BaseModel):
    """로그인 요청 모델"""
    username: str
    password: str

class RefreshTokenRequest(BaseModel):
    """토큰 갱신 요청 모델"""
    refresh_token: str

class LogoutRequest(BaseModel):
    """로그아웃 요청 모델"""
    access_token: str

class PasswordResetRequest(BaseModel):
    """비밀번호 재설정 요청 모델"""
    email: str

class PasswordChangeRequest(BaseModel):
    """비밀번호 변경 요청 모델"""
    user_id: str
    old_password: str
    new_password: str

# ===== Response Models =====

class LoginResponse(BaseModel):
    """로그인 성공 응답 모델"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user_id: str
    username: str

class RefreshTokenResponse(BaseModel):
    """토큰 갱신 응답 모델"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int

class LogoutResponse(BaseModel):
    """로그아웃 응답 모델"""
    message: str = "로그아웃이 완료되었습니다."

class PasswordResetResponse(BaseModel):
    """비밀번호 재설정 응답 모델"""
    message: str = "비밀번호 재설정 이메일이 발송되었습니다."
    email: str

class PasswordChangeResponse(BaseModel):
    """비밀번호 변경 응답 모델"""
    message: str = "비밀번호가 성공적으로 변경되었습니다."
    user_id: str

# ===== Error Response Models =====

class AuthErrorResponse(BaseModel):
    """인증 관련 에러 응답 모델"""
    error: str
    message: str
    error_code: Optional[str] = None

# ===== Exception Classes =====

class InvalidCredentialsException(Exception):
    """잘못된 인증 정보 예외"""
    def __init__(self, message: str = "Invalid credentials"):
        self.message = message
        super().__init__(self.message)

class TokenExpiredException(Exception):
    """토큰 만료 예외"""
    def __init__(self, message: str = "Token has expired"):
        self.message = message
        super().__init__(self.message)

class InvalidTokenException(Exception):
    """유효하지 않은 토큰 예외"""
    def __init__(self, message: str = "Invalid token"):
        self.message = message
        super().__init__(self.message)

class UnauthorizedException(Exception):
    """권한 없음 예외"""
    def __init__(self, message: str = "Unauthorized access"):
        self.message = message
        super().__init__(self.message) 