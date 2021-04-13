###  This example code uses: Maker Pi Pico ;; Reference: www.cytron.io/p-maker-pi-pico

import time
import board
import digitalio
import usb_hid
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.mouse import Mouse


# Configure built-in LED on Pi Pico
led = digitalio.DigitalInOut(board.GP25)
led.direction = digitalio.Direction.OUTPUT
led.value = False

# Configure buttons on Maker Pi Pico
btn1 = digitalio.DigitalInOut(board.GP20)
btn2 = digitalio.DigitalInOut(board.GP21)
btn3 = digitalio.DigitalInOut(board.GP22)
btn1.direction = digitalio.Direction.INPUT
btn2.direction = digitalio.Direction.INPUT
btn3.direction = digitalio.Direction.INPUT
btn1.pull = digitalio.Pull.UP
btn2.pull = digitalio.Pull.UP
btn3.pull = digitalio.Pull.UP

# Set up keyboard and mouse.
kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)
mouse = Mouse(usb_hid.devices)
direction = True

while True:
    # Test buttons on Maker Pi Pico
    if not btn1.value:
        # Debounce
        time.sleep(0.3)
        while not btn1.value:
            pass
        # Type 'abc' followed by newline.
        layout.write('abc\n')
        # Type numbers followed by newline.
        layout.write('789\n')
        # Type symbols followed by tab.
        layout.write('!?_*\t')
        # Type lowercase 'x'.
        kbd.send(Keycode.X)
        # Type capital 'Y'.
        kbd.send(Keycode.SHIFT, Keycode.Y)
        
    if not btn2.value:
        # Debounce
        time.sleep(0.3)
        while not btn2.value:
            pass
        # Toggle mouse wheel up/down by one unit
        if direction:
            mouse.move(wheel=1)
            direction = False
        else:
            mouse.move(wheel=-1)
            direction = True
        
    if not btn3.value:
        # Debounce
        time.sleep(0.3)
        while not btn3.value:
            pass
        mouse.move(x=60)
        mouse.move(y=-25)
        
    # Blink built-in LED on Pi Pico
    led.value = not led.value
    time.sleep(0.2)
