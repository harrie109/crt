import logging
import requests
import schedule
import time
import threading
from telegram import Bot
from telegram.ext import Updater, CommandHandler
from apscheduler.schedulers.background import BackgroundScheduler

# ✅ Your working bot token (make sure it's complete)
TOKEN = "8472184215:AAG7bZCJ6yprFlGFRtN3kB8IflyuRpHLdv8"
CHAT_ID = "6234179043"  # Replace with your actual chat ID or set dynamically

bot = Bot(token=TOKEN)

# Log setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def send_crt_signal():
    # Replace this with your logic to fetch and analyze CRT signals
    signal = "🔥 CRT Signal: BUY USD/JPY @ 14:32\nStrength: STRONG"
    bot.send_message(chat_id=CHAT_ID, text=signal)

def start(update, context):
    update.message.reply_text("Bot is running and will send CRT signals every 1 minute.")

def job_thread():
    schedule.every(1).minutes.do(send_crt_signal)
    while True:
        schedule.run_pending()
        time.sleep(1)

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    threading.Thread(target=job_thread).start()

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
