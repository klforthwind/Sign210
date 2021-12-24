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
        if cmd == 'ac':
            split_msg = msg.split()
            if len(split_msg) == 2:
                if pattern.match(split_msg[0]) and pattern.match(split_msg[1]):
                    res = db.query(f"SELECT * FROM COMMANDS WHERE command = '{split_msg[0]}'")
                    if len(res) == 0:
                        sql = "INSERT INTO COMMANDS (command, pic_name) VALUES " + \
                        f"('{split_msg[0]}', '{split_msg[1]}')"
                        db.query(sql)
        if cmd == 'dc':
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
            if len(res) > 0:
                for x in res:
                    pixels.show_image(x[1])
                    pixels.keep_strip()
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
                    print("YIKE")
                    db.set_evar(db.CURR_STRIP, "")
                    db.set_evar(db.DEF_STRIP, msg)

        if cmd == 'mariohat':
            db.set_evar(db.DEF_MAT, "m.png")
            db.set_evar(db.DEF_STRIP, "255,0,0")
        if cmd == 'wariohat':
            db.set_evar(db.DEF_MAT, "w.png")
            db.set_evar(db.DEF_STRIP, "200,200,0")
        if cmd == 'luigihat':
            db.set_evar(db.DEF_MAT, "l.png")
            db.set_evar(db.DEF_STRIP, "0,255,0")
        if cmd == 'waluigihat':
            db.set_evar(db.DEF_MAT, "lr.png")
            db.set_evar(db.DEF_STRIP, "75,0,130")
        if cmd == 'cheppyhat':
            db.set_evar(db.DEF_MAT, "c.png")
            db.set_evar(db.DEF_STRIP, "255,89,0")
        if cmd == 'forthhat' or cmd == 'forthwindhat':
            db.set_evar(db.DEF_MAT, "f.png")
            db.set_evar(db.DEF_STRIP, "0,0,255")
        if cmd == 'jjhat':
            db.set_evar(db.DEF_MAT, "jj.png")
            db.set_evar(db.DEF_STRIP, "255,0,0")

    if pattern.match(cmd):
        res = db.query(f"SELECT * FROM COMMANDS WHERE command = '{cmd}'")
        if len(res) > 0:
            pixels.show_image(res[0][1])
            pixels.keep_strip()
            db.set_evar(db.CURR_MAT, res[0][1])

            time.sleep(4)
