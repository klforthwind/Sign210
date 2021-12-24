# sudo apt install numpy-python
from show_functions import *
from random import randint
import time
import re
import os

class Show():
    regex = "^[A-Za-z0-9.-_]+$"

    def __init__(self):
        self.pattern = re.compile(self.regex)
        self.functions = {
            "SUB": self.run_sub,
            "RESUB": self.run_resub,
            "GIFTSUB": self.run_giftsub,
            "MYSTERYSUB": self.run_mysterysub,
            "CONTINUESUB": self.run_continuesub,
            "GAMECHANGE": self.run_gamechange,
            "CUSTOMREWARD": self.run_reward,
            "JOINREALM": self.run_realm,
            "NORMALCHAT": self.run_chat,
            "COMMAND": self.run_command,
            "FOLLOW": self.run_follow,
            "CHEER": self.run_cheer,
            "RAID": self.run_raid
        }

    def run(self, event, db, pixels):
        if not event:
            self.run_default(event, db, pixels)
            return
        
        # event = (id, ev_type, ev_extra, importance)
        ev_type = event[1]
        if ev_type in self.functions:
            self.functions[ev_type](event, db, pixels)

    def run_default(self, event, db, pixels):
        default_strip = db.get_evar(db.DEF_STRIP)

        hat_color = {
            "mariohat":(255,0,0),
            "luigihat":(0,255,0),
            "waluigihat":(75,0,130),
            "wariohat":(200,200,0)
        }

        strip = []
        for x in range(124):
            if x <= 23:
                strip.append((200,200,200))
            else:
                strip.append(hat_color[default_strip])

        pixels.set_strip(strip)
        pixels.keep_strip()

        curr_matrix = db.get_evar(db.CURR_MAT)
        default_matrix = db.get_evar(db.DEF_MAT)
        
        if curr_matrix != default_matrix:
            db.set_evar(db.CURR_MAT, default_matrix)
            pixels.show_image(default_matrix)
            pixels.keep_strip()

    def run_raid(self, event, db, pixels):
        # if event[2]['flags']['vip'] or event[2]['flags']['broadcaster']:
        if False:
            snake(event, db, pixels)
        else:
            loading_raid(event, db, pixels)

    def run_gamechange(self, event, db, pixels):
        show_game(event[2], pixels, 8)
    
    def run_follow(self, event, db, pixels):
        pulse(db, pixels, "follow.png", [14,2,36], [153,51,255], 8)
    
    def run_mysterysub(self, event, db, pixels):
        pulse(db, pixels, "ghost.png", [10,10,10], [200,200,200], 10)

    def run_cheer(self, event, db, pixels):
        cheer(event, db, pixels)

    def run_sub(self, event, db, pixels):
        slow_rainbow(event, db, pixels)
    
    def run_resub(self, event, db, pixels):
        self.run_sub(event, db, pixels)
    
    def run_giftsub(self, event, db, pixels):
        fast_rainbow(event, db, pixels)

    def run_continuesub(self, event, db, pixels):
        slow_rainbow_shift(event, db, pixels)
    
    def run_command(self, event, db, pixels):
        ev_extra = event[2]
        cmd = ev_extra['command'].lower()
        msg = ev_extra['message'].lower()

        # mod / broadcaster only commands
        if ev_extra['flags']['mod'] or ev_extra['flags']['broadcaster']:
            if cmd == 'ac':
                split_msg = msg.split()
                if len(split_msg) == 2:
                    if self.pattern.match(split_msg[0]) and self.pattern.match(split_msg[1]):
                        res = db.query(f"SELECT * FROM COMMANDS WHERE command = '{split_msg[0]}'")
                        if len(res) == 0:
                            sql = "INSERT INTO COMMANDS (command, pic_name) VALUES " + \
                            f"('{split_msg[0]}', '{split_msg[1]}')"
                            db.query(sql)
            if cmd == 'dc':
                if len(msg.split()) == 1:
                    if self.pattern.match(msg):
                        db.execute(f"DELETE FROM COMMANDS WHERE command = '{msg}'")
            if cmd == 'reboot':
                db.reset_config()
                os.system("sudo shutdown -r now")
            if cmd == 'shutdown':
                db.reset_config()
                os.system("sudo shutdown -h now")
            if cmd == 'showall':
                db.set_evar(db.CURR_MAT, "")
                res = db.query(f"SELECT * FROM COMMANDS ORDER BY command")
                if len(res) > 0:
                    for x in res:
                        pixels.show_image(x[1])
                        pixels.keep_strip()
                        time.sleep(0.5)
            if cmd == 'setdefault':
                if len(msg.split()) == 1:
                    if self.pattern.match(msg):
                        res = db.query(f"SELECT * FROM COMMANDS WHERE command = '{msg}'")
                        if len(res) > 0:
                            print(res[0][1])
                            print(res[0][1])
                            print(res[0][1])
                            db.set_evar(db.CURR_MAT, "")
                            db.set_evar(db.DEF_MAT, res[0][1])
                            pixels.show_image(res[0][1])
                            pixels.keep_strip()

            if cmd == 'mariohat':
                db.set_evar(db.DEF_MAT, "m.png")
                db.set_evar(db.DEF_STRIP, "mariohat")
            if cmd == 'wariohat':
                db.set_evar(db.DEF_MAT, "w.png")
                db.set_evar(db.DEF_STRIP, "wariohat")
            if cmd == 'luigihat':
                db.set_evar(db.DEF_MAT, "l.png")
                db.set_evar(db.DEF_STRIP, "luigihat")
            if cmd == 'waluigihat':
                db.set_evar(db.DEF_MAT, "lr.png")
                db.set_evar(db.DEF_STRIP, "waluigihat")

        if self.pattern.match(cmd):
            res = db.query(f"SELECT * FROM COMMANDS WHERE command = '{cmd}'")
            if len(res) > 0:
                pixels.show_image(res[0][1])
                pixels.keep_strip()
                db.set_evar(db.CURR_MAT, res[0][1])

                time.sleep(4)

        if cmd == "cheer":
            self.run_cheer(event, db, pixels)
        if cmd == "raidtime":
            self.run_raid(event, db, pixels)
        if cmd == "sub":
            self.run_sub(event, db, pixels)
        if cmd == "myst":
            self.run_mysterysub(event, db, pixels)
        if cmd == "foll":
            self.run_follow(event,db,pixels)
        if cmd == "gifty":
            self.run_giftsub(event,db,pixels)
        if cmd == "continue":
            self.run_continuesub(event,db,pixels)
        

    def run_realm(self, event, db, pixels):
        pass

    def run_reward(self, event, db, pixels):
        pass

    def run_chat(self, event, db, pixels):
        pass
