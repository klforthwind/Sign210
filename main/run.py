from db_conn import *
import git
import os

db = DBConn()
db.connect()

db.reset_config()

db.disconnect()

while True:
    try:
        g = git.Git('.')
        g.pull('origin','main')

        # Run python files using sudo - neopixel lights require sudo
        os.system("sudo python3 main.py")
    except:
        # Expecting errors on new updates - don't want program to crash
        pass
