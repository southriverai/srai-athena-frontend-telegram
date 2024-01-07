import os
import re
import time
import uuid
from hashlib import sha256
from threading import Thread
from time import sleep
from typing import List

from pymongo import MongoClient
from pymongo.server_api import ServerApi

from srai_athena_frontend_telegram.service_telegram_bot import ServiceTelegramBot


class SceduleItem:
    def __init__(
        self,
        scedule_item_id: str,
        creation_time: int,
        sceduled_time: int,
        chat_id: int,
        message: str,
        repeat_type: str,
    ) -> None:
        self.scedule_item_id = scedule_item_id
        self.creation_time = creation_time
        self.sceduled_time = sceduled_time
        self.chat_id = chat_id
        self.message = message
        if repeat_type not in ["once", "minute", "hour", "day"]:
            raise Exception("repeat_type not valid")
        self.repeat_type = repeat_type

    @staticmethod
    def create(delay_in_seconds: int, chat_id: int, message: str, repeat_type: str) -> "SceduleItem":
        scedule_item_id = str(uuid.uuid4())
        creation_time = int(time.time())
        sceduled_time = creation_time + delay_in_seconds
        return SceduleItem(scedule_item_id, creation_time, sceduled_time, chat_id, message, repeat_type)

    @staticmethod
    def from_dict(dict_scedule_item: dict) -> "SceduleItem":
        scedule_item_id = dict_scedule_item["scedule_item_id"]
        creation_time = dict_scedule_item["creation_time"]
        sceduled_time = dict_scedule_item["sceduled_time"]
        chat_id = dict_scedule_item["chat_id"]
        message = dict_scedule_item["message"]
        repeat_type = dict_scedule_item["repeat_type"]
        return SceduleItem(scedule_item_id, creation_time, sceduled_time, chat_id, message, repeat_type)

    def to_dict(self) -> dict:
        return {
            "scedule_item_id": self.scedule_item_id,
            "creation_time": self.creation_time,
            "sceduled_time": self.sceduled_time,
            "chat_id": self.chat_id,
            "message": self.message,
            "repeat_type": self.repeat_type,
        }


class ServiceSceduling:
    _instance: "ServiceSceduling" = None  # type: ignore

    @staticmethod
    def get_instance() -> "ServiceSceduling":
        if ServiceSceduling._instance is None:
            raise Exception("ServiceSceduling not initialized")
        return ServiceSceduling._instance

    @staticmethod
    def initialize(bot: ServiceTelegramBot) -> None:
        ServiceSceduling._instance = ServiceSceduling(bot)

    def __init__(self, bot: ServiceTelegramBot):
        self.bot = bot
        self.thread = Thread(target=self.run, args=())
        self.is_running = False
        self.list_scedule_item: List[SceduleItem] = []
        self.last_scedule_check = int(time.time())

        connection_string = os.environ["MONGODB_CONNECTION_STRING"]
        database_name = os.environ["MONGODB_DATABASE_NAME"]
        # Create a new client and connect to the server
        self.client = MongoClient(connection_string, server_api=ServerApi("1"))
        self.db = self.client.get_database(database_name)
        self.collection = self.db.get_collection("scedule_state")

    def load_scedule_state(self) -> dict:
        key = "base_scedule_state"
        key_hash = sha256(key.encode()).hexdigest()
        result = self.collection.find_one({"_id": key_hash})
        if result is None:
            self.collection.insert_one({"_id": key_hash, "scedule_state": {}})
        scedule_state_holder = self.collection.find_one({"_id": key_hash})
        if scedule_state_holder is None:
            return {}
        return scedule_state_holder["scedule_state"]

    def save_skill_state(self, scedule_state) -> None:
        key = "base_scedule_state"
        key_hash = sha256(key.encode()).hexdigest()
        result = self.collection.find_one({"_id": key_hash})
        if result is None:
            self.collection.insert_one({"_id": key_hash, "scedule_state": scedule_state})
        else:
            self.collection.update_one({"_id": key_hash}, {"$set": {"scedule_state": scedule_state}})

    def start(self):
        self.thread.start()

    def complete_task(self):
        pass

    def check_scedule(self):
        # self.bot.message_root("check_scedule ")
        current_scedule_check = int(time.time())
        list_scedule_item_new = []
        for scedule_item in self.list_scedule_item:
            if (
                self.last_scedule_check <= scedule_item.sceduled_time
                and scedule_item.sceduled_time < current_scedule_check
            ):
                self.bot.message_chat(scedule_item.chat_id, scedule_item.message)
                command_support = self.bot.dict_command["getsupport"]
                command_support.execute_command(scedule_item.chat_id, "getsupport")

                if scedule_item.repeat_type == "once":
                    continue
                if scedule_item.repeat_type == "minute":
                    delay_in_seconds = 60
                    list_scedule_item_new.append(
                        SceduleItem.create(
                            delay_in_seconds, scedule_item.chat_id, scedule_item.message, scedule_item.repeat_type
                        )
                    )
                elif scedule_item.repeat_type == "hour":
                    delay_in_seconds = 60 * 60
                    list_scedule_item_new.append(
                        SceduleItem.create(
                            delay_in_seconds, scedule_item.chat_id, scedule_item.message, scedule_item.repeat_type
                        )
                    )
                elif scedule_item.repeat_type == "day":
                    delay_in_seconds = 60 * 60 * 24
                    list_scedule_item_new.append(
                        SceduleItem.create(
                            delay_in_seconds, scedule_item.chat_id, scedule_item.message, scedule_item.repeat_type
                        )
                    )
        self.list_scedule_item.extend(list_scedule_item_new)
        self.last_scedule_check = current_scedule_check

    def get_scedule_items(self, chat_id: int) -> List[SceduleItem]:
        list_scedule_item = []
        for scedule_item in self.list_scedule_item:
            if scedule_item.chat_id == chat_id:
                list_scedule_item.append(scedule_item)
        return list_scedule_item

    def add_scedule(self, chat_id: int):
        # create posix timestamp
        delay_in_seconds = 30
        scedule_item = SceduleItem.create(delay_in_seconds, chat_id, "test", "day")
        self.list_scedule_item.append(scedule_item)

    def remove_scedule_item_all(self, chat_id: int) -> None:
        list_scedule_item_new = []
        for scedule_item in self.list_scedule_item:
            if scedule_item.chat_id != chat_id:
                list_scedule_item_new.append(scedule_item)
        self.list_scedule_item = list_scedule_item_new

    def run(self):
        self.is_running = True
        while self.is_running:
            try:
                self.check_scedule()
                sleep(5)
            except Exception as e:
                print(e)
                pass
