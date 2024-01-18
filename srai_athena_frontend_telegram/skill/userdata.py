from srai_athena_frontend_telegram.service_persistency import ServicePersistency
from srai_athena_frontend_telegram.service_telegram_bot import ServiceTelegramBot
from srai_athena_frontend_telegram.skill.command_base import CommandBase
from srai_athena_frontend_telegram.skill.skill_base import SkillBase


class CommandUpdateUsername(CommandBase):
    def __init__(self, skill: SkillBase) -> None:
        dict_tool_dict = self.get_tool_dict()
        super().__init__(skill, dict_tool_dict["function"])

    def get_usage(self) -> str:
        return """
        Usage:
        /update_username {chat_id} {newusername}
        Example:
        /update_username
        {
            dict_support = {
                "23343543565": "Jaap is a great guy and he will achieve great things.",
            }
        }
        Description:
        {self.description}
        """

    def get_tool_dict(self) -> str:
        tool_description = (
            {
                "type": "function",
                "function": {
                    "name": "get_current_weather",
                    "description": "Update the username of the user",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The new username of the user",
                            },
                        },
                        "required": ["username"],
                    },
                },
            },
        )
        return tool_description

    def execute_command(self, chat_id: int, command_message: str) -> None:
        ServicePersistency().get_instance().dao_userdata.update_username()


class Userdata(SkillBase):
    def __init__(self, service_telegram_bot: ServiceTelegramBot) -> None:
        super().__init__(service_telegram_bot)
        self.add_command(CommandUpdateUsername(self))
