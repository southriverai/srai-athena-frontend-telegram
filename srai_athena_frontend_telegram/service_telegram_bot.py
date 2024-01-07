from abc import ABC, abstractmethod
from typing import Dict

from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler, Updater

from srai_athena_frontend_telegram.skill.command_base import CommandBase
from srai_athena_frontend_telegram.skill.skill_base import SkillBase


class ServiceTelegramBot(ABC):
    def __init__(self, bot_token, root_id: int):
        self.bot_token = bot_token
        self.updater: Updater = None
        self.root_id = root_id
        self.list_admin_ids = [root_id]
        self.dict_skill: Dict[str, SkillBase] = {}
        self.dict_command: Dict[str, CommandBase] = {}

    def register_skill(self, skill: SkillBase):
        if skill.skill_name in self.dict_skill:
            raise Exception(f"Skill name {skill.skill_name} already registered")
        self.dict_skill[skill.skill_name] = skill
        for command in skill.get_command_dict().values():
            self.register_command(command)

    def register_command(self, command: CommandBase):
        if command.command_name in self.dict_command:
            raise Exception(f"Command name {command.command_name} already registered")
        self.dict_command[command.command_name] = command
        self.updater.dispatcher.add_handler(CommandHandler(command.command_name, command.execute_command_callback))

    def message_root(self, text: str):
        self.message_chat(chat_id=self.root_id, text=text)

    def message_admins(self, text: str):
        for admin_id in self.list_admin_ids:
            self.message_chat(chat_id=admin_id, text=text)

    def message_chat(self, chat_id: int, text: str):
        bot = self.updater.bot
        bot.send_message(chat_id=chat_id, text=text)
