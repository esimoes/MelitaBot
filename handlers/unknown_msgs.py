from telegram import Update
from telegram.ext import ContextTypes

async def unknown_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = 'Lo siento, pero no sé qué hacer😅'

    await update.effective_message.reply_text(msg, quote=True)