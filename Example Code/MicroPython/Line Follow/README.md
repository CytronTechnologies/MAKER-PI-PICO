This code will use Maker Pi Pico to receive the data from Maker Line and adjust the motor speed to right direction following the line.

# Requirements  
**Hardware:**  
* [Maker Pi Pico](https://cytron.io/p-maker-pi-pico?r=1)  
* [Maker Line: Simplifying Line Sensor For Beginner](https://cytron.io/p-maker-line-simplifying-line-sensor-for-beginner?r=1)
* [Maker Drive: Simplifying H-Bridge Motor Driver for Beginner](https://cytron.io/p-maker-drive-simplifying-h-bridge-motor-driver-for-beginner)

# Connection  

The connections between Maker Pi Pico, Maker Line, Maker Drive for this code is as table below:
| Maker Pi Pico | Maker Line | Maker Drive |
| ------------- | -----------|------------ |
| GND           | GND        |GND          |
| 3V3           | VCC        |             |
| GP26          | AN         |             |
| VSYS          |            |5VO          |
| GP2           |            |M2A          |
| GP3           |            |M2B          |
| GP4           |            |M1A          |
| GP5           |            |M1B          |

For more details tutorial you can visit this link on how to [Building Line Following Robot using Maker Pi Pico, Maker Drive and Maker Line](https://cytron.io/tutorial/building-line-following-robot-using-maker-pi-pico-maker-drive-and-maker-line?r=1). 
