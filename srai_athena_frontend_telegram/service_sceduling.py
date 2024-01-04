import os
import time
from hashlib import sha256
from threading import Thread
from time import sleep

from pymongo import MongoClient
from pymongo.server_api import ServerApi

from srai_athena_frontend_telegram.service_telegram_bot import ServiceTelegramBot


class ServiceSceduling:
    def __init__(self, bot: ServiceTelegramBot):
        self.bot = bot
        self.thread = Thread(target=self.run, args=())
        self.is_running = False
        self.list_scedule = []
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
        current_scedule_check = int(time.time())
        list_scedule_item_new = []
        for scedule in self.list_scedule:
            if current_scedule_check <= scedule["next_time"] and scedule["next_time"] < current_scedule_check:
                self.bot.message_admins(scedule["message"])
                creation_time = int(time.time())
                scedule_item_new = {
                    "creation_time": creation_time,
                    "next_time": creation_time + scedule["increment_in_seconds"],
                    "increment_in_seconds": scedule["increment_in_seconds"],
                    "chat_id": 1325892490,
                    "message": "test",
                }
                list_scedule_item_new.append(scedule_item_new)

        self.last_scedule_check = current_scedule_check

    def add_scedule(self):
        # create posix timestamp
        creation_time = int(time.time())
        increment_in_seconds = 30
        scedule = {
            "creation_time": creation_time,
            "next_time": creation_time + increment_in_seconds,
            "increment_in_seconds": increment_in_seconds,
            "chat_id": 1325892490,
            "message": "test",
        }
        self.list_scedule.append(scedule)

    def run(self):
        self.is_running = True
        while self.is_running:
            try:
                self.check_scedule()
                sleep(5)
            except Exception as e:
                pass
