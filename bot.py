import logging
import random
import time
from telegram import Bot
from telegram.ext import Updater, CommandHandler
from apscheduler.schedulers.background import BackgroundScheduler

# ✅ Replace with your bot token and chat ID
BOT_TOKEN = '8472184215:AAG7bZCJ6yprFlGFRtN3kB8IflyuRpHLdv8'
CHAT_ID = '6234179043'

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)

def generate_fake_snr_signal():
    """Simulates a CRT signal with strong SNR."""
    pairs = ["EUR/USD", "USD/JPY", "GBP/USD", "AUD/CAD", "USD/INR"]
    actions = ["CALL", "PUT"]
    strength_levels = ["Strong", "Very Strong", "Extreme"]

    # Simulate random signal data
    signal = {
        "pair": random.choice(pairs),
        "action": random.choice(actions),
        "strength": random.choice(strength_levels)
    }
    return signal

def send_crt_signal():
    try:
        signal = generate_fake_snr_signal()

        if not signal:
            logger.warning("No signal to send.")
            return

        message = f"🔔 CRT SIGNAL 🔔\n\n" \
                  f"📊 Pair: {signal['pair']}\n" \
                  f"📈 Action: {signal['action']}\n" \
                  f"💪 Strength: {signal['strength']}\n" \
                  f"🕒 Time: {time.strftime('%H:%M:%S')}"

        bot.send_message(chat_id=CHAT_ID, text=message)
        logger.info("Signal sent: %s", message)
    except Exception as e:
        logger.error("Failed to send CRT signal: %s", e)

def start(update, context):
    update.message.reply_text("✅ CRT Signal Bot Activated!\nYou will now receive 24/7 automated signals.")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))

    # Scheduler to send signal every 1 minute
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_crt_signal, 'interval', minutes=1)
    scheduler.start()

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
