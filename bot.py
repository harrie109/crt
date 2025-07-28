import logging
import requests
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext
import time

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Replace with your bot token
TOKEN = "8472184215:AAG7bZCJ6yprFlGFRtN3kB8IflyuRpHLdv8"

# SNR-based dummy signal generator (replace with real logic)
def get_crt_signal():
    return "📊 CRT Signal: EUR/USD 🔹 Strong Resistance at 1.0910 🔻 Sell\nStrength: 🔴 Strong"

# /start command handler
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('🤖 CRT Signal Bot Activated!\nYou will now receive 24/7 automated signals.')

def send_crt_signal(bot: Bot, chat_id: int):
    signal = get_crt_signal()
    bot.send_message(chat_id=chat_id, text=signal)

# Main polling and signal loop
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Register /start
    dp.add_handler(CommandHandler("start", start))

    updater.start_polling()
    bot = updater.bot
    chat_ids = set()

    # Listen to /start and store chat_id
    def capture_chat_id(update: Update, context: CallbackContext):
        chat_ids.add(update.message.chat_id)

    dp.add_handler(CommandHandler("start", capture_chat_id))

    # 24/7 signal loop
    while True:
        for chat_id in chat_ids:
            try:
                send_crt_signal(bot, chat_id)
            except Exception as e:
                print(f"Failed to send signal to {chat_id}: {e}")
        time.sleep(60)  # Wait 1 minute before sending next signal

if __name__ == '__main__':
    main()
