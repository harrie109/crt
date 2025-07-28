import logging
import pytz
from datetime import datetime
from telegram import Bot
from telegram.ext import Updater, CommandHandler
from apscheduler.schedulers.background import BackgroundScheduler
import requests

# === CONFIGURATION ===
TOKEN = "8472184215:AAG7bZCJ6yprFlGFRtN3kB8IflyuRpHLdv8"
CHAT_ID = "6234179043"
TIMEZONE = pytz.timezone("Asia/Kolkata")
LIVE_PAIRS = [
    "EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCHF",
    "NZDUSD", "USDCAD", "EURJPY", "GBPJPY", "EURGBP"
]  # only live Quotex pairs

bot = Bot(token=TOKEN)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# === SNR & CRT LOGIC ===
def detect_crt_signal(pair):
    try:
        url = f"https://api.tradingview.com/history?symbol=OANDA:{pair}&resolution=1&count=10"
        res = requests.get(url)
        data = res.json()

        if 'c' not in data:
            return None

        close = data['c'][-1]
        high = data['h'][-1]
        low = data['l'][-1]
        open_ = data['o'][-1]

        strength = "Low ⛔️"
        if abs(close - open_) > 0.0003:
            strength = "Medium ⚠️"
        if abs(close - open_) > 0.0006:
            strength = "High 🔥"

        # SNR Logic
        if abs(close - low) < 0.0002 and close > open_:
            pattern = "Rejection at Support"
            direction = "CALL"
        elif abs(close - high) < 0.0002 and close < open_:
            pattern = "Rejection at Resistance"
            direction = "PUT"
        elif close > high:
            pattern = "Breakout above Resistance"
            direction = "CALL"
        elif close < low:
            pattern = "Breakout below Support"
            direction = "PUT"
        else:
            return None

        return {
            "pair": pair,
            "pattern": pattern,
            "direction": direction,
            "strength": strength
        }
    except Exception as e:
        logging.error(f"Error for pair {pair}: {e}")
        return None

# === SCHEDULER JOB ===
def send_crt_signals():
    now = datetime.now(TIMEZONE).strftime("%I:%M %p")
    for pair in LIVE_PAIRS:
        signal = detect_crt_signal(pair)
        if signal:
            message = (
                f"🚨 CRT Signal Alert 🚨\n"
                f"Pair: {signal['pair']}\n"
                f"Pattern: {signal['pattern']}\n"
                f"Direction: {signal['direction']}\n"
                f"Strength: {signal['strength']}\n"
                f"Time: {now} (IST)"
            )
            try:
                bot.send_message(chat_id=CHAT_ID, text=message)
            except Exception as e:
                logging.error(f"Failed to send signal: {e}")

# === TELEGRAM HANDLER ===
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="🚀 CRT Signal Bot Activated!\nYou will now receive 24/7 automated signals")

# === MAIN ===
def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))

    scheduler = BackgroundScheduler()
    scheduler.add_job(send_crt_signals, 'interval', minutes=1)
    scheduler.start()

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
