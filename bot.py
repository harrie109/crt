import logging
from telegram import Bot, Update
from telegram.ext import CommandHandler, Updater
import random
import schedule
import time
import threading

TOKEN = "8472184215:AAG7bZCJ6yprFlGFRtN3kB8IflyuRpHLdv8
"  # Replace with your token
CHAT_ID = "6234179043"  # Replace with your actual chat ID

bot = Bot(token=TOKEN)

# Predefined dummy CRT signals for now
patterns = ["Rejection at Support", "Breakout at Resistance", "Fakeout below SNR", "Pinbar on Zone"]
directions = ["CALL", "PUT"]
strengths = ["High 🔥", "Medium ⚡", "Low ⚠️"]

def send_crt_signal():
    pattern = random.choice(patterns)
    direction = random.choice(directions)
    strength = random.choice(strengths)
    message = f"🚨 CRT Signal Alert 🚨\nPattern: {pattern}\nDirection: {direction}\nStrength: {strength}"
    try:
        bot.send_message(chat_id=CHAT_ID, text=message)
        print("Signal sent!")
    except Exception as e:
        print("Error sending signal:", e)

def start_command(update: Update, context):
    update.message.reply_text("🚨 CRT Signal Alert 🚨\nPattern: Rejection at Support\nDirection: CALL\nStrength: High 🔥")

def run_schedule():
    schedule.every(1).minutes.do(send_crt_signal)
    while True:
        schedule.run_pending()
        time.sleep(1)

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start_command))
    
    # Start the scheduler in a new thread
    threading.Thread(target=run_schedule, daemon=True).start()
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
