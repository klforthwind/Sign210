from datetime import datetime
from os.path import exists
from extra_funcs import *
import time
import os

def exec_command(event, db, pixels):
    """Executes command sent by Twitch User."""

    ev_extra = event[4]
    cmd = event[2].lower()
    msg = event[3].lower()

    flags = event[4]['flags']

    # Mod / broadcaster commands
    if flags['mod'] or flags['broadcaster']:
        if cmd in ['ac','addcommand']:
            split_msg = msg.split()
            if len(split_msg) == 2:
                if valid_msg(split_msg[0]) and valid_msg(split_msg[1]):
                    res = db.query(f"SELECT * FROM COMMANDS WHERE command = '{split_msg[0]}'")
                    if len(res) == 0 and exists(f"imgs/{split_msg[1]}"):
                        sql = "INSERT INTO COMMANDS (command, pic_name) VALUES " + \
                        f"('{split_msg[0]}', '{split_msg[1]}')"
                        db.execute(sql)
        elif cmd in ['dc','deletecommand']:
            if len(msg.split()) == 1 and valid_msg(msg):
                db.execute(f"DELETE FROM COMMANDS WHERE command = '{msg}'")
        elif cmd in ['reboot','restart']:
            db.reset_config()
            os.system("sudo shutdown -r now")
        elif cmd == 'shutdown':
            db.reset_config()
            os.system("sudo shutdown -h now")
        elif cmd == 'showall':
            db.set_evar(db.CURR_MAT, "")
            res = db.query(f"SELECT * FROM COMMANDS ORDER BY command")
            if len(res) > 0:
                strip = get_strip(db)

                for x in res:
                    pixels.show(x[1], strip)
                    time.sleep(0.5)
        elif cmd in ['setdefmatrix', 'sdm']:
            if len(msg.split()) == 1 and valid_msg(msg):
                res = db.query(f"SELECT * FROM COMMANDS WHERE command = '{msg}'")
                if len(res) > 0:
                    img = res[0][1]
                    db.set_evar(db.CURR_MAT, img)
                    db.set_evar(db.DEF_MAT, img)
                    strip = get_strip(db)
                    pixels.show(img,strip)
        elif cmd in ['setdefstrip', 'sds']:
            if len(msg.split()) == 1 and valid_rgb(msg):
                db.set_evar(db.CURR_STRIP, "")
                db.set_evar(db.DEF_STRIP, msg)
        elif cmd == 'happybirthday':
            db.set_evar(db.CURR_MAT, "")

            strip = get_strip(db)
            pixels.show(db.get_evar(db.DEF_MAT), strip)

            happybirthday = "Happy Birthday!!"
            for x in range(7, -150, -1):
                pixels.matrix.fill(0x000000)
                pixels.matrix.text(f"{happybirthday}", x, 1, int('0x%02x%02x%02x' % strip[120], 16))
                pixels.matrix.display()
                time.sleep(0.1)
            set_default(db, pixels)

        hats = {
            'mariohat': ("m.png", "255,0,0"),
            'wariohat': ("w.png", "200,200,0"),
            'luigihat': ("l.png", "0,255,0"),
            'waluigihat': ("lr.png", "75,0,130"),
            'cheppyhat': ("c.png", "255,89,0"),
            'forthhat': ("f.png", "0,0,255"),
            "jjhat": ("jj.png", "255,0,0"),
            "silverhat": ("silverdown.png", "60,60,60"),
            "weaselhat": ("coffee.png", "200,200,200"),
            "danhat": ("wwd.png", "120,33,0"),
            "fflhat": ("ffl.png", "0,255,0"),
            "dizhat": ("dizhat.png", "0,45,77"),
            "mokihat": ("jj_nft.png", "75,0,0"),
            "katahat": ("k.png", "221,3,207"),
            "goosehat": ("gus.png", "0,250,0"),
            "hobbshat": ("hobbs.png", "234,234,20"),
            "cassandrahat": ("snax.png", "0,0,60"),
            "blakehat": ("blake.png", "0,0,200"),
            "rbkhat": ("rootbeerking.png", "0,240,0"),
            "mokihat": ("craft_inc.png", "100,33,0"),
            "484hat": ("pac_ghost.png", "255,255,0"),
            "morguehat": ("skull.png", "0,181,207"),
            "rainbowhat": ("rainbowk.png", "253,182,40"),
            "gphat": ("gp.png", "0,181,255"),
            "charleshat": ("charles_star.png", "156,235,250"),
            "squroadhat": ("rick.png","0,0,250"),
            "b64hat": ("b64.png","250,0,0"),
			"madmanhat": ("madman.png","0,250,0"),
            "smbfanhat": ("smbfan.png","54,84,217"),
        }

        if cmd in hats:
            db.set_evar(db.DEF_MAT, hats[cmd][0])
            db.set_evar(db.DEF_STRIP, hats[cmd][1])

        if cmd == 'charleshat':
            strip = get_strip_from_color("156,235,250")
            DURATION = 4
            db.set_evar(db.CURR_MAT, "")
            j = 0
            end_time = time.time() + DURATION
            while time.time() < end_time:
                pixels.show(f"charles_star/star{(j//6)%12+1}.png", strip)
                time.sleep(0.0125)
                j+=2
        if cmd == 'squroadhat':
            strip = get_strip_from_color("0,0,250")
            DURATION = 8
            db.set_evar(db.CURR_MAT, "")
            j = 0
            end_time = time.time() + DURATION
            while time.time() < end_time:
                pixels.show(f"rick/{(j//6)%20+1}.png", strip)
                time.sleep(0.0125)
                j+=2
        if cmd == 'hats':
            db.set_evar(db.CURR_MAT, "")
            db.set_evar(db.CURR_STRIP, "")

            for h in hats:
                config = hats[h]
                strip = get_strip_from_color(config[1])
                pixels.show(config[0], strip)
                time.sleep(1)
    if cmd in ['ep', 'episode']:
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
        set_default(db, pixels)
    if cmd in ['cd', 'countdown']:
        db.set_evar(db.CURR_MAT, "")
        strip = get_strip(db)
        pixels.show(db.get_evar(db.DEF_MAT), strip)

        start = datetime.strptime('12/11/2022 23:59:00', '%m/%d/%Y %H:%M:%S')
        today = datetime.now()
        min_left = round((start - today).total_seconds() / 60)
        for x in range(7, -106, -1):
            pixels.matrix.fill(0x000000)
            pixels.matrix.text(f"Time Left: {min_left} mins", x, (x//2)%2, int('0x%02x%02x%02x' % strip[120], 16))
            pixels.matrix.display()
            time.sleep(0.1)
        set_default(db, pixels)
    if cmd in ['temps','tmp']:
        db.set_evar(db.CURR_MAT, "")

        strip = get_strip(db)
        pixels.show(db.get_evar(db.DEF_MAT), strip)

        temp = os.popen("vcgencmd measure_temp").read().split("=")[1]
        for x in range(7, -46, -1):
            pixels.matrix.fill(0x000000)
            pixels.matrix.text(f"{temp}", x, 1, int('0x%02x%02x%02x' % strip[120], 16))
            pixels.matrix.display()
            time.sleep(0.1)
        set_default(db, pixels)
    if cmd == 'lurk':
        db.set_evar(db.CURR_MAT, "")
        strip = get_strip(db)

        for x in range(9):
            pixels.show(f"lurk/{x}.png", strip)
            time.sleep(0.3)
        
        time.sleep(3)

        for x in range(8, -1, -1):
            pixels.show(f"lurk/{x}.png", strip)
            time.sleep(0.3)
    
    if cmd == 'wearhat':
        db.set_evar(db.CURR_MAT, "")
        strip = get_strip(db)

        for x in range(5):
            pixels.show(f"wearhat/{x}.png", strip)
            time.sleep(0.3)
        time.sleep(3)


    if valid_msg(cmd):
        res = db.query(f"SELECT command, pic_name FROM COMMANDS WHERE command = '{cmd}'")
        if len(res) > 0:
            strip = get_strip(db)

            pixels.show(res[0][1], strip)
            db.set_evar(db.CURR_MAT, res[0][1])

            time.sleep(4)
