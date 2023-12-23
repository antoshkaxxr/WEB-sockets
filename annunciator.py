class Annunciator:
    def __init__(self, chat):
        self.ws_chat = chat

    async def signal_user_log_in(self, _id):
        if not _id:
            return

        await self.inform_users(
            {
                'mtype': 'USER_ENTER',
                'id': _id
            }
        )

    async def signal_user_log_out(self, _id):
        if not _id:
            return

        await self.inform_users(
            {
                'mtype': 'USER_LEAVE',
                'id': _id
            }
        )

    async def inform_users(self, message):
        for _web_socket in self.ws_chat.conns.values():
            await _web_socket.send_json(message)
