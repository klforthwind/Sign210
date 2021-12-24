import time

def loading_raid(event, db, pixels):
    strip_len = pixels.STRIP_LEN
    hat_color = {
        "mariohat":(255,0,0),
        "luigihat":(0,255,0),
        "waluigihat":(75,0,130),
        "wariohat":(200,200,0)
    }

    color = hat_color[db.get_evar(db.DEF_STRIP)]

    red = (255, 0, 0)
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
    
    pixels.show_image("raid.png")
    db.set_evar(db.CURR_MAT, "raid.png")
    time.sleep(2)