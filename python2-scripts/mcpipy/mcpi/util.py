import collections
import math
from sys import version_info

try:
    basestring
except NameError:
    basestring = str  # compatibility for Python 3

def flatten(l):
    for e in l:
        if isinstance(e, collections.Iterable) and not isinstance(e, basestring):
            for ee in flatten(e): yield ee
        else: yield e

# this is highly optimized to iterables consisting at base level of ints and floats only
def floorFlatten(l):
    for e in l:
        if isinstance(e, int):
            yield str(e)
        elif isinstance(e, float):
            yield str(int(math.floor(e)))
        elif not e is None:
            for ee in floorFlatten(e): yield ee

def flatten_parameters_to_string(l):
    return ",".join(map(str, flatten(l)))
