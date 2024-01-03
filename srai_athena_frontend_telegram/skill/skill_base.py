import os
from abc import ABC, abstractmethod
from hashlib import sha256
from typing import Callable

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


class SkillBase(ABC):
    def __init__(self) -> None:
        self.skill_name = self.__class__.__name__

        connection_string = os.environ["MONGODB_CONNECTION_STRING"]
        database_name = os.environ["MONGODB_DATABASE_NAME"]
        # Create a new client and connect to the server
        self.client = MongoClient(connection_string, server_api=ServerApi("1"))
        self.db = self.client.get_database(database_name)
        self.collection = self.db.get_collection("skill_state")

    def load_skill_state(self, chat_id) -> dict:
        key = f"{self.skill_name}_{chat_id}"
        key_hash = sha256(key.encode()).hexdigest()
        result = self.collection.find_one({"_id": key_hash})
        if result is None:
            self.collection.insert_one({"_id": key_hash, "skill_state": {}})
        return self.collection.find_one({"_id": key_hash})["skill_state"]

    def save_skill_state(self, chat_id, skill_state) -> None:
        key = f"{self.skill_name}_{chat_id}"
        key_hash = sha256(key.encode()).hexdigest()
        result = self.collection.find_one({"_id": key_hash})
        if result is None:
            self.collection.insert_one({"_id": key_hash, "skill_state": skill_state})
        else:
            self.collection.update_one({"_id": key_hash}, {"$set": {"skill_state": skill_state}})

    @abstractmethod
    def get_command_dict(self) -> dict:
        raise NotImplementedError()

    def has_command_audio(self) -> bool:
        return False

    def get_command_audio(self) -> Callable:
        raise NotImplementedError()
