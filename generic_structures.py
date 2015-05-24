from __future__ import absolute_import, division, print_function, unicode_literals


from heapq import heappush, heappop

from generic_algorithms import add_vector


class List2D(list):

    """
    Sub-class of list which overrides accessor methods with 2D ones.

    The second dimension is bounded by constructor parameter, first dimension is
    bounded by the amount of items given to the list divided by the second
    dimension bound.

    Iterating the flat list gives items that increase quicker in the second
    dimension. In other words the first four items in a list with the second
    dimension bounded to two are: (0, 0), (0, 1), (1, 0), (1, 1).
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

    def __init__(self, iterable, second_dimension_bound):
        super(List2D, self).__init__(iterable)
        self._bound = second_dimension_bound

    def __getitem__(self, coord):
        return super().__getitem__(self.get_index(coord))

    def __setitem__(self, coord, value):
        return super().__setitem__(self.get_index(coord), value)

    def __delitem__(self, coord):
        return super().__delitem__(self.get_index(coord))

    def get_dimensions(self):
        return ((len(self) - 1) // self._bound) + 1, self._bound

    def get_coord(self, index):
        return self.get_coord_from_index(index, self._bound)

    def get_index(self, coord):
        return self.get_index_from_coord(coord, self._bound)

    def is_legal(self, coord, direction=(0, 0)):
        y, x = add_vector(coord, direction)
        rows, cols = self.get_dimensions()
        return (0 <= y < rows) and (0 <= x < cols)


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
