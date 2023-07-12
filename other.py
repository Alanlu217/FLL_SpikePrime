def _gen():
    yield
_gentype = type(_gen())

def isGen(obj):
    return type(obj) == _gentype