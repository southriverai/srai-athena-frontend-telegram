from typing import List, Optional

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from srai_athena_frontend_telegram.skill import userdata


class Userdata:
    def __init__(
        self,
        channel_id: str,
        username: Optional[str],
        date_of_birth: Optional[str],
        current_location: Optional[str],
    ) -> None:
        self.channel_id = channel_id
        self.username = username
        self.date_of_birth = date_of_birth
        self.current_location = current_location

    @staticmethod
    def from_dict(json_dict: dict) -> "Userdata":
        channel_id = json_dict["channel_id"]
        username = json_dict["username"]
        date_of_birth = json_dict["date_of_birth"]
        current_location = json_dict["current_location"]
        return Userdata(channel_id, username, date_of_birth, current_location)

    def to_dict(self) -> dict:
        json_dict = {}
        json_dict["channel_id"] = self.channel_id
        json_dict["username"] = self.username
        json_dict["date_of_birth"] = self.date_of_birth
        json_dict["current_location"] = self.current_location
        return json_dict


class DaoUserdata:
    def __init__(self, connection_string: str, database_name: str):
        self.mongo_database = MongoClient(connection_string, server_api=ServerApi("1")).get_database(database_name)
        self.mongo_collection = self.mongo_database.get_collection("userdata")

    def update_username(self, channel_id: str, username: str) -> Userdata:
        dict_userdata = self.mongo_collection.find_one({"channel_id": channel_id})
        if dict_userdata is None:
            userdata = Userdata(channel_id, username, None, None)
        else:
            userdata = Userdata.from_dict(dict_userdata)
            userdata.username = username
        self.mongo_collection.update_one({"channel_id": channel_id}, userdata.to_dict(), upsert=True)
        return userdata
