###  This example code uses: 3V3 I2C and SPI 1602 Serial Character LCD ;; Reference: https://my.cytron.io/p-3v3-i2c-and-spi-1602-serial-character-lcd
###  Make sure your LCD is 3.3V compatible

import machine
import utime

COLUMNS = 16
ROWS    = 2

#Instruction set
CLEARDISPLAY         = 0x01

ENTRYMODESET         = 0x04
ENTRYLEFT            = 0x02
ENTRYRIGHT           = 0x00
ENTRYSHIFTINCREMENT  = 0x01
ENTRYSHIFTDECREMENT  = 0x00

DISPLAYCONTROL       = 0x08
DISPLAYON            = 0x04
DISPLAYOFF           = 0x00
CURSORON             = 0x02
CURSOROFF            = 0x00
BLINKON              = 0x01
BLINKOFF             = 0x00

FUNCTIONSET          = 0x20
_5x10DOTS            = 0x04
_5x8DOTS             = 0x00
_1LINE               = 0x00
_2LINE               = 0x08
_8BITMODE            = 0x10
_4BITMODE            = 0x00

class LCD:
    def __init__(self, sda, scl):
        
        self.column = 0
        self.row = 0
        
        self.address = 62
        
        self.command = bytearray(2)

        _sda = machine.Pin(sda)
        _scl = machine.Pin(scl)
        
        if scl == 3 or scl == 7 or scl == 11 or scl == 15 or scl == 19 or scl == 27:
            self.i2c=machine.I2C(1, sda=_sda, scl=_scl, freq=400000)
        else:
            self.i2c=machine.I2C(0, sda=_sda, scl=_scl, freq=400000)
        
        utime.sleep_ms(50)
        
        for i in range(3):
            self._command(FUNCTIONSET | _2LINE )
            utime.sleep_ms(10)
        
        self.on()
        self.clear()
        
        self._command(ENTRYMODESET | ENTRYLEFT | ENTRYSHIFTDECREMENT)
        
        self.set_cursor(0, 0)
        
    def on(self, cursor=False, blink=False):
        if cursor == False and blink == False:
            self._command(DISPLAYCONTROL | DISPLAYON | CURSOROFF | BLINKOFF)
        elif cursor == False and blink == True:
            self._command(DISPLAYCONTROL | DISPLAYON | CURSOROFF | BLINKON)
        elif cursor == True and blink == False:
            self._command(DISPLAYCONTROL | DISPLAYON | CURSORON | BLINKOFF)
        elif cursor == True and blink == True:
            self._command(DISPLAYCONTROL | DISPLAYON | CURSORON | BLINKON)        
    
    def off(self):
        self._command(DISPLAYCONTROL | DISPLAYOFF | CURSOROFF | BLINKOFF)
        
    def clear(self):
        self._command(CLEARDISPLAY)
        self.set_cursor(0, 0)
    
    
    def set_cursor(self, column, row):
        column = column % COLUMNS
        row = row % ROWS
        if row == 0:
            command = column | 0x80
        else:
            command = column | 0xC0
        self.row = row
        self.column = column
        self._command(command)
    
    def write(self, s):
        for i in range(len(s)):
            utime.sleep_ms(10)
            self.i2c.writeto(self.address, b'\x40'+s[i])
            self.column = self.column + 1
            if self.column >= COLUMNS:
                self.set_cursor(0, self.row+1)
        
    def _command(self, value):
        self.command[0] = 0x80
        self.command[1] = value
        self.i2c.writeto(self.address, self.command)
        utime.sleep_ms(1)
