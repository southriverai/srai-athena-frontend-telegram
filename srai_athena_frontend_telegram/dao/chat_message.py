class ChatMessage:
    def __init__(self, message_id: str, chat_id: str, author_id: str, author_name: str, message: str):
        self.message_id = message_id
        self.chat_id = chat_id
        self.author_id = author_id
        self.author_name = author_name
        self.message = message

    def to_dict(self) -> dict:
        return {
            "message_id": self.message_id,
            "chat_id": self.chat_id,
            "author_id": self.author_id,
            "author_name": self.author_name,
            "message": self.message,
        }

    @staticmethod
    def from_dict(dict_message: dict) -> "ChatMessage":
        message_id = dict_message["message_id"]
        chat_id = dict_message["chat_id"]
        author_id = dict_message["author_id"]
        author_name = dict_message["author_name"]
        message = dict_message["message"]
        return ChatMessage(message_id, chat_id, author_id, author_name, message)
