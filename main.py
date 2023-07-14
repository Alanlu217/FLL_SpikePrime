from pybricks.hubs import InventorHub
from pybricks.parameters import Button, Axis
from pybricks.tools import wait

from menu import menu
from other import setRepl
from config import ConfigAlanSpike, ConfigBasicRobot

# Setup hub
hub = InventorHub(front_side=Axis.Y, top_side=Axis.Z)
    
# Choose configuration based on hostname
name = hub.system.name()
if name == "AlanSpike":
    m_config = ConfigAlanSpike(hub)
elif name == "Roo10":
    m_config = ConfigBasicRobot(hub)


# If left button pressed on startup
# Load in quiet mode
if Button.LEFT in m_config.hub.buttons.pressed():
    m_menu = menu(m_config, [m_config.page1, m_config.page2], [m_config.page1Names, m_config.page2Names], 0)
else:
    m_menu = menu(m_config, [m_config.page1, m_config.page2], [m_config.page1Names, m_config.page2Names], 50)

# Display menu
m_menu.display()

# Start menu loop
try:
    m_menu.start()
except KeyboardInterrupt: # Add shortcuts for debugging
    setRepl()
    c = m_config
    m = m_menu
    d = m_config.drive
    l = m_config.light

    raise KeyboardInterrupt
