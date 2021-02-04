###  This example code uses: Maker Pi Pico ;; Reference: www.cytron.io/p-maker-pi-pico
###  This example code uses: SR04P Ultrasonic Ranging Module ;; Reference: wwwcytron.io/c-sensor/c-ultrasonic-sensor/p-3v-5.5v-ultrasonic-ranging-module

import machine
import utime

# read ultrasonic

Trig = machine.Pin(6,machine.Pin.OUT)   # Connect Trig pin to pin 6 and set to OUTPUT
Echo = machine.Pin(7,machine.Pin.IN)    # Connect Echo pin to pin 7 and set to INPUT

def read_ultrasonic():
    
    Trig.value(0)                       
    utime.sleep_us(2)
    Trig.value(1)
    utime.sleep_us(10)
    Trig.value(0)
    
    while Echo.value() == 0:
        pulse_start = utime.ticks_us()
        
    while Echo.value() == 1:
        pulse_end = utime.ticks_us()
        
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration//58

    return distance

while True:
    print(read_ultrasonic())     # print ultrasonic distance
    utime.sleep(1)               # sleep 1 second