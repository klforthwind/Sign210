# import git
import os

while True:
    try:
        # g = git.Git('.')
        # g.pull('origin','main')
        os.system("sudo git pull")

        # Run python files using sudo - neopixel lights require sudo
        os.system("sudo python3 main.py")
    except:
        pass
