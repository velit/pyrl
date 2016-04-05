from __future__ import absolute_import, division, print_function, unicode_literals

from interface.lines_view import lines_view, Line
from config.bindings import Bind
from creature.equipment import Slot


def equipment(game_actions):
    ga = game_actions
    footer_fmt = "Press a slot key to (un)equip  {} to view backpack  {} to close"
    footer = footer_fmt.format(Bind.Equipment_View_Backpack.key, Bind.Cancel.key)
    equipment = ga.creature.equipment

    while True:
        lines = tuple(Line("{0:11}: {1}".format(slot.value, equipment.get_item(slot)), slot)
                      for slot in Slot)
        key, slot = lines_view(ga.io.whole_window, lines,
                               multi_select=False,
                               select_keys=Bind.Equipment_Select_Keys,
                               return_keys=Bind.Equipment_View_Backpack + Bind.Cancel,
                               header="Equipment",
                               footer=footer)

        if key in Bind.Cancel:
            return
        elif key in Bind.Equipment_View_Backpack:
            backpack(ga)
        elif slot in Slot:
            if equipment.get_item(slot) is None:
                backpack_equip_item(ga, slot)
            else:
                equipment.unequip(slot)
        else:
            assert False, "Got unhandled return values, key: {} value: {}".format(key, slot)


def backpack_equip_item(game_actions, slot):
    ga = game_actions

    lines = tuple(Line(str(item), i) for i, item in ga.enumerate_character_items()
                  if item.fits_to_slot(slot))
    key, item = lines_view(ga.io.whole_window, lines, select_keys=Bind.Backpack_Select_Keys,
                        header="Select item to equip")
    if key in Bind.Cancel:
        return
    else:
        ga.creature.equipment.equip_from_bag(item, slot)


def backpack(game_actions):
    ga = game_actions

    lines = tuple(Line(str(item), i) for i, item in ga.enumerate_character_items())
    key, selections = lines_view(
        ga.io.whole_window,
        lines,
        multi_select=True,
        select_keys=Bind.Backpack_Select_Keys,
        return_keys=Bind.Backpack_Drop_Items + Bind.Cancel,
        header="Backpack".format(Bind.Backpack_Drop_Items.key),
    )
    if key in Bind.Cancel:
        return
    elif key in Bind.Backpack_Drop_Items:
        return ga.drop_items(selections)


def pickup_items(game_actions):
    ga = game_actions

    lines = tuple(Line(str(item), i) for i, item in ga.enumerate_floor_items())

    if not lines:
        ga.io.msg("There aren't any items here to pick up.")
        return
    elif len(lines) == 1:
        return ga.pickup_items((lines[0][0], ))

    key, selections = lines_view(
        ga.io.whole_window,
        lines,
        multi_select=True,
        select_keys=Bind.Backpack_Select_Keys,
        header="Select items to pick up"
    )
    if key in Bind.Cancel and selections:
        return ga.pickup_items(selections)


def drop_items(game_actions):
    ga = game_actions

    lines = tuple(Line(str(item), i) for i, item in ga.enumerate_character_items())
    key, selections = lines_view(
        ga.io.whole_window,
        lines,
        multi_select=True,
        select_keys=Bind.Backpack_Select_Keys,
        header="Select items to drop".format(Bind.Backpack_Drop_Items.key)
    )
    if key in Bind.Cancel and selections:
        return ga.drop_items(selections)
