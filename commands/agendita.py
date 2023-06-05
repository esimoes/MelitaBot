from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CommandHandler, ContextTypes
from config import Config
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from google.oauth2 import service_account
from loguru import logger

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
creds = service_account.Credentials.from_service_account_file("credentials.json")
service = build('calendar', 'v3', credentials=creds)

async def get_calendar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Prints the start and name of the next 15 events on the user's calendar.
    """
    user = update.effective_user

    # Call the Calendar API
    now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    days30 = (datetime.utcnow() + timedelta(days=30)).isoformat() + 'Z'
    events_result = service.events().list(calendarId=Config.CALENDAR_ID, timeMin=now,
                                        timeMax=days30, maxResults=10, 
                                        singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])

    answer_message_text = (f"Hola {user.first_name}, esta es la agenda del mes:")
    await update.message.reply_text(answer_message_text,parse_mode=ParseMode.HTML,disable_web_page_preview=True)
    logger.info(f'/agendita used by {user.first_name} (id:{user.id})')
    if not events:
        answer = "Lo siento, no tengo nada para mostrarte. Prueba en otro momento a que me actualice"
        await update.message.reply_text(answer,parse_mode=ParseMode.HTML,disable_web_page_preview=False)
    else:
        i = 1
        answer = ""
        answer_message_text = []
        for event in events:       
            answer_aux = "\U0001F916 \U0001F916 \U0001F916 \U0001F916 \U0001F916 \U0001F916" # Robot face
            answer_aux += "\n<b>{}</b>".format(event['summary']) 
            if event.get('description'):
                answer_aux += "\n{}".format(event['description'])
            if event['start'].get('dateTime') is not None:
                answer_aux += "\n<b>Fecha : " + datetime.fromisoformat(event['start']['dateTime']).strftime("%d-%m-%Y") +"</b>"
                answer_aux += "\n<b>Hora : " + datetime.fromisoformat(event['start']['dateTime']).strftime("%H:%M") +"</b>"
            elif event['start'].get('date') is not None:
                answer_aux += "\n<b>Desde : " + datetime.fromisoformat(event['start']['date']).strftime("%d-%m-%Y") +"</b>"
                answer_aux += "\n<b>Hasta : " + datetime.fromisoformat(event['end']['date']).strftime("%d-%m-%Y") +"</b>"            
            if 'location' in event.keys():
                answer_aux += "\nUbicación : {}".format(event['location'])
            i += 1
            answer_aux += "\n\n\n"
            answer_aux = answer_aux.replace('<br>','\n')
            if len(answer)+len(answer_aux)<=4096:
                answer += answer_aux
            else:
                answer_message_text.append(answer)
                answer = answer_aux
        answer_message_text.append(answer)        
        for answers in answer_message_text:
            await update.message.reply_text(answers,parse_mode=ParseMode.HTML,disable_web_page_preview=False)


get_calendar_command_handler = CommandHandler('agendita', get_calendar)