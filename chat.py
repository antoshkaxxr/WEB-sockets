from aiohttp import web
import aiohttp
import json
import random
import string
from messenger import Messenger
from annunciator import Annunciator


class WSChat:
    def __init__(self, host='0.0.0.0', port=8080):
        self.host = host
        self.port = port
        self.conns = {}
        self.messenger = Messenger(self)
        self.annunciator = Annunciator(self)

    @staticmethod
    async def main_page(request):
        return web.FileResponse('./index.html')

    async def main_function(self, request):
        web_socket = web.WebSocketResponse()
        await web_socket.prepare(request)
        user_id = None
        async for message in web_socket:
            try:
                if message.type == aiohttp.WSMsgType.ERROR:
                    print(f'Websocket connection was suddenly closed: {web_socket.exception()}')

                if not (message.type == aiohttp.WSMsgType.TEXT and message.data):
                    continue

                _data = json.loads(message.data)
                _mtype = _data.get('mtype')

                if _mtype == 'INIT':
                    user_id = await self.maintain_init(_data, web_socket)

                if _mtype == 'TEXT':
                    await self.maintain_text(_data, user_id)
            except Exception:
                pass

        if user_id:
            del self.conns[user_id]
            await self.annunciator.signal_user_log_out(user_id)

        return web_socket

    async def maintain_init(self, data, web_socket):
        _user_id = data.get('id')
        self.conns[_user_id] = web_socket
        await self.annunciator.signal_user_log_in(_user_id)
        return _user_id

    async def maintain_text(self, data, _user_id):
        text, addressee_id = data.get('text'), data.get('to')
        if addressee_id:
            await self.messenger.send_direct_message(_user_id, addressee_id, text)
        else:
            await self.messenger.send_message_to_all_users(_user_id, text)

    def run(self):
        app = web.Application()

        app.router.add_get('/', self.main_page)
        app.router.add_get('/chat', self.main_function)

        web.run_app(app, host=self.host, port=self.port)


if __name__ == '__main__':
    WSChat().run()
