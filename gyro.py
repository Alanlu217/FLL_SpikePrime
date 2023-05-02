from pybricks.hubs import InventorHub
from pybricks.tools import wait
from ustruct import unpack, pack


class Gyro:
    def __init__(self, hub: InventorHub):
        self.hub: InventorHub = hub
        self.gyro = hub.imu

        self.readCal()
        print(self.multiplier)
        if (self.multiplier == 0):
            self.multiplier = 1

    def calibrate(self):
        self.gyro.reset_heading(0)
        wait(500)
        while len(self.hub.buttons.pressed()) == 0:
            wait(100)

        self.multiplier = 180 / self.gyro.heading()
        self.writeCal()

    def readCal(self):
        self.multiplier = unpack("f", self.hub.system.storage(0, read=4))[0]

    def writeCal(self):
        b = bytes(bytearray(pack("f", self.multiplier)))
        self.hub.system.storage(0, write=b)

    def heading(self):
        return self.gyro.heading() * self.multiplier

    def reset_heading(self, angle: int = 0):
        self.gyro.reset_heading(angle)
