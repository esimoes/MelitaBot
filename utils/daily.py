from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CommandHandler, ContextTypes, CallbackContext
from datetime import datetime, timedelta, time
from googleapiclient.discovery import build
from google.oauth2 import service_account
from config import Config
from loguru import logger

from utils.db_utils import get_session
from utils.user import get_all_users

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
creds = service_account.Credentials.from_service_account_file("credentials.json")
service = build('calendar', 'v3', credentials=creds)

async def daily_update(context: CallbackContext) -> None:

    # Call the Calendar API
    start_of_day = datetime.utcnow().isoformat() + 'Z'
    end_of_day = (datetime.utcnow() + timedelta(days=1)).isoformat() + 'Z'
    events_result = service.events().list(calendarId=Config.CALENDAR_ID, timeMin=start_of_day,
                                        timeMax=end_of_day, 
                                        singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])

    if events:
        i = 1
        answer = "Hola, te cuento de los eventos del día:\n\n"
        for event in events:       
            answer += "\U0001F916 \U0001F916 \U0001F916 \U0001F916 \U0001F916 \U0001F916" # Robot face
            answer += "\n<b>{}</b>".format(event['summary']) 
            if event.get('description'):
                answer += "\n{}".format(event['description'])
            if event['start'].get('dateTime') is not None:
                answer += "\n<b>Fecha : " + datetime.fromisoformat(event['start']['dateTime']).strftime("%d-%m-%Y") +"</b>"
                answer += "\n<b>Hora : " + datetime.fromisoformat(event['start']['dateTime']).strftime("%H:%M") +"</b>"
            elif event['start'].get('date') is not None:
                answer += "\n<b>Desde : " + datetime.fromisoformat(event['start']['date']).strftime("%d-%m-%Y") +"</b>"
                answer += "\n<b>Hasta : " + datetime.fromisoformat(event['end']['date']).strftime("%d-%m-%Y") +"</b>"
                #answer += "\n*Hora : --*"
            
            if 'location' in event.keys():
                answer += "\nUbicación : {}".format(event['location'])
            i += 1
            answer += "\n\n\n"
        answer_message_text = answer.replace('<br>','\n')

        async with get_session() as session:
            users = await get_all_users(session, active_flag=True)
    
        for user in users:
            try:
                await context.bot.send_message(chat_id=user.id, text=answer_message_text,parse_mode=ParseMode.HTML,disable_web_page_preview=False)
            except:
                error_message_text = f"User {user.first_name} id: {user.id} did not receive the msg, possibly bot was blocked"
                logger.info(error_message_text)
                await context.bot.send_message(chat_id=Config.DEV_ID, text=error_message_text,parse_mode=ParseMode.HTML,disable_web_page_preview=False)
            