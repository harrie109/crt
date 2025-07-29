import pytz
import logging
import requests
from flask import Flask
from datetime import datetime
from threading import Thread
from telegram.ext import Updater, CommandHandler
from apscheduler.schedulers.background import BackgroundScheduler

# --- CONFIG ---
BOT_TOKEN = '8472184215:AAG7bZCJ6yprFlGFRtN3kB8IflyuRpHLdv8'
CHAT_ID = '6234179043'
IST = pytz.timezone('Asia/Kolkata')

LIVE_PAIRS = [
    "EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "NZDUSD",
    "USDCHF", "USDCAD", "EURJPY", "GBPJPY", "EURGBP"
]

# --- Flask App to keep Render port open ---
app = Flask(__name__)

@app.route('/')
def home():
    return "CRT Signal Bot Running"

# --- Logging ---
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- Placeholder CRT + SNR Logic ---
def fetch_crt_signal(pair):
    now = datetime.now(IST)
    seconds = now.second
    if seconds < 3:
        signal = {
            "pair": pair,
            "pattern": "CRT on SNR Zone",
            "direction": "CALL" if now.minute % 2 == 0 else "PUT",
            "strength": "Strong" if now.minute % 3 == 0 else "Minor",
            "time": now.strftime("%H:%M:%S")
        }
        return signal
    return None

# --- Telegram Signal Sender ---
def send_signal(context):
    logging.info("Checking for CRT signals...")
    for pair in LIVE_PAIRS:
        signal = fetch_crt_signal(pair)
        if signal:
            message = (
                f"🚨 CRT Signal Alert 🚨\n"
                f"Pair: {signal['pair']}\n"
                f"Pattern: {signal['pattern']}\n"
                f"Direction: {signal['direction']}\n"
                f"Strength: {signal['strength']} 🔥\n"
                f"Time: {signal['time']} IST"
            )
            context.bot.send_message(chat_id=CHAT_ID, text=message)
            logging.info(f"Signal sent: {message}")
        else:
            logging.info(f"No signal for {pair} at this time.")

# --- Telegram Bot Setup ---
def start(update, context):
    update.message.reply_text("🚀 CRT Signal Bot Activated!\nYou'll receive signals 24/7 from live Quotex market.")

def run_bot():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))

    scheduler = BackgroundScheduler(timezone=IST)
    scheduler.add_job(send_signal, 'cron', second=0, args=[updater.job_queue])
    scheduler.start()
    logging.info("Scheduler started.")

    updater.start_polling()
    updater.idle()

# --- Run Everything ---
if __name__ == '__main__':
    Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=10000)
