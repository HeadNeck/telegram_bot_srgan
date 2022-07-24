

import os
from dotenv import load_dotenv




load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')

MODEL_NAMES = ['sr_gan',
               'swinir']

DIRECTORY_LR = 'lr'
DIRECTORY_SR = 'sr'
