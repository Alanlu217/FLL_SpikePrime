from pybricks.hubs import InventorHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop, Icon
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

from micropython import const
from menu import menu
from config import Config
from scheduler import scheduler

import other

m_config = Config()

scheduler.setConfig(m_config)


m_menu = menu(m_config, [m_config.page1, m_config.page2], [m_config.page1Names, m_config.page2Names], 50)
m_menu.display()

try:
    m_menu.start()
except KeyboardInterrupt:
    c = m_config
    m = m_menu
    d = m_config.drive
    l = m_config.light

    raise KeyboardInterrupt
