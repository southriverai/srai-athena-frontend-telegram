from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from srai_athena_frontend_telegram.dao.dao_message import DaoMessage
from srai_athena_frontend_telegram.dao.dao_mongo_base import DaoMongoBase


class ServicePersistency:
    _instance: "ServicePersistency" = None  # type: ignore

    @staticmethod
    def get_instance() -> "ServicePersistency":
        if ServicePersistency._instance is None:
            raise Exception("ServiceSceduling not initialized")
        return ServicePersistency._instance

    @staticmethod
    def initialize(connection_string: str, database_name: str) -> None:
        ServicePersistency._instance = ServicePersistency(connection_string, database_name)

    def __init__(self, connection_string: str, database_name: str):
        # Create a new client and connect to the server
        self.client = MongoClient(connection_string, server_api=ServerApi("1"))
        self.mongo_database = self.client.get_database(database_name)
        # daos
        self.dao_support_state = DaoMongoBase(connection_string, database_name, "support_state")
        self.dao_message = DaoMessage(connection_string, database_name)
        self.dao_userdata = DaoUserdata(connection_string, database_name)
