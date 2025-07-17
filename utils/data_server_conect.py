import aiohttp
from config.env_loader import ENV

async def request_to_server(method: str, endpoint: str, params: dict = None, data: dict = None, headers: dict = None):
    """HTTP 요청을 처리하는 공통 함수."""
    base_url = ENV["DATA_SERVER_URL"]
    apikey = ENV["DATA_SERVER_API_KEY"]
    url = f"http://{base_url}/{endpoint}"
    if headers:
        headers.update({"Authorization": f"Bearer {apikey}"})
    else:
        headers = {"Authorization": f"Bearer {apikey}"}

    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.request(method, url, params=params, json=data) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"API 호출 실패: {response.status} - {await response.text()}")
    except aiohttp.ClientError as e:
        # 네트워크 연결 오류만 여기서 처리
        raise Exception(f"{method} 연결 실패: {url} - {str(e)}")
    except Exception as e:
        if "API 호출 실패" in str(e):
            raise
        else:
            # 예상치 못한 다른 예외
            raise Exception(f"{method} 요청 중 오류: {url} - {str(e)}")

async def get_data_from_server(endpoint: str, params: dict = None, headers: dict = None):
    """데이터 서버에 데이터를 GET 요청으로 전송합니다."""
    return await request_to_server("GET", endpoint, params=params, headers=headers)

async def post_data_to_server(endpoint: str, data: dict = None, headers: dict = None):
    """데이터 서버에 데이터를 POST 요청으로 전송합니다."""
    return await request_to_server("POST", endpoint, data=data, headers=headers)

async def put_data_to_server(endpoint: str, data: dict = None, headers: dict = None):
    """데이터 서버에 데이터를 PUT 요청으로 전송합니다."""
    return await request_to_server("PUT", endpoint, data=data, headers=headers)

async def delete_data_from_server(endpoint: str, params: dict = None, headers: dict = None):
    """데이터 서버에 DELETE 요청을 보냅니다."""
    return await request_to_server("DELETE", endpoint, params=params, headers=headers)
