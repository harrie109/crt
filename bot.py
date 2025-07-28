import logging
from telegram import Bot
from telegram.ext import Updater
import time
import schedule
import os

# Telegram Bot Token
TOKEN = os.getenv("BOT_TOKEN")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Dummy CRT signal generator
def send_crt_signal():
    try:
        bot = Bot(token=TOKEN)
        message = "📈 *CRT Signal*\nPair: EUR/USD\nDirection: CALL\nStrength: *Strong*"
        bot.send_message(chat_id=CHAT_ID, text=message, parse_mode='Markdown')
        logger.info("CRT signal sent.")
    except Exception as e:
        logger.error(f"Failed to send CRT signal: {e}")

# Set your chat_id manually or retrieve from updates
CHAT_ID = 6234179043  # Replace with your actual chat ID

# Start signal scheduler
schedule.every(1).minutes.do(send_crt_signal)

# Run loop
while True:
    schedule.run_pending()
    time.sleep(1)
