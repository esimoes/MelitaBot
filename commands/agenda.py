from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CommandHandler, ContextTypes
import os.path
from datetime import datetime, timedelta, time
from googleapiclient.discovery import build
from google.oauth2 import service_account

AUTH_LIST = [-436350771, 568333079]
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
creds = service_account.Credentials.from_service_account_file("credentials.json")
service = build('calendar', 'v3', credentials=creds)
CALENDAR_ID = os.environ.get('CALENDAR_ID')


async def calendar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Prints the start and name of the next 15 events on the user's calendar.
    """
    user = update.effective_user

    # Call the Calendar API
    now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    days30 = (datetime.utcnow() + timedelta(days=30)).isoformat() + 'Z'
    events_result = service.events().list(calendarId=CALENDAR_ID, timeMin=now,
                                        timeMax=days30, maxResults=15, 
                                        singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])

    answer_message_text = (f"Hola {user.first_name}, esta es la agenda del mes:")
    await update.message.reply_text(answer_message_text,parse_mode=ParseMode.HTML,disable_web_page_preview=True)

    if not events:
        answer = "Sorry, you don't have any upcoming events in the next 30 days."
    else:
        i = 1
        answer = ""
        for event in events:       
            answer += "EVENT #{}".format(i)
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
    try:
        await update.message.reply_text(answer_message_text,parse_mode=ParseMode.HTML,disable_web_page_preview=False)
    except:
        print("error")

calendar_command_handler = CommandHandler('agenda', calendar)