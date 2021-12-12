# sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel
# sudo pip3 install adafruit-circuitpython-pixel-framebuf
# sudo apt-get install libopenjp2-7
# pip3 install python-dotenv

import mysql.connector
from dotenv import load_dotenv
import os
import time

import board
import neopixel
from PIL import Image
from adafruit_pixel_framebuf import PixelFramebuffer

load_dotenv()

pixel_pin = board.D18
pixel_width = 8
pixel_height = 8
strip_len = 124
num_pixels = pixel_width * pixel_height + strip_len

# all pixels
total = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.25, auto_write=False
)

# matrix pixels
pixel_framebuf = PixelFramebuffer(
    total, pixel_width, pixel_height, reverse_y=True
)

# displays image on matrix given pic_name
def show_image(pic_name):
    # Make a black background in RGBA Mode
    image = Image.new("RGBA", (pixel_width, pixel_height))

    icon = Image.open(f"imgs/{pic_name}")

    # Alpha blend the icon onto the background
    image.alpha_composite(icon.convert("RGBA"))

    # Convert the image to RGB and display it
    pixel_framebuf.image(image.convert("RGB"))
    pixel_framebuf.display()

# download picture given pic_name
def download_picture(pic_name):
    os.system(f"curl https://www.klforthwind.com/sign210/imgs/{pic_name} > imgs/{pic_name}")

# download_picture("redsus.png")

# show_image("redsus.png")

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user=os.getenv('MYSQL_USER'),
    password=os.getenv('MYSQL_PASSWORD'),
    database=os.getenv('MYSQL_DB')
)

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM EVENTS WHERE ev_type='NORMALCHAT'")

myresult = mycursor.fetchall()

for x in myresult:
  print(x)


# WHITE_START = 64
# RED_START = WHITE_START+23

# WHITE_BRIGHTNESS = 0.3
# WHITE_COLOR = int(255 * WHITE_BRIGHTNESS)

# for z in range(WHITE_START, led_count):
#     total[z] = (WHITE_COLOR,WHITE_COLOR,WHITE_COLOR)

# for z in range(RED_START, led_count):
#     total[z] = (255,0,0)

# total.show()

# # total.fill((0,0,0))
# # total.show()

# # os.system("curl https://www.klforthwind.com/sign210/L.png > L.png")



t_end = time.time() + 25
while time.time() < t_end:
    pass
