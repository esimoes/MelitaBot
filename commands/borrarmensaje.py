from telegram.ext import CommandHandler
from utils.send_message_db import delete_message


delete_command_handler = CommandHandler('delete', delete_message)