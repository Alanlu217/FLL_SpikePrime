from pybricks.hubs import InventorHub
from pybricks.tools import wait

class Gyro:
    def __init__(self, hub: InventorHub):
        self.hub = hub
        self.gyro = hub.imu
        self.multiplier = 1
    
    def calibrate(self):
        self.gyro.reset_heading(0)
        while len(self.hub.buttons.pressed()) == 0:
            wait(100)
        
        self.multiplier = 180 / self.gyro.heading()
    
    def heading(self):
        return self.gyro.heading() * self.multiplier
    
    def reset_heading(self, angle: int=0):
        self.gyro.reset_heading(angle)