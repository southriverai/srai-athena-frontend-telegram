from abc import ABC, abstractmethod


class ServiceTelegramBot(ABC):
    def __init__(self, bot_token):
        self.bot_token = bot_token

    @abstractmethod
    def message_root(self, text):
        raise NotImplementedError()

    @abstractmethod
    def message_admins(self, text):
        raise NotImplementedError()
