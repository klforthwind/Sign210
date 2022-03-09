# pip3 install gitpython
import git
import os

repo = git.Repo('../')
repo.remotes.origin.pull()

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
        os.system("sudo python3 main.py")
    except:
        # expecting errors on new updates - don't want program to crash
        pass
