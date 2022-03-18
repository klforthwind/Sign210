from db_conn import *
# import git
import os

db = DBConn()
db.connect()

db.reset_config()

db.disconnect()

while True:
    # g = git.Git('.')
    # g.pull('origin','main')
    os.system("sudo git pull")

    # Run python files using sudo - neopixel lights require sudo
    os.system("sudo python3 main.py")
