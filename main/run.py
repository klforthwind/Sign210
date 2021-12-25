from downloader import *
from db_conn import *
import os

LATEST_PY = "packager.py"

downloader = Downloader()

db = DBConn()
db.connect()

db.set_evar(db.DEF_STRIP, "255,0,0")
db.set_evar(db.CURR_STRIP, "")

db.set_evar(db.DEF_MAT, "jj.png")
db.set_evar(db.CURR_MAT, "")

db.disconnect()

while True:
    try:
        downloader.download(LATEST_PY)

        # run python files using sudo - neopixel lights require sudo
        os.system(f"sudo python3 {LATEST_PY}")
    except:
        # expecting errors on new updates - don't want program to crash
        pass
