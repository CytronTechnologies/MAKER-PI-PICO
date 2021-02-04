###  This example code uses: Maker Pi Pico ;; Reference: www.cytron.io/p-maker-pi-pico

import machine
import utime

# LED fade

led = machine.PWM(machine.Pin(10))    # set pin 10 as PWM OUTPUT
led.freq(1000)                        # set frequency 1000Hz

while True:
    # fade in
    for i in range(65535):                # from 0 to 65535
        led.duty_u16(i)                   # duty cycle from 0 to 65535
        utime.sleep_us(1)                 # sleep 1 microsecond
        
    # fade out
    for i in range(65535,-1,-1):          # from 65535 to 0
        led.duty_u16(i)                   # duty cycle from 65535 to 0
        utime.sleep_us(1)                 # sleep 1 microsecond
