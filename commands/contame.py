from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from loguru import logger

async def tellme(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    logger.info(f'/contame used by: {user.first_name} (id:{user.id})')
    await update.message.reply_audio("./resources/audio/Info.mp3")

tellme_command_handler = CommandHandler('contame', tellme)