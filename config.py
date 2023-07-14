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

class ConfigAlanSpike(Config):
    def __init__(self, hub):
        self.hub = hub

        # Sets up the constants for the drivebase
        self.SPEED_LIST_COUNT = const(2000)
        self.ACCELERATION = const(400)
        self.STARTSPEED = const(70)
        self.TURN_SPEED_MIN = const(30)
        self.TURN_SPEED_MAX = const(600)
        self.TURN_CORRECTION_SPEED = const(20)

        self.gyro = Gyro(self.hub) # Gets the gyro as an object

        self.light = LightSensor(Port.D, self.hub) # Creates a light sensor object
        self.light.loadValues() # Loads calibration values from internal storage

        # Sets up drive motors
        self.leftMotor = Motor(Port.F, Direction.CLOCKWISE)
        self.rightMotor = Motor(Port.B, Direction.COUNTERCLOCKWISE)

        # Sets up drivebase
        self.drive = Drivebase(
            self, self.gyro, self.leftMotor, self.rightMotor, 56, 88)

        # Sets up the menu
        self.page1 = [self.reset, [self.drive.turnTo(90), self.drive.turnTo(180), self.drive.turnTo(270), self.drive.turnTo(0)], self.drive.lineFollower(100000, self.light, speed=150, kp=1.2)] # Page 1

        self.page1Names = ["Reset", "Test Turn", "Test Run 1"] # Names for page 1

        self.page2 = [self.printInfo, self.lightCal,
                      self.gyroCal, self.tyreClean] # Page 2
        self.page2Names = ["Print Info", "Light Cal", "Gyro Cal", "Tyre Clean"] # Names for page 2

class ConfigBasicRobot(Config):
    def __init__(self, hub):
        self.hub = hub

        self.SPEED_LIST_COUNT = const(2000)
        self.ACCELERATION = const(400)
        self.STARTSPEED = const(70)
        self.TURN_SPEED_MIN = const(40)
        self.TURN_SPEED_MAX = const(600)
        self.TURN_CORRECTION_SPEED = const(5)

        self.curr = 0

        self.gyro = Gyro(self.hub)

        self.light = LightSensor(Port.B, self.hub)
        self.light.loadValues()

        self.leftMotor = Motor(Port.C, Direction.COUNTERCLOCKWISE)
        self.rightMotor = Motor(Port.D, Direction.CLOCKWISE)

        self.drive = Drivebase(
            self, self.gyro, self.leftMotor, self.rightMotor, 56, 112)

        self.page1 = [self.reset, [self.drive.turnTo(90), self.drive.turnTo(180), self.drive.turnTo(270), self.drive.turnTo(0)], self.drive.lineFollower(100000, self.light, speed=150, kp=1.8)]

        self.page1Names = ["Reset", "Test Turn", "Line"]

        self.page2 = [self.printInfo, self.lightCal,
                      self.gyroCal, self.tyreClean]
        self.page2Names = ["Print Info", "Light Cal", "Gyro Cal", "Tyre Clean"]
 