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
        """
        Calibrates on-board gyro

        Steps:
        Turn robot three times. Press center button to stop. Press Bluetooth button to save.
        """
        self.gyro.reset_heading(0)
        wait(500)
        while True:
            if (Button.CENTER in self.hub.buttons.pressed()):
                val = abs(self.gyro.heading())
                break
            wait(50)
        num = 1
        wait(200)
        buttons = self.hub.buttons.pressed()
        while True:
            self.hub.display.char(str(num))
            wait(200)
            if Button.LEFT in buttons:
                num -= 1
            elif Button.RIGHT in buttons:
                num += 1
            elif Button.CENTER in buttons:
                return (360 * num) / val
            num = min(9, max(1, num))
            buttons = self.hub.buttons.pressed()

    def readCal(self):
        """
        Loads calibration value from internal storage
        """
        self.multiplier = unpack("f", self.hub.system.storage(0, read=4))[0]

    def writeCal(self):
        """
        Saves calibration value to internal storage
        """
        b = bytes(bytearray(pack("f", self.multiplier)))
        self.hub.system.storage(0, write=b)

    def heading(self):
        """
        Returns calibrated heading of robot
        """
        return self.gyro.heading() * self.multiplier

    def reset_heading(self, angle: int = 0):
        """
        Resets current heading

        Defaults to 0
        """
        self.gyro.reset_heading(angle)

    def setCal(self, num):
        """
        Manual override to set calibration value
        """
        self.multiplier = num
