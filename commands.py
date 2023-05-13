class CommandBase:
  def init(self, config):
    pass
  
  def execute(self, config):
    pass

  def end(self, config):
    pass

  def done(self, config) -> bool:
    return True

class SequentialCommand(CommandBase):
  def __init__(self, commands: list(CommandBase)):
    self.commands = commands
    self.command = self.commands[0]
    self.index = 0
  
  def init(self, config):
    self.command.init(config)
  
  def execute(self, config):
    self.command.execute(config)
  
  def end(self, config):
    self.command.end(config)
    self.index += 1
    self.command = self.commands[self.index]
  
  def isFinished(self, config):
    return self.command.isFinished(config)

class ParrallelCommand(CommandBase):
  def __init__(self, commands: list(CommandBase)):
    self.commands = commands
  
  def init(self, config):
    for command in self.commands:
      command.init(config)

  def execute(self, config):
    for command in self.commands:
      command.execute(config)

  def end(self, config):
    for command in self.commands:
      command.end(config)

  def done(self, config):
    for command in self.commands:
      command.done(config)