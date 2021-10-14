Credit to Ben Williams for coding the pyRTOS https://github.com/Rybec/pyRTOS

# Basic Usage

A simple pyRTOS program consists of defining tasks functions and adding the tasks into the OS using `add_task()` function. 
Once all tasks are added, the start() function is used to start the RTOS.

Once started, the RTOS will schedule time for tasks, giving tasks CPU time based on a priority scheduling algorithm. When the tasks are well behaved, designed to work together, and given the right priorities, the operating system will orchestrate them so they work together to accomplish whatever goal the program was designed for.

Use the template file to begin working with pyRTOS. The blink file also provide an example of controlling 16 tasks, each blinking at different rates.

For other advanced usage, please refer to https://github.com/Rybec/pyRTOS
