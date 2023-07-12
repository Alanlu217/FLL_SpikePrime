from pybricks.pupdevices import ColorSensor
from pybricks.hubs import InventorHub
from ustruct import unpack, pack


class LightSensor:
    """
    Wrapper class for ColorSensor().
    Allows for calibration
    """
    def __init__(self, port, hub: InventorHub):
        self.sensor = ColorSensor(port)
        self.hub = hub
        self.min = 0
        self.max = 100

    def setCalValues(self, min, max):
        """
        Used to set each object's calibration values
        """

        self.min = min
        self.max = max
        #print(self.port, self.min, self.max)

    def saveValues(self):
        """
        Saves calibration values to internal storage
        """

        bmin = bytes(bytearray(pack("f", self.min)))
        bmax = bytes(bytearray(pack("f", self.max)))
        self.hub.system.storage(4, write=bmin)
        self.hub.system.storage(8, write=bmax)

    def loadValues(self):
        """
        Loads calibration values to internal storage
        """

        self.min = unpack("f", self.hub.system.storage(4, read=4))[0]
        self.max = unpack("f", self.hub.system.storage(8, read=4))[0]

    def readLight(self):
        """
        Calibrated version of colorsensor reflection()
        """

        raw_value = self.sensor.reflection()
        if raw_value <= self.min:
            return 0
        elif raw_value >= self.max:
            return 100
        output = ((raw_value - self.min) / (self.max - self.min)) * 100
        return round(output)

    def color(self):
        """
        Returns detected color
        """

        return self.sensor.color()
