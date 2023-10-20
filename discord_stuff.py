import aiohttp
import json
from config import DISCORD_CLIENT_ID, DISCORD_CLIENT_SECRET, DISCORD_REDIRECT_URI
import uuid
import storage

async def get_oauth_url():
    state = str(uuid.uuid4())
    params = {
        'client_id': DISCORD_CLIENT_ID,
        'redirect_uri': DISCORD_REDIRECT_URI,
        'response_type': 'code',
        'state': state,
        'scope': 'role_connections.write identify',
        'prompt': 'consent'
    }

    url = f"https://discord.com/api/oauth2/authorize?{'&'.join([f'{k}={v}' for k, v in params.items()])}"
    return url, state

async def get_oauth_tokens(code):
    url = 'https://discord.com/api/v10/oauth2/token'
    data = {
        'client_id': DISCORD_CLIENT_ID,
        'client_secret': DISCORD_CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': DISCORD_REDIRECT_URI
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as response:
            if response.status == 200:
                return await response.json()
            else:
                print(await response.text())
                response.raise_for_status()

async def get_user_data(tokens):
    url = 'https://discord.com/api/v10/oauth2/@me'
    headers = {
        'Authorization': f"Bearer {tokens['access_token']}"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                return await response.json()
            else:
                print(await response.text())
                response.raise_for_status()

async def push_metadata(user_id, tokens, metadata):
    url = f"https://discord.com/api/v10/users/@me/applications/{DISCORD_CLIENT_ID}/role-connection"
    headers = {
        'Authorization': f"Bearer {tokens['access_token']}",
        'Content-Type': 'application/json'
    }
    body = json.dumps({
        'platform_name': 'Example Linked Role Discord Bot',
        'metadata': metadata
    })

    async with aiohttp.ClientSession() as session:
        async with session.put(url, data=body, headers=headers) as response:
            if response.status != 200:
                print(await response.text())
                response.raise_for_status()
