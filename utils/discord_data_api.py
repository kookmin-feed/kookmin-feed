from utils.data_server_conect import request_to_server

# Direct Messages
async def get_all_direct_messages():
    """모든 Direct Message(DM) 리스트를 가져옵니다."""
    return await request_to_server("GET", "api/v1/discord/direct-messages")

async def create_direct_message(user_id: str, user_name: str, scrapers: list):
    """새로운 Direct Message(DM)를 생성합니다."""
    data = {"user_id": user_id, "user_name": user_name, "scrapers": scrapers}
    return await request_to_server("POST", "api/v1/discord/direct-messages", data=data)

async def get_direct_message(user_id: str):
    """특정 유저의 Direct Message(DM)를 조회합니다."""
    params = {"user_id": user_id}
    try: 
        return await request_to_server("GET", "api/v1/discord/direct-message", params=params)
    except:
        return None
    

async def update_direct_message(user_id: str, scrapers: list):
    """특정 유저의 Direct Message(DM)를 업데이트합니다."""
    data = {"user_id": user_id, "scrapers": scrapers}
    return await request_to_server("PUT", "api/v1/discord/direct-messages", data=data)

async def delete_direct_message(user_id: str):
    """특정 유저의 Direct Message(DM)를 삭제합니다."""
    params = {"user_id": user_id}
    return await request_to_server("DELETE", "api/v1/discord/direct-messages", params=params)

# Server Channels
async def get_all_server_channels():
    """모든 서버 채널 리스트를 가져옵니다."""
    return await request_to_server("GET", "api/v1/discord/server-channels")

async def create_server_channel(guild_name: str, channel_id: str, channel_name: str, scrapers: list):
    """새로운 서버 채널을 생성합니다."""
    data = {
        "guild_name": guild_name,
        "channel_id": channel_id,
        "channel_name": channel_name,
        "scrapers": scrapers
    }
    return await request_to_server("POST", "api/v1/discord/server-channels", data=data)

async def get_server_channel(channel_id: str):
    """특정 서버 채널을 조회합니다."""
    params = {"channel_id": channel_id}
    try:
        return await request_to_server("GET", "api/v1/discord/server-channel", params=params)
    except:
        return None

async def update_server_channel(channel_id: str, scrapers: list):
    """특정 서버 채널을 업데이트합니다."""
    data = {"channel_id": channel_id, "scrapers": scrapers}
    return await request_to_server("PUT", "api/v1/discord/server-channels", data=data)

async def delete_server_channel(channel_id: str):
    """특정 서버 채널을 삭제합니다."""
    params = {"channel_id": channel_id}
    return await request_to_server("DELETE", "api/v1/discord/server-channels", params=params)
