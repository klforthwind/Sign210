import time
import board
import neopixel_spi as neopixel

NUM_PIXELS = 188
PIXEL_ORDER = neopixel.GRB
COLORS = (0xFF0000, 0x00FF00, 0x0000FF,0xFFFFFF)
DELAY = .5

spi = board.SPI()

pixels = neopixel.NeoPixel_SPI(
    spi, 
    NUM_PIXELS, 
    brightness=.3, 
    pixel_order=PIXEL_ORDER,
    reset_time=.008,
    bit0=0b11000000,
    bit1=0b11111000,
    frequency=6553600,
    auto_write=False
)

while True:
    for color in COLORS:
            #pixels[i] = color
            #pixels.show()
            #time.sleep(DELAY)
        pixels.fill(color)
        pixels.show()
        time.sleep(DELAY)
