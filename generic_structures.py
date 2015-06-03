from __future__ import absolute_import, division, print_function, unicode_literals


from heapq import heappush, heappop
from itertools import zip_longest


def _disable_list_dynamicness(cls):
    _disabled_methods = ('append', 'copy', 'extend', 'insert', 'pop', 'remove', 'reverse',
                         'sort', '__delitem__', '__iadd__', '__imul__')
    for method in _disabled_methods:
        def disabled(not_implemented):
            raise NotImplementedError
        disabled.__name__ = method
        disabled.__doc__ = "This method isn't implemented in a non-dynamic array."
        setattr(cls, method, disabled)
    return cls


@_disable_list_dynamicness
class Array2D(list):

    """
    Mutable non-dynamic array with two-dimensional get- and setitem methods.

    Iterating over the whole array gives all items directly by iterating the second
    dimension tighter ie. 'line-wise' if second dimension is x.

    Underlying implementation is a one-dimensional dynamic list with dynamic methods
    disabled.
    """

    @staticmethod
    def get_index_from_coord(coord, second_dim_bound):
        first_dim, second_dim = coord
        if second_dim < second_dim_bound:
            return first_dim * second_dim_bound + second_dim
        else:
            msg = "Second dimension index out of range: {} < {}"
            raise IndexError(msg.format(second_dim, second_dim_bound))

    @staticmethod
    def get_coord_from_index(index, second_dim_bound):
        return index // second_dim_bound, index % second_dim_bound

    def __init__(self, dimensions, init_values=(), fillvalue=None):
        self.dimensions = dimensions
        size = self.dimensions[0] * self.dimensions[1]
        assert len(init_values) <= size, \
            "Given init_values ({}) exceed size by dimensions ({}).".format(len(init_values, size))
        init_seq = (value for _, value in zip_longest(range(size), init_values, fillvalue=fillvalue))
        super().__init__(init_seq)

    def __getitem__(self, coord):
        return super().__getitem__(self.get_index(coord))

    def __setitem__(self, coord, value):
        return super().__setitem__(self.get_index(coord), value)

    def get_coord(self, index):
        return self.get_coord_from_index(index, self.dimensions[1])

    def get_index(self, coord):
        return self.get_index_from_coord(coord, self.dimensions[1])

    def is_legal(self, coord):
        y, x = coord
        rows, cols = self.dimensions
        return (0 <= y < rows) and (0 <= x < cols)

    def clear(self):
        for i in range(self.dimensions[0] * self.dimensions[1]):
            super().__setitem__(self, i, None)

    def enumerate(self):
        for i, item in enumerate(self):
            yield self.get_coord(i), item


class PriorityQueue(object):

    def __init__(self):
        self.pq = []
        self.count = 0
        self.remove_set = set()

    def add(self, task, priority):
        self.count += 1
        entry = (priority, self.count, task)
        heappush(self.pq, entry)

    def remove(self, task):
        self.remove_set.add(task)

    def pop(self):
        while True:
            priority, count, task = heappop(self.pq)
            if task not in self.remove_set:
                return task, priority, count
            else:
                self.remove_set.remove(task)


class Event(object):

    def __init__(self):
        self.observers = []

    def subscribe(self, function):
        self.observers.append(function)

    def unsubscribe(self, function):
        self.observers.remove(function)

    def trigger(self, *args, **keys):
        for observer in self.observers:
            observer(*args, **keys)
