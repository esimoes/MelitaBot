from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CommandHandler, ContextTypes

from utils.db_utils import get_session
from utils.user import create_or_update_user

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user

    # Create a new user instance and add it to the database
    async with get_session() as session:
        await create_or_update_user(session, user)

    start_message_text = (f"<b>Hola {user.first_name}, encantada de conocerte.</b> Consultá mis comandos para interactuar conmigo.")

    await update.message.reply_text(start_message_text,parse_mode=ParseMode.HTML,disable_web_page_preview=True)
    await update.message.reply_audio("./resources/audio/Bienvenidx.mp3")


start_command_handler = CommandHandler('start', start)