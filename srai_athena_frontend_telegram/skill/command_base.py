from abc import ABC, abstractmethod

from telegram import Update
from telegram.ext import CallbackContext

from srai_athena_frontend_telegram.dao.chat_message import ChatMessage


class CommandBase(ABC):
    def __init__(self, skill, command_name: str) -> None:
        self.command_name = command_name
        from srai_athena_frontend_telegram.skill.skill_base import SkillBase  # avoiding circular import

        self.skill: SkillBase = skill

    def execute_command_callback(self, update: Update, context: CallbackContext) -> None:
        message_id = str(update.message.message_id)
        chat_id = str(update.message.chat_id)
        author_id = str(update.message.from_user.id)
        author_name = update.message.from_user.username
        message = ChatMessage(message_id, chat_id, author_id, author_name, update.message.text)
        self.skill.service_telegram_bot.dao_message.save_message(message)

        self.execute_command(update.message.chat_id, update.message.text)

    @abstractmethod
    def execute_command(self, chat_id: int, command_message: str) -> None:
        raise NotImplementedError()
