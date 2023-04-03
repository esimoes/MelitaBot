from telegram.ext import (Application,
                          MessageHandler,
                          filters)
import logging
import sys

from commands import (start_command_handler, 
                      get_calendar_command_handler, 
                      poem_command_handler, 
                      tellme_command_handler,
                      set_calendar_command_handler,
                      recommendations_command_handler)

from handlers import (error_handler, 
                      unknown_messages)

from config import Config
from utils.db_utils import check_db
from utils import daily_update
import datetime

logger = logging.getLogger(__name__)

def main():

    application = Application.builder().token(Config.BOT_TOKEN).build()

    # Check if DB exists DB
    if not check_db():
        logger.critical("DB not found!")
        sys.exit(1)

    job_queue = application.job_queue
    # Create a job that runs daily at 9 a.m.
    timezone = datetime.timezone(datetime.timedelta(hours=-3))
    job_queue.run_daily(daily_update, time=datetime.time(hour=8, minute=0,tzinfo=timezone))

    # Register commands
    application.add_handler(start_command_handler)
    application.add_handler(get_calendar_command_handler)
    application.add_handler(poem_command_handler)
    application.add_handler(tellme_command_handler)
    application.add_handler(set_calendar_command_handler)
    application.add_handler(recommendations_command_handler)

    # Register error handlers
    application.add_error_handler(error_handler)
    application.add_handler(MessageHandler(filters.ALL, unknown_messages))

    application.run_polling()

if __name__=="__main__":
    main()