import re

# try to prevent sql injections
msg_regex = "^[A-Za-z0-9,.-_ ]+$"
msg_pattern = re.compile(msg_regex)

# validates rgb patterns - ex: "255,0,30"
pixel_re = "([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])"
rgb_pattern = re.compile(f"^{pixel_re},{pixel_re},{pixel_re}$")

def valid_msg(msg):
    """Returns whether msg is valid. "", None, and file_names (micro_mage.png) are valid."""
    return msg == "" or msg == None or msg_pattern.match(msg)

def valid_rgb(msg):
    """Returns whether msg is in the format 'X,Y,Z' where X, Y, and Z are all 0-255."""
    return rgb_pattern.match(msg)

def get_strip_from_color(strip_color):
    """Returns valid 2-color strip (first 24 pixels are white), the rest are strip_color."""
    r,g,b = 255,0,0
    if rgb_pattern.match(strip_color):
        r,g,b = map(int, strip_color.split(","))
    
    if r==71 and g==45 and b==77:
        return [(50,0,0) if z <= 23 else (r,g,b) for z in range(124)]
    if r==100 and g==33 and b==0:
        return [(140,33,5) if z <= 23 else (r,g,b) for z in range(124)]

    return [(200,200,200) if z <= 23 else (r,g,b) for z in range(124)]

def get_strip(db):
    """Returns valid 2-color strip from DB default strip."""
    strip_color = db.get_evar(db.DEF_STRIP)
    return get_strip_from_color(strip_color)

def set_default(db, pixels):
    """Sets the strip and matrix to default stored DB values."""
    def_matrix = db.get_evar(db.DEF_MAT)
    strip = get_strip(db)

    pixels.show(def_matrix, strip)
