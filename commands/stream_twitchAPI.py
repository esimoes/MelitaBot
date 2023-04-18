from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CommandHandler, ContextTypes

from utils.db_utils import get_session
from utils.user import get_all_users

from config import Config
import requests

async def stream(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    url_stream="https://www.twitch.tv/elglitch404/"
    if user.id in [Config.DEV_ID, Config.OWNER_ID]:
        # URL para obtener un token de autenticación
        url = "https://id.twitch.tv/oauth2/token"
        # Parámetros de la solicitud
        params = {
            "client_id": "zs37gbfrlbfbi9o39r0ijoiknatmaz",
            "client_secret": "f8mhnadlk6kmyfxyo115xp3iz4luku",
            "grant_type": "client_credentials"
        }
        # ID del canal de Twitch
        channel_id = "707447498"

        # Hacer la solicitud para obtener el token
        response = requests.post(url, params=params)
        # Obtener el token de autenticación
        if response.status_code == 200:
            data = response.json()
            access_token = data["access_token"]

        else:
            print("Error al obtener el token de autenticación")
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Client-ID": "zs37gbfrlbfbi9o39r0ijoiknatmaz"
            }
        url = 'https://api.twitch.tv/helix/users?login=elglitch404'
        response = requests.get(url, headers=headers)

        # Hacer una solicitud a la API de Twitch
        response = requests.get(f"https://api.twitch.tv/helix/channels?broadcaster_id={channel_id}",
                                headers=headers)

        # Obtener el título del canal
        if response.status_code == 200:
            data = response.json()["data"]
            if len(data) > 0:
                channel_title = data[0]["title"]
                start_message_text = f"{channel_title}\n{url_stream}"
            else:
                print("Canal no encontrado")
        else:
            print("Error al hacer la solicitud")
                   

    await update.message.reply_text(start_message_text,parse_mode=ParseMode.HTML,disable_web_page_preview=False)

stream_command_handler = CommandHandler('stream', stream)



#elglitch id":"707447498"