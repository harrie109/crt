import logging
import requests
import json
import time
import schedule
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram import Update
from datetime import datetime

# === Telegram Bot Token ===
TOKEN = "8472184215:AAG7bZCJ6yprFlGFRtN3kB8IflyuRpHLdv8"

# === Logging ===
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# === Global ===
CHAT_ID = None

# === Function to fetch live data ===
def fetch_data():
    try:
        response = requests.get("https://api.wiseinvest.ai/market/quotes")  # Replace with valid endpoint
        data = response.json()
        return data
    except Exception as e:
        logger.error(f"Error fetching data: {e}")
        return {}

# === Function to find strong SNR levels ===
def get_strong_snr_signals():
    signals = []
    data = fetch_data()
    if not data:
        return signals

    for pair in data.get("data", []):
        symbol = pair.get("symbol", "")
        price = pair.get("price", 0)
        support = pair.get("support", 0)
        resistance = pair.get("resistance", 0)

        # Basic SNR check (replace with more advanced logic if needed)
        if abs(price - support) < 0.01:
            signals.append(f"🔵 BUY Signal on {symbol} near strong Support: {support}")
        elif abs(price - resistance) < 0.01:
            signals.append(f🔴 SELL Signal on {symbol} near strong Resistance: {resistance}")

    return signals

# === Job to send signals ===
def send_signals():
    global CHAT_ID
    if not CHAT_ID:
        return

    signals = get_strong_snr_signals()
    if signals:
        message = f"📡 CRT Signals ({datetime.now().strftime('%H:%M:%S')}):\n\n" + "\n".join(signals)
        updater.bot.send_message(chat_id=CHAT_ID, text=message)
    else:
        logger.info("No strong SNR signals found at this minute.")

# === /start Command Handler ===
def start(update: Update, context: CallbackContext):
    global CHAT_ID
    CHAT_ID = update.message.chat_id
    update.message.reply_text("✅ CRT Signal Bot Activated! You will now receive 24/7 CRT signals based on strong SNR levels.")

# === Main ===
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", start))

# === Schedule Signal Sending Every Minute ===
schedule.every(60).seconds.do(send_signals)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

# === Start Bot ===
import threading
threading.Thread(target=run_scheduler, daemon=True).start()
updater.start_polling()
updater.idle()
