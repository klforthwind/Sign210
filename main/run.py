# pip3 install gitpython
from db_conn import *
import git
import os

LATEST_PY = "packager.py"

downloader = Downloader()
repo = git.Repo('https://github.com/klforthwind/Sign210')

try:
    db = DBConn()
    db.connect()

    db.reset_config()

    db.disconnect()
except:
    pass

while True:
    try:
        repo.remotes.origin.pull()

        # run python files using sudo - neopixel lights require sudo
        os.system(f"sudo python3 {LATEST_PY}")
    except:
        # expecting errors on new updates - don't want program to crash
        pass
