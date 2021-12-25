import time
import re
regex = "^[A-Za-z0-9.-_]+$"
pattern = re.compile(regex)
pixel_r = "([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])"
rgb_pattern = re.compile(f"^{pixel_r},{pixel_r},{pixel_r}$")

def exec_command(event, db, pixels):
    ev_extra = event[2]
    cmd = ev_extra['command'].lower()
    msg = ev_extra['message'].lower()

    # mod / broadcaster only commands
    if ev_extra['flags']['mod'] or ev_extra['flags']['broadcaster']:
        if cmd == 'ac' or cmd == 'addcommand':
            split_msg = msg.split()
            if len(split_msg) == 2:
                if pattern.match(split_msg[0]) and pattern.match(split_msg[1]):
                    res = db.query(f"SELECT * FROM COMMANDS WHERE command = '{split_msg[0]}'")
                    if len(res):
                        pixels.show("ghost.png", [(255,255,255)]*124)
                    if len(res) == 0:
                        sql = "INSERT INTO COMMANDS (command, pic_name) VALUES " + \
                        f"('{split_msg[0]}', '{split_msg[1]}')"
                        db.query(sql)
        if cmd == 'dc' or cmd == 'deletecommand':
            if len(msg.split()) == 1:
                if pattern.match(msg):
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
            print(res)
            if len(res) > 0:
                r,g,b = 255,0,0
                strip_color = db.get_evar(db.DEF_STRIP)
                if rgb_pattern.match(strip_color):
                    r,g,b = map(int, strip_color.split(","))
                
                strip = []
                for z in range(124):
                    if z <= 23:
                        strip.append((200,200,200))
                    else:
                        strip.append((r,g,b))

                for x in res:
                    pixels.show(x[1], strip)
                    time.sleep(0.5)
        if cmd == 'setdefmatrix':
            if len(msg.split()) == 1:
                if pattern.match(msg):
                    res = db.query(f"SELECT * FROM COMMANDS WHERE command = '{msg}'")
                    if len(res) > 0:
                        print(res[0][1])
                        print(res[0][1])
                        print(res[0][1])
                        db.set_evar(db.CURR_MAT, "")
                        db.set_evar(db.DEF_MAT, res[0][1])
                        pixels.show_image(res[0][1])
                        pixels.keep_strip()
        if cmd == 'setdefstrip':
            if len(msg.split()) == 1:
                if rgb_pattern.match(msg):
                    db.set_evar(db.CURR_STRIP, "")
                    db.set_evar(db.DEF_STRIP, msg)

        hats = {
            'mariohat': ("m.png", "255,0,0"),
            'wariohat': ("w.png", "200,200,0"),
            'luigihat': ("l.png", "0,255,0"),
            'waluigihat': ("lr.png", "75,0,130"),
            'cheppyhat': ("c.png", "255,89,0"),
            'forthhat': ("f.png", "0,0,255"),
            'forthwindhat': ("f.png", "0,0,255"),
            "jjhat": ("jj.png", "255,0,0")
        }

        if cmd in hats:
            db.set_evar(db.DEF_MAT, hats[cmd][0])
            db.set_evar(db.DEF_STRIP, hats[cmd][1])

    if pattern.match(cmd):
        res = db.query(f"SELECT * FROM COMMANDS WHERE command = '{cmd}'")
        if len(res) > 0:

            r,g,b = 255,0,0
            strip_color = db.get_evar(db.DEF_STRIP)
            if rgb_pattern.match(strip_color):
                r,g,b = map(int, strip_color.split(","))
            
            strip = []
            for x in range(124):
                if x <= 23:
                    strip.append((200,200,200))
                else:
                    strip.append((r,g,b))

            print(cmd)
            
            pixels.show(res[0][1], strip)

            db.set_evar(db.CURR_MAT, res[0][1])

            time.sleep(4)
