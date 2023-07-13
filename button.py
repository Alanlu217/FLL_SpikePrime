from pybricks.hubs import InventorHub
from pybricks.parameters import Button
from pybricks.tools import StopWatch

class Buttons():

    def __init__(self, hub: InventorHub):
        self.hub = hub

        self.HOLD_TIME = 200
        self.DOUBLE_PRESS_TIME = 200

        self.button_list = [Button.LEFT, Button.RIGHT, Button.CENTER, Button.BLUETOOTH]
        self.last_buttons = {Button.LEFT: False, Button.RIGHT: False, Button.CENTER: False, Button.BLUETOOTH: False}
        self.last_button_times = {Button.LEFT: 1000, Button.RIGHT: 1000, Button.CENTER: 1000, Button.BLUETOOTH: 1000}
        self.buttons = {Button.LEFT: False, Button.RIGHT: False, Button.CENTER: False, Button.BLUETOOTH: False}
        self.time_buttons = {Button.LEFT: StopWatch(), Button.RIGHT: StopWatch(), Button.CENTER: StopWatch(), Button.BLUETOOTH: StopWatch()}

        for value in self.time_buttons.values():
            value.resume()
    
    def update(self):
        self.last_buttons = self.buttons.copy()

        for i in self.button_list:
            if i in self.hub.buttons.pressed():
                if self.last_buttons[i] == False:
                    self.time_buttons[i].reset()
                    self.time_buttons[i].resume()
                self.buttons[i] = self.time_buttons[i].time()
            else:
                self.buttons[i] = False
                if self.last_buttons[i] != False:
                    self.time_buttons[i].reset()
                    self.time_buttons[i].resume()
                self.last_button_times[i] = self.time_buttons[i].time()
        
    def pressed(self, button: Button):
        if self.buttons[button] != False and self.last_buttons[button] == False:
            return True
        return False
    
    def on(self, button: Button):
        if self.buttons[button]:
            return True
        return False
    
    def last_press(self, button: Button):
        return self.time_buttons[button].time()
    
    def one_pressed(self):
        temp = []
        for button in self.button_list:
            if self.pressed(button):
                temp.append(True)
        return len(temp) == 1

    def held(self, button: Button):
        if self.buttons[button] != False and self.buttons[button] > self.HOLD_TIME:
            return True
        return False

    def double_pressed(self, button: Button):
        if self.pressed(button) and self.last_button_times[button] <= self.DOUBLE_PRESS_TIME:
            return True
        return False