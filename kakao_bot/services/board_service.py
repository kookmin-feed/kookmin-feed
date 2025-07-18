from utils.kakao_server_connect import get_data_from_server
from kakao_bot.config.env_loader import ENV
from kakao_bot.config.logger_config import setup_logger

logger = setup_logger(__name__)

async def get_board_list(user_id: str) -> list:
    """
    게시판 목록 조회
    """
    try:
        # 카카오 유저 정보 조회후 유저가 등록한 게시판 목록 파싱
        url = f"http://{ENV['DATA_SERVER_URL']}/api/v1/kakao/user"
        params = {
            "user_id": user_id
        }
        headers = {
            "Authorization": f"Bearer {ENV['DATA_SERVER_API_KEY']}"
        }
        raise Exception("test")
        user = await get_data_from_server(url, params, headers)

        return user['scrapers']

    except Exception as e:
        raise e

