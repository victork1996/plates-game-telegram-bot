import argparse
import logging

from telegram.ext import Updater, CommandHandler
from commands.check_number import set_record_db_path, handle_check_number_command
from commands.check_autotel import handle_check_autotel_command


def configure_log():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.DEBUG)


def configure_handlers(updater, records_db_path):
    dispatcher = updater.dispatcher
    set_record_db_path(records_db_path)
    start_handler = CommandHandler('check', handle_check_number_command)
    dispatcher.add_handler(start_handler)
    autotel_handler = CommandHandler('autotel', handle_check_autotel_command)
    dispatcher.add_handler(autotel_handler)


def start_bot(records_db_path, bot_token):
    logging.info("Using bot token: {}".format(bot_token))
    logging.info("Using cars DB from: {}".format(records_db_path))

    configure_log()
    updater = Updater(token=bot_token, use_context=True)
    configure_handlers(updater, records_db_path)
    updater.start_polling()
    updater.idle()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("records_db_path")
    parser.add_argument("bot_token")
    args = parser.parse_args()
    start_bot(args.records_db_path, args.bot_token)


if __name__ == "__main__":
    main()
