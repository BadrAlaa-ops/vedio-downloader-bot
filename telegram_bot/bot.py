import telebot
from telebot import types
import yt_dlp
import os
from dotenv import load_dotenv

# تحميل التوكن من .env
load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN)

# 🔥 زرار البداية
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = types.KeyboardButton("تحميل فيديو 🎬")
    btn2 = types.KeyboardButton("تحميل صوت 🎧")

    markup.add(btn1, btn2)

    bot.send_message(
        message.chat.id,
        "🔥 أهلاً بيك في البوت الاحترافي\nاختار اللي عايزه 👇",
        reply_markup=markup
    )

# 📌 حالة المستخدم
user_state = {}

# 🎛️ التعامل مع الأزرار
@bot.message_handler(func=lambda m: True)
def handle(message):
    text = message.text

    if text == "تحميل فيديو 🎬":
        user_state[message.chat.id] = "video"
        bot.reply_to(message, "📥 ابعت لينك الفيديو")

    elif text == "تحميل صوت 🎧":
        user_state[message.chat.id] = "audio"
        bot.reply_to(message, "📥 ابعت لينك الفيديو لتحويله صوت")

    else:
        if message.chat.id not in user_state:
            bot.reply_to(message, "❗ اختار من الأزرار الأول")
            return

        mode = user_state[message.chat.id]
        url = message.text

        try:
            bot.send_message(message.chat.id, "⏳ جاري التحميل...")

            if mode == "video":
                ydl_opts = {
                    'format': 'best',
                    'outtmpl': '%(title)s.%(ext)s'
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    file = ydl.prepare_filename(info)

                with open(file, 'rb') as f:
                    bot.send_video(message.chat.id, f)

                os.remove(file)

            elif mode == "audio":
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': '%(title)s.%(ext)s',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                    }]
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    file = ydl.prepare_filename(info).replace(".webm", ".mp3").replace(".m4a", ".mp3")

                with open(file, 'rb') as f:
                    bot.send_audio(message.chat.id, f)

                os.remove(file)

        except Exception as e:
            bot.reply_to(message, "❌ حصل خطأ أو الرابط مش شغال")

bot.infinity_polling()