from pybricks.parameters import Port
from pybricks.hubs import InventorHub
from pybricks.pupdevices import Motor, ColorSensor
from pybricks.parameters import Port, Direction
from pybricks.geometry import Axis
from pybricks.robotics import DriveBase
from pybricks.tools import wait

import other
from drivebase import Drivebase
from gyro import Gyro

from micropython import const


class Config:
    def __init__(self):
        self.hub = InventorHub(
            front_side=Axis.Y, top_side=Axis.Z)  # type: ignore

        self.SPEED_LIST_COUNT = const(2000)
        self.ACCELERATION = const(400)
        self.STARTSPEED = const(70)
        self.TURN_SPEED_MIN = const(30)
        self.TURN_SPEED_MAX = const(600)
        self.TURN_CORRECTION_SPEED = const(20)

        self.gyro = Gyro(self.hub)

        self.leftMotor = Motor(Port.F, Direction.CLOCKWISE)
        self.rightMotor = Motor(Port.B, Direction.COUNTERCLOCKWISE)

        self.drive = Drivebase(
            self, self.gyro, self.leftMotor, self.rightMotor, 56, 88)

        self.page1 = [self.reset, self.testTurn, other.testRun1]

        self.page2 = [self.printInfo, other._lightCal,
                      self.gyroCal, self.tyreClean]

    def testTurn(self, config):
        self.drive.turnTo(90)

    def gyroCal(self, config):
        self.gyro.calibrate()

    def tyreClean(self, config):
        config.drive.drive.drive(100, 0)
        wait(200)
        while (len(config.hub.buttons.pressed()) == 0):
            pass
        config.drive.drive.stop()

    def reset(self, config):
        self.drive.setHead()

    def printInfo(self, config):
        print(config.hub.system.name())
        print(self.hub.battery.voltage())
        config.hub.display.text(str(config.hub.system.name()), 500, 50)
        self.hub.display.text(str(self.hub.battery.voltage()), 500, 50)
