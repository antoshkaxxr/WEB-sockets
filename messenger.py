class Messenger:
    def __init__(self, chat):
        self.ws_chat = chat

    async def send_message_to_all_users(self, sender_id, message_text):
        if not message_text:
            return

        for _id, web_socket in self.ws_chat.conns.items():
            if _id != sender_id:
                await web_socket.send_json(
                    {
                        'mtype': 'MSG',
                        'id': sender_id,
                        'text': message_text
                    }
                )

    async def send_direct_message(self, sender_id, addressee_id, message_text):
        if not message_text:
            return

        message = {
            'mtype': 'DM',
            'id': sender_id,
            'text': message_text
        }

        await self.inform_user(addressee_id, message)
        await self.inform_user(sender_id, message)

    async def inform_user(self, _id, message):
        if _id in self.ws_chat.conns:
            _web_socket = self.ws_chat.conns[_id]
            await _web_socket.send_json(message)
