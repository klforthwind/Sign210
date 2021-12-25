from downloader import *
from db_conn import *
import os

LATEST_PY = "packager.py"

downloader = Downloader()

try:
    db = DBConn()
    db.connect()

    db.reset_config()

    db.disconnect()
except:
    pass

while True:
    try:
        downloader.download(LATEST_PY)

        # run python files using sudo - neopixel lights require sudo
        os.system(f"sudo python3 {LATEST_PY}")
    except:
        # expecting errors on new updates - don't want program to crash
        pass
