from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CommandHandler, ContextTypes

from utils.db_utils import get_session
from utils.user import get_all_users

from config import Config

async def get_users(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user

    # Create a new user instance and add it to the database
    if user.id in [Config.DEV_ID, Config.OWNER_ID]:
        async with get_session() as session:
            users = await get_all_users(session)

        users_number = len(users)
        start_message_text = (f"<pre>Hay un total de {users_number} usuarios</pre>")
    else:
        start_message_text = (f"No puedo dejarte hacer eso.")

    await update.message.reply_text(start_message_text,parse_mode=ParseMode.HTML,disable_web_page_preview=True)

get_users_command_handler = CommandHandler('usuarios', get_users)