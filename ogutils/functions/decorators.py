from ..collections.transformations import degenerate

def listify(generator_func):
    '''
    Converts generator functions into list returning functions.

    @listify
    def test():
        yield 1
    test()
    # => [1]
    '''
    def list_func(*args, **kwargs):
        return degenerate(generator_func(*args, **kwargs))
    return list_func
