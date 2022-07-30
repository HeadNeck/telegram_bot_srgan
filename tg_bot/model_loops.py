

import os
from time import sleep
from srgan.inference import main as srgan_inf
from argparse import Namespace
from tg_bot.constants import DIRECTORY_LR, DIRECTORY_SR
from swinir.inference import main as swinir_inf




def swinir_loop(directory_lr = os.path.join(DIRECTORY_LR,"swinir"),
                directory_sr = DIRECTORY_SR):
    while True:
        try:
            for filename in os.listdir(directory_lr):
                 if filename.endswith(".png"):
                     input_path = os.path.join(directory_lr, filename)
                     weight_name = "001_classicalSR_DIV2K_s48w8_SwinIR-M_x4.pth"
                     args = Namespace(
                                      task = 'classical_sr',
                                      scale = 4,
                                      training_patch_size = 48,
                                      model_path = os.path.join("swinir",
                                                                "weights",
                                                                weight_name),
                                      path = input_path,
                                      output_path = os.path.join(directory_sr,
                                                                 filename),
                                      window_size = 16
                                      )
                     swinir_inf(args)
                     os.remove(input_path)
                 else:
                     pass
        except:
            sleep(3)

def sr_gan_loop(directory_lr = os.path.join(DIRECTORY_LR, "sr_gan"),
                directory_sr = DIRECTORY_SR):
    while True:
        try:
            for filename in os.listdir(directory_lr):
                 if filename.endswith(".png"):
                     input_path = os.path.join(directory_lr, filename)
                     weight_name = "SRGAN_x4-ImageNet-c71a4860.pth.tar"
                     srgan_args = Namespace(
                         inputs_path = input_path,
                         output_path = os.path.join(directory_sr, filename),
                         weights_path = os.path.join("srgan",
                                                     "weights",
                                                     weight_name)
                     )
                     srgan_inf(srgan_args)
                     os.remove(input_path)
                 else:
                     pass
        except:
            sleep(3)
