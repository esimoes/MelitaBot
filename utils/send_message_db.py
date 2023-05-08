from loguru import logger
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from utils.db_utils import get_session
from utils.user import get_all_users

from config import Config

async def send_message(context: ContextTypes.DEFAULT_TYPE, broadcast_message_text) -> None:

    async with get_session() as session:
        users = await get_all_users(session,active_flag=True)

    for user in users:
        try:
            logger.info(f'Sending message to {user.first_name} (id:{user.id})')
            await context.bot.send_message(chat_id=user.id, text=broadcast_message_text,parse_mode=ParseMode.HTML,disable_web_page_preview=False)
        except:
            error_message_text = f"User {user.first_name} id: {user.id} did not receive the msg, possibly bot was blocked"
            logger.info(error_message_text)
            await context.bot.send_message(chat_id=Config.DEV_ID, text=error_message_text,parse_mode=ParseMode.HTML,disable_web_page_preview=False)