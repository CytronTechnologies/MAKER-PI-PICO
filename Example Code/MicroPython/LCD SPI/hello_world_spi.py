###  This example code uses: 3V3 I2C and SPI 1602 Serial Character LCD ;; Reference: https://my.cytron.io/p-3v3-i2c-and-spi-1602-serial-character-lcd
###  Make sure your LCD is 3.3V compatible

from LCD_SPI import *    #import LCD_SPI library

# SPI LCD Display

lcd = LCD(sck=2, tx=3, cs=5)  # Create LCD object with LCD's sck pin connected to PICO's sck pin 2, LCD's sda pin connected to Pico's tx pin 3, LCD's cs pin connected to Pico's CSn pin 5
lcd.set_cursor(0,0)          # Set the cursor at first column, first row
lcd.write("Hello World")     # Write string to the LCD   
