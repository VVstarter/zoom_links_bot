import re

from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
)
from telegram.ext.callbackcontext import CallbackContext

from logger import logger


class ZoomLinksTelegramBot:

    def __init__(
            self,
            token: str,
            redirect_to_chat_id: str,
    ):
        self.updater = Updater(
            token=token,
            use_context=True,
        )
        self.dispatcher = self.updater.dispatcher
        self.dispatcher.add_handler(
            MessageHandler(
                filters=Filters.regex(
                    pattern=r'((?:https://)?\w{2}\d{2}web\.zoom\.\w{2}/\w{1}/\d+(?:\?pwd=.{32})?)',
                ),  # отталкивался от того что коды стран могут быть любыми (ua, fr, ... подходят) но должны совпадать
                callback=self._resend_message,
            )
        )
        self.dispatcher.add_handler(
            CommandHandler(
                command='help',
                callback=self._help,
            )
        )
        self.dispatcher.add_error_handler(self._error)
        self._redirect_to_chat_id = redirect_to_chat_id

    def run(
            self,
            interval: float,
    ) -> None:
        self.updater.start_polling(
            poll_interval=interval,
        )

    def _resend_message(
            self,
            update: Update,
            context: CallbackContext,
    ) -> None:
        matches_strings = re.findall(
            pattern=r'((?:https://)?\w{2}\d{2}web\.zoom\.\w{2}/\w{1}/\d+(?:\?pwd=.{32})?)',
            string=update.effective_message.text,
        )

        if any(
                map(
                    self._check_if_county_codes_match,
                    matches_strings,
                )
        ):
            update.effective_message.forward(chat_id=self._redirect_to_chat_id)

    @staticmethod
    def _help(
            update: Update,
            context: CallbackContext,
    ) -> None:
        help_text = "The bot commands:\n\n/help -> shows possible commands"
        update.effective_message.reply_text(help_text)

    @staticmethod
    def _error(
            update: Update,
            context: CallbackContext,
    ) -> None:
        logger.warning(
            'Update "%s" caused error "%s"',
            update,
            context.error,
        )

    @staticmethod
    def _check_if_county_codes_match(
            string_for_check: str,
    ) -> bool:
        return string_for_check[8:10] == string_for_check[21:23] \
            if 'https' in string_for_check.split('?')[0] \
            else string_for_check[0:2] == string_for_check[13:15]
