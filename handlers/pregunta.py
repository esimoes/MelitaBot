from telegram import Update
from telegram.ext import ContextTypes
import random
import re

async def answer(message):
    
    if re.search(r'hola', message):
        return "Holii" 

    if re.search(r'\?', message) or re.search(r'\¿', message):
        # Si el mensaje del usuario contiene un signo de interrogación
        # Responder con un texto random
        respuestas = ["Sí", "No", "Tal vez", "Probablemente", "Definitivamente no","No veo por qué no", "Haz lo que dicte tu corazón", "Sí, sin pensarlo", "Yo no lo haría", "No creo que debas"]
        return random.choice(respuestas)
    else:
        return "🤔🤔"


async def answer_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.message.text.lower()
    answer_message = await answer(msg)
    await update.effective_message.reply_text(answer_message, quote=True)


