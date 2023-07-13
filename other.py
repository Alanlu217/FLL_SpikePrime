# Dummy generator to compare object to a generator
def _gen():
    yield
_gentype = type(_gen())

# Checks whether an object is a generator
def isGen(obj):
    return type(obj) == _gentype

class movementDec():
    def __init__(self):
        self.REPL = False
    
    def coroutine(self, func):
        def wrapper(*args, **kwargs):
            if self.REPL:
                for i in func(*args, **kwargs)():
                    pass
            else:
                return func(*args, **kwargs)
        return wrapper

m_movementDec = movementDec()

coroutine = m_movementDec.coroutine

def setRepl():
    m_movementDec.REPL = True