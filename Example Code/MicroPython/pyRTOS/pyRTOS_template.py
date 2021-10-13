import pyRTOS

def Task1(self):
    # Task1 setup
    yield

    while True:
        # Task1 loop
        yield [pyRTOS.timeout(1)]           # Delay in seconds (Other task can run)
        
pyRTOS.add_task(pyRTOS.Task(led1))          # Add Task
pyRTOS.start()                              # Start pyRTOS