from kakao_bot.utils.kakao_server_connect import get_data_from_server, put_data_to_server
from kakao_bot.config.env_loader import ENV
from kakao_bot.config.logger_config import setup_logger
from kakao_bot.api.models.board_models import BoardAlreadyExists

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
        user = await get_data_from_server(url, params, headers)

        return user['scrapers']

    except Exception as e:
        raise e

async def add_board(user_id: str, board_name: str) -> bool:
    """
    게시판 등록
    """
    try:
        
        # 게시판 등록 로직 (실제 구현 필요)
        board_list = await get_board_list(user_id)
        if board_name in board_list:
            raise BoardAlreadyExists()
        board_list.append(board_name)
        url = f"http://{ENV['DATA_SERVER_URL']}/api/v1/kakao/user"

        params = {
            "user_id": user_id,
            "scrapers": board_list
        }
        headers = {
            "Authorization": f"Bearer {ENV['DATA_SERVER_API_KEY']}"
        }
        await put_data_to_server(url, params, headers)
        
        return True
    except Exception as e:
        raise e
