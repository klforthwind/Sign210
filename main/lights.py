# sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel
# sudo pip3 install adafruit-circuitpython-pixel-framebuf
# sudo apt-get install libopenjp2-7
# sudo apt-get install libjpeg-dev zlib1g-dev
# sudo pip3 install pillow

from adafruit_pixel_framebuf import PixelFramebuffer
from PIL import Image
import neopixel
import board
import re

class Lights():

    def __init__(self):
        self.PIXEL_PIN = board.D12
        self.PIXEL_WIDTH = 8
        self.PIXEL_HEIGHT = 8
        self.MATRIX_OFFSET = 64
        self.STRIP_LEN = 124
        self.NUM_PIXELS = self.PIXEL_WIDTH * self.PIXEL_HEIGHT + self.STRIP_LEN

        self.pixels = neopixel.NeoPixel(
            self.PIXEL_PIN, self.NUM_PIXELS, brightness=0.25, auto_write=False
        )

        self.matrix = PixelFramebuffer(
            self.pixels, self.PIXEL_WIDTH, self.PIXEL_HEIGHT, reverse_y=True
        )
    
    def __set_matrix(self, pic_name):
        # Make a black background in RGBA Mode
        image = Image.new("RGBA", (self.PIXEL_WIDTH, self.PIXEL_HEIGHT))

        icon = Image.open(f"imgs/{pic_name}")

        # Alpha blend the icon onto the background
        image.alpha_composite(icon.convert("RGBA"))

        # Convert the image to RGB and display it
        self.matrix.image(image.convert("RGB"))

    def __show_image(self, pic_name):
        self.__set_matrix(pic_name)
        self.matrix.display()

    def __set_strip(self, arr):
        for i in range(self.STRIP_LEN):
            self.pixels[self.MATRIX_OFFSET + i] = arr[i]
    
    def show(self, pic_name, strip_arr):
        self.__set_strip(strip_arr)
        self.__show_image(pic_name)
    
    def color_strip(self, arr):
        self.__set_strip(arr)
        self.pixels.show()
    
    def color_all(self, arr):
        for i in range(self.NUM_PIXELS):
            self.pixels[i] = arr[i]
        self.pixels.show()
