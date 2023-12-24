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
            },
            _id
        )

    async def signal_user_log_out(self, _id):
        if not _id:
            return

        await self.inform_users(
            {
                'mtype': 'USER_LEAVE',
                'id': _id
            },
            _id
        )

    async def inform_users(self, message, user_id):
        for _id, _web_socket in self.ws_chat.conns.items():
            if _id != user_id:
                await _web_socket.send_json(message)
