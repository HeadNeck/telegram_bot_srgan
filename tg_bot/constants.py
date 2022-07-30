

import os
from dotenv import load_dotenv




load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')

MODEL_NAMES = ['sr_gan',
               'swinir']

DIRECTORY_LR = 'lr'
DIRECTORY_SR = 'sr'

BOT_MSGS={
    "model_menu":"Choose a model",
    "photo_request":"Send photo please (please choose a photo smaller than 150x150)",
    "too_large_photo":"The bot runs on the free heroku server and has very little RAM. Please choose a photo smaller than 150x150",
    "request_to_wait":"Please wait until algorythm finish treir work",
    "heroku_warning":"The bot runs on the free heroku server and has very little RAM. The process may take several minutes.",
    "result_congrats":"Here your super photo!",
}
