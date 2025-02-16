import telebot
import instaloader
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from colorama import Fore
from cfonts import render
from threading import Thread 
from flask import Flask

# Initialize the bot
TOKEN = "7650349324:AAExzwjqK3BZBva-dFahXm_ak8PHYi-CQ1E"
bot = telebot.TeleBot(TOKEN)
L = instaloader.Instaloader()

app = Flask('')

@app.route('/')
def home():
    return "I am alive"

def run_http_server():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_http_server)
    t.start()
    
    
# Welcome message
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "\U0001F44B Welcome to Instagram Info Bot! Send me an Instagram username (without @) to get details.")

# Handle username input
@bot.message_handler(func=lambda message: True)
def fetch_instagram_info(message):
    profile_name = message.text
    try:
        profile = instaloader.Profile.from_username(L.context, profile_name)
        pf = "✅ Yes" if profile.is_private else "❌ No"
        user_id = profile.userid
        
        # Determine account creation year
        ranges = [
            (1279000, 2010), (17750000, 2011), (279760000, 2012), (900990000, 2013),
            (1629010000, 2014), (2500000000, 2015), (3713668786, 2016), (5699785217, 2017),
            (8597939245, 2018), (21254029834, 2019), (43464475395, 2020),
            (50289297647, 2021), (57464707082, 2022), (63313426938, 2023)
        ]
        year_associated = next((year for user_range, year in ranges if user_id <= user_range), "Unknown")
        
        # Create response message with emojis
        response = (f"\U0001F4C4 *Instagram Profile Details:*"
                    f"\U0001F464 *Username:* `{profile.username}`\n"
                    f"\U0001F3C5 *Full Name:* {profile.full_name}\n"
                    f"\U0001F4DC *Bio:* {profile.biography}\n"
                    f"\U0001F4F8 *Posts:* {profile.mediacount}\n"
                    f"\U0001F465 *Followers:* {profile.followers}\n"
                    f"\U0001F91D *Following:* {profile.followees}\n"
                    f"\U0001F4CA *User ID:* {user_id}\n"
                    f"\U0001F512 *Private:* {pf}\n"
                    f"\U0001F5D3 *Year Created:* {year_associated}\n"
                    f"🌐 [Instagram Profile](https://www.instagram.com/{profile.username})")
        
        bot.send_message(message.chat.id, response, parse_mode="Markdown", disable_web_page_preview=True)
    except Exception as e:
        bot.send_message(message.chat.id, "❌ Error: Username not found or Instagram is blocking requests.")

keep_alive ( )
# Run the bot
bot.polling(none_stop=True)
