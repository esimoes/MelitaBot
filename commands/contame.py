from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

async def tellme(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    await update.message.reply_audio("./resources/audio/Info.mp3")

tellme_command_handler = CommandHandler('contame', tellme)