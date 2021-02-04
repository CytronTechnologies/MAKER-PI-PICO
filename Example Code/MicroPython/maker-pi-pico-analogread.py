import machine
import time

potentiometer = machine.ADC(26)     # set GP26 as analog input pin

while True:
    print(potentiometer.read_u16()) # print analog value to serial
    time.sleep_ms(50)               # sleep for 50ms, then repeat.
    
