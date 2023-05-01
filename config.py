from pybricks.parameters import Port
from pybricks.hubs import InventorHub
import other


class config:
    def __init__(self, hub: InventorHub):
        self.hub = hub

        self.page1 = []

        self.page2 = [other.printName, other._lightCal,
                      other._gyroCal, other._tyreClear]
