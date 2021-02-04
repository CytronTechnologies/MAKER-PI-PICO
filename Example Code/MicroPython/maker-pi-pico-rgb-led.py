# This example uses Maker Pi Pico
# Reference: https:www.cytron.io/p-maker-pi-pico
# -----

import array, time
from machine import Pin
import rp2
from rp2 import PIO, StateMachine, asm_pio

# Configure the number of WS2812 LEDs
# - There's 1x built-in RGB LED on Maker Pi Pico board
NUM_LEDS = 1

@asm_pio(sideset_init=PIO.OUT_LOW, out_shiftdir=PIO.SHIFT_LEFT,
autopull=True, pull_thresh=24)
def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    label("bitloop")
    out(x, 1) .side(0) [T3 - 1]
    jmp(not_x, "do_zero") .side(1) [T1 - 1]
    jmp("bitloop") .side(1) [T2 - 1]
    label("do_zero")
    nop() .side(0) [T2 - 1]

# Create the StateMachine with the ws2812 program, outputting on pin GP28 (Maker Pi Pico).
sm = StateMachine(0, ws2812, freq=8000000, sideset_base=Pin(28))

# Start the StateMachine, it will wait for data on its FIFO.
sm.active(1)

# Display a pattern on the LEDs via an array of LED RGB values.
ar = array.array("I", [0 for _ in range(NUM_LEDS)])

while True:
    print("blue")
    for i in range(NUM_LEDS):
        ar[i] = 255
    sm.put(ar,8)
    time.sleep_ms(1000)

    print("red")
    for i in range(NUM_LEDS):
        ar[i] = 255<<8          # shift 8 bits to the left
    sm.put(ar,8)
    time.sleep_ms(1000)

    print("green")
    for i in range(NUM_LEDS):
        ar[i] = 255<<16         # shift 16 bits to the left
    sm.put(ar,8)
    time.sleep_ms(1000)

    print("white")
    for i in range(NUM_LEDS):
        ar[i] = 0xFFFFFF
    sm.put(ar,8)
    time.sleep_ms(1000)
