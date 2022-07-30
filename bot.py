

import os
import asyncio
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, types
from datetime import datetime
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from constants import API_TOKEN, BOT_MSGS
from keyboards import choose_model_kb, restart_kb
from aiogram.types import ReplyKeyboardRemove

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())




class FSMUser(StatesGroup):
    model_menu = State()
    sr_gan_wait_photo = State()
    swinir_wait_photo = State()


@dp.message_handler(commands=['start'], state=None)
async def load_models_menu(message: types.Message):
    await FSMUser.model_menu.set()
    await message.reply(BOT_MSGS["model_menu"],
                        reply_markup=choose_model_kb)

@dp.message_handler(commands=['sr_gan'], state=FSMUser.model_menu)
async def load_models_menu(message: types.Message, state: FSMContext):
    await FSMUser.sr_gan_wait_photo.set()
    await message.reply(BOT_MSGS["photo_request"],
                        reply_markup=ReplyKeyboardRemove())

@dp.message_handler(commands=['swinir'], state=FSMUser.model_menu)
async def load_models_menu(message: types.Message, state: FSMContext):
    await FSMUser.swinir_wait_photo.set()
    await message.reply(BOT_MSGS["photo_request"],
                        reply_markup=ReplyKeyboardRemove())

async def work_with_model(model_name, message, state):
    chat_id = message.from_user.id
    send_time = datetime.now().strftime("%d_%b_%Y_%H_%M_%S_%f")
    print(message.photo[-1])
    width = message.photo[-1]["width"]
    height = message.photo[-1]["height"]
    if ((width>150) or (height>150)):
        await message.answer(BOT_MSGS["too_large_photo"])
        await message.answer(BOT_MSGS["photo_request"])
    else:
        # download and save img
        await (message.photo[-1]
                      .download(os.path.join("lr",
                                             model_name,
                                             f"{chat_id}_{send_time}_img.png"),
                                make_dirs=False))
        await message.reply(BOT_MSGS["request_to_wait"])
        await message.answer(BOT_MSGS["heroku_warning"])
        # send image
        while True:
        	try:
        		await bot.send_photo(chat_id=chat_id,
                                     photo=open(os.path.join("sr",
                                        f"{chat_id}_{send_time}_img.png"), "rb")
                                    )
        		break
        	except:
        		await asyncio.sleep(1)
        await message.answer(BOT_MSGS["result_congrats"],
                             reply_markup=restart_kb)
        os.remove(os.path.join("sr",f"{chat_id}_{send_time}_img.png"))
        await state.finish()

@dp.message_handler(content_types=['photo'], state=FSMUser.sr_gan_wait_photo)
async def save_photo(message: types.Message, state: FSMContext):
    await work_with_model('sr_gan', message, state)

@dp.message_handler(content_types=['photo'], state=FSMUser.swinir_wait_photo)
async def save_photo(message: types.Message, state: FSMContext):
    await work_with_model('swinir', message, state)
