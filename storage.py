store = {}

async def store_discord_tokens(user_id, tokens):
    store[f"discord-{user_id}"] = tokens


async def get_discord_tokens(user_id):
    return store.get(f"discord-{user_id}")