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

# Logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- CRT Wick Rejection Logic from TradingView ---
def fetch_tradingview_data(pair):
    url = f"https://scanner.tradingview.com/forex/scan"
    payload = {
        "symbols": {"tickers": [f"OANDA:{pair}"], "query": {"types": []}},
        "columns": ["open", "close", "high", "low"]
    }
    try:
        response = requests.post(url, json=payload, timeout=5)
        data = response.json()
        d = data['data'][0]['d']
        return {
            "open": float(d[0]),
            "close": float(d[1]),
            "high": float(d[2]),
            "low": float(d[3])
        }
    except Exception as e:
        logging.error(f"{pair} data fetch failed: {e}")
        return None

def detect_crt_signal(pair):
    candle = fetch_tradingview_data(pair)
    if not candle:
        return None

    body = abs(candle['open'] - candle['close'])
    upper_wick = candle['high'] - max(candle['open'], candle['close'])
    lower_wick = min(candle['open'], candle['close']) - candle['low']

    if body == 0: return None  # avoid division by zero

    wick_ratio = max(upper_wick, lower_wick) / body

    if wick_ratio > 1.5:  # significant wick rejection
        direction = "CALL" if lower_wick > upper_wick else "PUT"
        strength = "Strong" if wick_ratio > 2.5 else "Moderate"
        return {
            "pair": pair,
            "pattern": "CRT Rejection at SNR",
            "direction": direction,
            "strength": strength,
            "time": datetime.now(IST).strftime("%H:%M:%S")
        }

    return None

# --- Telegram Logic ---
def send_crt_signals(context):
    for pair in LIVE_PAIRS:
        signal = detect_crt_signal(pair)
        if signal:
            message = f"🚨 CRT Signal Alert 🚨\n" \
                      f"Pair: {signal['pair']}\n" \
                      f"Pattern: {signal['pattern']}\n" \
                      f"Direction: {signal['direction']}\n" \
                      f"Strength: {signal['strength']} 🔥\n" \
                      f"Time: {signal['time']} IST"
            context.bot.send_message(chat_id=CHAT_ID, text=message)

def start(update, context):
    update.message.reply_text("🚀 CRT Signal Bot Activated!\nYou will now receive 24/7 automated signals.")

# --- Main Bot ---
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))

    scheduler = BackgroundScheduler(timezone=pytz.utc)
    scheduler.add_job(send_crt_signals, 'interval', minutes=1, next_run_time=datetime.now(pytz.utc), args=[updater.job_queue])
    scheduler.start()

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
