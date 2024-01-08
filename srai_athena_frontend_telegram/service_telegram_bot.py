from abc import ABC
from typing import Dict
from uuid import uuid4

from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler, Updater

from srai_athena_frontend_telegram.dao.chat_message import ChatMessage
from srai_athena_frontend_telegram.dao.dao_message import DaoMessage
from srai_athena_frontend_telegram.skill.command_base import CommandBase
from srai_athena_frontend_telegram.skill.skill_base import SkillBase


class ServiceTelegramBot(ABC):
    def __init__(self, bot_token, root_id: int, dao_message: DaoMessage):
        self.bot_token = bot_token
        self.updater: Updater = None
        self.root_id = root_id
        self.list_admin_ids = [root_id]
        self.dict_skill: Dict[str, SkillBase] = {}
        self.dict_command: Dict[str, CommandBase] = {}
        self.dao_message = dao_message

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

    def handle_text(self, update: Update, context: CallbackContext):
        """Handle text messages."""
        message_id = str(update.message.message_id)
        chat_id = str(update.message.chat_id)
        author_id = str(update.message.from_user.id)
        author_name = update.message.from_user.username
        message = ChatMessage(message_id, chat_id, author_id, author_name, update.message.text)
        self.dao_message.save_message(message)
        # TODO move this to a skill or mode

    def message_root(self, text: str):
        self.message_chat(chat_id=self.root_id, text=text)

    def message_admins(self, text: str):
        for admin_id in self.list_admin_ids:
            self.message_chat(chat_id=admin_id, text=text)

    def message_chat(self, chat_id: int, text: str):
        self.updater.bot.send_message(chat_id=chat_id, text=text)
        message_id = str(uuid4())
        self.dao_message.save_message(ChatMessage(message_id, str(chat_id), "0", "bot", text))
