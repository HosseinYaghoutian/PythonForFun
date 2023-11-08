# pip install pyTelegramBotAPI, pillow
import telebot
from telebot import types
from email import message

#2
import random

#3
import datetime

#6
from gtts import gTTS

#7
import qrcode

bot = telebot.TeleBot("5385900787:AAFK8xlrIccvN1HNGoqLL2F_3cCytEGshfw")

stop = False


#0
@bot.message_handler(commands=['help', 'Help'])
def send_welcome(message):
    bot.reply_to(
        message, """	
/help : توضیحات فرآیند ربات
/start : پیام خوش آمد

/game : بازی حدس عدد
/age : مشاهده سن 

/max : بزرگترین عدد در آرایه 
/argmax : اندیس بزرگترین عدد در آرایه

/voice : تبدیل متن انگلیسی به صدا 
/qrcode : ایجاد کیوارکد برای متن 
""")


#1
@bot.message_handler(commands=['start', 'Start'])
def send_welcome(message):
    bot.reply_to(
        message,
        f"سلام {message.from_user.first_name} برای دسترسی به اطلاعات بیشتر دستور /help رو بفرست"
    )


#2
@bot.message_handler(commands=['game', 'Game'])
def send_question_game(message):
    bot.reply_to(message, "عدد بین ۱تا۱۰۰ است، حدس بزن!")
    computer_num = random.randint(0, 100)

    @bot.message_handler(content_types=['text'])
    def game(message):
        user_num = int(message.text)
        if user_num == computer_num:
            bot.reply_to(message, "درست حدس زدی!")

        elif user_num < computer_num:
            bot.reply_to(message, "برو بالا")

        elif user_num > computer_num:
            bot.reply_to(message, "بیا پایین")


#3
@bot.message_handler(commands=['age', 'Age'])
def send_question_age(message):
    bot.reply_to(message, f"سال تولدت رو به شمسی وارد کن تا سنتو بگم!")

    @bot.message_handler(content_types=['text'])
    def echo(message):
        birth_year = int(message.text)
        age_now = (datetime.datetime.now().year - 622) - birth_year
        bot.reply_to(message, f"تو الان {age_now} سالته!")


#4
@bot.message_handler(commands=['max', 'Max'])
def list(message):
    myname = message.from_user.first_name
    list = []
    bot.reply_to(message, f"تعدادی عدد رو وارد کن تا بزرگترینشو بهت بگم!")

    @bot.message_handler(func=lambda m: True)
    def echo(message):
        list.append(int(message.text))
        max_value = max(list)

        bot.reply_to(message, f"{max_value}")


#5
@bot.message_handler(commands=['argmax', 'Argmax'])
def list(message):
    myname = message.from_user.first_name
    list = []
    bot.reply_to(message,
                 f"تعدادی عدد رو وارد کن تا جایگاه بزرگترینشو بهت بگم!")

    @bot.message_handler(func=lambda m: True)
    def echo(message):
        list.append(int(message.text))
        max_value = max(list)
        max_index = list.index(max_value)
        bot.reply_to(message, f"{max_index}")


#6
@bot.message_handler(commands=['voice', 'Voice'])
def send_voice(message):
    bot.reply_to(message, f"متن انگلیسی خودت رو بنویس تا به صدا تبدیل بشه")

    @bot.message_handler(content_types=['text'])
    def echo(message):
        gTTS(message.text).save('voice.mp3')
        bot.send_voice(message.chat.id, open('voice.mp3', 'rb'))


#7
@bot.message_handler(commands=['qrcode', 'QRCode'])
def send_qrcode(message):
    bot.reply_to(message, f"متن خودت رو بنویس تا به QRCode تبدیل بشه")

    @bot.message_handler(func=lambda message: True)
    def echo(message):
        qrcode.make(message.text).save("qrcode.png")
        bot.send_photo(message.chat.id, open('qrcode.png', 'rb'))


bot.infinity_polling()