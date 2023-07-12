# Dummy generator to compare object to a generator
def _gen():
    yield
_gentype = type(_gen())

# Checks whether an object is a generator
def isGen(obj):
    return type(obj) == _gentype