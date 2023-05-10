from pybricks.hubs import InventorHub
from pybricks.tools import wait
from pybricks.parameters import Button
from ustruct import unpack, pack


class Gyro:
    def __init__(self, hub: InventorHub):
        self.hub: InventorHub = hub
        self.gyro = hub.imu

        self.readCal()
        if (self.multiplier == 0):
            self.multiplier = 1

    def calibrate(self):
        self.gyro.reset_heading(0)
        wait(500)
        while True:
            if (Button.CENTER in self.hub.buttons.pressed()):
                return 1080 / abs(self.gyro.heading())
            elif (len(self.hub.buttons.pressed()) > 0):
                break
            wait(100)

    def readCal(self):
        self.multiplier = unpack("f", self.hub.system.storage(0, read=4))[0]

    def writeCal(self):
        b = bytes(bytearray(pack("f", self.multiplier)))
        self.hub.system.storage(0, write=b)

    def heading(self):
        return self.gyro.heading() * self.multiplier

    def reset_heading(self, angle: int = 0):
        self.gyro.reset_heading(angle)

    def setCal(self, num):
        self.multiplier = num
