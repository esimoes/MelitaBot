from telegram import Update
from telegram.ext import ContextTypes

async def unknown_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = 'Lo siento, ese es un comando no valido, pronto podremos hablar de otros temas'

    await update.effective_message.reply_text(msg, quote=True)