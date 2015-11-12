class FakeIterable(object):
    def __init__(self, iterable):
        self.iterable = iterable

    def __iter__(self):
        return self.iterable.__iter__()

    def __len__(self):
        return self.iterable.__len__()
