### This example code uses: Maker Pi Pico ;; Reference: www.cytron.io/p-maker-pi-pico
### This example code uses: Grove - OLED Display 0.96 inch - SSD1315 ;; Reference: www.cytron.io/p-grove-oled-display-0p96-inch-ssd1315
### OLED Pinout : GROVE 1 - SCL = GP1, SDA = GP0

import board
from analogio import AnalogIn
import busio as io
import adafruit_ssd1306

# define analog input pin 
analog_in = AnalogIn(board.GP27)

# helper function to calculate voltage from analog readings
def get_voltage(pin):
    return (pin.value * 3.3) / 65536

# initialize OLED
# I2C: SCL = GP1, SDA = GP0
# OLED: 128x64 pixels
i2c = io.I2C(board.GP1, board.GP0)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)


# program loop
while True:
	# clear all pixels
    oled.fill(0)
	
	# display analog value
	# text(string, x, y, color, *, font_name="font5x8.bin", size=1)
    oled.text('Analog value = ', 0, 0, 1)
    oled.text(str(analog_in.value), 90, 0, 1)
	
	# display voltage
    oled.text('Voltage = ', 0, 12, 1)
    oled.text(str(get_voltage(analog_in)), 60, 12, 1)
	
    # draw a rectangle based on analog value
	# fill_rect(x, y, width, height, color)
    oled.fill_rect(0, 30, (analog_in.value >> 9), 10, 1)

	# show on OLED
    oled.show()
