from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from kakao_bot.config.env_loader import ENV

# ===== Request Models =====

class KakaoSkillRequest(BaseModel):
    """카카오톡 스킬 요청 모델"""
    userRequest: Dict[str, Any]
    bot: Dict[str, Any]
    action: Dict[str, Any]

class KakaoCallbackRequest(BaseModel):
    """카카오톡 콜백 요청 모델"""
    user_id: str
    message: str
    intent: Optional[str] = None
    entities: Optional[Dict[str, Any]] = None

class KakaoBotCommandRequest(BaseModel):
    """카카오톡 봇 명령어 요청 모델"""
    command: str
    user_id: str
    parameters: Optional[Dict[str, Any]] = None

class KakaoQuickReplyRequest(BaseModel):
    """카카오톡 퀵 리플라이 요청 모델"""
    user_id: str
    selected_action: str
    context: Optional[Dict[str, Any]] = None

# ===== Response Models =====

class KakaoSimpleText(BaseModel):
    """카카오톡 단순 텍스트 응답 모델"""
    text: str

class KakaoBasicCard(BaseModel):
    """카카오톡 기본 카드 응답 모델"""
    title: str
    description: Optional[str] = None
    thumbnail: Optional[Dict[str, str]] = None
    buttons: Optional[List[Dict[str, Any]]] = None

class KakaoQuickReply(BaseModel):
    """카카오톡 퀵 리플라이 모델"""
    label: str
    action: str
    messageText: Optional[str] = None

class KakaoSkillResponse(BaseModel):
    """카카오톡 스킬 응답 모델"""
    version: str = "2.0"
    template: Dict[str, Any]
    context: Optional[Dict[str, Any]] = None
    data: Optional[Dict[str, Any]] = None

    @classmethod
    def create_simple_text(cls, text: str) -> "KakaoSkillResponse":
        """단순 텍스트 응답 생성"""
        return cls(
            template={
                "outputs": [
                    {
                        "simpleText": {
                            "text": text
                        }
                    }
                ]
            }
        )

    @classmethod
    def create_basic_card(cls, title: str, description: str = None, 
                         thumbnail: Dict[str, str] = None, 
                         buttons: List[Dict[str, Any]] = None) -> "KakaoSkillResponse":
        """기본 카드 응답 생성"""
        card = {
            "title": title
        }
        if description:
            card["description"] = description
        if thumbnail:
            card["thumbnail"] = thumbnail
        if buttons:
            card["buttons"] = buttons
            
        return cls(
            template={
                "outputs": [
                    {
                        "basicCard": card
                    }
                ]
            }
        )

    @classmethod
    def create_with_quick_replies(cls, text: str, 
                                 quick_replies: List[KakaoQuickReply]) -> "KakaoSkillResponse":
        """퀵 리플라이가 포함된 응답 생성"""
        return cls(
            template={
                "outputs": [
                    {
                        "simpleText": {
                            "text": text
                        }
                    }
                ],
                "quickReplies": [qr.dict() for qr in quick_replies]
            }
        )

class KakaoErrorResponse(BaseModel):
    """카카오톡 에러 응답 모델"""
    version: str = "2.0"
    template: Dict[str, Any]
    
    def __init__(self, error_message: str, **data):
        login_url = ENV.get('SERVER_URL', 'http://localhost:8000')
        template = {
            "outputs": [
                {
                    "simpleText": {
                        "text": f"{error_message}. 로그인하세요: {login_url}/login"
                    }
                }
            ]
        }
        super().__init__(template=template, **data)

# ===== Utility Models =====

class KakaoUser(BaseModel):
    """카카오톡 사용자 정보 모델"""
    id: str
    type: str
    properties: Optional[Dict[str, Any]] = None

class KakaoBot(BaseModel):
    """카카오톡 봇 정보 모델"""
    id: str
    name: str

class KakaoAction(BaseModel):
    """카카오톡 액션 정보 모델"""
    id: str
    name: str
    params: Optional[Dict[str, Any]] = None
    detailParams: Optional[Dict[str, Any]] = None
    clientExtra: Optional[Dict[str, Any]] = None

# ===== Exception Classes =====

class KakaoSkillException(Exception):
    """카카오톡 스킬 관련 예외"""
    def __init__(self, message: str, error_code: str = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)

class InvalidKakaoRequestException(Exception):
    """유효하지 않은 카카오톡 요청 예외"""
    def __init__(self, message: str = "Invalid Kakao request format"):
        self.message = message
        super().__init__(self.message) 