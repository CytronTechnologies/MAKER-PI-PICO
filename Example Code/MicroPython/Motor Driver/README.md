This code will use Maker Pi Pico to control the motor speed.

# Requirements  
**Hardware:**  
* [Maker Pi Pico](https://cytron.io/p-maker-pi-pico?r=1)  
* [Maker Drive: Simplifying H-Bridge Motor Driver for Beginner](https://cytron.io/p-maker-drive-simplifying-h-bridge-motor-driver-for-beginner)  

**Software:**  
Make sure to use [micropython firmware](https://micropython.org/download/rp2-pico/) on the Maker Pi Pico and run ```drive motor.py``` file.

# Connection  

The connections between Maker Pi Pico, Maker Line, Maker Drive for this code is as table below:
| Maker Pi Pico | Maker Drive |
| ------------- |------------ |
| GND           |GND          |
| VSYS          |5VO          |
| GP2           |M2A          |
| GP3           |M2B          |
| GP4           |M1A          |
| GP5           |M1B          |

Connect the VB+ and VB- on the Maker Drive with external battery or power supply in range 2.5V-9.5V.

For advanced tutorial you can visit this link on how to [Building Line Following Robot using Maker Pi Pico, Maker Drive and Maker Line](https://cytron.io/tutorial/building-line-following-robot-using-maker-pi-pico-maker-drive-and-maker-line?r=1). 
