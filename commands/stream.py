from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CommandHandler, ContextTypes

from utils.send_message_db import send_message
from loguru import logger
from config import Config
from utils.decorators import restricted
import requests

url_stream=Config.TWITCH_STREAM_URL
# URL para obtener un token de autenticación
url = "https://id.twitch.tv/oauth2/token"
# Parámetros de la solicitud
params = {
    "client_id": Config.TWITCH_CLIENT_ID,
    "client_secret": Config.TWITCH_CLIENT_SECRET,
    "grant_type": "client_credentials"
}
# ID del canal de Twitch
channel_id = Config.TWITCH_CHANNEL_ID


async def message_stream_with_api() -> str:
    stream_message_text = ""
    global url
    global params
    global channel_id
    # Hacer la solicitud para obtener el token
    access_token = ""
    try:
        logger.info(f'requesting to {url} with params={params}')
        response = requests.post(url, params=params)
    except:
        logger.info(f'Error requesting to {url} with params={params}')

    # Obtener el token de autenticación
    if response.status_code == 200:
        data = response.json()
        access_token = data["access_token"]
        logger.info(f'request OK - code 200, token:{access_token}')
    else:
        logger.info(f'Error geting Token')
        
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Client-ID": Config.TWITCH_CLIENT_ID
        }

    # For channel ID info    
#    url = 'https://api.twitch.tv/helix/users?login=elglitch404'
#
#    logger.info(f'requesting to {url} with headers={headers}')
#    response = requests.get(url, headers=headers)
#    logger.info(f'{response}')

    # Hacer una solicitud a la API de Twitch
    url = f'https://api.twitch.tv/helix/channels?broadcaster_id={channel_id}'

    logger.info(f'requesting to {url} with headers={headers}')
    response = requests.get(url,headers=headers)
    logger.info(f'{response}')

    # Obtener el título del canal
    if response.status_code == 200:
        data = response.json()["data"]
        if len(data) > 0:
            channel_title = data[0]["title"]
            stream_message_text = f"Prendé {channel_title}\n{url_stream}"
        else:
            logger.info(f'Channel not found')
        logger.info(f'request OK - code 200, channel_title={channel_title}')
    else:
        logger.info(f'Error in GET')
    
    return stream_message_text

@restricted
async def stream(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    broadcast_message_text = ""
    
    logger.info(f'Sending stream message by {user.first_name} (id:{user.id})')

    broadcast_message_text = await message_stream_with_api()

    if broadcast_message_text == "":
        broadcast_message_text = f'Prendé <b>PODER ALIEN</b> que ya estamos en <a href="{url_stream}">Twitch</a>'

    await send_message(context, broadcast_message_text)
    answer_message_text = '<pre>Se envió notificación.</pre>'

    await update.message.reply_text(answer_message_text,parse_mode=ParseMode.HTML,disable_web_page_preview=True)

stream_command_handler = CommandHandler('stream', stream)
