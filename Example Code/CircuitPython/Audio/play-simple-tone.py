# Plays a simple 8ksps 440 Hz sin wave
#
# Adapted from "Audio output via digital PWM article"
# https://circuitpython.readthedocs.io/en/latest/shared-bindings/audiopwmio/index.html
# for Maker Pi Pico
# 
# Copy this file to Maker Pi Pico CIRCUITPY drive as code.py to run it on power up.
# 

import audiocore
import audiopwmio
import board
import array
import time
import math

# Generate one period of sine wav.
length = 8000 // 440
sine_wave = array.array("H", [0] * length)
for i in range(length):
    sine_wave[i] = int(math.sin(math.pi * 2 * i / length) * (2 ** 15) + 2 ** 15)

dac = audiopwmio.PWMAudioOut(board.GP18)
sine_wave = audiocore.RawSample(sine_wave, sample_rate=8000)
dac.play(sine_wave, loop=True)
time.sleep(1)
dac.stop()