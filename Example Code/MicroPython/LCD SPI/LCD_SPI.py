###  This example code uses: 3V3 I2C and SPI 1602 Serial Character LCD ;; Reference: https://my.cytron.io/p-3v3-i2c-and-spi-1602-serial-character-lcd
###  Make sure your LCD is 3.3V compatible

import machine
import utime

COLUMNS = 16 
ROWS    = 2

#Instruction Set
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
_5x10DOTS             = 0x04
_5x8DOTS              = 0x00
_1LINE                = 0x00
_2LINE                = 0x08
_8BITMODE             = 0x10
_4BITMODE             = 0x00

class LCD:
    def __init__(self,sck,tx,cs):  # Initialize LCD
        
        self.column = 0
        self.row = 0
        
        self.data = bytearray(2)
        self.command = bytearray(2)
        
        
        _tx = machine.Pin(tx)
        _sck = machine.Pin(sck)
        
        self.CS = machine.Pin(cs, machine.Pin.OUT) 
        
        self.CS.value(1)
        
        # Cofigure SPI ports
        if sck == 10 or sck == 14:
            _rx = machine.Pin(12)
            self.spi=machine.SPI(1,baudrate=1000000,polarity = 0,phase = 0,bits=8,sck=_sck, mosi=_tx, miso=_rx)
        else:
            _rx = machine.Pin(4)
            self.spi=machine.SPI(0,baudrate=1000000,polarity = 0,phase = 0,bits=8,sck=_sck, mosi=_tx, miso=_rx)
        
        utime.sleep_ms(50)
        
        self._command(FUNCTIONSET | _2LINE )
        
        self.on()
        self.clear()
        self._command(ENTRYMODESET | ENTRYLEFT | ENTRYSHIFTDECREMENT)      
        self.set_cursor(0,0)
         
    def on(self, cursor=False, blink=False):  # Initialize LCD with or without cursor and blink 
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
        self.set_cursor(0,0)
    
    
    def set_cursor(self,column,row):
        column = column % COLUMNS
        row = row % ROWS
        if row == 0:
            command = column | 0x80
        else:
            command = column | 0xC0
        self.row = row
        self.column = column
        self._command(command)
    
    def write(self,s):
        for i in range(len(s)):
            utime.sleep_ms(10)
            _str = ord(s[i])
            self.data[0] = 0x80
            self.data[0] |= (_str >> 1)
            self.data[1] = ((_str & 1) << 7)
            self.CS.value(0)
            self.spi.write(self.data)
            self.CS.value(1)
            self.column = self.column + 1
            if self.column >= COLUMNS:
                self.set_cursor(0,self.row+1)
        
    def _command(self,value):
        self.command[0] = 0
        self.command[0] |= (value >> 1)
        self.command[1] = ((value & 1) << 7)
        self.CS.value(0)
        self.spi.write(self.command)
        self.CS.value(1)
        utime.sleep_ms(1)
