from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CommandHandler, ContextTypes


async def poem(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:


    await update.message.reply_audio("./resources/audio/poem/2.mp3")


poem_command_handler = CommandHandler('verso', poem)