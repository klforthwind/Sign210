# sudo apt install numpy-python OR
# sudo pip3 install numpy
from random import randint
from extra_funcs import *
import numpy as np
import time

def rick(event, db, pixels):
    """Loops Rick on the matrix and colors on the strip for 10 seconds"""
    DURATION = 10
    db.set_evar(db.CURR_MAT, "")
    j = 0
    end_time = time.time() + DURATION
    while time.time() < end_time:
        color = wheel(j & 255)
        pixels.show(f"rick/{(j//8)%21}.png", [color]*124)
        time.sleep(0.0125)
        j+=2

def loading_raid(event, db, pixels):
    """Loads hat with color, and then shows raid.png at end."""
    db.set_evar(db.CURR_MAT, "raid.png")
    strip_len = pixels.STRIP_LEN
    strip = get_strip(db)

    color = strip[123]

    white = (200,200,200)

    strip_len = 4
    endpx = 0
    pixels.color_all([(0,0,0)] * 188)

    ct = 0

    while endpx <= 126:
        newpx = 126
        while newpx > endpx:
            arr = []
            for x in range(124):
                if newpx + strip_len >= x >= newpx or x < endpx :
                    if ct < 6 or x <= 23:
                        arr.append(white)
                    else:
                        arr.append(color)
                else:
                    arr.append((0,0,0))
            
            pixels.color_strip(arr)
            
            newpx -= 3
        endpx += strip_len
        ct+=1
    
    pixels.show("raid.png", strip)
    time.sleep(2)

def animate_raid(event, db, pixels):
    """Runs loading_raid and then runs Rick if triggered by broadcaster or mod."""
    loading_raid(event, db, pixels)
    if event[4]['flags']['vip'] or event[4]['flags']['broadcaster'] or event[4]['flags']['moderator']:
        rick(event, db, pixels)

def pulse(db, pixels, image, rgb1_list, rgb2_list, run_time):
    """Shows image and pulse of colors using lerp function over time."""
    db.set_evar(db.CURR_MAT, "")
    low = np.array(rgb1_list)
    high = np.array(rgb2_list)
    lerp_colors(pixels, low, high, image, run_time)

def slow_rainbow(event, db, pixels):
    """Shows rotating mario star and strip changes rainbow colors."""
    DURATION = 10
    db.set_evar(db.CURR_MAT, "")
    j = 0
    end_time = time.time() + DURATION
    while time.time() < end_time:
        color = wheel(j & 255)
        pixels.show(f"star/star{(j//4)%5+1}.png", [color]*124)
        time.sleep(0.0125)
        j+=2

def fast_rainbow(event, db, pixels):
    """Shows rotating mario star and strip changes rainbow colors fast."""
    DURATION = 10
    db.set_evar(db.CURR_MAT, "")
    j = 0
    bri = 64    # brightness
    colors = [(0,0,bri),(bri,0,bri),(bri,0,0),(bri,bri,0),(0,bri,0),(bri,0,0),(bri,bri,bri)]

    end_time = time.time() + DURATION
    while time.time() < end_time:
        color = colors[(j%7)]
        pixels.show(f"star/star{(j//2)%5+1}.png", [color]*124)
        time.sleep(0.025)
        j+=1

def slow_rainbow_shift(event, db, pixels):
    """Shows rotating mario star and strip shifts (clockwise?) rainbow colors."""
    DURATION = 10
    db.set_evar(db.CURR_MAT, "")
    j = 0
    end_time = time.time() + DURATION
    while time.time() < end_time:
        strip = []
        for x in range(124):
            color = wheel((int(x * 255 / 124+j)%255))
            strip.append(color)
        pixels.show(f"star/star{(j//4)%5+1}.png", strip)
        time.sleep(0.025)
        j+=1

def show_game(db, pixels, game_title, wait_time):
    """Changes matrix to game_title for a certain amount of time."""

    db.set_evar(db.CURR_MAT, "")
    strip = get_strip(db)

    games = {
        "Minecraft": "mariograss.png",
        "Gartic Phone": "gartic.png",
        "Valheim": "valheim.png",
        "Golf": "golfball210.png",
        "Subnautica": "subnautica.png",
        "Satisfactory": "satisfactory.png",
        "Fall Guys": "fallguy.png",
        "Pokemon": "pokeball.png"
    }

    for game in games:
        if game in game_title:
            pixels.show(games[game], strip)
            time.sleep(wait_time)
            break

def cheer(event, db, pixels):
    """Shows bits picture on matrix and shifts purple, blue, and green around (clockwise?) the hat."""
    colors = [(153,51,255),(0,0,255),(0,255,0)]
    offset = 0

    db.set_evar(db.CURR_MAT, "bits.png")

    end_time = time.time() + 10
    while time.time() < end_time:
        offset += 1
        arr = []
        for x in range(124):
            arr.append(colors[((offset + x)// 3) % 3])
        
        pixels.show("bits.png", arr)

        time.sleep(0.1)

def lerp_colors(pixels, rgb1, rgb2, pic_name, run_time):
    """Shows picture pic_name and lerps colors based on min / max rgb1 and rgb2 values using run_time."""
    diff = rgb2 - rgb1
    change = diff
    j = 0
    full_loop = 60
    half_loop = full_loop / 2
    end_time = time.time() + run_time
    while time.time() < end_time:
        rela_pt = (j%full_loop)/(half_loop)
        color = (0,0,0)
        if rela_pt > 1:
            rgb = rgb2 - change * (rela_pt - 1)
            color = tuple(map(int, rgb))
        else:
            rgb = rgb1 + change * rela_pt
            color = tuple(map(int, rgb))
        
        pixels.show(pic_name, [color]*124)
        j += 1
        time.sleep(0.025)

def wheel(pos):
    """Generates and returns RGB value based on pos 0-255 (R -> G -> B -> R)."""
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r,g,b)
