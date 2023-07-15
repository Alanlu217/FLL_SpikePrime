from pybricks.parameters import Port
from pybricks.hubs import InventorHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction, Button, Color
from pybricks.geometry import Axis
from pybricks.robotics import DriveBase
from pybricks.tools import wait

from drivebase import Drivebase
from lightSensor import LightSensor
from gyro import Gyro

from micropython import const

class Config:
    def __init__(self, hub):
        self.hub: InventorHub = hub 
    
    def stop(self):
        pass

    def stop(self):
        """
        Function called at end of each run.

        Should stop everything from moving
        """
        self.drive.stop()

    def printInfo(self, config):
        """
        Prints info to the hub display
        """
        print(config.hub.system.name())
        print(self.hub.battery.voltage())
        config.hub.display.text(str(config.hub.system.name()), 150, 10)
        self.hub.display.text(str(self.hub.battery.voltage()), 250, 10)

    def lightCal(self, config):
        """
        Moves robot over a line and measures min and max light readings.

        Uses this to calibrate the light sensor.

        Also stores values to internal storage.
        """
        lmin = 100
        lmax = 0
        cancel = False

        config.drive.drive.reset()
        config.drive.drive.drive(50, 0)
        while self.drive.drive.distance() < 100:
            lmax = max(self.light.sensor.reflection(), lmax)
            lmin = min(self.light.sensor.reflection(), lmin)
        config.drive.stop()

        print("light %2i:%2i" % (lmin, lmax))

        config.hub.display.text("S?")
        buttons = config.hub.buttons.pressed()
        while len(buttons) == 0:
            buttons = config.hub.buttons.pressed()

        if Button.BLUETOOTH in buttons:
            config.light.setCalValues(lmin, lmax)
            config.light.saveValues()
            self.hub.light.on(Color.GREEN)
        else:
            self.hub.light.on(Color.RED)
        wait(100)

    def gyroCal(self, config):
        """
        Calibrates gyro and stores values to internal storage.

        Steps:
        1. Spin robot 3 times
        2. Press center button to finish
        3. Press bluetooth button to save values
        """
        val = config.gyro.calibrate()

        config.hub.display.text("S?")

        buttons = config.hub.buttons.pressed()
        while len(buttons) == 0:
            buttons = config.hub.buttons.pressed()

        if Button.BLUETOOTH in buttons:
            config.gyro.setCal(val)
            config.gyro.writeCal()
            self.hub.light.on(Color.GREEN)
        else:
            self.hub.light.on(Color.RED)
        wait(100)

    def tyreClean(self, config):
        """
        Spins drive motors at a constant speed

        Waits for button press to finish
        """
        config.drive.drive.drive(100, 0)
        wait(200)
        while (len(config.hub.buttons.pressed()) == 0):
            pass
        config.drive.drive.stop()

    def reset(self, config):
        self.drive.setHead()