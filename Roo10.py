from config import *

class Roo10(Config):
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

        self.page1 = [self.reset, 
                        [self.drive.turnTo(90), self.drive.turnTo(180),
                        self.drive.turnTo(270), self.drive.turnTo(0)],
                     self.drive.lineFollower(100000, self.light, speed=150, kp=1.8),
                     self.drive.moveDist(10000, speed=200)]

        self.page1Names = ["Reset", "Test Turn", "Line"]

        self.page2 = [self.printInfo, self.lightCal,
                      self.gyroCal, self.tyreClean]
        self.page2Names = ["Print Info", "Light Cal", "Gyro Cal", "Tyre Clean"]
 