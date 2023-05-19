from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CommandHandler, ContextTypes
from loguru import logger
import random
import time

from config import Config
from utils.random import get_random_row_values

sheet_id = Config.SPREADSHEET_ID
sheet_name = Config.SPREADSHEET_SHEET_FORTUNE

# Animations config
waiting_text = ["Verificando la retrogradación de Mercurio","Accediendo a la nave nodriza","Tomando muestra de ADN"]
wait_ascii = ["|", "/", "-", "\\"]
# global var
last_waiting_text_index = 0
current_wait_ascii_index = 0

def progress_bar(percent):
    global last_waiting_text_index, current_wait_ascii_index

    # when animation wait_ascii end, get a random waiting_text
    if current_wait_ascii_index == 0:
        last_waiting_text_index = random.randint(0, len(waiting_text) - 1)

    # update index of wait_ascii
    current_wait_ascii_index = (current_wait_ascii_index + 1) % len(wait_ascii)

    return f'( {wait_ascii[current_wait_ascii_index]} ) -- {waiting_text[last_waiting_text_index]} --'

async def fortuna(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    logger.info(f'Fortuna for {user.first_name} (id:{user.id}) is...')
    random_message = get_random_row_values(sheet_id, sheet_name,1)
    # Bucle de animación
    progress = progress_bar(1)
    progress_msg = await context.bot.send_message(chat_id=user.id,text=progress)
    logger.info(f'Beginning animation for {user.first_name} (id:{user.id})')
    try:
        for i in range(20):
            progress = progress_bar(i)
            # Envío de la salida como respuesta al mensaje recibido
            await progress_msg.edit_text(text=progress)
            time.sleep(0.1)
        logger.info(f'Ended animation for {user.first_name} (id:{user.id})')
    except:
        logger.info(f'Animation error for {user.first_name} (id:{user.id})')
    message = await random_message
    await progress_msg.edit_text(text='<span class="tg-spoiler"><i>~ '+ message +' ~</i></span>', parse_mode="HTML")
    logger.info(f'sent the message Fortuna to {user.first_name} (id:{user.id}) + {message}')

fortuna_command_handler = CommandHandler('fortuna', fortuna)