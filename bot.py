import logging
import time
import random
from telegram import Bot
from apscheduler.schedulers.background import BackgroundScheduler

# === CONFIGURATION ===
BOT_TOKEN = '8472184215:AAG7bZCJ6yprFlGFRtN3kB8IflyuRpHLdv8'  # Replace with your actual bot token
CHAT_ID = '6234179043'          # Replace with your actual Telegram chat ID

# === LOGGER SETUP ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === BOT INITIALIZATION ===
bot = Bot(token=BOT_TOKEN)
scheduler = BackgroundScheduler()

# === MOCK CURRENCY PAIRS ===
CURRENCY_PAIRS = [
    'EUR/USD', 'USD/JPY', 'GBP/USD', 'AUD/USD', 'USD/CAD',
    'NZD/USD', 'EUR/GBP', 'EUR/JPY', 'GBP/JPY', 'USD/CHF'
]

# === GENERATE FAKE STRONG SNR CRT SIGNAL ===
def generate_crt_signal():
    pair = random.choice(CURRENCY_PAIRS)
    direction = random.choice(['CALL 🔼', 'PUT 🔽'])
    strength = random.randint(80, 95)  # Simulate strong accuracy
    signal = f"""
⚡ *CRT SIGNAL ALERT* ⚡
———————————————
📉 Pair: *{pair}*
📍 Direction: *{direction}*
📊 Strength: *{strength}%*
⏱ Time: {time.strftime('%H:%M:%S')}
———————————————
"""
    return signal

# === SEND SIGNAL FUNCTION ===
def send_crt_signal():
    try:
        message = generate_crt_signal()
        bot.send_message(chat_id=CHAT_ID, text=message, parse_mode='Markdown')
        logger.info("Signal sent.")
    except Exception as e:
        logger.error(f"Failed to send signal: {e}")

# === START AUTOMATED SCHEDULER ===
def start_bot():
    logger.info("CRT Auto Bot Running...")
    send_crt_signal()  # Send one immediately at startup
    scheduler.add_job(send_crt_signal, 'interval', seconds=60)
    scheduler.start()

# === RUN ===
if __name__ == '__main__':
    start_bot()
    try:
        while True:
            time.sleep(10)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        logger.info("Bot stopped.")
