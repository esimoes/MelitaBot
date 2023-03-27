from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CommandHandler, ContextTypes
from datetime import datetime, timedelta, time


async def daily_update(update: Update,job_queue) -> None:
    """ Running on Mon, Tue, Wed, Thu, Fri = tuple(range(5)) """
    await update.message.reply_text(chat_id=312722597, text='Setting a daily notifications!')
    t = datetime.time(10, 00, 00, 000000)
    job_queue.run_daily(notify_assignees, t, days=tuple(range(5)), context=update)


async def notify_assignees(update: Update, job):
    await update.message.reply_text(chat_id=312722597, text="Some text!")


daily_update_handler = CommandHandler('daily', daily_update, pass_job_queue=True)
