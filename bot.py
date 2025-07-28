import logging
import random
import datetime
import pytz
import time
import threading

from telegram import Bot, Update
from telegram.ext import CommandHandler, Updater, CallbackContext

# === CONFIGURATION ===
TOKEN = "8472184215:AAG7bZCJ6yprFlGFRtN3kB8IflyuRpHLdv8"
chat_id = None  # Will be set when user sends /start

# === LOGGING ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === GENERATE DUMMY CRT SIGNAL (you can plug real logic here) ===
def generate_crt_signal():
    currency_pairs = ['EUR/USD', 'GBP/JPY', 'AUD/CAD', 'USD/JPY', 'EUR/INR', 'USD/INR']
    directions = ['BUY', 'SELL']
    strength_levels = ['Weak', 'Moderate', 'Strong', 'Very Strong']

    return {
        "pair": random.choice(currency_pairs),
        "direction": random.choice(directions),
        "strength": random.choice(strength_levels),
        "time": datetime.datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%H:%M:%S")
    }

# === SEND SIGNAL TO TELEGRAM ===
def send_crt_signal():
    if chat_id is None:
        logger.info("Chat ID not set yet. Skipping signal send.")
        return

    signal = generate_crt_signal()
    message = (
        f"📡 *CRT Signal Alert*\n\n"
        f"🔹 Pair: `{signal['pair']}`\n"
        f"🔸 Direction: *{signal['direction']}*\n"
        f"📊 Strength: `{signal['strength']}`\n"
        f"⏰ Time: `{signal['time']}`"
    )
    try:
        bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")
        logger.info("Signal sent successfully.")
    except Exception as e:
        logger.error(f"Failed to send signal: {e}")

# === LOOP THAT SENDS SIGNALS EVERY 60 SECONDS ===
def start_signal_loop():
    while True:
        send_crt_signal()
        time.sleep(60)  # 1-minute interval

# === /start COMMAND HANDLER ===
def start(update: Update, context: CallbackContext):
    global chat_id
    chat_id = update.effective_chat.id
  update.message.reply_text("✅ CRT Signal Bot Activated! You will now receive 24/7 CRT signals based on strong SNR levels.")

