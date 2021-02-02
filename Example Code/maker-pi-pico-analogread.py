import machine
import time

potentiometer = machine.ADC(26)

while True:
    print(potentiometer.read_u16())
    time.sleep_ms(50)
    