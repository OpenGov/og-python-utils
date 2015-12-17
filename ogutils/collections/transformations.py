import inspect
from checks import is_collection
from itertools import islice

def recursive_iter(enumerables):
    if not is_collection(enumerables) or isinstance(enumerables, (basestring, dict)):
        yield enumerables
    else:
        for elem in enumerables:
            for sub_elem in recursive_iter(elem):
                yield sub_elem

def flatten(enumerable):
    return list(recursive_iter(enumerable))

def degenerate(enumerable):
    '''
    Converts generators to lists

    degenerate(xrange(2))
    # => [0, 1]
    '''
    if (isinstance(enumerable, xrange) or
        inspect.isgeneratorfunction(enumerable) or
        inspect.isgenerator(enumerable)):
        return list(enumerable)
    return enumerable

def merge_dicts(*dicts, **copy_check):
    '''
    Combines dictionaries into a single dictionary. If the 'copy' keyword is passed
    then the first dictionary is copied before update.

    merge_dicts({'a': 1, 'c': 1}, {'a': 2, 'b': 1})
    # => {'a': 2, 'b': 1, 'c': 1}
    '''
    merged = {}
    if not dicts:
        return merged
    for index, merge_dict in enumerate(dicts):
        if index == 0 and not copy_check.get('copy'):
            merged = merge_dict
        else:
            merged.update(merge_dict)
    return merged

def batch(enumerable, batch_size):
    batch_size = max(int(batch_size), 1)
    try:
        enumerable.__getitem__
        total_size = len(enumerable)
    except (TypeError, AttributeError):
        enumerable = list(enumerable)
        total_size = len(enumerable)
    if total_size == 0:
        yield tuple()
    try:
        for batch_index in xrange(0, total_size, batch_size):
            yield enumerable[batch_index:min(batch_index + batch_size, total_size)]
    except TypeError:
        # Fall back on islice, though it's not as efficient the way we're using it
        for batch_start in xrange(0, total_size, batch_size):
            yield tuple(islice(enumerable, batch_start, min(batch_start + batch_size, total_size)))
