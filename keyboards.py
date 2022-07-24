

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton




b1 = KeyboardButton('/sr_gan')
b2 = KeyboardButton('/swinir')

choose_model_kb = ReplyKeyboardMarkup(resize_keyboard=True)
(choose_model_kb.add(b1)
                .add(b2))
