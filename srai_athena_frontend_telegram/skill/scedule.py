import datetime
import json
import os

from openai import OpenAI
from telegram import Update
from telegram.ext import CallbackContext

from srai_athena_frontend_telegram.skill.skill_base import SkillBase


class Scedule(SkillBase):
    def __init__(self):
        super().__init__()
        self.client_openai = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    def get_command_dict(self) -> dict:
        dict_command = {}
        dict_command["scedule_show"] = self.parse_message_scedule_show
        dict_command["scedule_set"] = self.parse_message_scedule_set
        dict_command["scedule_stop"] = self.parse_message_scedule_stop
        return dict_command

    def parse_message_scedule_show(self, update: Update, context: CallbackContext):
        skill_state = self.load_skill_state(update.message.chat_id)
        message = self.scedule_show(skill_state, update.message.text)
        self.save_skill_state(update.message.chat_id, skill_state)
        update.message.reply_text(message)

    def parse_message_scedule_set(self, update: Update, context: CallbackContext):
        skill_state = self.load_skill_state(update.message.chat_id)
        message = self.scedule_set(skill_state, update.message.text)
        self.save_skill_state(update.message.chat_id, skill_state)
        update.message.reply_text(message)

    def parse_message_scedule_stop(self, update: Update, context: CallbackContext):
        skill_state = self.load_skill_state(update.message.chat_id)
        message = self.scedule_stop(skill_state, update.message.text)
        self.save_skill_state(update.message.chat_id, skill_state)
        update.message.reply_text(message)

    def scedule_show(self, skill_state: dict, message: str):
        return "scedule_show"

    def scedule_set(self, skill_state: dict, message: str):
        return "scedule_set"

    def scedule_stop(self, skill_state: dict, message: str):
        return "scedule_stop"
