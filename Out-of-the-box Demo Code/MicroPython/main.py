# Test and Demo code for Maker Pi Pico using MicroPython firmware
# Reference: https://my.cytron.io/p-maker-pi-pico, https://my.cytron.io/p-grove-oled-display-0p96-inch-ssd1315
# OLED Pinout : GROVE 4 - SCL = GP7, SDA = GP6
# Installing MicroPython - https://projects.raspberrypi.org/en/projects/getting-started-with-the-pico/3
# Audio track credit: jeremy80 - L-R Tone Level Test @ -6 db max w/3 Sec. Countdown Leader
# Audio track reference: https://freesound.org/people/jeremy80/sounds/230639/

from machine import Pin, I2C, PWM, SPI, SoftI2C
import time
from neopixel import NeoPixel
from uos import mount
import uio
import ustruct as struct
import ssd1306
import sdcard
import uos
import utime
import wav_player

tones = {
        '0':    1,
        'B0':  31,
        'C1':  33,
        'CS1': 35,
        'D1':  37,
        'DS1': 39,
        'E1':  41,
        'F1':  44,
        'FS1': 46,
        'G1':  49,
        'GS1': 52,
        'A1':  55,
        'AS1': 58,
        'B1':  62,
        'C2':  65,
        'CS2': 69,
        'D2':  73,
        'DS2': 78,
        'E2':  82,
        'F2':  87,
        'FS2': 93,
        'G2':  98,
        'GS2': 104,
        'A2':  110,
        'AS2': 117,
        'B2':  123,
        'C3':  131,
        'CS3': 139,
        'D3':  147,
        'DS3': 156,
        'E3':  165,
        'F3':  175,
        'FS3': 185,
        'G3':  196,
        'GS3': 208,
        'A3':  220,
        'AS3': 233,
        'B3':  247,
        'C4':  262,
        'CS4': 277,
        'D4':  294,
        'DS4': 311,
        'E4':  330,
        'F4':  349,
        'FS4': 370,
        'G4':  392,
        'GS4': 415,
        'A4':  440,
        'AS4': 466,
        'B4':  494,
        'C5':  523,
        'CS5': 554,
        'D5':  587,
        'DS5': 622,
        'E5':  659,
        'F5':  698,
        'FS5': 740,
        'G5':  784,
        'GS5': 831,
        'A5':  880,
        'AS5': 932,
        'B5':  988,
        'C6':  1047,
        'CS6': 1109,
        'D6':  1175,
        'DS6': 1245,
        'E6':  1319,
        'F6':  1397,
        'FS6': 1480,
        'G6':  1568,
        'GS6': 1661,
        'A6':  1760,
        'AS6': 1865,
        'B6':  1976,
        'C7':  2093,
        'CS7': 2217,
        'D7':  2349,
        'DS7': 2489,
        'E7':  2637,
        'F7':  2794,
        'FS7': 2960,
        'G7':  3136,
        'GS7': 3322,
        'A7':  3520,
        'AS7': 3729,
        'B7':  3951,
        'C8':  4186,
        'CS8': 4435,
        'D8':  4699,
        'DS8': 4978,
        }

# Initialize led pins
LED = []
pins = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,19,20,21,22,25,26,27,28]

for pin in pins:
    digout = Pin(pin, Pin.OUT)
    LED.append(digout)

# RGB Pin
RGB = LED[25]
# RGB Colors
pixel_off = (0, 0, 0)
pixel_red = (0, 10, 0)
pixel_green = (10, 0, 0)
pixel_blue = (0, 0, 10)
pixel_white = (10,10,10)

# Initialize buzzer
buzzer = PWM(Pin(18)) 

# Melody
mario = ['E7', 'E7', '0', 'E7', '0', 'C7', 'E7', '0', 'G7', '0', '0', '0', 'G6', '0', '0', '0', 'C7', '0','0', 'G6', '0', '0', 'E6', '0', '0', 'A6', '0',
         'B6', '0', 'AS6', 'A6', '0', 'G6', 'E7', '0', 'G7', 'A7', '0', 'F7', 'G7', '0', 'E7', '0','C7', 'D7', 'B6', '0', '0','0','0','0']
up = ['E4','D4','C4']

# Global variables
button1_pressed = False
button2_pressed = False
button3_pressed = False
button_pressed_flag = True
I2C = False
delay1 = 0.15

# monitor button presses
def waiting_for_button(duration):
    global button1_pressed
    global button2_pressed
    global button3_pressed
    end = utime.ticks_ms() + duration*1000
    while utime.ticks_ms() < end:
        if button1.value() == False:
            button1_pressed = True
            #print("Button 20 pressed")
        if button2.value() == False:
            button2_pressed = True
            #print("Button 21 pressed")
        if button3.value() ==  False:
            button3_pressed = True
            #print("Button 22 pressed")

# Startup code
def startup():
    initialize_OLED()
    if I2C:
        print("display OLED Startup")      
        oled.text('STARTUP CODE',20,10, 1)
        oled.text('RUNNING LIGHT',15,25, 1)
        oled.text('WITH',50,40, 1)
        oled.text('MARIO MELODY',20,55, 1)
        deinitialize_OLED()
    x=0
    for i in range(26):
        play_mario_tone(i)
        
        if i != 22:   # Exclude GP25
            LED[i].value(True)
            time.sleep(0.15)
            LED[i].value(False)
        else:
            time.sleep(0.15)


    for i in range(24,-1,-1):
        play_mario_tone(i+x)    
        x +=2
        
        if i != 22:   # Exclude GP25
            if i >= 0:
                LED[i].value(True)
                time.sleep(0.15)
                LED[i].value(False)
            else:
                time.sleep(0.15)
        else:
            time.sleep(0.15)
    
    #Deinitialize LED pins
    LED[19].off()
    LED[21].off()
    LED[20].off()
    
    #Initialize button pins
    global button1
    global button2
    global button3    
    button1 = Pin(20, Pin.IN, Pin.PULL_UP)
    button2 = Pin(21, Pin.IN, Pin.PULL_UP)
    button3 = Pin(22, Pin.IN, Pin.PULL_UP)
                
    initialize_OLED()
    if SoftI2C:
        oled.text('GP20:CHECK LED',0,13, 1)
        oled.text('GP21:CHECK AUDIO',0,23, 1)
        oled.text('GP21:CHECK RGB',0,33, 1)
        oled.text('GP22:CHECK SDCARD',0,43, 1)
        oled.text('GP22:DEMO CODE',0,53, 1)
        deinitialize_OLED()

# Check leds
def button1_handler():
    #Deinitialize button pins
    global button1
    global button2
    global button3
    button1.off()
    button2.off()
    button3.off()
    
    #Initialize LED pins
    LED[19] = Pin(19, Pin.OUT)
    LED[20] = Pin(20, Pin.OUT)
    LED[21] = Pin(21, Pin.OUT)
    
    global button_pressed_flag
    if button_pressed_flag:
        initialize_OLED()
        if I2C:
            oled.text('GP20 PRESSED',20,10, 1)
            oled.text('ALL LEDs',30,25, 1)
            oled.text('TURNS ON',30,40, 1)
            deinitialize_OLED()
        for i in range(26):
            LED[i].value(True) 
        button_pressed_flag = False
        
    elif not button_pressed_flag:
        initialize_OLED()
        if I2C:
            oled.text('GP20 PRESSED',20,10, 1)
            oled.text('ALL LEDs',30,25, 1)
            oled.text('TURNS OFF',29,40, 1)
            deinitialize_OLED()
        for i in range(26):
            LED[i].value(False)
        button_pressed_flag = True
        
    for i in up:
        buzzer.freq(tones[i])
        buzzer.duty_u16(19660)
        time.sleep(0.15)
    buzzer.duty_u16(0)
    
    #Deinitialize LED pins
    LED[19].off()
    LED[20].off()
    LED[21].off()
    
    #Initialize button pins
    button1 = Pin(20, Pin.IN, Pin.PULL_UP)
    button2 = Pin(21, Pin.IN, Pin.PULL_UP)
    button3 = Pin(22, Pin.IN, Pin.PULL_UP)
    time.sleep(0.5)

# Check audio and RGB
def button2_handler():
    global buzzer
    buzzer.deinit()
    LED[18].off()
    print("Button 21 pressed")

    initialize_OLED()
    if I2C:
        oled.text('GP21 PRESSED',20,10, 1)
        oled.text('CHECK AUDIO',22,25, 1)
        oled.text('LEFT RIGHT',25,40, 1)
        oled.text('CHANNEL',35,55, 1)
        deinitialize_OLED()
        
    # Replace "L-R.wav" with the name of your stereo .wav file
    wav_player.play_wav("L-R.wav", left_channel=Pin(18), right_channel=Pin(19))
    
    time.sleep(3)

    initialize_OLED()
    if I2C:
        oled.text('GP21 PRESSED',20,20, 1)
        oled.text('CHECK RGB',27,40, 1)
        deinitialize_OLED()
    RGB.value(False)
    np = NeoPixel(RGB, 8)
    np[0] = pixel_red
    np.write()
    time.sleep(0.5)
    np[0] = pixel_green
    np.write()
    time.sleep(0.5)
    np[0] = pixel_blue
    np.write()
    time.sleep(0.5)
    np[0] = pixel_white
    np.write()
    time.sleep(0.5)
    np[0] = pixel_off
    np.write()
    time.sleep(0.5)
    
    LED[18] = Pin(18, Pin.OUT)
    LED[19] = Pin(19, Pin.OUT)
    buzzer = PWM(Pin(18))
    LED[19].off()
    # pass

# Check SD Card and demo code 
def button3_handler():
    check_SDCARD()
    print("Button 22 pressed")
    RGB.value(False)
    np = NeoPixel(RGB, 8)
    for i in range(0,10,1):
        np[0] = (i, 0, 0)
        np.write()
        play_mario_tone(i)
        time.sleep(delay1)
        
    for i in range(0,10,1):
        np[0] = (10-i,i,0)
        np.write()
        play_mario_tone(i+10)
        time.sleep(delay1)
        
    for i in range(0,10,1):
        np[0] = (0,10-i,i)
        np.write()
        play_mario_tone(i+20)
        time.sleep(delay1)

        
    for i in range(0,10,1):
        np[0] = (i,i,10)
        np.write()
        play_mario_tone(i+30)
        time.sleep(delay1)

        
    for i in range(0,8,1):
        np[0] = (i,i,10)
        np.write()
        play_mario_tone(i+40)
        time.sleep(delay1)
        
    # Clear Neopixel
    np[0] = pixel_off
    np.write()
    # pass

def play_mario_tone(notes):
    if mario[notes] == '0':
        buzzer.duty_u16(0)
    else:
        buzzer.duty_u16(19660)
        buzzer.freq(tones[mario[notes]])
        

def initialize_OLED():
    global I2C
    try:
        LED[6].off()
        LED[7].off()
        global i2c
        i2c = SoftI2C(scl=Pin(7), sda=Pin(6))
        time.sleep(0.1)
        global oled
        oled_width = 128
        oled_height = 64
        oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
        oled.fill(0)
        I2C = True
        print("Initialize OLED")
    except:
        LED[6] = Pin(6, Pin.OUT)
        LED[7] = Pin(7, Pin.OUT)
        I2C = False
        print("Failed to Initialize OLED")

def deinitialize_OLED():
    try:
        #global oled
        oled.show()
        time.sleep(0.1)
        i2c.stop()
        LED[6] = Pin(6, Pin.OUT)
        LED[7] = Pin(7, Pin.OUT)
        
        LED[6].off()
        LED[7].off()
    except:
        LED[6] = Pin(6, Pin.OUT)
        LED[7] = Pin(7, Pin.OUT)
        
        LED[6].off()
        LED[7].off()
        

def check_SDCARD():
    initialize_OLED()
        
    LED[10].off()
    LED[11].off()
    LED[12].off()
    LED[15].off()
    
    try:
        global sd
        
        # Assign chip select (CS) pin (and start it high)
        cs = Pin(15, Pin.OUT)

        # Intialize SPI peripheral (start with 1 MHz)
        spi = SPI(1,
                  baudrate=1000000,
                  polarity=0,
                  phase=0,
                  bits=8,
                  firstbit=SPI.MSB,
                  sck=Pin(10),
                  mosi=Pin(11),
                  miso=Pin(12))

        # Initialize SD card
        sd = sdcard.SDCard(spi, cs)

        # Mount filesystem
        vfs = uos.VfsFat(sd)
        uos.mount(vfs, "/sd")

        # Create a file and write something to it
        with open("/sd/pico.txt", "w") as file:
            file.write("1. Hello, world!\r\n")

        # Open the file we just created and read from it
        with open("/sd/pico.txt", "r") as file:
            for line in file:
                if line == "1. Hello, world!\r\n":
                    for i in up:
                        buzzer.freq(tones[i])
                        buzzer.duty_u16(19660)
                        time.sleep(0.15)
                        
                    buzzer.duty_u16(0)
                    print("The SDCard working properly")
                    
                    if I2C:
                        oled.text('GP22 PRESSED',20,10, 1)
                        oled.text('SD CARD TEST:',10,30, 1)
                        oled.text('PASS',50,45, 1)
                    
                else:
                    if I2C:
                        oled.text('GP22 PRESSED',20,10, 1)
                        oled.text('SD CARD TEST:',10,25, 1)
                        oled.text('FAILED',45,40, 1)
                        oled.text('WRONG DATA',23,50, 1)
                        print("The SDCard wrong Data")
                    
                    buzzer.freq(1661)
                    buzzer.duty_u16(19660)
                    time.sleep(0.2)
                    buzzer.duty_u16(0)
                    time.sleep(0.1)
                    buzzer.duty_u16(19660)
                    time.sleep(0.5)
                    buzzer.duty_u16(0)
                    
        uos.umount(vfs)
        
    except:
        if I2C:
            oled.text('GP22 PRESSED',20,10, 1)
            oled.text('SD CARD TEST:',10,25,1)
            oled.text('FAILED',35,40,1)
            oled.text('NO SD CARD',23,55,1)
            print("No SDCard")

        buzzer.freq(1661)
        buzzer.duty_u16(19660)
        time.sleep(0.2)
        buzzer.duty_u16(0)
        time.sleep(0.1)
        buzzer.duty_u16(19660)
        time.sleep(0.5)
        buzzer.duty_u16(0)
        
        
    if I2C:
        deinitialize_OLED()
        
    LED[10] = Pin(10, Pin.OUT)
    LED[11] = Pin(11, Pin.OUT)
    LED[12] = Pin(12, Pin.OUT)
    LED[15] = Pin(15, Pin.OUT)
    
    time.sleep(0.5)
    
    
startup()

while True:
    waiting_for_button(1)

    if button1_pressed:
        button1_handler()
        waiting_for_button(0.2)
        button1_pressed = False

    elif button2_pressed:
        button2_handler()
        waiting_for_button(0.2)
        button2_pressed = False

    elif button3_pressed:
        button3_handler()
        waiting_for_button(0.2)
        button3_pressed = False
