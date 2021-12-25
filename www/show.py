# sudo apt install numpy-python
from show_functions import *
from extra_funcs import *
from command import *

class Show():

    def __init__(self):
        self.functions = {
            "SUB": self.run_sub,
            "RESUB": self.run_resub,
            "GIFTSUB": self.run_giftsub,
            "MYSTERYSUB": self.run_mysterysub,
            "CONTINUESUB": self.run_continuesub,
            "GAMECHANGE": self.run_gamechange,
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
        curr_strip = db.get_evar(db.CURR_STRIP)
        default_strip = db.get_evar(db.DEF_STRIP)

        curr_matrix = db.get_evar(db.CURR_MAT)
        default_matrix = db.get_evar(db.DEF_MAT)

        changed_matrix = curr_matrix != default_matrix
        changed_strip = curr_strip != default_strip

        if changed_matrix or changed_strip:
            db.set_evar(db.CURR_MAT, default_matrix)
            db.set_evar(db.CURR_STRIP, default_strip)

            strip = get_strip(db)
            pixels.show(default_matrix, strip)

    def run_raid(self, event, db, pixels):
        animate_raid(event, db, pixels)

    def run_gamechange(self, event, db, pixels):
        show_game(db, pixels, event[2], 8)
    
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
        cmd = event[2]['command'].lower()
        msg = event[2]['message'].upper()

        if cmd == "mod":
            if msg in self.functions:
                self.functions[msg](event, db, pixels)

        exec_command(event, db, pixels)
