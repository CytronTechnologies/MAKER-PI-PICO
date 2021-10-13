import pyRTOS

def task1(self):
    # Task1 setup here
    yield

    while True:
        # Task1 loop here
        yield [pyRTOS.timeout(1)]           # Delay in seconds (Other task can run)
        
pyRTOS.add_task(pyRTOS.Task(task1))          # Add Task
pyRTOS.start()                              # Start pyRTOS
