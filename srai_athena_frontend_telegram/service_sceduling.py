import time
from threading import Thread
from time import sleep

from srai_athena_frontend_telegram.service_telegram_bot import ServiceTelegramBot


class ServiceSceduling:
    def __init__(self, bot: ServiceTelegramBot):
        self.bot = bot
        self.thread = Thread(target=self.run, args=())
        self.is_running = False
        self.list_scedule = []
        self.last_scedule_check = int(time.time())

    def start(self):
        self.thread.start()

    def complete_task(self):
        pass

    def check_scedule(self):
        current_scedule_check = int(time.time())
        for scedule in self.list_scedule:
            if current_scedule_check <= scedule["next_time"] and scedule["next_time"] < current_scedule_check:
                self.bot.message_admins(scedule["message"])

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
