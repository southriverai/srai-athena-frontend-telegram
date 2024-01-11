from typing import List

from srai_athena_frontend_telegram.dao.chat_message import ChatMessage
from srai_athena_frontend_telegram.dao.dao_message import DaoMessage
from srai_athena_frontend_telegram.service_telegram_bot import ServiceTelegramBot


class DaoMessageTest(DaoMessage):
    def __init__(self):
        self.dict_message = {}

    def save_message(self, message: ChatMessage) -> None:
        self.dict_message[message.message_id] = message.to_dict()

    def load_messages(self, query: dict) -> List[dict]:
        return list(self.dict_message.values())

    def load_messages_all(self) -> List[dict]:
        return list(self.dict_message.values())


class ServiceChatTest(ServiceTelegramBot):
    def __init__(self):
        super().__init__("", 0, DaoMessageTest())

    def message_chat(self, chat_id: int, text: str):
        print(text)
