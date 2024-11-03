import html
import json
import logging
import traceback

from config import Config
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    err_msg_len = 1000 - 4  # Because "...\n" used

    logger.error(msg="Exception while handling an update.")

    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = "".join(tb_list)

    if len(tb_string) > err_msg_len:
        tb_string = "...\n" + tb_string[-err_msg_len:].strip()

    update_str = update.to_dict() if isinstance(update, Update) else str(update)

    # Inform developer
    msg = (
        f"⚠ Error\n\n"
        f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}</pre>"
    )
    msg2 = (
        f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
        f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>"
    )
    msg3 = f"<pre>{html.escape(tb_string)}</pre>"

    try:
        await context.bot.send_message(chat_id=Config.DEV_ID, text=msg, parse_mode=ParseMode.HTML)
        await context.bot.send_message(chat_id=Config.DEV_ID, text=msg2, parse_mode=ParseMode.HTML)
        await context.bot.send_message(chat_id=Config.DEV_ID, text=msg3, parse_mode=ParseMode.HTML)
    except:
        logger.error(msg="Error sending error message.")

    # Inform user
    error_text = 'Perdón, algo salió mal. Ya he notificado al desarrollador.'
    try:
        await update.effective_message.reply_text(text=error_text, reply_to_message_id=update.effective_message)
    except:
        logger.error(msg="Error sending reply. httpx error")