from telegram.ext import *
from datetime import datetime, timedelta, time
import os.path
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from commands import start_command_handler, calendar_command_handler, poem_command_handler, tellme_command_handler

BOT_TOKEN = os.environ.get('BOT_TOKEN')

def main():

    try:
        application = Application.builder().token(BOT_TOKEN).build()

        # Register commands
        application.add_handler(start_command_handler)
        application.add_handler(calendar_command_handler)
        application.add_handler(poem_command_handler)
        application.add_handler(tellme_command_handler)
    
        application.run_polling()
    except:
        print("Invalid TOKEN")

if __name__=="__main__":
    main()
