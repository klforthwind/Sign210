# sudo apt install numpy-python
from random import randint
from extra_funcs import *
import numpy as np
import time

#
#
#
#
def rick(event, db, pixels):
    db.set_evar(db.CURR_MAT, "")
    j = 0
    end_time = time.time() + 10
    while time.time() < end_time:
        color = wheel(j & 255)
        pixels.show(f"rick/{(j//8)%21}.png", [color]*124)
        time.sleep(0.0125)
        j+=2

#
#
#
#
# def snake(event, db, pixels):
#     strip_len = pixels.STRIP_LEN
#     color = (255,0,0)
#     if event[2]['user'].lower() == "beta64":
#         color = (255,0,255)
#     start = randint(0,strip_len-1)
#     size = 5

#     apple = randint(0,strip_len-1)

#     # while size < strip_len:
#     while size < 10:
#         old_start = start
#         start = (start + 5) % strip_len
#         if start >= apple >= old_start:
#             size += 1
#             if start + size >= strip_len:
#                 apple = randint((start + size) % strip_len, start-1)
#             else:
#                 if start != 0:
#                     apple = (randint(0, start-1), randint(start+size,strip_len-1))[randint(0,1)]
#                 else:
#                     apple = randint(start+size,strip_len-1)
        
#         strip = []
#         for x in range(124):
#             if x == apple:
#                 strip.append(color)
#             elif start + size >= strip_len:
#                 if x <= (start + size) % strip_len:
#                     strip.append(color)
#                 elif x >= start:
#                     strip.append(color)
#                 else:
#                     strip.append((0,0,0))
#             else:
#                 if start <= x < start+size:
#                     strip.append(color)
#                 else:
#                     strip.append((0,0,0))
        
#         pixels.color_strip(strip)
#         time.sleep(0.01)

#
#
#
#
def loading_raid(event, db, pixels):
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

#
#
#
#
def animate_raid(event, db, pixels):
    if False:
        rick(event, db, pixels)
    else:
        loading_raid(event, db, pixels)

    set_default(event, db, pixels)

#
#
#
#
def pulse(db, pixels, image, rgb1_list, rgb2_list, run_time):
    db.set_evar(db.CURR_MAT, "")
    low = np.array(rgb1_list)
    high = np.array(rgb2_list)
    lerp_colors(pixels, low, high, image, run_time)

#
#
#
#
def slow_rainbow(event, db, pixels):
    db.set_evar(db.CURR_MAT, "")
    j = 0
    end_time = time.time() + 10
    while time.time() < end_time:
        color = wheel(j & 255)
        pixels.show(f"star/star{(j//4)%5+1}.png", [color]*124)
        time.sleep(0.0125)
        j+=2

    set_default(event, db, pixels)

#
#
#
#
def fast_rainbow(event, db, pixels):
    db.set_evar(db.CURR_MAT, "")
    j = 0
    bri = 64    # brightness
    colors = [(0,0,bri),(bri,0,bri),(bri,0,0),(bri,bri,0),(0,bri,0),(bri,0,0),(bri,bri,bri)]

    end_time = time.time() + 10
    while time.time() < end_time:
        color = colors[(j%7)]
        pixels.show(f"star/star{(j//2)%5+1}.png", [color]*124)
        time.sleep(0.025)
        j+=1

    set_default(event, db, pixels)

#
#
#
#
def slow_rainbow_shift(event, db, pixels):
    db.set_evar(db.CURR_MAT, "")
    j = 0
    end_time = time.time() + 10
    while time.time() < end_time:
        strip = []
        for x in range(124):
            color = wheel((int(x * 255 / 124+j)%255))
            strip.append(color)
        pixels.show(f"star/star{(j//4)%5+1}.png", strip)
        time.sleep(0.025)
        j+=1

    set_default(event, db, pixels)

#
#
#
#
def show_game(db, pixels, game_title, wait_time):
    db.set_evar(db.CURR_MAT, "")
    strip = get_strip(db)

    games = {
        "Minecraft": "mariograss.png",
        "Gartic Phone": "gartic.png",
        "Valheim": "valheim.png",
        "Golf": "golfball210.png",
        "Subnautica": "subnautica.png"
    }

    for game in games:
        if game in game_title:
            pixels.show(games[game], strip)
            time.sleep(wait_time)
            break
    
    set_default(event, db, pixels)

def cheer(event, db, pixels):
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
    
    set_default(event, db, pixels)




#
#
#
#
def lerp_colors(pixels, rgb1, rgb2, pic_name, run_time):
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

#
#
#
#
def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
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
