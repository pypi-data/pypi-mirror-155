from functools import reduce
import operator
from friendlylog import colored_logger as log


class dotdict(dict):
    """
    a dictionary that supports dot notation 
    as well as dictionary access notation 
    usage: d = dotdict() or d = dotdict({'val1':'first'})
    set attributes: d.val2 = 'second' or d['val2'] = 'second'
    get attributes: d.val2 or d['val2']
    """
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __init__(self, dct):
        for key, value in dct.items():
            if hasattr(value, 'keys'):
                value = dotdict(value)
            self[key] = value


def dotpath_exists(obj, key):
    arr = key.split('.')
    while arr:
        k = arr.pop(0)
        if k not in obj:
            return False
        obj = obj[k]
        if not obj:
            break
        if (arr and isinstance(obj, list)):
            remainder = '.'.join(arr)
            for i in range(len(obj)):
                if not dotpath_exists(obj[i], remainder):
                    return False
    return True


def dotpath_get_value(obj, key):
    """
    Get a value from a dict using a dot notation field path.
    """
    arr = key.split('.')
    while arr:
        k = arr.pop(0)
        if k not in obj:
            log.debug(f"Key '{key}' not found in object {obj}")
            return None
        obj = obj[k]
        if not obj:
            break
        if (arr and isinstance(obj, list)):
            remainder = '.'.join(arr)
            results = []
            for i in range(len(obj)):
                x = dotpath_get_value(obj[i], remainder)
                if x:
                    if isinstance(x, list):
                        results += x
                    else:
                        results += [x]
            return results
    return obj


def dotpath_set_value(obj, key, value):
    keys = key.split('.')
    array_set_value(obj, keys, value)


def array_get_value(dataDict, mapList):
    return reduce(operator.getitem, mapList, dataDict)


def array_set_value(dataDict, mapList, value):
    array_get_value(dataDict, mapList[:-1])[mapList[-1]] = value


def array_create_structure(dataDict, mapList):
    for path in mapList:
        current_level = dataDict
        for part in path:
            if part not in current_level:
                current_level[part] = {}
            current_level = current_level[part]
