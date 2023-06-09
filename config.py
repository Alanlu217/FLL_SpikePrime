from pybricks.parameters import Port
from pybricks.hubs import InventorHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction, Button, Color
from pybricks.geometry import Axis
from pybricks.tools import wait

from drivebase import Drivebase
from lightSensor import LightSensor
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
        self.TURN_CORRECTION_SPEED = const(5)

        self.curr = 0

        self.gyro = Gyro(self.hub)

        self.light = LightSensor(Port.B, self.hub)
        self.light.loadValues()

        self.leftMotor = Motor(Port.C, Direction.COUNTERCLOCKWISE)
        self.rightMotor = Motor(Port.D, Direction.CLOCKWISE)

        self.drive = Drivebase(
            self, self.gyro, self.leftMotor, self.rightMotor, 56, 112)

        self.page1 = [self.reset, self.testTurn, self.testRun1]

        self.page1Names = ["Reset", "Test Turn", "Test Run 1"]

        self.page2 = [self.printInfo, self.lightCal,
                      self.gyroCal, self.tyreClean]
        self.page2Names = ["Print Info", "Light Cal", "Gyro Cal", "Tyre Clean"]

    def testTurn(self, config):
        self.drive.turnTo(self.curr)
        self.curr += 90

    def printInfo(self, config):
        print(config.hub.system.name())
        print(self.hub.battery.voltage())
        config.hub.display.text(str(config.hub.system.name()), 500, 50)
        self.hub.display.text(str(self.hub.battery.voltage()), 500, 50)

    def lightCal(self, config):
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
        config.drive.drive.drive(100, 0)
        wait(200)
        while (len(config.hub.buttons.pressed()) == 0):
            pass
        config.drive.drive.stop()

    def reset(self, config):
        self.drive.stop()
        self.drive.setHead()

    def testRun1(self, config):
        self.drive.moveDist(100000, speed=100)