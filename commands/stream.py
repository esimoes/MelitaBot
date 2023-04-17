from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CommandHandler, ContextTypes

from utils.send_message_db import send_message

from config import Config

async def stream(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    url_stream="https://www.twitch.tv/elglitch404/"
    broadcast_message_text = f'Prendé <b>PODER ALIEN</b> que ya estamos en <a href="{url_stream}">Twitch</a>'

    if user.id in [Config.DEV_ID, Config.OWNER_ID]:
        await send_message(context, broadcast_message_text)
        answer_message_text = '<pre>Se envió notificación.</pre>'
    else:
        answer_message_text = "No puedo dejarte hacer eso."

    await update.message.reply_text(answer_message_text,parse_mode=ParseMode.HTML,disable_web_page_preview=True)

stream_command_handler = CommandHandler('stream', stream)
