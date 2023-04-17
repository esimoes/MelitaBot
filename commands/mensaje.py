from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CommandHandler, ContextTypes
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
from config import Config

from utils.send_message_db import send_message

TYPING_REPLY, FINISH = range(2)

reply_keyboard = [
    ["Enviar", "Cancelar"]
    ]

reply_message = ""

markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True)

async def message_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the conversation and ask user for input."""
    user = update.effective_user
    if user.id in [Config.OWNER_ID]:
        answer_message_text = (f"<pre>Hola {user.first_name}, a continuación escribe el mensaje a enviar.</pre>")
    else:
        answer_message_text = "No puedo dejarte hacer eso."
        await update.message.reply_text(answer_message_text,parse_mode=ParseMode.HTML)
        return ConversationHandler.END

    await update.message.reply_text(answer_message_text,parse_mode=ParseMode.HTML,reply_markup=markup)

    return TYPING_REPLY

async def typing_reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global reply_message
    reply_message = update.effective_message.text
    preview_message = "<pre>Vista previa del mensaje, si está correcto dale al botón 'Enviar'.</pre>"
    
    await update.message.reply_text(preview_message,parse_mode=ParseMode.HTML)
    await update.message.reply_text(reply_message,parse_mode=ParseMode.HTML,disable_web_page_preview=False)

    return FINISH

async def waiting_send(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print ("esperando enviar mensaje")

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global reply_message
    answer_message_text = '<pre>Se envió notificación.</pre>'

    if reply_message == "":
        answer_message_text = '<pre>Mensaje vacío, se canceló la acción.</pre>'
    else:
        await send_message(context, reply_message)
    reply_message = ""
    await update.message.reply_text(answer_message_text,parse_mode=ParseMode.HTML,disable_web_page_preview=True,reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global reply_message
    reply_message = ""
    answer_message_text = '<pre>Mensaje cancelado.</pre>'
    await update.message.reply_text(answer_message_text,parse_mode=ParseMode.HTML,disable_web_page_preview=True,reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END
   
message_command_handler = ConversationHandler(
        entry_points=[CommandHandler("mensaje", message_command)],
        states={
            TYPING_REPLY: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^(Enviar|Cancelar)$")), typing_reply
                )
            ],
            FINISH: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^(Enviar|Cancelar)$")), waiting_send
                )
            ],
        },
        fallbacks=list([MessageHandler(filters.Regex("^Enviar$"), done),MessageHandler(filters.Regex("^Cancelar$"), cancel)]),
    )
