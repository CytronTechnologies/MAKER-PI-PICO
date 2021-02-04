import machine
import utime

# Button Controlled LED

button = machine.Pin(20,machine.Pin.IN,machine.Pin.PULL_UP)   # set pin 20 as INPUT with PULL_UP
led = machine.Pin(25, machine.Pin.OUT)                        # set pin 25 as OUTPUT

while True:
    if button.value() == 0:                                   # if button is pressed
        led.value(1)                                          # turn on the LED
    else:
        led.value(0)                                          # turn off the LED
        