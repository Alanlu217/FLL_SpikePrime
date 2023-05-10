from pybricks.hubs import InventorHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop, Icon
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

import umath
import uselect
import usys
from config import Config


class menu:
    def __init__(self, config: Config, pages: list, pageName: list, volume: int = 100):
        self.config = config
        self.hub = config.hub

        self.pages = pages
        self.pageNames = pageName

        self.numPages = len(self.pages)

        self.page = 0
        self.index = 0

        self.hub.system.set_stop_button((Button.LEFT, Button.RIGHT))
        self.hub.speaker.volume(volume)
        self.config.hub.light.on(Color.WHITE)

        self.keyboard = uselect.poll()
        self.keyboard.register(usys.stdin, uselect.POLLIN)  # type: ignore
        self.timer = StopWatch()
        self.timer.resume()

        self.bluetooth_pressed = False
        self.last_time_help = 0

    def update(self):

        # print(self.config.hub.imu.heading())
        if (self.keyboard.poll(0)):
            usys.stdin.read(1)  # type: ignore
            char = usys.stdin.read(1)  # type: ignore
            if (ord(char) in range(49, 58)):
                self.index = ord(char) - 49
            elif (ord(char) == 61):
                self.page += 1
                self.index = 0
            elif (ord(char) == 45):
                self.page -= 1
                self.index = 0
            elif (ord(char) == 10):
                self.run()

            self.wrapIdx()

            self.hub.display.off()
            self.display()

        if (self.bluetooth_pressed and self.timer.time() - self.last_time_help > 200):
            self.page += 1
            self.index = 0
            self.bluetooth_pressed = False

            self.wrapIdx()
            self.hub.display.off()
            self.display()

        buttons = self.hub.buttons.pressed()
        if (len(buttons) != 1):
            wait(50)
            return

        self.hub.display.off()
        self.hub.speaker.beep(500, 50)
        if Button.LEFT in buttons:
            self.index -= 1
        elif Button.RIGHT in buttons:
            self.index += 1
        elif Button.BLUETOOTH in buttons:
            last_time_exit = self.timer.time()
            while Button.BLUETOOTH in buttons:
                if (self.timer.time() - last_time_exit > 200):
                    raise KeyboardInterrupt

                buttons = self.hub.buttons.pressed()

            self.last_time_help = self.timer.time()
            if (self.bluetooth_pressed):
                self.bluetooth_pressed = False
                self.printInfo()
            else:
                self.bluetooth_pressed = True

        elif Button.CENTER in buttons:
            self.config.hub.light.on(Color.RED)
            self.run()
            self.config.hub.light.on(Color.WHITE)

        self.wrapIdx()

        self.display()
        if not self.bluetooth_pressed:
            wait(200)

    def display(self):
        for i in range(0, self.index+1):
            self.hub.display.pixel(
                self.page*2 + umath.floor(i / 5), i % 5, 100)

    def run(self):
        self.pages[self.page][self.index](self.config)
        self.index += 1

    def wrapIdx(self):
        if (self.page < 0):
            self.page = self.numPages - 1
        elif (self.page >= self.numPages):
            self.page = 0

        if (self.index < 0):
            self.index = len(self.pages[self.page]) - 1
        elif (self.index >= len(self.pages[self.page])):
            self.index = 0

    def printInfo(self):
        self.hub.display.text(self.pageNames[self.page][self.index])

    def start(self):
        while True:
            self.update()
