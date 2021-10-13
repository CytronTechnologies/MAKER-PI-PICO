import machine
import pyRTOS

def task1(self):
    ledpin1 = machine.Pin(0, machine.Pin.OUT)
    ledpin1.value(0)
    yield
    
    while True:
        ledpin1.toggle()
        yield [pyRTOS.timeout(1)]

def task2(self):
    ledpin2 = machine.Pin(1, machine.Pin.OUT)
    ledpin2.value(0)
    yield
    
    while True:
        ledpin2.toggle()
        yield [pyRTOS.timeout(0.95)]
    
def task3(self):
    ledpin3 = machine.Pin(2, machine.Pin.OUT)
    ledpin3.value(0)
    yield
    
    while True:
        ledpin3.toggle()
        yield [pyRTOS.timeout(0.90)]

def task4(self):
    ledpin4 = machine.Pin(3, machine.Pin.OUT)
    ledpin4.value(0)
    yield
    
    while True:
        ledpin4.toggle()
        yield [pyRTOS.timeout(0.85)]

def task5(self):
    ledpin5 = machine.Pin(4, machine.Pin.OUT)
    ledpin5.value(0)
    yield
    
    while True:
        ledpin5.toggle()
        yield [pyRTOS.timeout(0.80)]

def task6(self):
    ledpin6 = machine.Pin(5, machine.Pin.OUT)
    ledpin6.value(0)
    yield
    
    while True:
        ledpin6.toggle()
        yield [pyRTOS.timeout(0.75)]

def task7(self):
    ledpin7 = machine.Pin(6, machine.Pin.OUT)
    ledpin7.value(0)
    yield
    
    while True:
        ledpin7.toggle()
        yield [pyRTOS.timeout(0.70)]

def task8(self):
    ledpin8 = machine.Pin(7, machine.Pin.OUT)
    ledpin8.value(0)
    yield
    
    while True:
        ledpin8.toggle()
        yield [pyRTOS.timeout(0.65)]

def task9(self):
    ledpin9 = machine.Pin(8, machine.Pin.OUT)
    ledpin9.value(0)
    yield
    
    while True:
        ledpin9.toggle()
        yield [pyRTOS.timeout(0.60)]


def task10(self):
    ledpin10 = machine.Pin(9, machine.Pin.OUT)
    ledpin10.value(0)
    yield

    while True:
        ledpin10.toggle()
        yield [pyRTOS.timeout(0.55)]

def task11(self):
    ledpin11 = machine.Pin(10, machine.Pin.OUT)
    ledpin11.value(0)
    yield

    while True:
        ledpin11.toggle()
        yield [pyRTOS.timeout(0.50)]

def task12(self):
    ledpin12 = machine.Pin(11, machine.Pin.OUT)
    ledpin12.value(0)
    yield

    while True:
        ledpin12.toggle()
        yield [pyRTOS.timeout(0.45)]

def task13(self):
    ledpin13 = machine.Pin(12, machine.Pin.OUT)
    ledpin13.value(0)
    yield

    while True:
        ledpin13.toggle()
        yield [pyRTOS.timeout(0.40)]

def task14(self):
    ledpin14 = machine.Pin(13, machine.Pin.OUT)
    ledpin14.value(0)
    yield

    while True:
        ledpin14.toggle()
        yield [pyRTOS.timeout(0.35)]

def task15(self):
    ledpin15 = machine.Pin(14, machine.Pin.OUT)
    ledpin15.value(0)
    yield

    while True:
        ledpin15.toggle()
        yield [pyRTOS.timeout(0.30)]

def task16(self):
    ledpin16 = machine.Pin(15, machine.Pin.OUT)
    ledpin16.value(0)
    yield

    while True:
        ledpin16.toggle()
        yield [pyRTOS.timeout(0.25)]

pyRTOS.add_task(pyRTOS.Task(task1))
pyRTOS.add_task(pyRTOS.Task(task2))
pyRTOS.add_task(pyRTOS.Task(task3))
pyRTOS.add_task(pyRTOS.Task(task4))
pyRTOS.add_task(pyRTOS.Task(task5))
pyRTOS.add_task(pyRTOS.Task(task6))
pyRTOS.add_task(pyRTOS.Task(task7))
pyRTOS.add_task(pyRTOS.Task(task8))
pyRTOS.add_task(pyRTOS.Task(task9))
pyRTOS.add_task(pyRTOS.Task(task10))
pyRTOS.add_task(pyRTOS.Task(task11))
pyRTOS.add_task(pyRTOS.Task(task12))
pyRTOS.add_task(pyRTOS.Task(task13))
pyRTOS.add_task(pyRTOS.Task(task14))
pyRTOS.add_task(pyRTOS.Task(task15))
pyRTOS.add_task(pyRTOS.Task(task16))

pyRTOS.start()
