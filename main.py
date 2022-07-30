

import os
import threading
from bot import dp
from utils import create_dir, clean_folders
from aiogram import executor
from model_loops import sr_gan_loop, swinir_loop
from constants import MODEL_NAMES, DIRECTORY_LR, DIRECTORY_SR




def create_required_dirs():
    models_dirs = [os.path.join(DIRECTORY_LR, model_name)
                        for model_name in MODEL_NAMES]
    require_dirs = [
                    DIRECTORY_SR,
                    DIRECTORY_LR
                   ]
    require_dirs.extend(models_dirs)
    create_dir(require_dirs)
    clean_folders(models_dirs)


if __name__ == '__main__':
    create_required_dirs()

    sr_gan_loop = threading.Thread(target=sr_gan_loop)
    swinir_loop = threading.Thread(target=swinir_loop)
    sr_gan_loop.start()
    swinir_loop.start()

    executor.start_polling(dp, skip_updates=True)
