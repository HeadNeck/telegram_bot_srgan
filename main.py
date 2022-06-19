

import telebot
import requests
from srgan.inference import main as srgan_inf
from argparse import Namespace

API_TOKEN = "5456722168:AAFdPg-o6RPk4TJOrSBTVUs6lKlU5wKmjrM"




bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Just send me a photo and get the better one!")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, "That's not a photo!")

@bot.message_handler(content_types=['photo'])
def handle_docs_audio(message):
	# download and save img
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open("./lr/img.png","wb") as new_file:
        new_file.write(downloaded_file)

    srgan_args = Namespace(
        inputs_path= "./lr/img.png",
        output_path= "./sr/img.png",
        weights_path= "./srgan/weights/SRGAN_x4-ImageNet-c71a4860.pth.tar"
    )

    srgan_inf(srgan_args)
    # send image
    chat_id = message.from_user.id
    photo = open("./sr/img.png", "rb")
    bot.send_photo(chat_id, photo)

bot.infinity_polling()
































































































###
