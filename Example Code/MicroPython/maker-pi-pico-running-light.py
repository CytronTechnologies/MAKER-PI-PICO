###  This example code uses: Maker Pi Pico ;; Reference: www.cytron.io/p-maker-pi-pico

import machine
import utime

# RUNNING LIGHT

for i in range(29):                     # from 0 to 28  
    if i != 23 and i != 24:             # pin 23 and 24 are not GPIO pins
        machine.Pin(i,machine.Pin.OUT)  # set the pins to output

while True:
    for i in range(29):                      
        if i != 23 and i != 24:      
            machine.Pin(i).value(0)     # turn off the LED
            utime.sleep(0.1)            # sleep for 100ms
            machine.Pin(i).value(1)     # turn on the LED
            
    for i in range(28,-1,-1):           # from 28 to 0
        if i != 23 and i != 24:
            machine.Pin(i).value(1)     # turn on the LED
            utime.sleep(0.1)
            machine.Pin(i).value(0)     # turn off the LED
