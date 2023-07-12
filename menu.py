from pybricks.parameters import Button, Color
from pybricks.tools import wait, StopWatch

import umath
import uselect
import usys
from other import isGen
from config import Config


# Main menu class that manages all user interface
class menu:
    def __init__(self, config: Config, pages: list, pageName: list, volume: int = 100):
        self.config = config
        self.hub = config.hub

        self.pages = pages
        self.pageNames = pageName

        self.numPages = len(self.pages)

        self.page = 0
        self.index = 0

        self.hub.system.set_stop_button((Button.LEFT, Button.RIGHT)) # Change stop buttons to left and right at the same time
        self.hub.speaker.volume(volume)
        self.config.hub.light.on(Color.WHITE)

        # Setup keyboard controls
        self.keyboard = uselect.poll()
        self.keyboard.register(usys.stdin, uselect.POLLIN)  # type: ignore

        self.timer = StopWatch()
        self.timer.resume()

        self.bluetooth_pressed = False
        self.last_time_help = 0

    def update(self):
        """
        Main loop
        """
        # Handles keyboard input
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

        # If bluetooth button pressed once, switches pages
        if (self.bluetooth_pressed and self.timer.time() - self.last_time_help > 200):
            self.page += 1
            self.index = 0
            self.bluetooth_pressed = False

            self.wrapIdx()
            self.hub.display.off()
            self.display()

        # Check if one button is pressed on the robot
        buttons = self.hub.buttons.pressed()
        if (len(buttons) != 1):
            wait(50)
            return

        # If pressed turns display off and beeps
        self.hub.display.off()
        self.hub.speaker.beep(500, 50)

        if Button.LEFT in buttons:
            self.index -= 1
        elif Button.RIGHT in buttons:
            self.index += 1
        elif Button.BLUETOOTH in buttons: # If bluetooth button held, prints information on selected item
            last_time_exit = self.timer.time()
            while Button.BLUETOOTH in buttons:
                if (self.timer.time() - last_time_exit > 300):
                    self.printInfo()
                    self.hub.display.off()
                    self.display()
                    return

                buttons = self.hub.buttons.pressed()

            self.last_time_help = self.timer.time()
            if (self.bluetooth_pressed): # If pressed twice, turns in REPL mode
                raise KeyboardInterrupt
            else:
                self.bluetooth_pressed = True

        elif Button.CENTER in buttons: # Runs selected run if center button pressed
            self.run()

        self.wrapIdx() # Makes sure index is within bounds

        self.display() # Update display
        if not self.bluetooth_pressed:
            wait(200) # Adds small delay

    def display(self):
        """
        Displays the dots on the screen in accord to currently selected run
        """
        for i in range(0, self.index+1):
            self.hub.display.pixel(
                self.page*2 + umath.floor(i / 5), i % 5, 100)

    def run(self):
        """
        Runs selected item
        """
        self.config.hub.light.on(Color.CYAN) # Shows cyan when run active

        self.execute() # Handles generator / normal function
        self.config.stop() # Stops all motors once completed

        wait(400)

        self.index += 1 # Moves to next run
        self.config.hub.light.on(Color.WHITE) # Changes back to white when idle

    def execute(self):
        """
        Runs should be in format of:
        [
            action1(),
            action2(),
            [action3(), action4()] # Use for simultanious movement
        ]

        Items in menu can also be singular e.g:
        action1()
        """

        try:
            for item in self.pages[self.page][self.index]:
                if callable(item):
                    try:
                        temp = item()
                        if isGen(temp):
                            while next(temp):
                                if self.quit(): return
                    except TypeError:
                        item(self.config)
                else:
                    count = len(item)
                    item = [i() for i in item]
                    while count != 0:
                        for i in range(len(item) - 1, -1, -1):
                            if self.quit(): return
                            if not next(item[i]):
                                count -= 1
                                del item[i]
        except TypeError:
            try:
                temp = self.pages[self.page][self.index]()
                if isGen(temp):
                    while next(temp):
                        if self.quit(): return
            except TypeError:
                self.pages[self.page][self.index](self.config)

    def wrapIdx(self):
        """
        Confines index to within menu bounds
        """
        if (self.page < 0):
            self.page = self.numPages - 1
        elif (self.page >= self.numPages):
            self.page = 0

        if (self.index < 0):
            self.index = len(self.pages[self.page]) - 1
        elif (self.index >= len(self.pages[self.page])):
            self.index = 0

    def printInfo(self):
        """
        Prints name of selected item to brick screen
        """
        self.hub.display.text(self.pageNames[self.page][self.index], on=150, off=10)

    def start(self):
        """
        Starts the menu's main loop
        """
        self.hub.speaker.beep(550, 50)
        while True:
            self.update()
    
    def quit(self):
        """
        Condition for when a run is quit
        """
        if Button.BLUETOOTH in self.hub.buttons.pressed():
            return True
        return False
