from functools import wraps
from telegram import Update
from telegram.ext import CallbackContext, ContextTypes
from config import Config
from loguru import logger

def restricted(func):
    @wraps(func)
    async def wrapped(update: Update, context: CallbackContext, *args, **kwargs):
        user_id = update.message.from_user.id
        if user_id in [Config.DEV_ID, Config.OWNER_ID]:
            return await func(update, context, *args, **kwargs)
        else:
            await update.message.reply_text("No tienes permiso para ejecutar este comando.")
            logger.info(f'No authorization command for user id: {user_id}')

    return wrapped





