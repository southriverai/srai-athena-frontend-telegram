from queue import Queue
from threading import Thread
from typing import Dict

from srai_core.base_command_handler import BaseCommandHandler
from srai_core.tools_docker import get_client_ssh, start_container_ssh

from srai_athena_frontend_telegram.service_telegram_bot import ServiceTelegramBot


class JobManager:
    def __init__(self, telegram_bot: ServiceTelegramBot) -> None:
        self.jobs = {}
        self.telegram_bot = telegram_bot
        print(telegram_bot, flush=True)

        self.is_running = False
        self.job_queue = Queue()
        self.thread = Thread(target=self.run, args=())

    def start(self):
        self.is_running = True
        self.thread.start()

    def run(self):
        print("run", flush=True)
        self.telegram_bot.message_admins(text="Job started:")
        while self.is_running:
            self.telegram_bot.message_admins(text="Job started:")
            audio_id = self.job_queue.get()
            self.telegram_bot.message_admins(text=f"Job finished: {audio_id}")
            self.telegram_bot.send_transcription(self.telegram_bot.admin_id, audio_id)
            # s3.download_file(s3_source_bucket, audio_file_name, local_audio_path)

    def start_container(
        command_handler: BaseCommandHandler,
        account_id: str,
        region_name: str,
        image_tag: str,
        container_name: str,
        dict_env: Dict[str, str],
    ) -> None:
        # TODO make this work
        pass
