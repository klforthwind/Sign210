from downloader import *

LATEST_PY = "packager.py"

downloader = Downloader()

while True:
    try:
        downloader.download(LATEST_PY)

        # run python files using sudo - neopixel lights require sudo
        os.system(f"sudo python3 {LATEST_PY}")
    except(error):
        # expecting errors on new updates - don't want program to crash
        pass
