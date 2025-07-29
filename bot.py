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

# Live Quotex currency pairs (no OTC)
LIVE_PAIRS = [
    "EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "NZDUSD",
    "USDCHF", "USDCAD", "EURJPY", "GBPJPY", "EURGBP"
]

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- Signal Logic (Simulated CRT + SNR Logic) ---
def fetch_crt_signal(pair):
    now = datetime.now(IST).strftime("%H:%M:%S")
    second = datetime.now().second

    # Simulate logic
    direction = "CALL" if second % 2 == 0 else "PUT"
    strength = "Strong" if second % 3 == 0 else "Minor"
    pattern = f"CRT on {strength} SNR"

    return {
        "pair": pair,
        "pattern": pattern,
        "direction": direction,
        "strength": strength,
        "time": now
    }

# --- Telegram Signal Sender ---
def send_signal(bot):
    for pair in LIVE_PAIRS:
        signal = fetch_crt_signal(pair)
        message = f"🚨 CRT Signal Alert 🚨\n" \
                  f"Pair: {signal['pair']}\n" \
                  f"Pattern: {signal['pattern']}\n" \
                  f"Direction: {signal['direction']}\n" \
                  f"Strength: {signal['strength']} 🔥\n" \
                  f"Time: {signal['time']} IST"
        bot.send_message(chat_id=CHAT_ID, text=message)

# --- /start Handler ---
def start(update, context):
    update.message.reply_text("🚀 CRT Signal Bot Activated!\nYou will now receive 24/7 automated signals.")

# --- Main Bot Logic ---
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))

    scheduler = BackgroundScheduler(timezone=pytz.utc)
    scheduler.add_job(send_signal, 'interval', minutes=1, next_run_time=datetime.now(pytz.utc), args=[updater.bot])
    scheduler.start()

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
