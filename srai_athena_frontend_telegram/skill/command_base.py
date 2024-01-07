from abc import ABC, abstractmethod

from telegram import Update
from telegram.ext import CallbackContext


class CommandBase(ABC):
    def __init__(self, skill, command_name: str) -> None:
        self.command_name = command_name
        from srai_athena_frontend_telegram.skill.skill_base import SkillBase  # avoiding circular import

        self.skill: SkillBase = skill

    def execute_command_callback(self, update: Update, context: CallbackContext):
        self.execute_command(update.message.chat_id, update.message.text)

    @abstractmethod
    def execute_command(self, chat_id: int, command_message: str) -> None:
        raise NotImplementedError()
