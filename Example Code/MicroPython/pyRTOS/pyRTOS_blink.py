import machine
import utime
import pyRTOS

def led1(self):
    ledpin1 = machine.Pin(0, machine.Pin.OUT)
    ledpin1.value(0)
    yield
    
    while True:
        ledpin1.toggle()
        yield [pyRTOS.timeout(1)]

def led2(self):
    ledpin2 = machine.Pin(1, machine.Pin.OUT)
    ledpin2.value(0)
    yield
    
    while True:
        ledpin2.toggle()
        yield [pyRTOS.timeout(0.95)]
    
def led3(self):
    ledpin3 = machine.Pin(2, machine.Pin.OUT)
    ledpin3.value(0)
    yield
    
    while True:
        ledpin3.toggle()
        yield [pyRTOS.timeout(0.90)]

def led4(self):
    ledpin4 = machine.Pin(3, machine.Pin.OUT)
    ledpin4.value(0)
    yield
    
    while True:
        ledpin4.toggle()
        yield [pyRTOS.timeout(0.85)]

def led5(self):
    ledpin5 = machine.Pin(4, machine.Pin.OUT)
    ledpin5.value(0)
    yield
    
    while True:
        ledpin5.toggle()
        yield [pyRTOS.timeout(0.80)]

def led6(self):
    ledpin6 = machine.Pin(5, machine.Pin.OUT)
    ledpin6.value(0)
    yield
    
    while True:
        ledpin6.toggle()
        yield [pyRTOS.timeout(0.75)]

def led7(self):
    ledpin7 = machine.Pin(6, machine.Pin.OUT)
    ledpin7.value(0)
    yield
    
    while True:
        ledpin7.toggle()
        yield [pyRTOS.timeout(0.70)]

def led8(self):
    ledpin8 = machine.Pin(7, machine.Pin.OUT)
    ledpin8.value(0)
    yield
    
    while True:
        ledpin8.toggle()
        yield [pyRTOS.timeout(0.65)]

def led9(self):
    ledpin9 = machine.Pin(8, machine.Pin.OUT)
    ledpin9.value(0)
    yield
    
    while True:
        ledpin9.toggle()
        yield [pyRTOS.timeout(0.60)]


def led10(self):
    ledpin10 = machine.Pin(9, machine.Pin.OUT)
    ledpin10.value(0)
    yield

    while True:
        ledpin10.toggle()
        yield [pyRTOS.timeout(0.55)]

def led11(self):
    ledpin11 = machine.Pin(10, machine.Pin.OUT)
    ledpin11.value(0)
    yield

    while True:
        ledpin11.toggle()
        yield [pyRTOS.timeout(0.50)]

def led12(self):
    ledpin12 = machine.Pin(11, machine.Pin.OUT)
    ledpin12.value(0)
    yield

    while True:
        ledpin12.toggle()
        yield [pyRTOS.timeout(0.45)]

def led13(self):
    ledpin13 = machine.Pin(12, machine.Pin.OUT)
    ledpin13.value(0)
    yield

    while True:
        ledpin13.toggle()
        yield [pyRTOS.timeout(0.40)]

def led14(self):
    ledpin14 = machine.Pin(13, machine.Pin.OUT)
    ledpin14.value(0)
    yield

    while True:
        ledpin14.toggle()
        yield [pyRTOS.timeout(0.35)]

def led15(self):
    ledpin15 = machine.Pin(14, machine.Pin.OUT)
    ledpin15.value(0)
    yield

    while True:
        ledpin15.toggle()
        yield [pyRTOS.timeout(0.30)]

def led16(self):
    ledpin16 = machine.Pin(15, machine.Pin.OUT)
    ledpin16.value(0)
    yield

    while True:
        ledpin16.toggle()
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