from pybricks.pupdevices import ColorSensor
from pybricks.hubs import InventorHub
from ustruct import unpack, pack

# Wrapper class for colorsensor
# Allows for calibration of lightsensor


class LightSensor:
    def __init__(self, port, hub: InventorHub):
        self.sensor = ColorSensor(port)
        self.hub = hub
        self.min = 0
        self.max = 100

    # Used to set each object's calibration values
    def setCalValues(self, min, max):
        self.min = min
        self.max = max
        #print(self.port, self.min, self.max)

    def saveValues(self):
        bmin = bytes(bytearray(pack("f", self.min)))
        bmax = bytes(bytearray(pack("f", self.max)))
        self.hub.system.storage(4, write=bmin)
        self.hub.system.storage(8, write=bmax)

    def loadValues(self):
        self.min = unpack("f", self.hub.system.storage(4, read=4))[0]
        self.max = unpack("f", self.hub.system.storage(8, read=4))[0]

    # Calibrated version of colorsensor reflection()
    def readLight(self):
        raw_value = self.sensor.reflection()
        if raw_value <= self.min:
            return 0
        elif raw_value >= self.max:
            return 100
        output = ((raw_value - self.min) / (self.max - self.min)) * 100
        return round(output)

    def color(self):
        return self.sensor.color()
