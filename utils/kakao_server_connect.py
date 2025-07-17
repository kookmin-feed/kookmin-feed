

import aiohttp
from config.env_loader import ENV

async def request_to_server(method: str, url: str, params: dict = None, data: dict = None, headers: dict = None):
    """HTTP 요청을 처리하는 공통 함수."""
    try:
        if headers and headers.get("Content-Type") == "application/x-www-form-urlencoded;charset=utf-8":
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.request(method, url, params=params, data=data) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        raise Exception(f"API 호출 실패: {response.status} - {await response.text()}")
        else:
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.request(method, url,params=params, json=data) as response:
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

async def get_data_from_server(url: str, params: dict = None, headers: dict = None):
    """데이터 서버에 데이터를 GET 요청으로 전송합니다."""
    return await request_to_server("GET", url, params=params, headers=headers)

async def post_data_to_server(url: str, data: dict = None, headers: dict = None):
    """데이터 서버에 데이터를 POST 요청으로 전송합니다."""
    return await request_to_server("POST", url, data=data, headers=headers)

async def put_data_to_server(url: str, data: dict = None, headers: dict = None):
    """데이터 서버에 데이터를 PUT 요청으로 전송합니다."""
    return await request_to_server("PUT", url, data=data, headers=headers)

async def delete_data_from_server(url: str, params: dict = None, headers: dict = None):
    """데이터 서버에 DELETE 요청을 보냅니다."""
    return await request_to_server("DELETE", url, params=params, headers=headers)
