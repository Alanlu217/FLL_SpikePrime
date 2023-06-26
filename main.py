from pybricks.hubs import InventorHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop, Icon, Axis
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

from micropython import const
from menu import menu
from config import ConfigAlanSpike, ConfigBasicRobot

import other

hub = InventorHub(front_side=Axis.Y, top_side=Axis.Z)
    
name = hub.system.name()
if name == "AlanSpike":
    m_config = ConfigAlanSpike(hub)
elif name == "Roo10":
    m_config = ConfigBasicRobot(hub)


if Button.LEFT in m_config.hub.buttons.pressed():
    m_menu = menu(m_config, [m_config.page1, m_config.page2], [m_config.page1Names, m_config.page2Names], 0)
else:
    m_menu = menu(m_config, [m_config.page1, m_config.page2], [m_config.page1Names, m_config.page2Names], 50)
m_menu.display()

wait(200)

try:
    m_menu.start()
except KeyboardInterrupt:
    c = m_config
    m = m_menu
    d = m_config.drive
    l = m_config.light

    raise KeyboardInterrupt
