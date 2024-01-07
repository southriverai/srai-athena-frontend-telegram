import os
import time

from openai import OpenAI

from srai_athena_frontend_telegram.service_sceduling import ServiceSceduling
from srai_athena_frontend_telegram.service_telegram_bot import ServiceTelegramBot
from srai_athena_frontend_telegram.skill.command_base import CommandBase
from srai_athena_frontend_telegram.skill.skill_base import SkillBase


class CommandSceduleShow(CommandBase):
    def __init__(self, skill: SkillBase) -> None:
        super().__init__(skill, "scedule_show")

    def execute_command(self, chat_id: int, command_message: str) -> None:
        skill_state = self.skill.load_skill_state(chat_id)
        list_scedule_items = ServiceSceduling.get_instance().get_scedule_items(chat_id)
        if len(list_scedule_items) == 0:
            self.skill.service_telegram_bot.message_chat(chat_id, "No scedule items")
            return
        message = ""
        for scedule_item in list_scedule_items:
            time_until = scedule_item.sceduled_time - int(time.time())
            message += f"{scedule_item.scedule_item_id} time until {time_until}"
            message += f"{scedule_item.message}\n"
        self.skill.service_telegram_bot.message_chat(chat_id, message)
        self.skill.save_skill_state(chat_id, skill_state)


class CommandSceduleSet(CommandBase):
    def __init__(self, skill: SkillBase) -> None:
        super().__init__(skill, "scedule_set")

    def execute_command(self, chat_id: int, command_message: str) -> None:
        ServiceSceduling.get_instance().add_scedule(chat_id)
        message = (
            "All your daily messages are now scheduled to the current time of day and will fire 30 seconds from now"
        )
        self.skill.service_telegram_bot.message_chat(chat_id, message)


class CommandSceduleStop(CommandBase):
    def __init__(self, skill: SkillBase) -> None:
        super().__init__(skill, "scedule_stop")

    def execute_command(self, chat_id: int, command_message: str) -> None:
        ServiceSceduling.get_instance().remove_scedule_item_all(chat_id)
        message = "All your daily messages are now stopped"
        self.skill.service_telegram_bot.message_chat(chat_id, message)


class Scedule(SkillBase):
    def __init__(self, service_telegram_bot: ServiceTelegramBot):
        super().__init__(service_telegram_bot)
        self.client_openai = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        self.add_command(CommandSceduleShow(self))
        self.add_command(CommandSceduleSet(self))
        self.add_command(CommandSceduleStop(self))
