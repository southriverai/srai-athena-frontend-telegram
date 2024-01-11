import os
import sys

from service_chat_test import ServiceChatTest

from srai_athena_frontend_telegram.service_persistency import ServicePersistency
from srai_athena_frontend_telegram.skill.mode_support import ModeSupport


def main() -> None:
    connection_string = os.environ["MONGODB_CONNECTION_STRING"]
    database_name = os.environ["MONGODB_DATABASE_NAME"]
    ServicePersistency.initialize(connection_string, database_name)
    if "-r" in sys.argv:
        print("resetting database")
        ServicePersistency.get_instance().dao_support_state.collection.delete_many({})
    mode_support = ModeSupport(ServiceChatTest())
    mode_support.process_message(0, "")
    while True:
        user_message = input("user :")
        mode_support.process_message(0, user_message)


if __name__ == "__main__":
    main()
