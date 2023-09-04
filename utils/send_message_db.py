from loguru import logger
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, CallbackContext

from utils.db_utils import get_session
from utils.user import get_all_users
from utils.decorators import restricted

from config import Config

message_store = []

async def send_message(context: ContextTypes.DEFAULT_TYPE, broadcast_message_text) -> None:

    message_store.clear()
    async with get_session() as session:
        users = await get_all_users(session,active_flag=True)

    for user in users:
        try:
            logger.info(f'Sending message to {user.first_name} (id:{user.id})')
            message = await context.bot.send_message(chat_id=user.id, text=broadcast_message_text,parse_mode=ParseMode.HTML,disable_web_page_preview=False)
            message_store.append({"user_id": user.id, "message_id": message.message_id}) # Store messages on array
        except:
            error_message_text = f"User {user.first_name} id: {user.id} did not receive the msg, possibly bot was blocked"
            logger.info(error_message_text)
            await context.bot.send_message(chat_id=Config.DEV_ID, text=error_message_text,parse_mode=ParseMode.HTML,disable_web_page_preview=False)

# Comando para borrar mensajes
@restricted
async def delete_message(update: Update, context: CallbackContext) -> None:

    for i, message_info in enumerate(message_store):
        try:
            await context.bot.delete_message(message_info['user_id'],message_info['message_id'])
        except:
            error_message_text = f"User id: {message_info['user_id']} msg_id: {message_info['message_id']}, message couldn't be deleted"
            logger.info(error_message_text)
        del message_store[i]