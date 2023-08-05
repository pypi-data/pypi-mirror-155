def length(__o: object):
    """Bypass C-Python len function."""
    return __o.__len__()
