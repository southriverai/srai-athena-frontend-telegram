import datetime
import json
import os

from openai import OpenAI
from telegram import Update
from telegram.ext import CallbackContext

from srai_athena_frontend_telegram.service_telegram_bot import ServiceTelegramBot
from srai_athena_frontend_telegram.skill.skill_base import SkillBase


class Postplan(SkillBase):
    def __init__(self, service_telegram_bot: ServiceTelegramBot):
        super().__init__(service_telegram_bot)
        self.client_openai = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    def get_command_dict(self) -> dict:
        dict_command = {}
        dict_command["postplan"] = self.parse_message_postplan
        dict_command["postgenerate"] = self.parse_message_postgenerate
        return dict_command

    def parse_message_postplan(self, update: Update, context: CallbackContext):
        skill_state = self.load_skill_state(update.message.chat_id)
        message = self.parse_command_postplan(skill_state, update.message.text)
        self.save_skill_state(update.message.chat_id, skill_state)
        update.message.reply_text(message)

    def parse_message_postgenerate(self, update: Update, context: CallbackContext):
        skill_state = self.load_skill_state(update.message.chat_id)
        message = self.parse_command_postgenerate(skill_state, update.message.text)
        self.save_skill_state(update.message.chat_id, skill_state)
        update.message.reply_text(message)

    def parse_command_postplan(self, skill_state: dict, message: str):
        command_part = message.split(" ")
        if 1 < len(command_part):
            date = command_part[1]
        else:
            date = None

        if date is not None:
            return self.get_postplan_date(
                skill_state,
                date,
            )
        else:
            return self.get_postplan(
                skill_state,
            )

    def parse_command_postgenerate(self, skill_state: dict, message: str):
        command_part = message.split(" ")
        if 1 < len(command_part):
            date = command_part[1]
        else:
            date = None

        if date is None:
            return "Please provide a valid date argument"
        else:
            return self.postgenerate(skill_state, date)

    def get_postplan_dict(self, skill_state: dict) -> dict:
        postplan = {}
        postplan["plan"] = {}
        postplan["plan"] = {
            "monday": {
                "title": "Manual Monday",
                "time_gmt": "12:00",
                "goal": "Manual Monday is a day where we post a manual on project athena. ",
            },
            "tuesday": {
                "title": "Turbulent Tuesday",
                "time_gmt": "12:00",
                "goal": "Generate a 500 word linkedin blog based on the weekly news",
            },
            "wednesday": {
                "title": "Wired Wednesday",
                "time_gmt": "12:00",
                "goal": "Generate a 500 word linkedin blog showcasing the weekly code changes. ",
            },
            "thursday": {
                "title": "Trepid Thursday",
                "time_gmt": "12:00",
                "goal": "Generate a 500 word linkedin blog filled with corperate bullshit. ",
            },
            "friday": {
                "title": "Voicenote Friday",
                "time_gmt": "12:00",
                "goal": "MGenerate a 500 word linkedin blog based on a series of voicenotes. ",
            },
        }
        postplan["scedule"] = {}
        date_today = datetime.datetime.now()
        for i in range(7):
            date = date_today + datetime.timedelta(days=i)
            date_str = date.strftime("%Y-%m-%d")
            day = date.strftime("%A").lower()
            if day in postplan["plan"]:
                postplan["scedule"][date_str] = postplan["plan"][day]
        return postplan
        # generate scedule for the next 7 days

    def get_postplan(
        self,
        skill_state: dict,
    ) -> str:
        postplan = self.get_postplan_dict(skill_state)
        message = "Postplan" + json.dumps(postplan, indent=4, sort_keys=True)
        return message

    def get_postplan_date(
        self,
        skill_state: dict,
        date: str,
    ) -> str:
        postplan = self.get_postplan_dict(skill_state)
        if date in postplan["scedule"]:
            postplan_date = postplan["scedule"][date]
            message = "Postplan date" + json.dumps(postplan_date, indent=4, sort_keys=True)
            return message
        else:
            message = "no postplan found for date: " + date
            return message

    def postgenerate(
        self,
        skill_state: dict,
        date: str,
    ) -> str:
        postplan = self.get_postplan_dict(skill_state)
        if date in skill_state:
            message = skill_state[date]
            message = "Postplan date" + json.dumps(postplan_date, indent=4, sort_keys=True)
            return message
        if date in postplan["scedule"]:
            postplan_date = postplan["scedule"][date]

            system_message = {
                "role": "system",
                "content": """
                You are a asssitent for writing blog posts for linkedin.
                Post should be about 3 paragraphs long and should be about 500 words.
                Post are based on a json template.
                Post should follow the goal of the template.
                Post should incorperate the datasources in the template.
                """,
            }
            user_message = {
                "role": "user",
                "content": json.dumps(postplan_date),
            }

            suffix = """
            Generation Code Repo
            https://lnkd.in/eTXDGWxY
            Content repo
            https://lnkd.in/e9ZhJeQZ
            """

            list_message = []
            list_message.append(system_message)
            list_message.append(user_message)
            response = self.client_openai.chat.completions.create(
                model="gpt-4",
                messages=list_message,
                temperature=1,
            )

            message = postplan_date["title"] + "\n" + response.choices[0].message.content + suffix
            return message
        else:
            message = "no postplan found for date: " + date
            return message
