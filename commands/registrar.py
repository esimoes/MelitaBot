from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CommandHandler, ContextTypes
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    CommandHandler,
    BaseHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
from config import Config
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from google.oauth2 import service_account
from typing import Dict

AUTH_LIST = [-436350771, 568333079]
SCOPES = ['https://www.googleapis.com/auth/calendar.events']
creds = service_account.Credentials.from_service_account_file("credentials.json")

CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

reply_keyboard = [
    ["Nombre", "Descripción"],
    ["Fecha y hora", "Lugar"],
    ["Listo"],
    ["Cancelar"],
]

markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True)

async def set_calendar_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the conversation and ask user for input."""
    user = update.effective_user
    answer_message_text = (f"Hola {user.first_name}, para continuar con el registro quiero que me cuentes sobre el evento:")
    await update.message.reply_text(answer_message_text, reply_markup=markup)

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
      answer_message_text = (f"¿Qué día es? ¿A qué hora? Formato que me ayuda a entenderte.\nFecha - Hora\n<b>ejemplo: 16/03/23 - 20:00</b>\nSi es de varios días formato\nFecha Inicio - Fecha Fin\n<b>ejemplo: 16/03/23 - 20/03/23</b>")

    await update.message.reply_text(answer_message_text,parse_mode=ParseMode.HTML,reply_markup=ReplyKeyboardRemove())

    return TYPING_REPLY

async def check_date(user_data) -> bool:
  for format in ("%d/%m/%y - %H:%M","%d/%m/%y - %d/%m/%y"):
    try:
      if format == "%d/%m/%y - %d/%m/%y":
        d = user_data.split(" - ")
        for i in d:
          date = datetime.strptime(i, "%d/%m/%y")
        return True
      date = datetime.strptime(user_data, format)
      return True
    except ValueError:
      pass
  return False

async def convert_date(user_data) -> str:
  for format in ("%d/%m/%y - %H:%M","%d/%m/%y - %d/%m/%y"):
    try:
      if format == "%d/%m/%y - %d/%m/%y":
        d = user_data.split(" - ")
        date_txt = ""
        for i in d:
          date = datetime.strptime(i,"%d/%m/%y")
          date_txt += datetime.strftime(date,"%Y-%m-%d")+","
        return date_txt
      date = datetime.strptime(user_data,"%d/%m/%y - %H:%M") #formato calendar '2015-05-28T09:00:00-07:00'
      date_e = date + + timedelta(hours=3)
      date_txt = datetime.strftime(date,"%Y-%m-%dT%H:%M:%S-03:00")+","+datetime.strftime(date_e,"%Y-%m-%dT%H:%M:%S-03:00")
      return date_txt
    except ValueError:
      pass
  return " "

async def received_information(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Store info provided by user and ask for the next category."""
    user_data = context.user_data
    text = update.message.text
    
    if user_data["choice"] == "Fecha y hora":
      if not await check_date(update.message.text):
        answer_message_text = (f"Formato Incorrecto")
        await update.message.reply_text(answer_message_text, reply_markup=markup,)
        return TYPING_REPLY

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
        "timeZone": "America/Argentina/Buenos_Aires",
      },
      "end": {
        "timeZone": "America/Argentina/Buenos_Aires",
      },
    }
    success = False
    if 'Fecha y hora' in user_data:
      date = await convert_date(user_data["Fecha y hora"])
      date = date.split(",")
      if len(date) >= 3:
        event['start']['date'] = date[0]
        event['end']['date'] = date[1]
      else:
        event['start']['dateTime'] = date[0]
        event['end']['dateTime'] = date[1]
    else:
       return success
    
    if 'Nombre' in user_data:
      event['summary'] = user_data['Nombre']
    else:
      event['summary'] = " "
    
    if 'Descripción' in user_data:
      event['description'] = user_data['Descripción']
    else:
      event['description'] = " "
    
    if 'Lugar' in user_data:
      event['location'] = user_data['Lugar']
    else:
      event['location'] = " "

    try:
      service = build('calendar', 'v3', credentials=creds)
      event = service.events().insert(calendarId=Config.CALENDAR_ID_SEC, body=event).execute()
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

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    answer_message_text = (f"Registro cancelado")
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
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^(Listo|Cancelar)$")), regular_choice
                )
            ],
            TYPING_REPLY: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^(Listo|Cancelar)$")),
                    received_information,
                )
            ],
        },
        fallbacks=list([MessageHandler(filters.Regex("^Listo$"), done),MessageHandler(filters.Regex("^Cancelar$"), cancel)]),
    )
