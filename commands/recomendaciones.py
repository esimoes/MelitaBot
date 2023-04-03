import random
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CommandHandler, ContextTypes

from google.oauth2 import service_account
from googleapiclient.discovery import build

from config import Config

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = service_account.Credentials.from_service_account_file("credentials.json")
service = build('sheets', 'v4', credentials=creds)

sheet_id = Config.SPREADSHEET_ID
sheet_name = Config.SPREADSHEET_SHEET

def get_random_row_values(sheet_id, sheet_name) -> str:

    # Obtener los valores de la hoja de cálculo
    result = service.spreadsheets().values().get(spreadsheetId=sheet_id, range=sheet_name).execute()
    values = result.get('values', [])

    # Obtener una fila aleatoria
    if not values:
        return "No tengo nada para recomendar, prueba en otro momento"
    else:
        random_row = random.choice(values)

    # Obtener los valores de las columnas de la URL y la descripción
    url_index = 0  # Índice de la columna que contiene la URL
    desc_index = 1  # Índice de la columna que contiene la descripción
    url = random_row[url_index] if len(random_row) > url_index else ''
    desc = random_row[desc_index] if len(random_row) > desc_index else ''

    text = f"{url}\n{desc}"

    return text

async def recommendations(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    start_message_text = get_random_row_values(sheet_id, sheet_name)

    await update.message.reply_text(start_message_text,parse_mode=ParseMode.HTML,disable_web_page_preview=False)

recommendations_command_handler = CommandHandler('recomendaciones', recommendations)