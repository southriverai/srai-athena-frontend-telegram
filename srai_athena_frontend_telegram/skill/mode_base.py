import os
from abc import ABC
from copy import copy
from hashlib import sha256
from typing import Callable

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from srai_athena_frontend_telegram.skill.command_base import CommandBase


class ModeBase(ABC):
    def __init__(self, service_telegram_bot) -> None:
        self.skill_name = self.__class__.__name__

        from srai_athena_frontend_telegram.service_telegram_bot import ServiceTelegramBot  # avoiding circular import

        self.service_telegram_bot: ServiceTelegramBot = service_telegram_bot
        self.command_dict = {}

        connection_string = os.environ["MONGODB_CONNECTION_STRING"]
        database_name = os.environ["MONGODB_DATABASE_NAME"]
        # Create a new client and connect to the server
        self.client = MongoClient(connection_string, server_api=ServerApi("1"))
        self.db = self.client.get_database(database_name)
        self.collection = self.db.get_collection("skill_state")

    def load_mode_state(self, chat_id) -> dict:
        key = f"{self.skill_name}_{chat_id}"
        key_hash = sha256(key.encode()).hexdigest()
        result = self.collection.find_one({"_id": key_hash})
        skill_state = {}
        if result is None:
            self.collection.insert_one({"_id": key_hash, "skill_state": skill_state})
        return skill_state

    def save_mode_state(self, chat_id, skill_state) -> None:
        key = f"{self.skill_name}_{chat_id}"
        key_hash = sha256(key.encode()).hexdigest()
        result = self.collection.find_one({"_id": key_hash})
        if result is None:
            self.collection.insert_one({"_id": key_hash, "skill_state": skill_state})
        else:
            self.collection.update_one({"_id": key_hash}, {"$set": {"skill_state": skill_state}})

    def add_command(self, command: CommandBase) -> None:
        self.command_dict[command.command_name] = command

    def get_command_dict(self) -> dict:
        return copy(self.command_dict)

    def has_command_audio(self) -> bool:
        return False

    def get_command_audio(self) -> Callable:
        raise NotImplementedError()
