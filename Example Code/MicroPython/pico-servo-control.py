###  This example code uses: Maker Pi Pico ;; Reference: www.cytron.io/p-maker-pi-pico
###  This example code uses: Analog Micro Servo 9g (3V-6V) ;; Reference: www.cytron.io/p-analog-micro-servo-9g-3v-6v

from machine import Pin, PWM
import time

# fine tune the duty cycle values which work for your servo motor
MIN_DUTY = 1600
MAX_DUTY = 8400

pwm = PWM(Pin(1))     # Connect servo at pin 1
pwm.freq(50)          # Set PWM frequency to 50Hz

while True:
    pwm.duty_u16(MIN_DUTY)    # Set duty cycle
    time.sleep_ms(1000)
    pwm.duty_u16(MAX_DUTY)
    time.sleep_ms(1000)
