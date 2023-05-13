from pybricks.parameters import Button

from config import Config
from commands import *

class Scheduler:
  def __init__(self):
    self.commands = []
  
  def setConfig(self, config: Config):
    self.config = config
  
  def update(self):
    toRemove = []
    for command in self.commands:
      if isinstance(command, CommandBase):
        command.execute(self.config)
        if (command.done(self.config)):
          toRemove.append(command)
      else:
        command(self.config)
        toRemove.append(command)
    
    for command in toRemove:
      if isinstance(command, CommandBase):
        command.end(self.config)
      self.commands.remove(command)
    
  def empty(self) -> bool:
    return True if len(self.commands) == 0 else False
  
  def add(self, command: CommandBase):
    self.commands.append(command)
    if isinstance(command, CommandBase):
      command.init(self.config)

  def clear(self):
    for command in self.commands:
      if isinstance(command, CommandBase):
        command.end(self.config)
    self.commands = []
  
scheduler = Scheduler()