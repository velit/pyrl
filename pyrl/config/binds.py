from __future__ import annotations

import tomllib
from collections.abc import MutableMapping, Iterable
from importlib.resources import files
from itertools import chain

from pyrl.engine.enums.directions import Direction, Dir
from pyrl.engine.enums.keys import AnyKey, Key, KeySequence

unbound = KeySequence([Key.UNDEFINED] * 4)

class Binds:

    General                 = unbound
    Yes                     = unbound
    Strong_Yes              = unbound
    Cancel                  = unbound
    Debug_Commands          = unbound

    ScrollKeys              = unbound
    Next_Line               = unbound
    Previous_Line           = unbound
    Next_Page               = unbound
    Previous_Page           = unbound
    Filter                  = unbound

    MultiSelectKeys         = unbound
    Select_All              = unbound
    Deselect_All            = unbound

    MainView                = unbound
    Help                    = unbound
    Look_Mode               = unbound
    Equipment               = unbound
    Backpack                = unbound
    Drop_Items              = unbound
    Pick_Up_Items           = unbound
    Descend                 = unbound
    Ascend                  = unbound
    Quit                    = unbound
    Save                    = unbound
    Attack                  = unbound
    Redraw                  = unbound
    History                 = unbound
    Walk_Mode               = unbound
    Show_Vision             = unbound
    Skip_To_Last_Message    = unbound

    EquipmentSelectKeys     = unbound
    Equipment_Select_Head   = unbound
    Equipment_Select_Body   = unbound
    Equipment_Select_Right  = unbound
    Equipment_Select_Left   = unbound
    Equipment_Select_Feet   = unbound

    EquipmentView           = unbound
    Equipment_View_Backpack = unbound

    BackpackView            = unbound
    Backpack_Select_Keys    = unbound
    Backpack_Drop_Items     = unbound

    Directions              = unbound
    SouthWest               = unbound
    South                   = unbound
    SouthEast               = unbound
    West                    = unbound
    Stay                    = unbound
    East                    = unbound
    NorthWest               = unbound
    North                   = unbound
    NorthEast               = unbound

    InstantWalk             = unbound
    Instant_SouthWest       = unbound
    Instant_South           = unbound
    Instant_SouthEast       = unbound
    Instant_West            = unbound
    Instant_Stay            = unbound
    Instant_East            = unbound
    Instant_NorthWest       = unbound
    Instant_North           = unbound
    Instant_NorthEast       = unbound

    Other                   = unbound
    Toggle_Fullscreen       = unbound
    Next_Tileset            = unbound
    Previous_Tileset        = unbound
    Next_Bdf                = unbound
    Previous_Bdf            = unbound

    _direction_keys: dict[AnyKey, Direction] = {}

    @classmethod
    def load_binds(cls) -> None:
        """Load binds from config and fill the to_direction dict direction lookup"""
        with files("pyrl").joinpath("hotkeys.toml").open("rb") as binds_toml:
            hotkeys = tomllib.load(binds_toml)

        # Set all hotkeys and their categories to Binds namespace
        for category_name, category in hotkeys.items():
            for bind_name, binds in category.items():
                setattr(cls, bind_name, KeySequence(binds))
            category_binds = chain.from_iterable(binds for binds in category.values())
            setattr(cls, category_name, KeySequence(category_binds))
        cls.set_directions()

    @classmethod
    def set_directions(cls) -> None:
        def set_every_to(every: Iterable[AnyKey], to: Direction, at: MutableMapping[AnyKey, Direction]) -> None:
            for item in every:
                at[item] = to

        cls._direction_keys.clear()
        set_every_to(cls.SouthWest + cls.Instant_SouthWest, to=Dir.SouthWest, at=cls._direction_keys)
        set_every_to(cls.South     + cls.Instant_South,     to=Dir.South,     at=cls._direction_keys)
        set_every_to(cls.SouthEast + cls.Instant_SouthEast, to=Dir.SouthEast, at=cls._direction_keys)
        set_every_to(cls.West      + cls.Instant_West,      to=Dir.West,      at=cls._direction_keys)
        set_every_to(cls.Stay      + cls.Instant_Stay,      to=Dir.Stay,      at=cls._direction_keys)
        set_every_to(cls.East      + cls.Instant_East,      to=Dir.East,      at=cls._direction_keys)
        set_every_to(cls.NorthWest + cls.Instant_NorthWest, to=Dir.NorthWest, at=cls._direction_keys)
        set_every_to(cls.North     + cls.Instant_North,     to=Dir.North,     at=cls._direction_keys)
        set_every_to(cls.NorthEast + cls.Instant_NorthEast, to=Dir.NorthEast, at=cls._direction_keys)

    @classmethod
    def undefined_keys(cls) -> Iterable[AnyKey]:
        return [key for key, value in vars(cls).items() if value is unbound]

    @classmethod
    def get_direction(cls, bind: AnyKey) -> Direction:
        return cls._direction_keys[bind]

Binds.load_binds()
