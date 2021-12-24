def snake(events, db, pixels):
    strip_len = pixels.STRIP_LEN
    color = (255,0,0)
    if event[2]['user'].lower() == "beta64":
        color = (255,0,255)
    start = randint(0,strip_len-1)
    size = 5

    apple = randint(0,strip_len-1)

    while size < strip_len:
        start = (start + 1) % strip_len
        if apple == start:
            print("X")
            size += 32
            if start + size >= strip_len:
                apple = randint((start + size) % strip_len, start-1)
            else:
                if start != 0:
                    apple = (randint(0, start-1), randint(start+size,strip_len-1))[randint(0,1)]
                else:
                    apple = randint(start+size,strip_len-1)
        strip = []
        for x in range(124):
            if start + size >= strip_len:
                if x <= (start + size) % strip_len:
                    strip.append(color)
                elif x >= start:
                    strip.append(color)
                else:
                    strip.append((0,0,0))
            else:
                if start <= x < start+size:
                    strip.append(color)
                else:
                    strip.append((0,0,0))
        
        pixels.color_strip(strip)
        time.sleep(0.01)