from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CommandHandler, ContextTypes
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
import os.path
from datetime import datetime, timedelta, time
from googleapiclient.discovery import build
from google.oauth2 import service_account
from typing import Dict

AUTH_LIST = [-436350771, 568333079]
SCOPES = ['https://www.googleapis.com/auth/calendar.events']
creds = service_account.Credentials.from_service_account_file("credentials.json")

CALENDAR_ID = os.environ.get('CALENDAR_ID_SEC')
CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

reply_keyboard = [
    ["Nombre", "Descripción"],
    ["Fecha y hora", "Lugar"],
    ["Listo"],
]

markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

async def set_calendar_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the conversation and ask user for input."""
    user = update.effective_user
    answer_message_text = (f"Hola {user.first_name}, para continuar con el registro quiero que me cuentes sobre el evento:")
    await update.message.reply_text(answer_message_text, reply_markup=markup, )

    return CHOOSING

def facts_to_str(user_data: Dict[str, str]) -> str:
    """Helper function for formatting the gathered user info."""
    facts = [f"{key} - {value}" for key, value in user_data.items()]
    return "\n".join(facts).join(["\n", "\n"])

async def regular_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for info about the selected predefined choice."""
    text = update.message.text
    context.user_data["choice"] = text

    if text == "Nombre":
      answer_message_text = (f"Contame cual es el Nombre del evento, anuncio o actividad")
    if text == "Descripción":
      answer_message_text = (f"Contame un poco más de qué se trata")
    if text == "Lugar":
      answer_message_text = (f"¿Dónde es?  ya sea físico o virtual dejame la data acá")
    if text == "Fecha y hora":
      answer_message_text = (f"¿Qué día es? ¿A qué hora? Formato que me ayuda a entenderte. Fecha - Hora, <b>ejemplo: 16/03/23 - 20:00</b>. Si es de varios días formato Fecha Inicio - Fecha Fin, <b>ejemplo: 16/03/23 - 20/03/23</b>")
      defaultButton = {'text': 'default','web_app': {'url': 'https://expented.github.io/tgdtp/'}}
      hideTimeButton = {'text': 'only date','web_app': {'url': 'https://expented.github.io/tgdtp/?hide=time'}}
      betweenButton = {'text': 'May 1 to May 20','web_app': {'url': 'https://expented.github.io/tgdtp/?min=2022-05-01&max=2022-05-20'}}
      print = 'choose date and time'
      reply_keyboard_ = [
    [defaultButton, hideTimeButton],
    [betweenButton],
]
      markup_ = ReplyKeyboardMarkup(reply_keyboard_, one_time_keyboard=True)
      await update.message.reply_text(print, reply_markup=markup_)
                                                                          
    await update.message.reply_text(answer_message_text,parse_mode=ParseMode.HTML)

    return TYPING_REPLY


async def received_information(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Store info provided by user and ask for the next category."""
    user_data = context.user_data
    text = update.message.text
    category = user_data["choice"]
    user_data[category] = text
    del user_data["choice"]

    answer_message_text = (f"¡Entendido!Esto es lo que me contaste hasta el momento:\n{facts_to_str(user_data)}\nPuedes contarme más, o cambiar algún dato.")

    await update.message.reply_text(answer_message_text, reply_markup=markup,)

    return CHOOSING

async def save_calendar(user_data) -> bool:
    
    event = {
  "summary": "",
  "location": "",
  "description": "",
  "start": {
    "dateTime": "",
    "timeZone": "America/Argentina/Buenos_Aires",
  },
    "end": {
    "dateTime": "",
    "timeZone": "America/Argentina/Buenos_Aires",
  },
}
    success = False
    if user_data['Fecha y hora']:
      event['start']['dateTime'] = "2023-03-18T17:00:00-03:00"
      event['end']['dateTime'] = "2023-03-18T19:00:00-03:00"
    else:
       return success
    if user_data['Nombre']:
      event['summary'] = user_data['Nombre']
      pass
    else:
      return success
    
    event['description'] = user_data['Descripción']
    event['location'] = user_data['Lugar']

    try:
      service = build('calendar', 'v3', credentials=creds)
      event = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
      print ('Event created: %s' % (event.get('htmlLink')))
      success = True
    except:
       success = False

    return success
      
async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Display the gathered info and end the conversation."""
    user_data = context.user_data
    if "choice" in user_data:
        del user_data["choice"]

    if await save_calendar(user_data):
      answer_message_text = (f"Hemos registrado el evento")
    else:
      answer_message_text = (f"No he podido registrar el evento")

    await update.message.reply_text(answer_message_text,reply_markup=ReplyKeyboardRemove(),)

    user_data.clear()
    return ConversationHandler.END

set_calendar_command_handler = ConversationHandler(
        entry_points=[CommandHandler("registrar", set_calendar_command)],
        states={
            CHOOSING: [
                MessageHandler(
                    filters.Regex("^(Nombre|Descripción|Fecha y hora|Lugar)$"), regular_choice
                ),
            ],
            TYPING_CHOICE: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^Listo$")), regular_choice
                )
            ],
            TYPING_REPLY: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^Listo$")),
                    received_information,
                )
            ],
        },
        fallbacks=[MessageHandler(filters.Regex("^Listo$"), done)],
    )
