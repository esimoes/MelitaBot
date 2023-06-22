import logging
import sys
from warnings import filterwarnings

from loguru import logger
from telegram.warnings import PTBUserWarning

from utils.env_utils import load_env_variable

class Config:
    ###########################################################################
    #                         Set up env vars below ⬇                         #
    ###########################################################################
    DEBUG_FLAG = bool(load_env_variable('DEBUG_FLAG', int))  # Enables debug level logging

    BOT_TOKEN = load_env_variable('BOT_TOKEN')  # Your Telegram bot token

    OWNER_ID = load_env_variable('OWNER_ID', int)  # Bot owner Telegram id
    DEV_ID = load_env_variable('DEV_ID', int, False)  # Bot dev Telegram id
    DB_URL = load_env_variable('DB_URL')  # URL to your db # f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    USER_DB= load_env_variable('USER_DB', str)

    CALENDAR_ID = load_env_variable('CALENDAR_ID', str)
    CALENDAR_ID_SEC = load_env_variable('CALENDAR_ID_SEC', str)

    SPREADSHEET_ID=load_env_variable('SPREADSHEET_ID', str)
    SPREADSHEET_SHEET=load_env_variable('SPREADSHEET_SHEET_RECO', str)
    SPREADSHEET_SHEET_FORTUNE=load_env_variable('SPREADSHEET_SHEET_FORTUNE', str)
    #####################
    #   Twitch API vars #
    #####################
    TWITCH_CLIENT_ID = load_env_variable('TWITCH_CLIENT_ID', str)
    TWITCH_CLIENT_SECRET = load_env_variable('TWITCH_CLIENT_SECRET', str)
    TWITCH_CHANNEL_ID = load_env_variable('TWITCH_CHANNEL_ID', str)
    TWITCH_STREAM_URL = load_env_variable('TWITCH_STREAM_URL', str)
    # Youtube API
    YOUTUBE_API_KEY = load_env_variable('YOUTUBE_API_KEY', str)


    logging_lvl = logging.DEBUG if DEBUG_FLAG else logging.INFO

    class InterceptLogsHandler(logging.Handler):
        def emit(self, record):
            # Get corresponding Loguru level if it exists.
            try:
                level = logger.level(record.levelname).name
            except ValueError:
                level = record.levelno

            # Find caller from where originated the logged message.
            frame, depth = sys._getframe(6), 6
            while frame and frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back
                depth += 1

            logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())

    format = ('<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name: '
              '<20.20}</cyan> | <level>{message}</level> ')

    logger.remove()
    logger.add(sys.stderr, format=format)
    logger.level("DEBUG", color="<fg #787878>")
    logger.level("INFO", color="<fg #ffffff>")

    logging.basicConfig(handlers=[InterceptLogsHandler()], level=logging_lvl, force=True)

    if not DEBUG_FLAG:
        filterwarnings(action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning)