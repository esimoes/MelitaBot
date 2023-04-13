from loguru import logger
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CommandHandler, ContextTypes

from utils.db_utils import get_session
from utils.user import get_all_users

from config import Config

async def stream(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    url_stream="https://www.twitch.tv/elglitch404/"
    broadcast_message_text = f'Prendé <b>PODER ALIEN</b> que ya estamos en <a href="{url_stream}">Twitch</a>'

    if user.id in [Config.DEV_ID, Config.OWNER_ID]:
        async with get_session() as session:
            users = await get_all_users(session)
        answer_message_text = '<pre>Se envió notificación.</pre>'
    else:
        answer_message_text = "No puedo dejarte hacer eso."

    for user in users:
        try:
            await context.bot.send_message(chat_id=user.id, text=broadcast_message_text,parse_mode=ParseMode.HTML,disable_web_page_preview=False)
        except:
            error_message_text = f"User {user.first_name} id: {user.id} did not receive the msg, possibly bot was blocked"
            logger.info(error_message_text)
            await context.bot.send_message(chat_id=Config.DEV_ID, text=error_message_text,parse_mode=ParseMode.HTML,disable_web_page_preview=False)

    await update.message.reply_text(answer_message_text,parse_mode=ParseMode.HTML,disable_web_page_preview=True)

stream_command_handler = CommandHandler('stream', stream)
