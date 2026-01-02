from adafruit_pixel_framebuf import PixelFramebuffer
from PIL import Image
from pi5neo import Pi5Neo

class Pi5NeoPixelAdapter:
    """
    Adapter so Pi5Neo can be used anywhere a CircuitPython 'pixels' object is expected
    (PixelFramebuffer, LED Animation, etc.).
    """
    def __init__(self, spi_dev: str, num_pixels: int, spi_speed_khz: int = 800, *, auto_write: bool = False, brightness: float = 1.0):
        self._dev = Pi5Neo(spi_dev, num_pixels, spi_speed_khz)
        self.n = num_pixels  # common attribute name in CircuitPython land
        self.auto_write = auto_write  # PixelFramebuffer checks this :contentReference[oaicite:5]{index=5}
        self.brightness = float(brightness)  # optional; implemented in software here

    def _apply_brightness(self, r: int, g: int, b: int):
        # simple scalar brightness; keep ints 0..255
        if self.brightness >= 0.999:
            return r, g, b
        r = int(r * self.brightness)
        g = int(g * self.brightness)
        b = int(b * self.brightness)
        return r, g, b

    def __setitem__(self, index: int, val):
        r, g, b = val
        r, g, b = self._apply_brightness(int(r), int(g), int(b))
        # Pi5Neo uses set_led_color() :contentReference[oaicite:6]{index=6}
        self._dev.set_led_color(index, r, g, b)
        if self.auto_write:
            self._dev.update_strip()

    def __getitem__(self, index: int):
        # optional; PixelFramebuffer doesn’t require it for drawing,
        # but some animation helpers might. If you need it, we can store a shadow buffer.
        raise NotImplementedError("Reading pixels is not implemented (write-only adapter).")

    def fill(self, color):
        r, g, b = color
        r, g, b = self._apply_brightness(int(r), int(g), int(b))
        # Pi5Neo has fill_strip() and update_strip() :contentReference[oaicite:7]{index=7}
        self._dev.fill_strip(r, g, b)
        if self.auto_write:
            self._dev.update_strip()

    def show(self):
        self._dev.update_strip()

    def deinit(self):
        # best-effort “turn off”
        self._dev.clear_strip()
        self._dev.update_strip()


class Lights:
    def __init__(self):
        self.PIXEL_WIDTH = 8
        self.PIXEL_HEIGHT = 8
        self.MATRIX_OFFSET = 64
        self.STRIP_LEN = 124
        self.NUM_PIXELS = self.PIXEL_WIDTH * self.PIXEL_HEIGHT + self.STRIP_LEN

        # Pi5Neo init per library docs :contentReference[oaicite:8]{index=8}
        self.pixels = Pi5NeoPixelAdapter(
            "/dev/spidev0.0",
            self.NUM_PIXELS,
            spi_speed_khz=800,
            auto_write=False,
            brightness=0.3,   # software brightness scaling
        )

        self.matrix = PixelFramebuffer(
            self.pixels, self.PIXEL_WIDTH, self.PIXEL_HEIGHT, reverse_y=True
        )

    def __set_matrix(self, pic_name):
        image = Image.new("RGBA", (self.PIXEL_WIDTH, self.PIXEL_HEIGHT))
        icon = Image.open(f"imgs/{pic_name}")
        image.alpha_composite(icon.convert("RGBA"))
        self.matrix.image(image.convert("RGB"))

    def __show_image(self, pic_name):
        self.__set_matrix(pic_name)
        self.matrix.display()
        self.pixels.show()

    def __set_strip(self, arr):
        for i in range(self.STRIP_LEN):
            self.pixels[self.MATRIX_OFFSET + i] = arr[i]
        self.pixels.show()

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
