import logging
import requests
import pytz
from datetime import datetime
from telegram import Bot
from telegram.ext import Updater, CommandHandler
import time
import threading

# === CONFIGURATION ===
BOT_TOKEN = "8472184215:AAG7bZCJ6yprFlGFRtN3kB8IflyuRpHLdv8"
CHAT_ID = "6234179043"  # Replace with your own chat ID
CHECK_INTERVAL = 60  # every 1 minute
TIMEZONE = pytz.timezone("Asia/Kolkata")

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === SNR & CRT LOGIC (DUMMY EXAMPLE FOR DEMO) ===
def fetch_live_data():
    # Simulated Quotex data (replace with real API or method later)
    return [
        {"pair": "EUR/USD", "candle": "green", "snr": "support", "strength": "High"},
        {"pair": "USD/JPY", "candle": "red", "snr": "resistance", "strength": "Medium"},
        {"pair": "GBP/USD", "candle": "green", "snr": "support", "strength": "Low"},
    ]

def detect_crt_signals():
    signals = []
    data = fetch_live_data()
    for d in data:
        if d["snr"] in ["support", "resistance"]:
            direction = "CALL" if d["candle"] == "green" and d["snr"] == "support" else "PUT"
            signals.append({
                "pair": d["pair"],
                "pattern": f"Rejection at {d['snr'].capitalize()}",
                "direction": direction,
                "strength": d["strength"]
            })
    return signals

# === TELEGRAM BOT ===
bot = Bot(token=BOT_TOKEN)

def send_signal(signal):
    message = f"""🚨 CRT Signal Alert 🚨
Pair: {signal['pair']}
Pattern: {signal['pattern']}
Direction: {signal['direction']}
Strength: {signal['strength']} 🔥
Time: {datetime.now(TIMEZONE).strftime('%I:%M:%S %p')} IST"""
    bot.send_message(chat_id=CHAT_ID, text=message)

def signal_loop():
    while True:
        try:
            signals = detect_crt_signals()
            for sig in signals:
                send_signal(sig)
        except Exception as e:
            logger.error(f"Error sending signal: {e}")
        time.sleep(CHECK_INTERVAL)

def start(update, context):
    update.message.reply_text("🚨 CRT Signal Bot Activated!\nYou will now receive 24/7 automated signals")

# === MAIN ===
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    updater.start_polling()
    logger.info("Bot started. Sending CRT signals every minute.")

    # Start signal loop in background
    threading.Thread(target=signal_loop, daemon=True).start()
    updater.idle()

if __name__ == "__main__":
    main()
