class ChatMessage:
    def __init__(self, message_id: str, channel_id: str, author_id: str, author_name: str, message_content: dict):
        self.message_id = message_id
        self.channel_id = channel_id
        self.author_id = author_id
        self.author_name = author_name
        self.message_content = message_content

    def to_dict(self) -> dict:
        return {
            "message_id": self.message_id,
            "channel_id": self.channel_id,
            "author_id": self.author_id,
            "author_name": self.author_name,
            "message_content": self.message_content,
        }

    @staticmethod
    def from_dict(dict_message: dict) -> "ChatMessage":
        message_id = dict_message["message_id"]
        chat_id = dict_message["channel_id"]
        author_id = dict_message["author_id"]
        author_name = dict_message["author_name"]
        message_content = dict_message["message_content"]
        return ChatMessage(message_id, chat_id, author_id, author_name, message_content)
