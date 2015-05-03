"""To user: even though this module is in the config folder, don't modify anything here."""
from __future__ import absolute_import, division, print_function, unicode_literals

from string import ascii_lowercase

from enums.directions import Dir


class BindingTuple(tuple):

    @property
    def key(self):
        return self[0]

    def __str__(self):
        return ", ".join("{}".format(key) for key in self)


def finalize_bindings(cls):

    _BindingTuplefy_attributes(cls)

    cls.item_view_keys = cls.Next_Line + cls.Previous_Line + cls.Next_Page + cls.Previous_Page
    cls.query_keys = cls.Yes + cls.No + cls.Default_Yes + cls.Default_No + cls.Default_Query

    select_filter = cls.Cancel + cls.item_view_keys
    cls.item_select_keys = tuple(key for key in ascii_lowercase if key not in select_filter)

    action_tuple = (
        (cls.SouthWest,  Dir.SouthWest),
        (cls.South,      Dir.South),
        (cls.SouthEast,  Dir.SouthEast),
        (cls.West,       Dir.West),
        (cls.Stay,       Dir.Stay),
        (cls.East,       Dir.East),
        (cls.NorthWest,  Dir.NorthWest),
        (cls.North,      Dir.North),
        (cls.NorthEast,  Dir.NorthEast),
    )
    cls.action_direction = {key: direction for keys, direction in action_tuple for key in keys}

    walk_tuple = (
        (cls.Instant_SouthWest,  Dir.SouthWest),
        (cls.Instant_South,      Dir.South),
        (cls.Instant_SouthEast,  Dir.SouthEast),
        (cls.Instant_West,       Dir.West),
        (cls.Instant_Stay,       Dir.Stay),
        (cls.Instant_East,       Dir.East),
        (cls.Instant_NorthWest,  Dir.NorthWest),
        (cls.Instant_North,      Dir.North),
        (cls.Instant_NorthEast,  Dir.NorthEast),
    )
    cls.walk_mode_direction = {key: direction for keys, direction in walk_tuple for key in keys}

    return cls


def _BindingTuplefy_attributes(cls):
    def is_public_attr(attr, value):
        return not attr.startswith('_')

    attrs = tuple((attr, value) for attr, value in vars(cls).items() if is_public_attr(attr, value))
    for attr, value in attrs:
        if isinstance(value, str):
            binding_tuple = BindingTuple([value])
        else:
            binding_tuple = BindingTuple(value)
        setattr(cls, attr, binding_tuple)
