from importlib import resources
from itertools import chain
from typing import Union, Iterable

import toml

from pyrl import config


class Bind(tuple):

    def __new__(cls, iterable_or_str: Union[str, Iterable[str]] = (), /):
        if isinstance(iterable_or_str, str):
            return super().__new__(cls, (iterable_or_str, ))  # type: ignore
        else:
            return super().__new__(cls, iterable_or_str)  # type: ignore

    @property
    def key(self):
        if self:
            return self[0]
        else:
            return "Unbound"

    def __str__(self):
        return "/".join("{}".format(key) for key in self)


undefined = Bind()


class Binds:

    General = undefined
    Yes = undefined
    Strong_Yes = undefined
    Cancel = undefined
    Debug_Commands = undefined

    ScrollKeys = undefined
    Next_Line = undefined
    Previous_Line = undefined
    Next_Page = undefined
    Previous_Page = undefined
    Filter = undefined

    MultiSelectKeys = undefined
    Select_All = undefined
    Deselect_All = undefined

    MainView = undefined
    Help = undefined
    Look_Mode = undefined
    Equipment = undefined
    Backpack = undefined
    Drop_Items = undefined
    Pick_Up_Items = undefined
    Descend = undefined
    Ascend = undefined
    Quit = undefined
    Save = undefined
    Attack = undefined
    Redraw = undefined
    History = undefined
    Walk_Mode = undefined
    Show_Vision = undefined
    Skip_To_Last_Message = undefined

    EquipmentView = undefined
    Equipment_Select_Keys = undefined
    Equipment_Select_Feet = undefined
    Equipment_View_Backpack = undefined

    BackpackView = undefined
    Backpack_Select_Keys = undefined
    Backpack_Drop_Items = undefined

    Directions = undefined

    SouthWest = undefined
    South = undefined
    SouthEast = undefined
    West = undefined
    Stay = undefined
    East = undefined
    NorthWest = undefined
    North = undefined
    NorthEast = undefined

    InstantWalk = undefined

    Instant_SouthWest = undefined
    Instant_South = undefined
    Instant_SouthEast = undefined
    Instant_West = undefined
    Instant_Stay = undefined
    Instant_East = undefined
    Instant_NorthWest = undefined
    Instant_North = undefined
    Instant_NorthEast = undefined


with resources.open_text(config, "binds.toml") as f:
    hotkeys = toml.load(f)


# Set all hotkeys and their categories to Binds namespace
for category_name, category in hotkeys.items():
    for bind_name, binds in category.items():
        setattr(Binds, bind_name, Bind(binds))
    category_binds = chain.from_iterable(binds for binds in category.values())
    setattr(Binds, category_name, Bind(category_binds))


def undefined_keys():
    return [key for key, value in vars(Binds).items() if value is undefined]

