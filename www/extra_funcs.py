import re

# try to prevent sql injections
msg_regex = "^[A-Za-z0-9.-_]+$"
msg_pattern = re.compile(msg_regex)

# validates rgb patterns - ex: "255,0,30"
pixel_re = "([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])"
rgb_pattern = re.compile(f"^{pixel_re},{pixel_re},{pixel_re}$")

def valid_msg(msg):
    return msg == "" or msg_pattern.match(msg)

def valid_rgb(msg):
    return rgb_pattern.match(msg)

def get_strip(db):
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
    return strip

def set_default(event, db, pixels):
    def_matrix = db.get_evar(db.DEF_MAT)
    strip = get_strip(db)

    pixels.show(def_matrix, strip)
