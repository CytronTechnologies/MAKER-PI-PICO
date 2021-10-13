import board
import digitalio
import time
import pyRTOS

def led1(self):
    ledpin1 = digitalio.DigitalInOut(board.GP0)
    ledpin1.direction = digitalio.Direction.OUTPUT
    ledpin1.value = False
    yield

    while True:
        ledpin1.value = not ledpin1.value
        yield [pyRTOS.timeout(1)]

def led2(self):
    ledpin2 = digitalio.DigitalInOut(board.GP1)
    ledpin2.direction = digitalio.Direction.OUTPUT
    ledpin2.value = False
    yield

    while True:
        ledpin2.value = not ledpin2.value
        yield [pyRTOS.timeout(0.95)]

def led3(self):
    ledpin3 = digitalio.DigitalInOut(board.GP2)
    ledpin3.direction = digitalio.Direction.OUTPUT
    ledpin3.value = False
    yield

    while True:
        ledpin3.value = not ledpin3.value
        yield [pyRTOS.timeout(0.90)]

def led4(self):
    ledpin4 = digitalio.DigitalInOut(board.GP3)
    ledpin4.direction = digitalio.Direction.OUTPUT
    ledpin4.value = False
    yield

    while True:
        ledpin4.value = not ledpin4.value
        yield [pyRTOS.timeout(0.85)]

def led5(self):
    ledpin5 = digitalio.DigitalInOut(board.GP4)
    ledpin5.direction = digitalio.Direction.OUTPUT
    ledpin5.value = False
    yield

    while True:
        ledpin5.value = not ledpin5.value
        yield [pyRTOS.timeout(0.80)]

def led6(self):
    ledpin6 = digitalio.DigitalInOut(board.GP5)
    ledpin6.direction = digitalio.Direction.OUTPUT
    ledpin6.value = False
    yield

    while True:
        ledpin6.value = not ledpin6.value
        yield [pyRTOS.timeout(0.75)]

def led7(self):
    ledpin7 = digitalio.DigitalInOut(board.GP6)
    ledpin7.direction = digitalio.Direction.OUTPUT
    ledpin7.value = False
    yield

    while True:
        ledpin7.value = not ledpin7.value
        yield [pyRTOS.timeout(0.70)]

def led8(self):
    ledpin8 = digitalio.DigitalInOut(board.GP7)
    ledpin8.direction = digitalio.Direction.OUTPUT
    ledpin8.value = False
    yield

    while True:
        ledpin8.value = not ledpin8.value
        yield [pyRTOS.timeout(0.65)]

def led9(self):
    ledpin9 = digitalio.DigitalInOut(board.GP8)
    ledpin9.direction = digitalio.Direction.OUTPUT
    ledpin9.value = False
    yield

    while True:
        ledpin9.value = not ledpin9.value
        yield [pyRTOS.timeout(0.60)]

def led10(self):
    ledpin10 = digitalio.DigitalInOut(board.GP9)
    ledpin10.direction = digitalio.Direction.OUTPUT
    ledpin10.value = False
    yield

    while True:
        ledpin10.value = not ledpin10.value
        yield [pyRTOS.timeout(0.55)]

def led11(self):
    ledpin11 = digitalio.DigitalInOut(board.GP10)
    ledpin11.direction = digitalio.Direction.OUTPUT
    ledpin11.value = False
    yield

    while True:
        ledpin11.value = not ledpin11.value
        yield [pyRTOS.timeout(0.50)]

def led12(self):
    ledpin12 = digitalio.DigitalInOut(board.GP11)
    ledpin12.direction = digitalio.Direction.OUTPUT
    ledpin12.value = False
    yield

    while True:
        ledpin12.value = not ledpin12.value
        yield [pyRTOS.timeout(0.45)]

def led13(self):
    ledpin13 = digitalio.DigitalInOut(board.GP12)
    ledpin13.direction = digitalio.Direction.OUTPUT
    ledpin13.value = False
    yield

    while True:
        ledpin13.value = not ledpin13.value
        yield [pyRTOS.timeout(0.40)]

def led14(self):
    ledpin14 = digitalio.DigitalInOut(board.GP13)
    ledpin14.direction = digitalio.Direction.OUTPUT
    ledpin14.value = False
    yield

    while True:
        ledpin14.value = not ledpin14.value
        yield [pyRTOS.timeout(0.35)]

def led15(self):
    ledpin15 = digitalio.DigitalInOut(board.GP14)
    ledpin15.direction = digitalio.Direction.OUTPUT
    ledpin15.value = False
    yield

    while True:
        ledpin15.value = not ledpin15.value
        yield [pyRTOS.timeout(0.30)]

def led16(self):
    ledpin16 = digitalio.DigitalInOut(board.GP15)
    ledpin16.direction = digitalio.Direction.OUTPUT
    ledpin16.value = False
    yield

    while True:
        ledpin16.value = not ledpin16.value
        yield [pyRTOS.timeout(0.25)]

pyRTOS.add_task(pyRTOS.Task(led1, name="1"))
pyRTOS.add_task(pyRTOS.Task(led2, name="2"))
pyRTOS.add_task(pyRTOS.Task(led3, name="3"))
pyRTOS.add_task(pyRTOS.Task(led4, name="4"))
pyRTOS.add_task(pyRTOS.Task(led5, name="5"))
pyRTOS.add_task(pyRTOS.Task(led6, name="6"))
pyRTOS.add_task(pyRTOS.Task(led7, name="7"))
pyRTOS.add_task(pyRTOS.Task(led8, name="8"))
pyRTOS.add_task(pyRTOS.Task(led9, name="9"))
pyRTOS.add_task(pyRTOS.Task(led10, name="10"))
pyRTOS.add_task(pyRTOS.Task(led11, name="11"))
pyRTOS.add_task(pyRTOS.Task(led12, name="12"))
pyRTOS.add_task(pyRTOS.Task(led13, name="13"))
pyRTOS.add_task(pyRTOS.Task(led14, name="14"))
pyRTOS.add_task(pyRTOS.Task(led15, name="15"))
pyRTOS.add_task(pyRTOS.Task(led16, name="16"))

pyRTOS.start()
