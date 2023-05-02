from pybricks.hubs import InventorHub
from pybricks.robotics import DriveBase
from pybricks.tools import StopWatch, wait
import umath

from gyro import Gyro


class Drivebase:
    def __init__(self, config, gyro, leftMotor, rightMotor, wheelDiameter, axleTrack):
        self.config = config
        self.hub: InventorHub = config.hub

        self.gyro: Gyro = gyro

        self.leftMotor = leftMotor
        self.rightMotor = rightMotor

        self.wheelDiameter = wheelDiameter
        self.axleTrack = axleTrack

        self.drive = DriveBase(self.leftMotor, self.rightMotor,
                               self.wheelDiameter, self.axleTrack)

    def getSpeed(self, distance):
        return round(umath.sqrt(distance*2*self.config.ACCELERATION + self.config.STARTSPEED**2))

    # Gets current heading
    def getHead(self):
        return (self.gyro.heading() + 180) % 360 - 180

    # Sets current heading
    def setHead(self, angle=0):
        self.gyro.reset_heading(angle)

    def sign(self, x):
        return 1 if x >= 0 else -1

    def limit(self, input, bound):
        return max(min(input, bound[1]), bound[0])

    def stop(self):
        self.drive.stop()

    def turnSpeed(self, angle):
        turn_speed = angle / 180 * (self.config.TURN_SPEED_MAX - self.config.TURN_SPEED_MIN) +\
            self.sign(angle) * self.config.TURN_SPEED_MIN
        return turn_speed

    def turnAngle(self, heading):
        return (heading - self.getHead() + 180) % 360 - 180

    def turnTo(self, heading, tolerance=2, timeout=4000):
        angle = self.turnAngle(heading)
        runTime = StopWatch()
        while angle not in range(-tolerance, tolerance) and runTime.time() < timeout:
            self.drive.drive(0, self.turnSpeed(angle))
            angle = self.turnAngle(heading)
        self.stop()
