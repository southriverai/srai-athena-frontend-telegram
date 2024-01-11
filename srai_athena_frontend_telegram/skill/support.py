import os

from openai import OpenAI

from srai_athena_frontend_telegram.service_telegram_bot import ServiceTelegramBot
from srai_athena_frontend_telegram.skill.command_base import CommandBase
from srai_athena_frontend_telegram.skill.skill_base import SkillBase


class CommandGetSupport(CommandBase):
    def __init__(self, skill: SkillBase) -> None:
        super().__init__(skill, "getsupport")
        self.client_openai = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    def get_usage(self) -> str:
        return """
        /getsupport
        Generates a message of support and happiness for the day.
        Messages are generated using the GPT-3 engine.
        Promt can be enhanced with tha add_support command.
        """

    def execute_command(self, chat_id: int, command_message: str) -> None:
        system_message = """
        You are a system for writing uplifting message of support.
        Never add a header to your message like "Dear [name]".
        Never add a footer to your message like "warm regards".
        """
        skill_state = self.skill.load_skill_state(chat_id)
        if "user_message" not in skill_state:
            user_message = (
                """Please write me a very brief telegram style message of support and happiness for the day."""
            )
            skill_state["user_message"] = user_message
            skill_state["list_friend_message"] = []
            self.skill.save_skill_state(chat_id, skill_state)
        else:
            user_message = skill_state["user_message"]
            for friend_message in skill_state["list_friend_message"]:
                user_message += "Friend message:"
                user_message += friend_message

        completion = self.client_openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {
                    "role": "user",
                    "content": user_message,
                },
            ],
        )

        message: str = completion.choices[0].message.content  # type: ignore
        # list_message_part = message.split("\n")
        # if 1 < len(list_message_part):
        #     for message_part in list_message_part[1:]:
        #         if 0 < len(message_part.strip()):
        #             message = message_part
        #         message = "\n".join(message_part[1:])
        self.skill.service_telegram_bot.message_chat(chat_id, message)


class CommandAddSupport(CommandBase):
    def __init__(self, skill: SkillBase) -> None:
        super().__init__(skill, "addsupport")

    def get_usage(self) -> str:
        return """
        Usage:
        /addsupport {chat_id} {support_message}
        Example:
        /addsupport 23343543565 Jaap is a great guy and he will achieve great things.
        Description:
        Changes the support prompt for another chat.
        """

    def execute_command(self, chat_id: int, command_message: str) -> None:
        command_part = command_message.split(" ")

        # parse chat_id
        if 1 < len(command_part):
            chat_id_other = command_part[1]
        else:
            error_message = "Missing argument chat_id \n"
            error_message += self.get_usage()
            self.skill.service_telegram_bot.message_chat(chat_id, error_message)
            return

        # parse support_message
        if 2 < len(command_part):
            support_message = " ".join(command_part[2:])
        else:
            error_message = "Missing argument {support_message} \n"
            error_message += self.get_usage()
            self.skill.service_telegram_bot.message_chat(chat_id, error_message)
            return

        # save support_message
        self.skill.service_telegram_bot.message_chat(chat_id, f"Added support to {chat_id_other}")


class CommandShowSupport(CommandBase):
    def __init__(self, skill: SkillBase) -> None:
        super().__init__(skill, "showsupport")

    def get_usage(self) -> str:
        return """
        Usage:
        /showsupport {chat_id} {support_message}
        Example:
        /showsupport
        {
            dict_support = {
                "23343543565": "Jaap is a great guy and he will achieve great things.",
            }
        }
        Description:
        Shows the statedict for the users support message
        """

    def execute_command(self, chat_id: int, command_message: str) -> None:
        command_part = command_message.split(" ")

        # parse chat_id
        if 1 < len(command_part):
            chat_id = int(command_part[1])
        else:
            error_message = "Missing argument chat_id \n"
            error_message += self.get_usage()
            self.skill.service_telegram_bot.message_chat(chat_id, error_message)
            return

        # parse support_message
        if 1 < len(command_part):
            support_message = " ".join(command_part[2:])
            skill_state = self.skill.load_skill_state(chat_id)
            if "dict_support_message" not in skill_state:
                skill_state["dict_support_message"] = {}
            skill_state["dict_support_message"][str(chat_id)] = support_message
            self.skill.save_skill_state(chat_id, skill_state)
        else:
            error_message = "Missing argument {support_message} \n"
            error_message += self.get_usage()
            self.skill.service_telegram_bot.message_chat(chat_id, error_message)
            return

        # save support_message
        self.skill.service_telegram_bot.message_chat(chat_id, "Adding support...")


class Support(SkillBase):
    def __init__(self, service_telegram_bot: ServiceTelegramBot) -> None:
        super().__init__(service_telegram_bot)
        self.add_command(CommandGetSupport(self))
        self.add_command(CommandAddSupport(self))
        self.add_command(CommandShowSupport(self))
