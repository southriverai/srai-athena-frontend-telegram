import datetime
import json
import os

from openai import OpenAI

from srai_athena_frontend_telegram.service_telegram_bot import ServiceTelegramBot
from srai_athena_frontend_telegram.skill.command_base import CommandBase
from srai_athena_frontend_telegram.skill.skill_base import SkillBase


def get_postplan_dict(skill_state: dict) -> dict:
    postplan = {}
    postplan["plan"] = {}
    postplan["plan"] = {
        "monday": {
            "title": "Manual Monday",
            "time_gmt": "12:00",
            "generator_type": "manual",
            "goal": "Manual Monday is a day where we post a manual on project athena. ",
        },
        "tuesday": {
            "title": "Turbulent Tuesday",
            "time_gmt": "12:00",
            "generator_type": "hackernews",
            "goal": "Generate a 500 word linkedin blog based on the weekly news",
        },
        "wednesday": {
            "title": "Wired Wednesday",
            "time_gmt": "12:00",
            "generator_type": "github",
            "goal": "Generate a 500 word linkedin blog showcasing the weekly code changes. ",
        },
        "thursday": {
            "title": "Image Thursday",
            "time_gmt": "12:00",
            "generator_type": "image",
            "goal": "Generate a 500 word linkedin blog filled with corperate bullshit. ",
        },
        "friday": {
            "title": "Voicenote Friday",
            "time_gmt": "12:00",
            "generator_type": "voice",
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


class CommandPostplan(CommandBase):
    def __init__(self, skill: SkillBase) -> None:
        super().__init__(skill, "postplan")

    def get_usage(self) -> str:
        return """
        Usage:
        /postplan {date}
        Example:
        /postplan 2024-01-04
        Description:
        Gets a postplan for a specified date.
        """

    def execute_command(self, chat_id: int, command_message: str) -> None:
        command_part = command_message.split(" ")
        skill_state = {}
        # parse chat_id
        if 1 < len(command_part):
            date = command_part[1]
        else:
            date = None

        if date is not None:
            self.get_postplan_date(
                chat_id,
                skill_state,
                date,
            )
        else:
            self.get_postplan(
                chat_id,
                skill_state,
            )

    def get_postplan(
        self,
        chat_id: int,
        skill_state: dict,
    ) -> None:
        postplan = get_postplan_dict(skill_state)
        message = "Postplan" + json.dumps(postplan, indent=4, sort_keys=True)
        self.skill.service_telegram_bot.message_chat(chat_id, message)

    def get_postplan_date(
        self,
        chat_id: int,
        skill_state: dict,
        date: str,
    ) -> None:
        postplan = get_postplan_dict(skill_state)
        if date in postplan["scedule"]:
            postplan_date = postplan["scedule"][date]
            message = "Postplan date" + json.dumps(postplan_date, indent=4, sort_keys=True)
            self.skill.service_telegram_bot.message_chat(chat_id, message)
        else:
            message = "no postplan found for date: " + date
            self.skill.service_telegram_bot.message_chat(chat_id, message)


class CommandPostGenerate(CommandBase):
    def __init__(self, skill: SkillBase) -> None:
        super().__init__(skill, "postgenerate")
        self.client_openai = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    def get_usage(self) -> str:
        return """
        Usage:
        /postgenerate {date}
        Example:
        /postgenerate 2024-01-04
        Description:
        Generates a post for a specified date.
        """

    def execute_command(self, chat_id: int, command_message: str) -> None:
        command_part = command_message.split(" ")
        date = None
        if 1 < len(command_part):
            date = command_part[1]
        else:
            message = "Please provide a valid date argument"
            message += self.get_usage()
            self.skill.service_telegram_bot.message_chat(chat_id, message)
            return
        if date == "today":
            date = datetime.datetime.now().strftime("%Y-%m-%d")
        self.postgenerate(chat_id, date)

    def postgenerate(
        self,
        chat_id: int,
        date: str,
    ) -> None:
        skill_state = self.skill.load_skill_state(chat_id)
        postplan = get_postplan_dict(skill_state)
        # if date in skill_state:
        #     postplan_date
        #     message = skill_state[date]
        #     message = "Postplan date" + json.dumps(postplan_date, indent=4, sort_keys=True)
        #     return message

        if date not in postplan["scedule"]:
            message = "no postplan found for date: " + date
            self.skill.service_telegram_bot.message_chat(chat_id, message)
        else:
            postplan_date = postplan["scedule"][date]

            if postplan_date["generator_type"] == "hackernews":
                message = "Generating Hackernews Post"
                self.skill.service_telegram_bot.message_chat(chat_id, message)
                message = self.postgenerate_hackernews(postplan_date)
            else:
                message = "generator_type not supported"
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


class Postplan(SkillBase):
    def __init__(self, service_telegram_bot: ServiceTelegramBot):
        super().__init__(service_telegram_bot)
        self.add_command(CommandPostplan(self))
        self.add_command(CommandPostGenerate(self))
