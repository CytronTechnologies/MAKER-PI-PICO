###  This example code uses: 3V-5.5V SR04P Ultrasonic Ranging Module ;; Reference: https://my.cytron.io/p-3v-5.5v-ultrasonic-ranging-module

from machine import Pin
import utime

trigger = Pin(7, Pin.OUT)
echo = Pin(6, Pin.IN)

distance = 0
def ultrasound():
    global distance
    trigger.low()
    utime.sleep_us(2)
    trigger.high()
    utime.sleep_us(5)
    trigger.low()
    while echo.value() == 0:
        signaloff = utime.ticks_us()
    while echo.value() == 1:
        signalon = utime.ticks_us()
    timepassed = signalon - signaloff
    distance = (timepassed * 0.0343) / 2

while True:
    ultrasound()
    print("The distance from object is ", distance, "cm")
    utime.sleep(1)
