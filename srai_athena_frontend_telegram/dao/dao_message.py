from typing import List

from srai_athena_frontend_telegram.dao.chat_message import ChatMessage
from srai_athena_frontend_telegram.dao.dao_mongo_base import DaoMongoBase


class DaoMessage(DaoMongoBase):
    def __init__(self, connection_string: str, database_name: str) -> None:
        super().__init__(connection_string, database_name, "chat_message")

    def save_message(self, message: ChatMessage) -> None:
        self.insert_one(message.to_dict())

    def load_messages(self, query: dict) -> List[dict]:
        return self.find(query)

    def load_messages_all(self) -> List[dict]:
        return self.find({})  # type: ignore
