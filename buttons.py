#!/usr/bin/env python3

import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display.rgb import color565
import adafruit_rgb_display.st7789 as st7789
from gpiozero import Button, DigitalOutputDevice
from sys import exit
from subprocess import run

BORDER = 20
FONTSIZE = 24

cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

BAUDRATE = 64000000

spi = board.SPI()

disp = st7789.ST7789(
    spi,
    rotation=90,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE
)

if disp.rotation % 180 == 90:
    height = disp.width
    width = disp.height
else:
    width = disp.width
    height = disp.height

backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

# 13 is ground for up
pin13 = DigitalOutputDevice(13)
pin13.off()
up = Button(6)
down = Button(12)
left = Button(5)
right = Button(16)

image = Image.new("RGB", (width, height))

draw = ImageDraw.Draw(image)

draw.rectangle((0, 0, width, height), fill=(0, 0, 0))
disp.image(image)

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", FONTSIZE)

def dprint(text):
    draw.rectangle((0, 0, width, height), fill=(0, 0, 0))
    (font_width, font_height) = font.getsize(text)
    draw.text(
        (width // 2 - font_width // 2, height // 2 - font_height // 2),
        text,
        font=font,
        fill=(255, 255, 0),
    )
    disp.image(image)

while True:
    try:
        status=''
        if not buttonA.value:
            status = status + '-'
        if not buttonB.value:
            status = status + '+'
        if up.is_pressed:
            status = status + '↑'
        if down.is_pressed:
            status = status + '↓'
        if left.is_pressed:
            status = status + '←'
        if right.is_pressed:
            status = status + '→'
        if not len(status):
            status = '?'
        dprint(status)
    except KeyboardInterrupt:
        backlight.deinit()
        run(['echo 22 > /sys/class/gpio/export 2>/dev/null'], shell=True)
        run(['echo out > /sys/class/gpio/gpio22/direction'], shell=True)
        exit()