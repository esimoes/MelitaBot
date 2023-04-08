from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CommandHandler, ContextTypes

from utils.db_utils import get_session
from utils.user import update_user

async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user

    # Create a new user instance and add it to the database
    async with get_session() as session:
       await update_user(session, user, user_data= {'active': False})

    start_message_text = (f"Dejarás de recibir actualizaciones diarias")

    await update.message.reply_text(start_message_text,parse_mode=ParseMode.HTML,disable_web_page_preview=True)

end_command_handler = CommandHandler('end', end)