import json
import aiohttp
import asyncio

from config import DISCORD_CLIENT_ID, DISCORD_TOKEN

async def register_metadata():
    url = f"https://discord.com/api/v10/applications/{DISCORD_CLIENT_ID}/role-connections/metadata"

    body = [
        {
            "key": "isiron",
            "name": "iron",
            "description": "Player is iron?",
            "type": 7,
        },
        {
            "key": "isbronze",
            "name": "Bronze",
            "description": "Player is bronze?",
            "type": 7,
        },
        {
            "key": "issilver",
            "name": "Silver",
            "description": "Player is silver?",
            "type": 7,
        },
    ]

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bot {DISCORD_TOKEN}'
    }

    async with aiohttp.ClientSession() as session:
        async with session.put(url, data=json.dumps(body), headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                print(data)
            else:
                data = await response.text()
                print(data)

asyncio.run(register_metadata())