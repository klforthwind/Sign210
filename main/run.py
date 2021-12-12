# pip3 install python-dotenv
from dotenv import load_dotenv
from os.path import exists
from os.path import getsize
import os

if not exists(".env"):
    raise Exception(".env file not found")

load_dotenv()
PY_FILE_DIR = os.getenv('PY_FILE_DIR')
LATEST_PY = os.getenv('LATEST_PY')
CURR_PY = os.getenv('CURR_PY')

while True:
    
    try:
        # curl latest python from server
        os.system(f"curl {PY_FILE_DIR}/packager.py > {LATEST_PY}")

        # verify curr_py exists (in order to diff it)
        if not exists(CURR_PY):
            os.system(f"touch {CURR_PY}")

        # obtain changes between latest python and current python
        changes = os.popen(f"diff {CURR_PY} {LATEST_PY}").read()
        
        # update on change and latest_py isn't 404 (178bytes)
        if len(changes) != 0 and getsize(LATEST_PY) > 210:
            os.system(f"cp {LATEST_PY} {CURR_PY}")

        # run python files using sudo - neopixel lights require sudo
        os.system(f"sudo python3 {LATEST_PY}")
    except:
        # expecting errors on new updates - don't want program to crash
        pass
