import logging
import pytz
import random
import datetime
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from apscheduler.schedulers.background import BackgroundScheduler

# ✅ Replace with your real bot token
BOT_TOKEN = "8472184215:AAG7bZCJ6yprFlGFRtN3kB8IflyuRpHLdv8"

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Define signal strength labels
strength_levels = ["Weak", "Moderate", "Strong", "Very Strong"]

# Simulated function for CRT signal generation
def generate_crt_signal():
    pairs = ["EUR/USD", "USD/JPY", "GBP/USD", "AUD/USD", "USD/CAD", "EUR/JPY"]
    directions = ["Buy 🟢", "Sell 🔴"]
    return {
        "pair": random.choice(pairs),
        "direction": random.choice(directions),
        "strength": random.choice(strength_levels),
        "time": datetime.datetime.now().strftime("%H:%M:%S"),
    }

# Send signal to user
def send_crt_signal():
    signal = generate_crt_signal()
    message = (
        f"📡 *CRT Signal Alert*\n\n"
        f"🔹 Pair: `{signal['pair']}`\n"
        f"🔸 Direction: *{signal['direction']}*\n"
        f"📊 Strength: `{signal['strength']}`\n"
        f"⏰ Time: `{signal['time']}`"
    )
    bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")

# Handle /start command
def start(update: Update, context: CallbackContext):
    global chat_id
    chat_id = update.message.chat_id
    context.bot.send_message(
        chat_id=chat_id,
        text="✅ CRT Signal Bot Activated!\nYou will now receive 24/7 automated signals",
    )

# Main setup
def main():
    global bot
    updater = Updater(BOT_TOKEN, use_context=True)
    bot = updater.bot
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))

    # ✅ Use pytz timezone to avoid APScheduler error
    timezone = pytz.timezone("Asia/Kolkata")

    scheduler = BackgroundScheduler(timezone=timezone)
    scheduler.add_job(send_crt_signal, "interval", minutes=1)
    scheduler.start()

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
