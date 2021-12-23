from downloader import *
import os

class Packager():

    def __init__(self):
        self.downloader = Downloader()
    
    def install_files(self):
        # self.downloader.download("table_handler.py")
        self.downloader.download("twitch_api.py")
        self.downloader.download("db_conn.py")
        # self.downloader.download("lights.py")
        self.downloader.download("show.py")
        self.downloader.download("main.py")
        # self.downloader.download_img("imgs/bits.png")
        # self.downloader.download_img("imgs/bluesus.png")
        # self.downloader.download_img("imgs/celeste.png")
        # self.downloader.download_img("imgs/CraftyJJ.png")
        # self.downloader.download_img("imgs/emcot.png")
        # self.downloader.download_img("imgs/follow.png")
        # self.downloader.download_img("imgs/frog.png")
        # self.downloader.download_img("imgs/ghost.png")
        # self.downloader.download_img("imgs/Golfball210.png")
        # self.downloader.download_img("imgs/JustinIRL.png")
        # self.downloader.download_img("imgs/L.png")
        # self.downloader.download_img("imgs/LR.png")
        # self.downloader.download_img("imgs/M.png")
        # self.downloader.download_img("imgs/MarioGrass.png")
        # self.downloader.download_img("imgs/micro_mage.png")
        # self.downloader.download_img("imgs/pokeball.png")
        # self.downloader.download_img("imgs/prime.png")
        # self.downloader.download_img("imgs/raid.png")
        # self.downloader.download_img("imgs/REDBLUEDOT.png")
        # self.downloader.download_img("imgs/redsus.png")
        # self.downloader.download_img("imgs/rupee.png")
        # self.downloader.download_img("imgs/terminal.png")
        # self.downloader.download_img("imgs/tetris.png")
        # self.downloader.download_img("imgs/uhc.png")
        # self.downloader.download_img("imgs/Valheim.png")
        # self.downloader.download_img("imgs/W.png")
        # self.downloader.download_img("imgs/gartic.png")
        print("DONE DOWNLOADING FILES")
        pass

    def run(self):
        os.system(f"sudo python3 main.py")

packager = Packager()
packager.install_files()
packager.run()
