import json
import os
from datetime import datetime, timedelta
from typing import List

from openai import OpenAI

from srai_athena_frontend_telegram.dao.dao_mongo_base import DaoMongoBase
from srai_athena_frontend_telegram.service_persistency import ServicePersistency
from srai_athena_frontend_telegram.skill.mode_base import ModeBase


class ModeSupportState:
    def __init__(self, list_context_previous: List, list_message_current: List, date_str_current) -> None:
        self.list_context_previous = list_context_previous
        self.list_message_current = list_message_current
        self.date_str_current = date_str_current

    @staticmethod
    def create() -> "ModeSupportState":
        date_str_current = datetime.now().strftime("%Y-%m-%d")
        return ModeSupportState([], [], date_str_current)

    @staticmethod
    def from_dict(json_dict: dict) -> "ModeSupportState":
        print("loading state")
        print(json_dict)
        list_context_previous = json_dict["list_context_previous"]
        list_message_current = json_dict["list_message_current"]
        date_str_current = json_dict["date_str_current"]
        return ModeSupportState(list_context_previous, list_message_current, date_str_current)

    def to_dict(self) -> dict:
        json_dict = {}
        json_dict["list_context_previous"] = self.list_context_previous
        json_dict["list_message_current"] = self.list_message_current
        json_dict["date_str_current"] = self.date_str_current
        return json_dict

    def advance_context(self) -> None:
        if 0 < len(self.list_message_current):
            print("advancing context")
            self.list_context_previous.append(
                {"date_str": self.date_str_current, "list_message": self.list_message_current}
            )
            self.list_message_current = []
            # parse datetime
            date_current = datetime.strptime(self.date_str_current, "%Y-%m-%d")
            self.date_str_current = (date_current + timedelta(1)).strftime("%Y-%m-%d")
        else:
            print("not advancing context because list_message_current is empty")


class ModeSupport(ModeBase):
    def __init__(self, service_telegram_bot) -> None:
        super().__init__(service_telegram_bot)
        self.client_openai = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        self.dao_state = ServicePersistency.get_instance().dao_support_state

    # TODO figure out when to advance context
    #        if 0 < len(self.list_message_current):
    #            self.advance_context()

    def load_state(self, chat_id_str: str) -> "ModeSupportState":
        dict_state = self.dao_state.find_one({"chat_id_str": chat_id_str})
        if dict_state is None:
            return ModeSupportState.create()
        else:
            return ModeSupportState.from_dict(dict_state["state"])

    def save_state(self, chat_id_str: str, state: ModeSupportState) -> None:
        print("saving state")
        result = self.dao_state.update_one(
            {"chat_id_str": chat_id_str},
            {"$set": {"state": state.to_dict()}},
            upsert=True,
        )

    def process_message(self, chat_id: int, user_message_content: str) -> None:
        state = self.load_state(str(chat_id))
        if user_message_content == "":
            if 0 < len(state.list_message_current):
                if state.list_message_current[-1]["role"] == "assistant":
                    self.service_telegram_bot.message_chat(chat_id, state.list_message_current[-1]["content"])
                    return

        if user_message_content == "next":
            state.advance_context()

        # context_current = self.dict_context[self.context_current_id]
        # context_current_str = json.dumps(context_current, indent=4, sort_keys=True)
        # system_message = """
        # You are a friend that checks in on people during their morning routine.
        # Only provide a RFC8259 compliant JSON response following this format without deviation.
        # User the next_question field to ask the user a question.
        # """
        system_message_content = f"""
        You are a friend that checks in on people during their morning routine.
        Be kind but also brief and to the point
        Todays date is {state.date_str_current}.
        """
        if 0 < len(state.list_context_previous):
            conversation_previous_str = str(state.list_context_previous[-1]["list_message"])
            date_previous_str = state.list_context_previous[-1]["date_str"]
            system_message_content += f"""
            Here is a summary of the conversation for {date_previous_str}:
            {conversation_previous_str}
            """
        system_message_content += """
        Eventually you want answers to the following questions but only ask one question at a time:
        "Did the user sleep well?"
        "Is the user looking forward to their day?"
        "Does the user have any worries?"
        If the user awnsers negatively to any of these questions, ask them why.
        """

        #        system_message += context_current_str
        # skill_state = self.skill.load_skill_state(chat_id)
        if len(state.list_message_current) == 0:
            state.list_message_current.append({"role": "system", "content": system_message_content})
        if user_message_content != "":
            state.list_message_current.append({"role": "user", "content": user_message_content})

        completion = self.client_openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=state.list_message_current,
        )
        assistent_message_content = completion.choices[0].message.content
        state.list_message_current.append({"role": "assistant", "content": assistent_message_content})
        self.service_telegram_bot.message_chat(chat_id, assistent_message_content)
        self.save_state(str(chat_id), state)
