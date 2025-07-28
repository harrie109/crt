import time
import logging
from telegram import Bot
from telegram.error import TelegramError
from datetime import datetime
import random

# Replace with your actual bot token and chat ID
TOKEN = '8472184215:AAG7bZCJ6yprFlGFRtN3kB8IflyuRpHLdv8'
CHAT_ID = '6234179043'  # Replace with real chat ID

bot = Bot(token=TOKEN)

logging.basicConfig(level=logging.INFO)
print("CRT Auto Bot Running...")

# Dummy function to simulate CRT signal based on SNR
def generate_crt_signal():
    patterns = ['Rejection at Support', 'Rejection at Resistance']
    directions = ['CALL', 'PUT']
    strengths = ['High 🔥', 'Medium ⚡']

    return {
        'pattern': random.choice(patterns),
        'direction': random.choice(directions),
        'strength': random.choice(strengths)
    }

def send_signal():
    signal = generate_crt_signal()
    message = f"""🚨 CRT Signal Alert 🚨
Pattern: {signal['pattern']}
Direction: {signal['direction']}
Strength: {signal['strength']}"""
    
    try:
        bot.send_message(chat_id=CHAT_ID, text=message)
        print(f"✅ Sent: {message}")
    except TelegramError as e:
        print(f"❌ Telegram error: {e}")

# Main loop: sends signal every 60 seconds
while True:
    now = datetime.now()
    print(f"📤 Sending signal at {now.strftime('%H:%M:%S')}...")
    send_signal()
    time.sleep(60)
