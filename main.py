

import os
import requests
import asyncio
import threading
from utils import create_dir, clean_folders
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, executor, types
from datetime import datetime
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from model_loops import sr_gan_loop, swinir_loop
from constants import API_TOKEN, MODEL_NAMES, DIRECTORY_LR, DIRECTORY_SR
from keyboards import choose_model_kb
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
    await message.reply("Choose a model", reply_markup=choose_model_kb)

@dp.message_handler(commands=['sr_gan'], state=FSMUser.model_menu)
async def load_models_menu(message: types.Message, state: FSMContext):
    await FSMUser.sr_gan_wait_photo.set()
    await message.reply("Send photo please", reply_markup=ReplyKeyboardRemove())

@dp.message_handler(commands=['swinir'], state=FSMUser.model_menu)
async def load_models_menu(message: types.Message, state: FSMContext):
    await FSMUser.swinir_wait_photo.set()
    await message.reply("Send photo please", reply_markup=ReplyKeyboardRemove())

async def work_with_model(model_name, message, state):
    chat_id = message.from_user.id
    send_time = datetime.now().strftime("%d_%b_%Y_%H_%M_%S_%f")
    # download and save img
    await (message.photo[-1]
                  .download(os.path.join("lr",
                                f"{model_name}/{chat_id}_{send_time}_img.png"),
                            make_dirs=False))
    await message.reply("Please wait until algorythm finish treir work")
    # send image
    while True:
    	try:
    		await bot.send_photo(chat_id=chat_id,
                                 photo=open(os.path.join("sr",
                                    f"{chat_id}_{send_time}_img.png"), "rb")
                                )
    		break
    	except:
    		print("Wait for image")
    		await asyncio.sleep(1)
    await message.answer("Here your super photo!")
    os.remove(os.path.join("sr",f"{chat_id}_{send_time}_img.png"))
    await state.finish()

@dp.message_handler(content_types=['photo'], state=FSMUser.sr_gan_wait_photo)
async def save_photo(message: types.Message, state: FSMContext):
    await work_with_model('sr_gan', message, state)

@dp.message_handler(content_types=['photo'], state=FSMUser.swinir_wait_photo)
async def save_photo(message: types.Message, state: FSMContext):
    await work_with_model('swinir', message, state)




if __name__ == '__main__':
    models_dirs = [os.path.join(DIRECTORY_LR, model_name)
                        for model_name in MODEL_NAMES]
    require_dirs = [
                    DIRECTORY_SR,
                    DIRECTORY_LR
                   ]
    require_dirs.extend(models_dirs)
    create_dir(require_dirs)
    clean_folders(models_dirs)

    sr_gan_loop = threading.Thread(target=sr_gan_loop)
    swinir_loop = threading.Thread(target=swinir_loop)
    sr_gan_loop.start()
    swinir_loop.start()

    executor.start_polling(dp, skip_updates=True)



































































































###
