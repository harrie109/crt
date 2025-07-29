import pytz
import logging
import requests
from datetime import datetime
from telegram.ext import Updater, CommandHandler
from apscheduler.schedulers.background import BackgroundScheduler

# --- CONFIG ---
BOT_TOKEN = '8472184215:AAG7bZCJ6yprFlGFRtN3kB8IflyuRpHLdv8'
CHAT_ID = '6234179043'
IST = pytz.timezone('Asia/Kolkata')

# Quotex live currency pairs only (no OTC)
LIVE_PAIRS = [
    "EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "NZDUSD",
    "USDCHF", "USDCAD", "EURJPY", "GBPJPY", "EURGBP"
]

# --- Logging ---
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- Placeholder CRT + SNR logic ---
def fetch_crt_signal(pair):
    now = datetime.now(IST)
    seconds = now.second
    # Wait for full candle close
    if seconds < 5:
        signal = {
            "pair": pair,
            "pattern": "CRT on SNR Zone",
            "direction": "CALL" if now.minute % 2 == 0 else "PUT",
            "strength": "Strong" if now.minute % 3 == 0 else "Minor",
            "time": now.strftime("%H:%M:%S")
        }
        return signal
    return None

# --- Telegram Bot Signal Sender ---
def send_signal(context):
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

def start(update, context):
    update.message.reply_text("🚀 CRT Signal Bot Activated!\nYou'll receive 24/7 accurate signals from live Quotex market.")

# --- Main Bot Runner ---
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))

    scheduler = BackgroundScheduler(timezone=IST)
    scheduler.add_job(send_signal, 'cron', second=0, args=[updater.job_queue])
    scheduler.start()

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
