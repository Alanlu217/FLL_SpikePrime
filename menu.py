from pybricks.hubs import InventorHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop, Icon
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

import umath
from config import Config


class menu:
    def __init__(self, config: Config, pages: list, volume: int = 100):
        self.config = config
        self.hub = config.hub

        self.pages = pages

        self.numPages = len(self.pages)

        self.page = 0
        self.index = 0

        self.hub.system.set_stop_button((Button.LEFT, Button.RIGHT))
        self.hub.speaker.volume(volume)
        self.config.hub.light.on(Color.WHITE)
        self.timer = StopWatch()

    def update(self):

        # print(self.config.hub.imu.heading())

        buttons = self.hub.buttons.pressed()
        if (len(buttons) != 1):
            self.display()
            wait(50)
            return

        self.hub.display.off()
        self.hub.speaker.beep(500, 50)
        if Button.LEFT in buttons:
            self.index -= 1
            if (self.index < 0):
                self.index = len(self.pages[self.page]) - 1
        elif Button.RIGHT in buttons:
            self.index += 1
            if (self.index >= len(self.pages[self.page])):
                self.index = 0
        elif Button.BLUETOOTH in buttons:
            self.timer.reset()
            self.timer.resume()
            while Button.BLUETOOTH in buttons:
                if (self.timer.time() > 200):
                    raise KeyboardInterrupt
                buttons = self.hub.buttons.pressed()
            self.page += 1
            if (self.page >= self.numPages):
                self.page = 0
            self.index = 0
        elif Button.CENTER in buttons:
            self.config.hub.light.on(Color.RED)
            self.pages[self.page][self.index](self.config)
            self.config.hub.light.on(Color.WHITE)

        self.display()
        wait(200)

    def display(self):
        for i in range(0, self.index+1):
            self.hub.display.pixel(
                self.page*2 + umath.floor(i / 5), i % 5, 100)
