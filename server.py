from aiohttp import web
import aiohttp
import json
from config import DISCORD_CLIENT_ID, DISCORD_TOKEN, COOKIE_SECRET, DISCORD_CLIENT_SECRET, DISCORD_REDIRECT_URI
import discord_stuff
import storage
import asyncio

routes = web.RouteTableDef()


@routes.get('/')
async def hello(request):
    return web.Response(text="👋")


@routes.get('/linked-role')
async def linked_role(request):
    url, state = await discord_stuff.get_oauth_url()
    response = web.HTTPFound(location=url)
    response.set_cookie('clientState', state, max_age=60 * 5)  # 5 minutes
    return response


@routes.get('/discord-oauth-callback')
async def discord_oauth_callback(request):
    try:
        code = request.rel_url.query['code']
        discord_state = request.rel_url.query['state']
        client_state = request.cookies.get('clientState')

        if client_state != discord_state:
            print('State verification failed.')
            raise web.HTTPForbidden()

        tokens = await discord_stuff.get_oauth_tokens(code)
        me_data = await discord_stuff.get_user_data(tokens)
        user_id = me_data['user']['id']

        await storage.store_discord_tokens(user_id, tokens)

        await update_metadata(user_id)
        return web.Response(text="You did it! Now go back to Discord.")
    except Exception as e:
        print(e)
        raise web.HTTPInternalServerError()


@routes.post('/update-metadata')
async def update_metadata_route(request):
    try:
        body = await request.json()
        user_id = body.get('userId')
        await update_metadata(user_id)
        raise web.HTTPNoContent()
    except Exception as e:
        print(e)
        raise web.HTTPInternalServerError()


async def update_metadata(user_id):
    tokens = await storage.get_discord_tokens(user_id)
    metadata = {
        'isiron': 0,
        'isbronze': 1,
        'issilver': 0
    }
    await discord_stuff.push_metadata(user_id, tokens, metadata)


app = web.Application()
app.add_routes(routes)

if __name__ == '__main__':
    web.run_app(app, port=3000)
