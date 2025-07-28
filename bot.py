from telegram import Bot, Update
from telegram.ext import CommandHandler, Updater
import logging
import schedule
import time
import threading
import requests

# === Telegram Bot Token ===
TOKEN = '8472184215:AAG7bZCJ6yprFlGFRtN3kB8IflyuRpHLdv8'  # Replace with your real token

# === Logging ===
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# === Command Handler ===
def start(update: Update, context):
    update.message.reply_text("🤖 CRT Signal Bot is Active.")

# === CRT Signal Sending Function (Example only) ===
def send_crt_signal(context=None):
    try:
        signal_text = "📈 CRT SIGNAL\nPAIR: EUR/USD\nTYPE: CALL 🔼\nSTRENGTH: STRONG"
        bot.send_message(chat_id=YOUR_CHAT_ID, text=signal_text)  # Replace YOUR_CHAT_ID
    except Exception as e:
        logger.error(f"Error sending signal: {e}")

# === Background Task Scheduler ===
def run_scheduler():
    schedule.every(1).minutes.do(send_crt_signal)
    while True:
