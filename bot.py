
# bot.py - CRT + SNR based signal bot for Quotex (1-minute candles)
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import random

TOKEN = 'YOUR_BOT_TOKEN'
CHAT_ID = 'YOUR_CHAT_ID'

def generate_signal():
    # Simulated logic (replace with live data logic)
    patterns = ['Engulfing at Resistance', 'Rejection at Support', 'Breakout Doji']
    direction = random.choice(['CALL', 'PUT'])
    strength = random.choice(['High 🔥', 'Medium ⚠️'])
    return f"🚨 CRT Signal Alert 🚨\nPattern: {random.choice(patterns)}\nDirection: {direction}\nStrength: {strength}"

def start(update: Update, context: CallbackContext):
    signal = generate_signal()
    context.bot.send_message(chat_id=update.effective_chat.id, text=signal)

def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
