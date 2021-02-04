###  This example code uses: Maker Pi Pico ;; Reference: www.cytron.io/p-maker-pi-pico

import machine
import utime
from pitches import *

# Melody Mario

buzzer = machine.PWM(machine.Pin(18))  # set pin 18 as PWM OUTPUT

# mario notes
mario = [E7, E7, 0, E7, 0, C7, E7, 0, G7, 0, 0, 0, G6, 0, 0, 0, C7, 0, 0, G6, 0, 0, E6, 0, 0, A6, 0, B6, 0, AS6, A6, 0, G6, E7, 0, G7, A7, 0, F7, G7, 0, E7, 0,C7, D7, B6, 0, 0, C7, 0, 0, G6, 0, 0, E6, 0, 0, A6, 0, B6, 0, AS6, A6, 0, G6, E7, 0, G7, A7, 0, F7, G7, 0, E7, 0,C7, D7, B6, 0, 0]

for i in mario:
    if i == 0:
        buzzer.duty_u16(0)            # 0% duty cycle
    else:
        buzzer.freq(i)                # set frequency (notes)
        buzzer.duty_u16(19660)        # 30% duty cycle
    utime.sleep(0.15)
