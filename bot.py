import pytz
import logging
import requests
from datetime import datetime, timedelta
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


# --- Real SNR + CRT Signal Logic ---
def fetch_candle_data(pair):
    try:
        url = f"https://scanner.tradingview.com/crypto/scan"
        payload = {
            "symbols": {"tickers": [f"FX:{pair}"], "query": {"types": []}},
            "columns": ["close", "open", "low", "high"]
        }
        response = requests.post(url, json=payload)
        result = response.json()
        candles = result["data"][0]["d"]
        return {
            "open": candles[1],
            "close": candles[0],
            "low": candles[2],
            "high": candles[3]
        }
    except Exception as e:
        logging.warning(f"Failed to fetch data for {pair}: {e}")
        return None


def is_crt_rejection(candle):
    body_size = abs(candle["close"] - candle["open"])
    wick_top = candle["high"] - max(candle["open"], candle["close"])
    wick_bottom = min(candle["open"], candle["close"]) - candle["low"]

    if body_size == 0:
        return None  # Avoid division by zero

    bottom_ratio = wick_bottom / body_size
    top_ratio = wick_top / body_size

    if bottom_ratio > 1.5 and candle["close"] > candle["open"]:
        return "CALL"
    elif top_ratio > 1.5 and candle["close"] < candle["open"]:
        return "PUT"
    else:
        return None


def determine_strength(candle):
    body = abs(candle["close"] - candle["open"])
    range_ = candle["high"] - candle["low"]
    if body / range_ > 0.6:
        return "High"
    elif body / range_ > 0.3:
        return "Moderate"
    else:
        return "Low"


def generate_signal(pair):
    candle = fetch_candle_data(pair)
    if not candle:
        return None

    direction = is_crt_rejection(candle)
    if not direction:
        return None

    strength = determine_strength(candle)
    time_now = datetime.now(IST).strftime("%H:%M:%S")

    return {
        "pair": pair,
        "pattern": "CRT Rejection at SNR",
        "direction": direction,
        "strength": strength,
        "time": time_now
    }


# --- Telegram Logic ---
def send_signals(context):
    for pair in LIVE_PAIRS:
        signal = generate_signal(pair)
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
    update.message.reply_text(
        "🚀 CRT Signal Bot Activated!\nYou will now receive 24/7 automated signals."
    )


# --- Main Runner ---
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))

    scheduler = BackgroundScheduler(timezone=pytz.utc)
    scheduler.add_job(send_signals, 'interval', minutes=1, next_run_time=datetime.now(pytz.utc), args=[updater.job_queue])
    scheduler.start()

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
