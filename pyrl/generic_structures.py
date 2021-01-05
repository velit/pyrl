from collections import namedtuple
from itertools import zip_longest
from random import randrange


Coord = namedtuple("Coord", "y, x")
TableDims = namedtuple("Size2D", "rows, cols")


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
        self.rows, self.cols = dimensions
        size = self.rows * self.cols
        assert len(init_values) <= size, \
            f"Given {len(init_values)=} exceed {size=}."
        init_seq = (value for _, value in zip_longest(range(size), init_values, fillvalue=fillvalue))
        super().__init__(init_seq)

    def __getitem__(self, coord):
        return super().__getitem__(self.get_index(coord))

    def __setitem__(self, coord, value):
        return super().__setitem__(self.get_index(coord), value)

    def get_coord(self, index):
        return self.get_coord_from_index(index, self.cols)

    def get_index(self, coord):
        return self.get_index_from_coord(coord, self.cols)

    def is_legal(self, coord):
        y, x = coord
        rows, cols = self.dimensions
        return (0 <= y < rows) and (0 <= x < cols)

    def clear(self):
        for i in range(self.rows * self.cols):
            super().__setitem__(self, i, None)

    def enumerate(self):
        for i, item in enumerate(self):
            yield self.get_coord(i), item

    def coord_iter(self):
        for i, item in enumerate(self):
            yield self.get_coord(i)

    def random_coord(self):
        return randrange(self.rows), randrange(self.cols)

    @property
    def dimensions(self):
        return self.rows, self.cols


class OneToOneMapping(dict):

    """A dict-like object which guarantees uniqueness for values in addition to keys."""

    def __setitem__(self, key, value):
        if value in self.values():
            raise ValueError("Value {} already exists in mapping.".format(value))
        super().__setitem__(key, value)

    def getkey(self, arg_value):
        for key, value in self.items():
            if value == arg_value:
                return key
        raise KeyError("Value {} not found in mapping.".format(arg_value))

    def update(self, E=None, **kwords):
        if E is not None:
            if hasattr(E, "keys"):
                for key in E:
                    self[key] = E[key]
            else:
                for key, value in E:
                    self[key] = value
        for key in kwords:
            self[key] = kwords[key]


class Event(object):

    def __init__(self):
        self.observers = []

    def subscribe(self, function):
        self.observers.append(function)

    def unsubscribe(self, function):
        self.observers.remove(function)

    def trigger(self, *args, **kwargs):
        for observer in self.observers:
            observer(*args, **kwargs)
