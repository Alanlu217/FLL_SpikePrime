from pybricks.parameters import Port
from pybricks.hubs import InventorHub
from pybricks.pupdevices import Motor, ColorSensor
from pybricks.parameters import Port, Direction
from pybricks.geometry import Axis
from pybricks.robotics import DriveBase

import other
from drivebase import Drivebase
from gyro import Gyro

from micropython import const


class Config:
    def __init__(self):
        self.hub = InventorHub(
            front_side=Axis.Y, top_side=Axis.Z)  # type: ignore

        self.SPEED_LIST_COUNT = const(2000)
        self.ACCELERATION = const(200)
        self.STARTSPEED = const(30)
        self.TURN_SPEED_MIN = const(50)
        self.TURN_SPEED_MAX = const(400)

        self.gyro = Gyro(self.hub)

        self.leftMotor = Motor(Port.F, Direction.CLOCKWISE)
        self.rightMotor = Motor(Port.B, Direction.COUNTERCLOCKWISE)

        self.drive = Drivebase(
            self, self.gyro, self.leftMotor, self.rightMotor, 56, 88)

        self.page1 = [self.reset, self.testTurn, other.testRun1]

        self.page2 = [self.printInfo, other._lightCal,
                      self.gyroCal, other._tyreClear]

    def testTurn(self, config):
        self.drive.turnTo(90)

    def gyroCal(self, config):
        self.gyro.calibrate()

    def reset(self, config):
        self.drive.setHead()

    def printInfo(self, config):
        print(config.hub.system.name())
        print(self.hub.battery.voltage())
        config.hub.display.text(str(config.hub.system.name()), 500, 50)
        self.hub.display.text(str(self.hub.battery.voltage()), 500, 50)
