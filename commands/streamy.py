from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CommandHandler, ContextTypes

from utils.send_message_db import send_message
from loguru import logger
from config import Config

from googleapiclient.discovery import build

async def get_youtube_live(channel_id):
    api_key = Config.YOUTUBE_API_KEY

    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        response = youtube.search().list(
            part='id',
            channelId=channel_id,
            type='video',
            eventType='live',
        ).execute()
    except:
        logger.info(f'-- Error in Youtube API --')
        return None

    if 'items' in response:
        if len(response['items']) == 0:
            logger.info(f'No Youtube live to send')
            return None
        else:
            video_id = response['items'][0]['id']['videoId']
            logger.info(f'Video ID obtained from Youtube channel')
            return video_id

    return None

async def streamy(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    broadcast_message_text = ""
    
    if user.id in [Config.DEV_ID, Config.OWNER_ID]:
        logger.info(f'Sending youtube message by {user.first_name} (id:{user.id})')
        broadcast_message_text = 'https://www.youtube.com/live/'
        video_id = await get_youtube_live("UCi04K9eRbtzWpWmSVSnfr7Q")

        if video_id == None:
            broadcast_message_text = f'Prendé <b>"Ponete el Chip"</b> que ya estamos en <a href="https://www.youtube.com/@chiptecno">Youtube</a>'
        else:
            broadcast_message_text += video_id
            
        await send_message(context, broadcast_message_text)
        answer_message_text = '<pre>Se envió notificación.</pre>'
    else:
        logger.info(f'No authorization - Attempt sending stream message by {user.first_name} (id:{user.id})')
        answer_message_text = "No puedo dejarte hacer eso."

    await update.message.reply_text(answer_message_text,parse_mode=ParseMode.HTML,disable_web_page_preview=True)

streamy_command_handler = CommandHandler('youtube', streamy)