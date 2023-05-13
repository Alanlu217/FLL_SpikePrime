from pybricks.hubs import InventorHub
from pybricks.robotics import DriveBase
from pybricks.tools import StopWatch, wait
import umath
from commands import CommandBase

from gyro import Gyro
from lightSensor import LightSensor


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
        self.SPEEDLIST = [self.getSpeed(dist)
                          for dist in range(0, config.SPEED_LIST_COUNT)]

    def getSpeed(self, distance):
        return round(umath.sqrt(distance*2*self.config.ACCELERATION + self.config.STARTSPEED**2))

    # Gets current heading
    def getHead(self):
        return (self.gyro.heading() + 180) % 360 - 180

    # Sets current heading
    def setHead(self, angle=0):
        self.gyro.reset_heading(round(angle / self.gyro.multiplier))

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

    def _turnTo(self, heading, tolerance=1, timeout=4000):
        angle = self.turnAngle(heading)
        runTime = StopWatch()
        while round(angle) not in range(-tolerance, tolerance) and runTime.time() < timeout:
            self.drive.drive(0, self.turnSpeed(angle))
            angle = self.turnAngle(heading)
        self.stop()

    def rampSpeed(self, distance, curr_distance, speedLimit):
        if curr_distance > distance / 2:
            delta_distance = round(abs(distance - curr_distance))
        else:
            delta_distance = round(abs(curr_distance))
        speed = self.SPEEDLIST[min(
            delta_distance, self.config.SPEED_LIST_COUNT-1)]
        return self.sign(speedLimit) * min(speed, abs(speedLimit))

    class moveDist(CommandBase):
        def __init__(self, distance, speed=500, heading=None, up=True, down=True, timeout=None):
            self.distance = distance
            self.speed = speed
            self.heading = heading
            self.up = up
            self.down = down
            self.timeout = timeout
            self.cancel = False
        
        def init(self, config):
            self.posDistance = abs(self.distance)
            if self.speed < 0:
                print("Error Negative speed")
                self.cancel = True
            
            if self.heading == None:
                self.heading = config.drive.getHead()
            
            self.rampSpeed_max = config.drive.rampSpeed(self.posDistance, self.posDistance/2, self.speed)
            if self.timeout == None:
                self.timeout = (self.posDistance / self.rampSpeed_max) * 2 * 1000 + 500
            
            config.drive.drive.reset()
            self.timer = StopWatch()
        
        def execute(self, config):
            self.curr_distance = abs(config.drive.drive.distance())
            if self.up == False and self.curr_distance < self.posDistance/2:
                drive_speed = self.speed
            elif self.down == False and self.curr_distance > self.posDistance/2:
                drive_speed = self.speed
            else:
                drive_speed = config.drive.rampSpeed(self.posDistance, self.curr_distance, self.speed)

            config.drive.drive.drive(drive_speed*config.drive.sign(self.distance),
                             config.drive.turnAngle(self.heading) * config.TURN_CORRECTION_SPEED)

        def end(self, config):
            config.drive.stop()
        
        def done(self, config):
            return self.curr_distance >= self.posDistance or self.timer.time() > self.timeout


    def _moveDist(self, distance, speed=500, heading=None, turn=True, up=True, down=True, timeout=None):
        posDistance = abs(distance)
        if speed < 0:
            print("Error Negative speed", speed)
            return

        if heading == None:
            heading = self.getHead()
        elif turn and abs(self.turnAngle(heading)) > 5:
            self.turnTo(heading)

        rampSpeed_max = self.rampSpeed(posDistance, posDistance/2, speed)
        if timeout == None:
            # * 2000 to double time and convert to milliseconds
            timeout = (posDistance / rampSpeed_max) * 2 * 1000 + 500
        # logData = []

        self.drive.reset()
        timer = StopWatch()
        while timer.time() < timeout:
            # print(runState.getStopFlag(), runButton.pressed())
            curr_distance = abs(self.drive.distance())
            if curr_distance >= posDistance:
                break
            if up == False and curr_distance < posDistance/2:
                drive_speed = speed
            elif down == False and curr_distance > posDistance/2:
                drive_speed = speed
            else:
                drive_speed = self.rampSpeed(posDistance, curr_distance, speed)

            self.drive.drive(drive_speed*self.sign(distance),
                             self.turnAngle(heading) * self.config.TURN_CORRECTION_SPEED)
            # print("Speed, drive_speed, distance: ", speed, drive_speed, \
            #        curr_distance)
            # logData.append([drive_speed, curr_distance])
        # print("MoveDist timeout=", timeout, "ms")
        self.stop()

    def _lineFollower(self, distance: int, sensor: LightSensor, speed=250, side=1, kp=1.2, ki=0, kd=10):
        self.drive.reset()

        lastError = 0
        integral = 0

        curr_distance = abs(self.drive.distance())
        while curr_distance < distance:
            error = 60 - sensor.readLight()

            derivative = error - lastError
            lastError = error
            integral = (integral / 2) + error

            turnRate = (error * kp) + (derivative * kd) + (integral * ki)

            ramp_speed = self.rampSpeed(distance, curr_distance, speed)

            self.drive.drive(ramp_speed, turnRate * side)

            curr_distance = abs(self.drive.distance())
        self.stop()

    def _moveArc(self, radius, heading, speed=100, timeout=10000):
        turn_rate = (360 * speed) / (umath.pi * 2 * radius)
        tolerance = int(2 * abs(speed) / 100)

        runTime = StopWatch()
        self.drive.drive(speed, turn_rate)
        while round(self.turnAngle(heading)) not in range(-tolerance, tolerance) and runTime.time() < timeout:
            pass
        self.stop()
