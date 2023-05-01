def _lightCal(config):
    print("lightCal")


def _gyroCal(config):
    print("gyroCal")


def _tyreClear(config):
    print("tyreClear")


def printName(config):
    config.hub.display.text(str(config.hub.system.name()), 300, 20)
