from loguru import logger
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CommandHandler, ContextTypes

from config import Config
from utils.random import get_random_row_values

sheet_id = Config.SPREADSHEET_ID
sheet_name = Config.SPREADSHEET_SHEET

async def recommendations(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    logger.info(f'Recomendaciones used by {user.first_name} (id:{user.id})')
    
    start_message_text = await get_random_row_values(sheet_id, sheet_name)

    await update.message.reply_text(start_message_text,parse_mode=ParseMode.HTML,disable_web_page_preview=False)

recommendations_command_handler = CommandHandler('recomendaciones', recommendations)