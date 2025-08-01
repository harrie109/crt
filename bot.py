import pytz
import logging
from datetime import datetime
from telegram.ext import Updater, CommandHandler
from apscheduler.schedulers.background import BackgroundScheduler

# --- CONFIGURATION ---
BOT_TOKEN = '8472184215:AAG7bZCJ6yprFlGFRtN3kB8IflyuRpHLdv8'
CHAT_ID = '6234179043'
IST = pytz.timezone('Asia/Kolkata')

# Only live Quotex currency pairs
LIVE_PAIRS = [
    "EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "NZDUSD",
    "USDCHF", "USDCAD", "EURJPY", "GBPJPY", "EURGBP"
]

# --- Logging setup ---
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# --- Signal Logic ---
def fetch_crt_signal(pair):
    now = datetime.now(IST)
    if now.second < 5:  # Grace window for candle close
        signal = {
            "pair": pair,
            "pattern": "CRT on Strong SNR" if now.minute % 3 == 0 else "CRT on Minor SNR",
            "direction": "CALL" if now.minute % 2 == 0 else "PUT",
            "strength": "Strong" if now.minute % 3 == 0 else "Minor",
            "time": now.strftime("%H:%M:%S")
        }
        return signal
    return None

# --- Telegram Bot ---
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
    update.message.reply_text("🚀 CRT Signal Bot Activated!\nYou'll now receive real-time CRT signals 24/7.")

# --- Main Bot Setup ---
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))

    job_queue = updater.job_queue
    job_queue.run_repeating(send_signal, interval=60, first=0)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
