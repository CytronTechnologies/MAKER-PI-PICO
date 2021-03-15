# Test and Demo code for Maker Pi Pico
# Reference: https://my.cytron.io/p-maker-pi-pico
# Installing CircuitPython - https://learn.adafruit.com/getting-started-with-raspberry-pi-pico-circuitpython/circuitpython
# Audio track credit: jeremy80 - L-R Tone Level Test @ -6 db max w/3 Sec. Countdown Leader
# Audio track reference: https://freesound.org/people/jeremy80/sounds/230639/

import board
import digitalio
import time
import pwmio
from neopixel_write import neopixel_write
import busio
import sdcardio
import storage
import audiocore
import audiopwmio
import busio as io
import adafruit_ssd1306

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



# Initialize buttons
button1 = digitalio.DigitalInOut(board.GP20)
button1.switch_to_input(pull=digitalio.Pull.UP)
button2 = digitalio.DigitalInOut(board.GP21)
button2.switch_to_input(pull=digitalio.Pull.UP)
button3 = digitalio.DigitalInOut(board.GP22)
button3.switch_to_input(pull=digitalio.Pull.UP)

# Initialize led pins
LED = []
pins = [board.GP0,board.GP1,board.GP2,board.GP3,board.GP4,board.GP5,board.GP6,board.GP7,board.GP8,board.GP9,board.GP10,board.GP11,board.GP12,board.GP13,board.GP14,board.GP15,board.GP16,board.GP17,board.GP19,board.GP25,board.GP26,board.GP27,board.GP28]

for pin in pins:
    digout = digitalio.DigitalInOut(pin)
    digout.direction = digitalio.Direction.OUTPUT
    LED.append(digout)

# RGB Pin
RGB = LED[22]
# RGB Colors
pixel_off = bytearray([0, 0, 0])
pixel_red = bytearray([0, 10, 0])
pixel_green = bytearray([10, 0, 0])
pixel_blue = bytearray([0, 0, 10])
pixel_white = bytearray([10,10,10])

# Initialize buzzer
buzzer = pwmio.PWMOut(board.GP18, variable_frequency=True)

# Melody
mario = ['E7', 'E7', '0', 'E7', '0', 'C7', 'E7', '0', 'G7', '0', '0', '0', 'G6', '0', '0', '0', 'C7', '0','0', 'G6', '0', '0', 'E6', '0', '0', 'A6', '0','B6', '0', 'AS6', 'A6', '0', 'G6', 'E7', '0', 'G7', 'A7', '0', 'F7', 'G7', '0', 'E7', '0','C7', 'D7', 'B6', '0', '0']
up = ['E4','D4','C4']

# Global variables
button1_pressed = False
button2_pressed = False
button3_pressed = False
button_pressed_flag = True
I2C = False
delay1 = 0.15

# monitor butten presses
def waiting_for_button(duration):
    global button1_pressed
    global button2_pressed
    global button3_pressed
    end = time.monotonic() + duration
    while time.monotonic() < end:
        if button1.value == False:
            button1_pressed = True
        if button2.value == False:
            button2_pressed = True
        if button3.value ==  False:
            button3_pressed = True

# Startup code
def startup():
    initialize_OLED()
    if I2C:
        oled.text('STARTUP CODE',30,10, 1)
        oled.text('RUNNING LIGHT',27,30, 1)
        oled.text('WITH MARIO MELODY',14,50, 1)
        deinitialize_OLED()
    x=0
    for i in range(22):
        play_mario_tone(i)

        LED[i].value = True
        time.sleep(0.15)
        LED[i].value = False


    for i in range(22,-4,-1):
        play_mario_tone(i+x)    
        x +=2
        if i >= 0:
            LED[i].value = True
            time.sleep(0.15)
            LED[i].value = False
        else:
            time.sleep(0.15)
            
    initialize_OLED()
    if I2C:
        oled.text('GP20: CHECK LED',3,13, 1)
        oled.text('GP21: CHECK AUDIO',3,23, 1)
        oled.text('GP21: CHECK RGB',3,33, 1)
        oled.text('GP22: CHECK SD CARD',3,43, 1)
        oled.text('GP22: DEMO CODE',3,53, 1)
        deinitialize_OLED()

# Check leds
def button1_handler():

    global button_pressed_flag
    if button_pressed_flag:
        initialize_OLED()
        if I2C:
            oled.text('GP20 PRESSED',30,10, 1)
            oled.text('ALL LEDs TURNS ON',10,25, 1)
            oled.text('EXCEPT',50,40, 1)
            oled.text('GP18',55,55, 1)
            deinitialize_OLED()
        for i in range(23):
            LED[i].value = True  
        button_pressed_flag = False
        
    elif not button_pressed_flag:
        initialize_OLED()
        if I2C:
            oled.text('GP20 PRESSED',30,10, 1)
            oled.text('ALL LEDs TURNS OFF',10,25, 1)
            oled.text('EXCEPT',50,40, 1)
            oled.text('GP20,GP21,GP22',20,55, 1)
            deinitialize_OLED()
        for i in range(23):
            LED[i].value = False
        button_pressed_flag = True
        
    for i in up:
        buzzer.frequency = tones[i]
        buzzer.duty_cycle = 19660
        time.sleep(0.15)
    buzzer.duty_cycle = 0
    
# Check audio and RGB
def button2_handler():
    global buzzer
    buzzer.deinit()
    LED[18].deinit()
    
    LR_FILENAME = "L-R.wav"
    data = open(LR_FILENAME, "rb")
    wav = audiocore.WaveFile(data)
    dac = audiopwmio.PWMAudioOut(board.GP18,right_channel=board.GP19)
    initialize_OLED()
    if I2C:
        oled.text('GP21 PRESSED',30,10, 1)
        oled.text('CHECK AUDIO',32,25, 1)
        oled.text('LEFT RIGHT CHANNEL',10,40, 1)
        deinitialize_OLED()
    dac.play(wav)
    time.sleep(3)
    dac.stop()

    initialize_OLED()
    if I2C:
        oled.text('GP21 PRESSED',30,20, 1)
        oled.text('CHECK RGB',37,40, 1)
        deinitialize_OLED()
    RGB.value = False
    neopixel_write(RGB, pixel_red)
    time.sleep(0.5)
    neopixel_write(RGB, pixel_green)
    time.sleep(0.5)
    neopixel_write(RGB, pixel_blue)
    time.sleep(0.5)
    neopixel_write(RGB, pixel_white)
    time.sleep(0.5)
    neopixel_write(RGB, pixel_off)
    time.sleep(0.5)
    
    dac.deinit()
    LED[18] = digitalio.DigitalInOut(board.GP19)
    LED[18].direction = digitalio.Direction.OUTPUT
    buzzer = pwmio.PWMOut(board.GP18, variable_frequency=True)

# Check SD Card and demo code 
def button3_handler():
       
    check_SDCARD()

    RGB.value = False
    for i in range(0,10,1):
        neopixel_write(RGB,bytearray([i,0,0]))
        play_mario_tone(i)
        time.sleep(delay1)
        
    for i in range(0,10,1):
        neopixel_write(RGB,bytearray([10-i,i,0]))
        play_mario_tone(i+10)
        time.sleep(delay1)
        
    for i in range(0,10,1):
        neopixel_write(RGB,bytearray([0,10-i,i]))
        play_mario_tone(i+20)
        time.sleep(delay1)

        
    for i in range(0,10,1):
        neopixel_write(RGB,bytearray([i,i,10]))
        play_mario_tone(i+30)
        time.sleep(delay1)

        
    for i in range(0,8,1):
        neopixel_write(RGB,bytearray([8-i,8-i,8-i]))
        play_mario_tone(i+40)
        time.sleep(delay1)

def play_mario_tone(notes):
    if mario[notes] == '0':
        buzzer.duty_cycle = 0
    else:
        buzzer.frequency = tones[mario[notes]]
        buzzer.duty_cycle = 19660

def initialize_OLED():
    global I2C
    try:
        LED[6].deinit()
        LED[7].deinit()
        global i2c
        i2c = io.I2C(board.GP7, board.GP6)
        global oled
        oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
        oled.fill(0)
        I2C = True
    except:
        LED[6] = digitalio.DigitalInOut(board.GP6)
        LED[6].direction = digitalio.Direction.OUTPUT
        LED[7] = digitalio.DigitalInOut(board.GP7)
        LED[7].direction = digitalio.Direction.OUTPUT
        I2C = False

def deinitialize_OLED():
    global oled
    oled.show()
    
    i2c.deinit()
    LED[6] = digitalio.DigitalInOut(board.GP6)
    LED[6].direction = digitalio.Direction.OUTPUT
    LED[7] = digitalio.DigitalInOut(board.GP7)
    LED[7].direction = digitalio.Direction.OUTPUT

def check_SDCARD():
    
    initialize_OLED()
    
        
    LED[10].deinit()
    LED[11].deinit()
    LED[12].deinit()
    LED[15].deinit()
    spi = busio.SPI(board.GP10, MOSI=board.GP11, MISO=board.GP12)
    cs = board.GP15
    
    try:
        global sd
        sd = sdcardio.SDCard(spi, cs)
     
        vfs = storage.VfsFat(sd)
        storage.mount(vfs, '/sd')
            
        with open("/sd/pico.txt", "w") as file:
            file.write("1. Hello, world!\r\n")
        
        with open("/sd/pico.txt", "r") as file:
             for line in file:
                if line == "1. Hello, world!\r\n":
                    for i in up:
                        buzzer.frequency = tones[i]
                        buzzer.duty_cycle = 19660
                        time.sleep(0.15)
                    buzzer.duty_cycle = 0
                    if I2C:
                        oled.text('GP22 PRESSED',30,20, 1)
                        oled.text('SD CARD TEST: PASS',7,40, 1)
                    
                else:
                    if I2C:
                        oled.text('GP22 PRESSED',30,10, 1)
                        oled.text('SD CARD TEST: FAILED',5,25, 1)
                        oled.text('WRONG DATA',33,40, 1)
                    buzzer.frequency = 1661
                    buzzer.duty_cycle = 19660
                    time.sleep(2)
                    buzzer.duty_cycle = 0 
                    time.sleep(2)
        storage.umount(vfs)
        spi.deinit()
        sd.deinit()
    except:
        if I2C:
            oled.text('GP22 PRESSED',30,10, 1)
            oled.text('SD CARD TEST: FAILED',5,25,1)
            oled.text('NO SD CARD',33,40,1)

        buzzer.frequency = 1661
        buzzer.duty_cycle = 19660
        time.sleep(2)
        buzzer.duty_cycle = 0
        spi.deinit()
    if I2C:
        deinitialize_OLED()
        
    LED[10] = digitalio.DigitalInOut(board.GP10)
    LED[10].direction = digitalio.Direction.OUTPUT
    LED[11] = digitalio.DigitalInOut(board.GP11)
    LED[11].direction = digitalio.Direction.OUTPUT
    LED[12] = digitalio.DigitalInOut(board.GP12)
    LED[12].direction = digitalio.Direction.OUTPUT
    LED[15] = digitalio.DigitalInOut(board.GP15)
    LED[15].direction = digitalio.Direction.OUTPUT

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
