import logging
import os

from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Updater

from srai_athena_frontend_telegram.service_sceduling import ServiceSceduling
from srai_athena_frontend_telegram.service_telegram_bot import ServiceTelegramBot

# from srai_athena_frontend_telegram.skill.postplan import Postplan
from srai_athena_frontend_telegram.skill.scedule import Scedule
from srai_athena_frontend_telegram.skill.support import Support

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

logger = logging.getLogger(__name__)


class SraiTelegramBot(ServiceTelegramBot):
    def __init__(self, token: str):
        root_id = int(os.environ["TELEGRAM_ROOT_ID"])
        super().__init__(token, root_id)
        self.list_available_command = []
        self.list_available_command.append("help")
        self.list_available_command.append("image_tag")
        self.list_available_command.append("chat_id")

    def help(self, update: Update, context: CallbackContext):
        """Send a message when the command /help is issued."""
        message = "Available commands:\n"
        for command in self.list_available_command:
            message += f"/{command}\n"

        for command in self.dict_command.keys():
            message += f"/{command}\n"
        update.message.reply_text(message)

    def chat_id(self, update: Update, context: CallbackContext):
        """Send a message when the command /help is issued."""
        update.message.reply_text(str(update.message.chat_id))

    def get_image_tag(self):
        image_tag = os.environ.get("IMAGE_TAG")
        if image_tag is None:
            message = "IMAGE_TAG not set"
        else:
            message = f"{image_tag}"
        return message

    def image_tag(self, update: Update, context: CallbackContext):
        """Send a message /image_tag is issued."""
        update.message.reply_text(self.get_image_tag())

    def error(self, update: Update, context: CallbackContext):
        """Log Errors caused by Updates."""
        logger.warning('Update "%s" caused error "%s"', update, context.error)

    def initialize(self):
        """Start the bot."""
        # Create the Updater and pass it your bot's token.
        # Make sure to set use_context=True to use the new context based callbacks
        # Post version 12 this will no longer be necessary
        self.updater = Updater(self.bot_token, use_context=True)
        try:
            # on different commands - answer in Telegram
            self.updater.dispatcher.add_handler(CommandHandler("help", self.help))
            self.updater.dispatcher.add_handler(CommandHandler("image_tag", self.image_tag))
            self.updater.dispatcher.add_handler(CommandHandler("chat_id", self.chat_id))
            # dp.add_handler(CommandHandler("reset", self.reset))
            # self.register_skill(Postplan())
            self.register_skill(Scedule(self))
            self.register_skill(Support(self))

            # log all errors
            self.updater.dispatcher.add_error_handler(self.error)  # type: ignore
        except Exception as e:
            bot = self.updater.bot
            bot.send_message(
                chat_id=self.root_id,
                text=f"Error during startup with image tag {self.get_image_tag()}: {e}",
            )
            raise e

    def main(self):
        # send a message to jaap about update
        self.message_admins(f"Startup succes with image tag {self.get_image_tag()}")
        #
        #  Start the Bot
        self.updater.start_polling()

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        # TODO have this come from
        self.updater.idle()


if __name__ == "__main__":
    telegram_token = os.environ.get("SRAI_TELEGRAM_TOKEN")
    if telegram_token is None:
        raise Exception("SRAI_TELEGRAM_TOKEN not set")

    bot = SraiTelegramBot(token=telegram_token)
    # initialize services
    ServiceSceduling.initialize(bot)
    bot.initialize()

    # start services
    ServiceSceduling.get_instance().start()  # TODO there is a race condition here

    # start bot
    bot.main()
