from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CommandHandler, ContextTypes

from utils.db_utils import get_session
from utils.user import get_all_users
from loguru import logger
from utils.decorators import restricted

@restricted
async def get_users(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user

    async with get_session() as session:
        users = await get_all_users(session)

    users_number = len(users)
    start_message_text = (f"<pre>- Hay un total de {users_number} usuarios</pre>")
    users_inactive =[user for user in users if not user.active]
    count_inactive_users = len(users_inactive)
    start_message_text += (f"\n<pre>- {count_inactive_users} están inactivos</pre>")
    logger.info(f'/usuarios used by {user.first_name} (id:{user.id})')

    await update.message.reply_text(start_message_text,parse_mode=ParseMode.HTML,disable_web_page_preview=True)

get_users_command_handler = CommandHandler('usuarios', get_users)