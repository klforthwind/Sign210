import os

try:
    db = DBConn()
    db.connect()

    db.reset_config()

    db.disconnect()
except:
    pass

while True:
    try:
        os.system("git pull")

        # run python files using sudo - neopixel lights require sudo
        os.system("sudo python3 main.py")
    except:
        # expecting errors on new updates - don't want program to crash
        pass
