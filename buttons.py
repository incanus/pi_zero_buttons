#!/usr/bin/env python3

import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display.rgb import color565
import adafruit_rgb_display.st7789 as st7789
from gpiozero import Button, DigitalOutputDevice
from sys import exit
from time import sleep

BORDER = 20
FONTSIZE = 24

cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

BAUDRATE = 64000000

BOUNCE = None
DELAY = 0.1
START = 95

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

output = '>'
val = START
cur = ''
caps = False

def do_select():
    global caps, val
    if val != START:
        if caps and val <= 90:
            val = val + 32
        elif not caps and val <= 122:
            val = val - 32
    caps = not caps

def do_start():
    pass

def do_up():
    global val
    if val == START:
        val = 97
    else:
        val = val + 1

def do_down():
    global val
    if val == START:
        val = 97
    else:
        val = val - 1

def do_left():
    global output, val
    if len(output) > 1:
        if val == START:
            output = output[0 : len(output) - 1]
        else:
            val = START

def do_right():
    global output, val
    if val == START:
        val = 32
    output = output + chr(val)
    val = START

select = Button(23, bounce_time=BOUNCE)
select.when_pressed = do_select
start = Button(24, bounce_time=BOUNCE)
start.when_pressed = do_start

# 13 is ground for 'up'
pin13 = DigitalOutputDevice(13)
pin13.off()
up = Button(6, bounce_time=BOUNCE, hold_time=0.25, hold_repeat=True)
up.when_pressed = do_up
up.when_held = do_up
down = Button(12, bounce_time=BOUNCE, hold_time=0.25, hold_repeat=True)
down.when_pressed = do_down
down.when_held = do_down
left = Button(5, bounce_time=BOUNCE)
left.when_pressed = do_left
right = Button(16, bounce_time=BOUNCE)
right.when_pressed = do_right

image = Image.new("RGB", (width, height))

draw = ImageDraw.Draw(image)

draw.rectangle((0, 0, width, height), fill=(0, 0, 0))
disp.image(image)

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", FONTSIZE)

def dprint(text):
    draw.rectangle((0, 0, width, height), fill=(0, 0, 0))
    draw.text(
        (0, 0),
        text,
        font=font,
        fill=(255, 255, 0)
    )
    disp.image(image)

while True:
    try:
        dprint(output + chr(val))
        sleep(DELAY)
    except KeyboardInterrupt:
        exit()