from datetime import datetime
from os.path import exists
from extra_funcs import *
import time
import os

def exec_command(event, db, pixels):
    ev_extra = event[4]
    cmd = event[2].lower()
    msg = event[3].lower()

    # mod / broadcaster only commands
    if ev_extra['flags']['mod'] or ev_extra['flags']['broadcaster']:
        if cmd == 'ac' or cmd == 'addcommand':
            split_msg = msg.split()
            if len(split_msg) == 2:
                if valid_msg(split_msg[0]) and valid_msg(split_msg[1]):
                    res = db.query(f"SELECT * FROM COMMANDS WHERE command = '{split_msg[0]}'")
                    if len(res) == 0 and exists(f"imgs/{split_msg[1]}"):
                        sql = "INSERT INTO COMMANDS (command, pic_name) VALUES " + \
                        f"('{split_msg[0]}', '{split_msg[1]}')"
                        db.query(sql)
        if cmd == 'dc' or cmd == 'deletecommand':
            if len(msg.split()) == 1:
                if valid_msg(msg):
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
                strip = get_strip(db)

                for x in res:
                    pixels.show(x[1], strip)
                    time.sleep(0.5)
        if cmd == 'setdefmatrix':
            if len(msg.split()) == 1:
                if valid_msg(msg):
                    res = db.query(f"SELECT * FROM COMMANDS WHERE command = '{msg}'")
                    if len(res) > 0:
                        img = res[0][1]
                        db.set_evar(db.CURR_MAT, img)
                        db.set_evar(db.DEF_MAT, img)
                        strip = get_strip(db)
                        pixels.show(img,strip)
        if cmd == 'setdefstrip':
            if len(msg.split()) == 1:
                if valid_rgb(msg):
                    db.set_evar(db.CURR_STRIP, "")
                    db.set_evar(db.DEF_STRIP, msg)
        if cmd == 'ep' or cmd == 'episode':
            db.set_evar(db.CURR_MAT, "")

            strip = get_strip(db)
            pixels.show(db.get_evar(db.DEF_MAT), strip)

            start = datetime.strptime('03/17/2020', '%m/%d/%Y')
            today = datetime.today()
            ep_num = (today - start).days + 1
            for x in range(7, -46, -1):
                pixels.matrix.fill(0x000000)
                pixels.matrix.text(f"EP. {ep_num}", x, (x//2)%2, int('0x%02x%02x%02x' % strip[120], 16))
                pixels.matrix.display()
                time.sleep(0.1)
            set_default(event, db, pixels)
        if cmd == 'temps':
            db.set_evar(db.CURR_MAT, "")

            strip = get_strip(db)
            pixels.show(db.get_evar(db.DEF_MAT), strip)

            temp = os.popen("vcgencmd measure_temp").read().split("=")[1]
            print(temp)
            for x in range(7, -46, -1):
                pixels.matrix.fill(0x000000)
                pixels.matrix.text(f"{temp}", x, 1, int('0x%02x%02x%02x' % strip[120], 16))
                pixels.matrix.display()
                time.sleep(0.1)
            set_default(event, db, pixels)


        hats = {
            'mariohat': ("m.png", "255,0,0"),
            'wariohat': ("w.png", "200,200,0"),
            'luigihat': ("l.png", "0,255,0"),
            'waluigihat': ("lr.png", "75,0,130"),
            'cheppyhat': ("c.png", "255,89,0"),
            'forthhat': ("f.png", "0,0,255"),
            'forthwindhat': ("f.png", "0,0,255"),
            "jjhat": ("jj.png", "255,0,0"),
            "silverhat": ("silverdown.png", "60,60,60"),
            "cheesyhat": ("richandcheesy.png", "234,234,20"),
            "danhat": ("d.png", "140,33,0")
        }

        if cmd in hats:
            db.set_evar(db.DEF_MAT, hats[cmd][0])
            db.set_evar(db.DEF_STRIP, hats[cmd][1])

    if valid_msg(cmd):
        res = db.query(f"SELECT * FROM COMMANDS WHERE command = '{cmd}'")
        if len(res) > 0:

            strip = get_strip(db)

            pixels.show(res[0][1], strip)

            db.set_evar(db.CURR_MAT, res[0][1])

            time.sleep(4)
