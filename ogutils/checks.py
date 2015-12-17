import distutils
from .collections.checks import is_collection, is_empty

def booleanize(truthy):
    '''
    Smartly converts argument to true or false. Strings and variants of
    'true' and 'false' convert to appropriate types, along with normal
    bool() like conversions.
    '''
    if truthy is None:
        return False
    elif isinstance(truthy, basestring):
        if truthy:
            try:
                return bool(distutils.util.strtobool(truthy))
            except ValueError:
                return True
        else:
            return False
    elif is_collection(truthy):
        return not is_empty(truthy)
    else:
        return bool(truthy)
