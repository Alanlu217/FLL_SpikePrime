def _lightCal(config):
    print("lightCal")


def _gyroCal(config):
    print("gyroCal")


def _tyreClear(config):
    print("tyreClear")


def testRun1(config):
    d = config.drive

    d.moveDist(500, heading=0)
    d.turnTo(90)
    d.moveDist(500, heading=90)
    d.turnTo(180)
    d.moveDist(500, heading=180)
    d.turnTo(-90)
    d.moveDist(500, heading=-90)
    d.turnTo(0)


def printName(config):
    config.hub.display.text(str(config.hub.system.name()), 300, 20)
