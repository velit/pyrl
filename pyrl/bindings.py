class Bind(object):

    """The BindGroup metaclass sets all the game's binds into this class for use in the code."""

    pass


class BindingTuple(tuple):

    @property
    def key(self):
        if self:
            return self[0]
        else:
            return "Unbound"

    def __str__(self):
        return "/".join("{}".format(key) for key in self)


def _is_public_attr(attr):
    return not attr.startswith('_')


class _BindDict(dict):

    def __init__(self):
        super().__init__()
        self._all_binds = []

    def __setitem__(self, key, value):
        if _is_public_attr(key):
            if key in self:
                raise KeyError("Binding {} is defined multiple times.".format(key))
            if value == "" or value is None:
                value = BindingTuple()
            elif isinstance(value, str):
                value = BindingTuple((value,))
            else:
                try:
                    value = BindingTuple(value)
                except TypeError:
                    exit("Error in config/hotkeys.py: {0} = {1} is not a valid hotkey.".format(key, value))
            self._all_binds.extend(value)
            setattr(Bind, key, value)
        super().__setitem__(key, value)


class BindGroup(type):

    @classmethod
    def __prepare__(metaclass, class_name, bases):
        return _BindDict()

    def __new__(cls, name, bases, namespace):
        bind_class = type.__new__(cls, name, bases, dict(namespace))
        setattr(Bind, name, tuple(namespace._all_binds))
        return bind_class


import pyrl.config.hotkeys
