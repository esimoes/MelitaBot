from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

from utils.decorators import restricted
from utils import daily_update
from loguru import logger

@restricted
async def enviar_agenda(update: Update, context: CallbackContext) -> None:
    user = update.effective_user

    await daily_update(context)
    logger.info(f'Sending events manually: {user.first_name} (id:{user.id})')


sendcalendar_command_handler = CommandHandler('enviaragenda', enviar_agenda)