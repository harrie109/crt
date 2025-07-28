import logging
import pytz
import datetime
import requests
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from apscheduler.schedulers.background import BackgroundScheduler

# === Configuration ===
TOKEN = "8472184215:AAG7bZCJ6yprFlGFRtN3kB8IflyuRpHLdv8"  # Replace with your bot token
CHAT_ID = "6234179043"           # Replace with your Telegram chat ID
PAIR_LIST = ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "EURJPY", "GBPJPY", "USDCHF", "NZDUSD"]  # Add more pairs if needed
TIMEZONE = pytz.timezone("Asia/Kolkata")

# === Logging Setup ===
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# === Support/Resistance Detection Logic (Dummy Example) ===
def fetch_candle_data(symbol):
    try:
        # Example API endpoint – replace with real one or your data fetch logic
        url = f"https://api.example.com/1m-candles?symbol={symbol}"
        response = requests.get(url)
        data = response.json()
        return data  # Expected: list of dicts with 'open', 'high', 'low', 'close'
    except Exception as e:
        logging.error(f"Error fetching data for {symbol}: {e}")
        return []

def calculate_strong_snr(candles):
    if len(candles) < 10:
        return None, None

    recent_highs = [c["high"] for c in candles[-10:]]
    recent_lows = [c["low"] for c in candles[-10:]]

    resistance = max(recent_highs)
    support = min(recent_lows)

    return resistance, support

def generate_crt_signal():
    signals = []
    for symbol in PAIR_LIST:
        candles = fetch_candle_data(symbol)
        if not candles:
            continue

        last_close = candles[-1]["close"]
        resistance, support = calculate_strong_snr(candles)

        if not resistance or not support:
            continue

        if last_close >= resistance * 0.997:
            signals.append(f"🔴 SELL Signal on {symbol} near strong Resistance: {resistance}")
        elif last_close <= support * 1.003:
            signals.append(f"🟢 BUY Signal on {symbol} near strong Support: {support}")

    return signals

def send_crt_signal(context: CallbackContext):
    signals = generate_crt_signal()
    if signals:
        now = datetime.datetime.now(TIMEZONE).strftime("%d-%b-%Y %I:%M:%S %p")
        message = f"📡 *CRT Signal Update* [{now} IST]\n\n" + "\n".join(signals)
        context.bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")
    else:
        logging.info("No signals generated.")

def start(update: Update, context: CallbackContext):
    update.message.reply_text("✅ CRT Signal Bot Activated!")

# === Main Entrypoint ===
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    scheduler = BackgroundScheduler(timezone=TIMEZONE)
    scheduler.add_job(lambda: send_crt_signal(updater.bot), 'interval', minutes=1)
    scheduler.start()

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
