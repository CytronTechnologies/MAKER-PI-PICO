from machine import Pin, PWM
import time

# fine tune the duty cycle values which work for your servo motor
MIN_DUTY = 1600
MAX_DUTY = 8400

pwm = PWM(Pin(1))
pwm.freq(50)

while True:
    pwm.duty_u16(MIN_DUTY)
    time.sleep_ms(1000)
    pwm.duty_u16(MAX_DUTY)
    time.sleep_ms(1000)
