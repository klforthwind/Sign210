from downloader import *
import os

class Packager():

    def __init__(self):
        self.downloader = Downloader()

    def install_files(self):
        # twitch api handler
        # self.downloader.download("twitch_api.py")

        # main events / lights handler
        # self.downloader.download("table_handler.py")
        # self.downloader.download("show_functions.py")
        # self.downloader.download("extra_funcs.py")
        # self.downloader.download("command.py")
        # self.downloader.download("db_conn.py")
        # self.downloader.download("lights.py")
        # self.downloader.download("show.py")
        # self.downloader.download("main.py")


        # images - directory nonexistent
        # os.system("mkdir imgs/rick")
        # for x in range(21):
        #     self.downloader.download_img(f"imgs/rick/{x}.png")

        # os.system("mkdir imgs/star")
        # self.downloader.download_img("imgs/star/star1.png")
        # self.downloader.download_img("imgs/star/star2.png")
        # self.downloader.download_img("imgs/star/star3.png")
        # self.downloader.download_img("imgs/star/star4.png")
        # self.downloader.download_img("imgs/star/star5.png")

        # self.downloader.download_img("imgs/bits.png")
        # self.downloader.download_img("imgs/bluesus.png")
        # self.downloader.download_img("imgs/c.png")
        # self.downloader.download_img("imgs/celeste.png")
        # self.downloader.download_img("imgs/craftyjj.png")
        # self.downloader.download_img("imgs/d.png")
        # self.downloader.download_img("imgs/emcot.png")
        # self.downloader.download_img("imgs/f.png")
        # self.downloader.download_img("imgs/follow.png")
        # self.downloader.download_img("imgs/frog.png")
        # self.downloader.download_img("imgs/gartic.png")
        # self.downloader.download_img("imgs/ghost.png")
        # self.downloader.download_img("imgs/golfball210.png")
        # self.downloader.download_img("imgs/hearthstone.png")
        # self.downloader.download_img("imgs/jj.png")
        # self.downloader.download_img("imgs/justinirl.png")
        # self.downloader.download_img("imgs/kaeris.png")
        # self.downloader.download_img("imgs/l.png")
        # self.downloader.download_img("imgs/lr.png")
        # self.downloader.download_img("imgs/m.png")
        # self.downloader.download_img("imgs/mariograss.png")
        # self.downloader.download_img("imgs/mcpick.png")
        # self.downloader.download_img("imgs/micro_mage.png")
        # self.downloader.download_img("imgs/panda.png")
        # self.downloader.download_img("imgs/pepsi.png")
        # self.downloader.download_img("imgs/pokeball.png")
        # self.downloader.download_img("imgs/prime.png")
        # self.downloader.download_img("imgs/raid.png")
        # self.downloader.download_img("imgs/redbluedot.png")
        # self.downloader.download_img("imgs/redsus.png")
        # self.downloader.download_img("imgs/richandcheesy.png")
        # self.downloader.download_img("imgs/rupee.png")
        # self.downloader.download_img("imgs/silverdown.png")
        # self.downloader.download_img("imgs/star.png")
        # self.downloader.download_img("imgs/subnautica.png")
        # self.downloader.download_img("imgs/terminal.png")
        # self.downloader.download_img("imgs/tetris.png")
        # self.downloader.download_img("imgs/triforce.png")
        # self.downloader.download_img("imgs/uhc.png")
        # self.downloader.download_img("imgs/valheim.png")
        # self.downloader.download_img("imgs/w.png")
        pass

    def run(self):
        os.system(f"sudo python3 main.py")

packager = Packager()
packager.install_files()
packager.run()
