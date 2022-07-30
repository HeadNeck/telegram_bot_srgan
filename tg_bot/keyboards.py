

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton




m1 = KeyboardButton('/sr_gan')
m2 = KeyboardButton('/swinir')

choose_model_kb = ReplyKeyboardMarkup(resize_keyboard=True)
(choose_model_kb.add(m1)
                .add(m2))

r1 = KeyboardButton('/start')
restart_kb = ReplyKeyboardMarkup(resize_keyboard=True)
restart_kb.add(r1)
