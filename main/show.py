# sudo apt install numpy-python
from show_functions import *
from extra_funcs import *
from command import *
import json
import subprocess

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
        """Run function depending on event."""
        if not event:
            self.run_default(event, db, pixels)
            return
        
        ev_type = event[1]
        if ev_type in self.functions:
            self.functions[ev_type](list(event), db, pixels)
            set_default(db, pixels)

    def run_default(self, event, db, pixels):
        """Sets hat lights back to default, setting current variables to default variables."""
        default_strip = db.get_evar(db.DEF_STRIP)
        default_matrix = db.get_evar(db.DEF_MAT)

        changed_matrix = db.get_evar(db.CURR_MAT) != default_matrix
        changed_strip = db.get_evar(db.CURR_STRIP) != default_strip

        if changed_matrix or changed_strip:
            db.set_evar(db.CURR_MAT, default_matrix)
            db.set_evar(db.CURR_STRIP, default_strip)

            strip = get_strip(db)
            pixels.show(default_matrix, strip)
            subprocess.run(["/home/justin/test.php", str(strip)]) 

    def run_raid(self, event, db, pixels):
        animate_raid(event, db, pixels)

    def run_gamechange(self, event, db, pixels):
        show_game(db, pixels, event[3], 8)
    
    def run_follow(self, event, db, pixels):
        pulse(db, pixels, "follow.png", [14,2,36], [153,51,255], 8)
    
    def run_mysterysub(self, event, db, pixels):
        pulse(db, pixels, "ghost.png", [10,10,10], [200,200,200], 10)

    def run_cheer(self, event, db, pixels):
        cheer(event, db, pixels)

    def run_sub(self, event, db, pixels):
        slow_rainbow(event, db, pixels)
    
    def run_resub(self, event, db, pixels):
        slow_rainbow(event, db, pixels)
    
    def run_giftsub(self, event, db, pixels):
        fast_rainbow(event, db, pixels)

    def run_continuesub(self, event, db, pixels):
        slow_rainbow_shift(event, db, pixels)
    
    def run_command(self, event, db, pixels):
        """Runs mod-triggered events (bits, subs, etc.) and then calls exec_command for other commands."""
        cmd = event[2].lower()
        msg = event[3].upper()
        
        flags = event[4]['flags']
        mod_status = flags['mod'] or flags['broadcaster']

        if cmd == "mod" and mod_status:
            if msg in self.functions:
                self.functions[msg](event, db, pixels)

        exec_command(event, db, pixels)
