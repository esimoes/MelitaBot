from telegram import Update
from telegram.ext import ContextTypes
from loguru import logger

async def unknown_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update._effective_user
    user_msg = update.effective_message.text
    msg = 'Lo siento, ese es un comando no valido, pronto podremos hablar de otros temas'
    logger.info(f'bad command: {user_msg} by {user.first_name} (id:{user.id})')
    await update.effective_message.reply_text(msg, quote=True)