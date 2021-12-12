# pip3 install python-dotenv
from dotenv import load_dotenv
from os.path import exists
import os

import board
import neopixel
from PIL import Image
from adafruit_pixel_framebuf import PixelFramebuffer


while True:
    
    # make sure .env exists
    if not exists(".env"):
        os.system(f"curl https://www.klforthwind.com/sign210/.env > .env")
    load_dotenv()

    NEW_PYTHON = os.getenv('PROJECT_UPDATES')
    try:
        os.system(f"curl {NEW_PYTHON} > new.py")
        x = os.popen('diff curr.py new.py').read()
        if len(x) != 0:
            os.system(f"cp new.py curr.py")

        os.system("python3 new.py")
        # os.system("sudo python3 new.py")
    except:
        pass