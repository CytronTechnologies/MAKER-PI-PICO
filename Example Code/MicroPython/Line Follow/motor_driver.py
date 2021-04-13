import machine
import utime

class motor_driver():
    def __init__(self,M1A,M1B,M2A,M2B):  # Intialize motor driver
        
        self.M1A = machine.PWM(machine.Pin(M1A))
        self.M1B = machine.PWM(machine.Pin(M1B))
        self.M2A = machine.PWM(machine.Pin(M2A))
        self.M2B = machine.PWM(machine.Pin(M2B))
    
    # Will return a integer
    def convert(self,x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

    def speed(self,speedLeft, speedRight):
        speedLeft = self.convert(speedLeft,0,100,0,65534)
        speedRight = self.convert(speedRight,0,100,0,65534)
        if speedLeft > 0:
            self.M1A.duty_u16(speedLeft)
            self.M1B.duty_u16(0)
        else:
            self.M1A.duty_u16(0)
            self.M1B.duty_u16(abs(speedLeft))

        if speedRight > 0:
            self.M2A.duty_u16(speedRight)
            self.M2B.duty_u16(0)
        else:
            self.M2A.duty_u16(0)
            self.M2B.duty_u16(abs(speedRight))
            
    def brake(self):
        self.speed(0,0)
        
