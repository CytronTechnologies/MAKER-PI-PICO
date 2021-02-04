from LCD_I2C import *    #import LCD_I2C library

# I2C LCD Display

lcd = LCD(sda=2, scl=3)  # Create LCD object with LCD's sda pin connected to PICO's sda pin 2, LCD's sck pin connected to Pico's scl pin 3
lcd.set_cursor(0,0)          # Set the cursor at first column, first row
lcd.write("Hello World")     # Write string to the LCD  