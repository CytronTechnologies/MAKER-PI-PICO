import machine
import utime

# LED BLINKING

led = machine.Pin(10, machine.Pin.OUT)   # set pin 10 as OUTPUT
       
while True:    
    led.toggle()     # toggle LED
    utime.sleep(0.5) # sleep 500ms