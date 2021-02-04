###  This example code uses: Maker Pi Pico ;; Reference: www.cytron.io/p-maker-pi-pico  
###  This example code uses: Maker Line ;; Reference: www.cytron.io/p-maker-line-simplifying-line-sensor-for-beginner  

from motor_driver import *         # import motor driver library

line = machine.ADC(26)             # set pin 26 as analog INPUT

motor = motor_driver(4,5,2,3)      # M1A = 4, M1B = 5, M2A = 2, M2B = 3

def read_line_sensor():
    return line.read_u16()        

while True:
    line_value = read_line_sensor()   # read line sensor
    if line_value > 60000:    # all line
        motor.speed(80,80)    # straight
    elif line_value > 40000:  # S5 or S4+S5
        motor.speed(80,20)    # right
    elif line_value > 34000:  # S4 or S3+S4
        motor.speed(80,50)    # slight right
    elif line_value > 30000:  # S3
        motor.speed(80,80)    # straight
    elif line_value > 22000:  # S2 or S3+S2
        motor.speed(50,80)    # slight left
    elif line_value > 10000:  # S1 or S2+S1
        motor.speed(20,80)    # left