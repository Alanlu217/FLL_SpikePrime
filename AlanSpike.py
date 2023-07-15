from config import *

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
