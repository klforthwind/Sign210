# sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel
# sudo pip3 install adafruit-circuitpython-pixel-framebuf
# sudo apt-get install libopenjp2-7
# sudo apt-get install libjpeg-dev zlib1g-dev
# sudo pip3 install pillow
from adafruit_pixel_framebuf import PixelFramebuffer
from PIL import Image
import neopixel_spi
import board
from pi5neo import Pi5Neo
import re
#import gpiod

class Lights():

    def __init__(self):
        self.PIXEL_PIN = board.D12
        self.PIXEL_WIDTH = 8
        self.PIXEL_HEIGHT = 8
        self.MATRIX_OFFSET = 64
        self.STRIP_LEN = 124
        self.NUM_PIXELS = self.PIXEL_WIDTH * self.PIXEL_HEIGHT + self.STRIP_LEN

        #self.pixels = neopixel_spi.NeoPixel_SPI(board.SPI(),
        #    self.NUM_PIXELS, brightness=1, auto_write=False
        #)
        #self.pixels = neopixel_spi.NeoPixel_SPI(board.SPI(), self.NUM_PIXELS, brightness=.2,reset_time=0.0000001,bit0=0b10000000,auto_write=False)
        self.pixels = neopixel_spi.NeoPixel_SPI(
            board.SPI(),
            self.NUM_PIXELS,
            brightness=.3,
            pixel_order=neopixel_spi.GRB,
            reset_time=0.000008,
            bit0=0b10000000,
            bit1=0b01111100,
            frequency=6553600,
            auto_write=False
        )

	#self.pixels = Pi5Neo('/dev/spidev0.0',self.NUM_PIXELS,800);

        self.matrix = PixelFramebuffer(
            self.pixels, self.PIXEL_WIDTH, self.PIXEL_HEIGHT, reverse_y=True
        )
    
    def __set_matrix(self, pic_name):
        """Sets matrix to picture pic_name."""
        # Make a black background in RGBA Mode
        image = Image.new("RGBA", (self.PIXEL_WIDTH, self.PIXEL_HEIGHT))

        icon = Image.open(f"imgs/{pic_name}")

        # Alpha blend the icon onto the background
        image.alpha_composite(icon.convert("RGBA"))

        # Convert the image to RGB and display it
        self.matrix.image(image.convert("RGB"))
        #print("cow")

    def __show_image(self, pic_name):
        """Displays image pic_name in pixel matrix."""
        self.__set_matrix(pic_name)
        self.matrix.display()
        self.pixels.show()

    def __set_strip(self, arr):
        """Set strip to array of RGB values [...,(255,255,255),...]."""
        for i in range(self.STRIP_LEN):
            self.pixels[self.MATRIX_OFFSET + i] = arr[i]
        self.pixels.show()
    
    def show(self, pic_name, strip_arr):
        """Sets and shows pixel matrix to picture pic_name and pixel strip to strip_arr."""
        self.__set_strip(strip_arr)
        self.__show_image(pic_name)
    
    def color_strip(self, arr):
        """Sets and shows pixel strip to arr."""
        self.__set_strip(arr)
        self.pixels.show()
    
    def color_all(self, arr):
        """Colors and shows all pixels (matrix included) to arr."""
        for i in range(self.NUM_PIXELS):
            self.pixels[i] = arr[i]
        self.pixels.show()
