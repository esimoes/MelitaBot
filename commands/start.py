from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CommandHandler, ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user

    start_message_text = (f"<b>Hola {user.first_name}, encantada de conocerte</b>. Todavia estoy en una etapa de prueba pero ya podés acceder a muchas de mis funcionalidades, consultá mis comandos")

    await update.message.reply_text(start_message_text,parse_mode=ParseMode.HTML,disable_web_page_preview=True)
    await update.message.reply_audio("./resources/audio/Bienvenidx.ogg")


start_command_handler = CommandHandler('start', start)