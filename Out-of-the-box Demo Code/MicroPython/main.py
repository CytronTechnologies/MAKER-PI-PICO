import machine
import utime
import array, time
from machine import Pin
import rp2
from rp2 import PIO, StateMachine, asm_pio
import _thread

B0  = 31
C1  = 33
CS1 = 35
D1  = 37
DS1 = 39
E1  = 41
F1  = 44
FS1 = 46
G1  = 49
GS1 = 52
A1  = 55
AS1 = 58
B1  = 62
C2  = 65
CS2 = 69
D2  = 73
DS2 = 78
E2  = 82
F2  = 87
FS2 = 93
G2  = 98
GS2 = 104
A2  = 110
AS2 = 117
B2  = 123
C3  = 131
CS3 = 139
D3  = 147
DS3 = 156
E3  = 165
F3  = 175
FS3 = 185
G3  = 196
GS3 = 208
A3  = 220
AS3 = 233
B3  = 247
C4  = 262
CS4 = 277
D4  = 294
DS4 = 311
E4  = 330
F4  = 349
FS4 = 370
G4  = 392
GS4 = 415
A4  = 440
AS4 = 466
B4  = 494
C5  = 523
CS5 = 554
D5  = 587
DS5 = 622
E5  = 659
F5  = 698
FS5 = 740
G5  = 784
GS5 = 831
A5  = 880
AS5 = 932
B5  = 988
C6  = 1047
CS6 = 1109
D6  = 1175
DS6 = 1245
E6  = 1319
F6  = 1397
FS6 = 1480
G6  = 1568
GS6 = 1661
A6  = 1760
AS6 = 1865
B6  = 1976
C7  = 2093
CS7 = 2217
D7  = 2349
DS7 = 2489
E7  = 2637
F7  = 2794
FS7 = 2960
G7  = 3136
GS7 = 3322
A7  = 3520
AS7 = 3729
B7  = 3951
C8  = 4186
CS8 = 4435
D8  = 4699
DS8 = 4978

# Configure the number of WS2812 LEDs.
NUM_LEDS = 1

button_1 = machine.Pin(20,machine.Pin.IN,machine.Pin.PULL_UP)
button_2 = machine.Pin(21,machine.Pin.IN,machine.Pin.PULL_UP)
button_3 = machine.Pin(22,machine.Pin.IN,machine.Pin.PULL_UP)
buzzer = machine.PWM(machine.Pin(18))

delay1 = 4

up = [C4,D4,E4]
mario = [E7, E7, 0, E7, 0, C7, E7, 0, G7, 0, 0, 0, G6, 0, 0, 0, C7, 0, 0, G6, 0, 0, E6, 0, 0, A6, 0, B6, 0, AS6, A6, 0, G6, E7, 0, G7, A7, 0, F7, G7, 0, E7, 0,C7, D7, B6, 0, 0]
start = [E7, E7, 0, E7, 0, C7, E7, 0, G7, 0, 0, 0]


for i in range(29):
    if i != 18 and i != 20 and i != 21 and i != 22 and i != 23 and i != 24:
        machine.Pin(i,machine.Pin.OUT)

def first_thread():
    audio_left = machine.PWM(machine.Pin(18))
    audio_right = machine.PWM(machine.Pin(19))
    for i in start:
        if i == 0:
            audio_left.duty_u16(0)
            audio_right.duty_u16(0)
        else:
            buzzer.freq(i)
            audio_left.duty_u16(19660)
            audio_right.duty_u16(19600) #30%
        utime.sleep(0.15)

def second_thread():
    audio_left = machine.PWM(machine.Pin(18))
    audio_right = machine.PWM(machine.Pin(19))
    for i in mario:
        if i == 0:
            audio_left.duty_u16(0)
            audio_right.duty_u16(0)
        else:
            buzzer.freq(i)
            audio_left.duty_u16(19660)
            audio_right.duty_u16(19600)
        utime.sleep(0.15)

def button1_handler(pin):
    machine.Pin(19,machine.Pin.OUT)
    button_1.irq(handler=None)
    for i in range(29):
        if i != 23 and i != 24:
            machine.Pin(i).toggle()
            
    for i in up:
        buzzer.freq(i)
        buzzer.duty_u16(19660)
        utime.sleep(0.15)
        buzzer.duty_u16(0)
    utime.sleep(0.5)
    
def button2_handler(pin):
    @asm_pio(sideset_init=PIO.OUT_LOW, out_shiftdir=PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
    def ws2812():
        T1 = 2
        T2 = 5
        T3 = 3
        label("bitloop")
        out(x, 1) .side(0) [T3 - 1]
        jmp(not_x, "do_zero") .side(1) [T1 - 1]
        jmp("bitloop") .side(1) [T2 - 1]
        label("do_zero")
        nop() .side(0) [T2 - 1]
        
    # Create the StateMachine with the ws2812 program, outputting on Pin(22).
    sm = StateMachine(0, ws2812, freq=8000000, sideset_base=Pin(28))

    # Start the StateMachine, it will wait for data on its FIFO.
    sm.active(1)

    for i in up:
        buzzer.freq(i)
        buzzer.duty_u16(19660)

        utime.sleep(0.15)
        buzzer.duty_u16(0)
    utime.sleep(0.5)

    ar = array.array("I", [0 for _ in range(NUM_LEDS)])

    ar[0] = 100
    sm.put(ar,8)
    time.sleep_ms(500)
    ar[0] = 100<<8
    sm.put(ar,8)
    time.sleep_ms(500)
    ar[0] = 100<<16
    sm.put(ar,8)
    time.sleep_ms(500)
    ar[0] = 0
    sm.put(ar,8)
    
    
def bt3_transition():
    @asm_pio(sideset_init=PIO.OUT_LOW, out_shiftdir=PIO.SHIFT_LEFT,autopull=True, pull_thresh=24)
    def ws2812():
        T1 = 2
        T2 = 5
        T3 = 3
        label("bitloop")
        out(x, 1) .side(0) [T3 - 1]
        jmp(not_x, "do_zero") .side(1) [T1 - 1]
        jmp("bitloop") .side(1) [T2 - 1]
        label("do_zero")
        nop() .side(0) [T2 - 1]
        
    # Create the StateMachine with the ws2812 program, outputting on Pin(28).
    sm = StateMachine(0, ws2812, freq=8000000, sideset_base=Pin(28))

    # Start the StateMachine, it will wait for data on its FIFO.
    sm.active(1)

    # Display a pattern on the LEDs via an array of LED RGB values.
    ar = array.array("I", [0 for _ in range(NUM_LEDS)])


    # RGB demo
    def rgb_transition():
        # grb = 0, 0, inc
        for j in range(0, 255):
            for i in range(NUM_LEDS):
                ar[i] = j
            sm.put(ar,8)
            time.sleep_ms(delay1)
        
        # grb = 0, inc, 255
        for j in range(0, 255):
            for i in range(NUM_LEDS):
                ar[i] = j<<8 | 255
            sm.put(ar,8)
            time.sleep_ms(delay1)

        # grb = 0, 255, dec
        for j in range(0, 255):
            for i in range(NUM_LEDS):
                ar[i] = 255<<8 | (255-j)
            sm.put(ar,8)
            time.sleep_ms(delay1)
            
        # grb = inc, 255, 0
        for j in range(0, 255):
            for i in range(NUM_LEDS):
                ar[i] = j<<16 | 255<<8 | 0
            sm.put(ar,8)
            time.sleep_ms(delay1)

        # grb = 255, dec, 0
        for j in range(0, 255):
            for i in range(NUM_LEDS):
                ar[i] = 255<<16 | (255-j)<<8 | 0
            sm.put(ar,8)
            time.sleep_ms(delay1)

        # grb = 255, 0, inc
        for j in range(0, 255):
            for i in range(NUM_LEDS):
                ar[i] = 255<<16 | j
            sm.put(ar,8)
            time.sleep_ms(delay1)

        # grb = 255, inc, 255
        for j in range(0, 255):
            for i in range(NUM_LEDS):
                ar[i] = 255<<16 | j<<8 | 255
            sm.put(ar,8)
            time.sleep_ms(delay1)

        # grb = dec, dec, dec
        for j in range(0, 255):
            for i in range(NUM_LEDS):
                ar[i] = (255-j)<<16 | (255-j)<<8 | (255-j)
            sm.put(ar,8)
            time.sleep_ms(delay1)
        
    rgb_transition()

def button3_handler(pin):
    _thread.start_new_thread(second_thread, ())
    bt3_transition()
        
def startup():
    _thread.start_new_thread(first_thread, ())
  
    for i in range(29):
        if i != 23 and i != 24:
            machine.Pin(i).value(1)
            utime.sleep(0.03)
            machine.Pin(i).value(0)
    for i in range(28,-1,-1):
        if i != 23 and i != 24:
            machine.Pin(i).value(1)
            utime.sleep(0.03)
            machine.Pin(i).value(0)
            
 
 
startup()

while True:
    
    button_1.irq(trigger=machine.Pin.IRQ_RISING, handler=button1_handler)
    button_2.irq(trigger=machine.Pin.IRQ_RISING, handler=button2_handler)
    button_3.irq(trigger=machine.Pin.IRQ_RISING, handler=button3_handler)
        
        


