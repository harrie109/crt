import logging
import requests
import pytz
from datetime import datetime
from telegram import Bot, ParseMode
from telegram.ext import Updater, CommandHandler
from apscheduler.schedulers.background import BackgroundScheduler

# === CONFIGURATION ===
BOT_TOKEN = "8472184215:AAG7bZCJ6yprFlGFRtN3kB8IflyuRpHLdv8"
CHAT_ID = "6234179043"
TRADINGVIEW_API = "https://scanner.tradingview.com/crypto/scan"
TIMEZONE = pytz.timezone("Asia/Kolkata")

# === LOGGER SETUP ===
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# === TELEGRAM BOT ===
bot = Bot(token=BOT_TOKEN)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
        text="🚨 CRT Signal Bot Activated!\nYou will now receive 24/7 automated signals")

# === CORE CRT SIGNAL LOGIC ===
def fetch_signals():
    try:
        pairs = ["EURUSD", "USDJPY", "GBPUSD", "AUDUSD", "NZDUSD", "USDCHF", "USDCAD"]  # Only live
        headers = {'Content-Type': 'application/json'}

        payload = {
            "symbols": {
                "tickers": [f"OANDA:{pair}" for pair in pairs],
                "query": {"types": []}
            },
            "columns": ["Recommend.Other", "close", "volume"]
        }

        response = requests.post(TRADINGVIEW_API, json=payload, headers=headers, timeout=10)
        result = response.json()

        for data in result.get("data", []):
            symbol = data.get("s", "")
            recommendation = data["d"][0]

            direction = "CALL" if recommendation > 0.3 else "PUT" if recommendation < -0.3 else None
            strength = (
                "🔥 Strong" if abs(recommendation) > 0.5 else
                "⚠️ Medium" if abs(recommendation) > 0.3 else
                "Weak"
            )

            if direction and strength != "Weak":
                now = datetime.now(TIMEZONE).strftime("%Y-%m-%d %H:%M:%S")
                message = f"""
📍 *CRT SIGNAL ALERT* [{now}]
Pair: `{symbol.split(':')[1]}`
Direction: *{direction}*
Strength: *{strength}*
                """
                bot.send_message(chat_id=CHAT_ID, text=message, parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        logging.error(f"[Signal Error] {e}")

# === SETUP SCHEDULER ===
scheduler = BackgroundScheduler(timezone=TIMEZONE)
scheduler.add_job(fetch_signals, "interval", minutes=1)
scheduler.start()

# === TELEGRAM SETUP ===
def main():
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
