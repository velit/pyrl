from __future__ import absolute_import, division, print_function, unicode_literals

from interface.lines_view import lines_view, multi_select_lines_view, Line
from config.bindings import Bind
from creature.equipment import Slot


def equipment(game_actions):
    ga = game_actions
    select_keys = Bind.Equipment_Select_Keys
    return_keys = Bind.Equipment_View_Backpack
    header = "Equipment"
    footer_fmt = "Press a slot key to (un)equip  {} to view backpack  {} to close"
    footer = footer_fmt.format(Bind.Equipment_View_Backpack.key, Bind.Cancel.key)
    equipment = game_actions.creature.equipment

    while True:
        lines = tuple(Line(slot, "{0:11}: {1}".format(slot.value, equipment.get_item(slot))) for slot in Slot)
        retval = lines_view(ga.io.whole_window, lines, select_keys, return_keys, header, footer)

        if retval in Bind.Cancel:
            return
        elif retval in Bind.Equipment_View_Backpack:
            backpack(ga)
        elif retval in Slot:
            slot = retval
            if equipment.get_item(slot) is None:
                backpack_equip_item(ga, slot)
            else:
                equipment.unequip(slot)
        else:
            assert False, "Got unhandled return value as input {}".format(retval)


def backpack_equip_item(game_actions, slot):
    ga = game_actions

    lines = tuple(Line(i, str(item)) for i, item in ga.enumerate_character_items() if item.fits_to_slot(slot))
    retval = lines_view(ga.io.whole_window, lines, select_keys=Bind.Backpack_Select_Keys, header="Select item to equip")
    if retval in Bind.Cancel:
        return
    else:
        ga.creature.equipment.equip_from_bag(retval, slot)


def backpack(game_actions):
    ga = game_actions

    lines = tuple(Line(i, str(item)) for i, item in ga.enumerate_character_items())
    key, selected_item_indexes = multi_select_lines_view(ga.io.whole_window, lines,
                                                         select_keys=Bind.Backpack_Select_Keys,
                                                         return_keys=Bind.Backpack_Drop_Items,
                                                         header="Backpack  {} to drop items".format(Bind.Backpack_Drop_Items.key))
    if key in Bind.Cancel:
        return
    elif key in Bind.Backpack_Drop_Items:
        return ga.drop_items(selected_item_indexes)


def pickup_items(game_actions):
    ga = game_actions

    lines = tuple(Line(i, str(item)) for i, item in ga.enumerate_floor_items())

    if not lines:
        ga.io.msg("There aren't any items here to pick up.")
        return
    elif len(lines) == 1:
        return ga.pickup_items((lines[0][0], ))

    key, selected_item_indexes = multi_select_lines_view(ga.io.whole_window, lines,
                                                   select_keys=Bind.Backpack_Select_Keys, header="Select items to pick up")
    if selected_item_indexes:
        return ga.pickup_items(selected_item_indexes)

    if key in Bind.Cancel:
        return


def drop_items(game_actions):
    ga = game_actions

    lines = tuple(Line(i, str(item)) for i, item in ga.enumerate_character_items())
    key, selected_item_indexes = multi_select_lines_view(ga.io.whole_window, lines,
                                                         select_keys=Bind.Backpack_Select_Keys,
                                                         header="Select items to drop".format(Bind.Backpack_Drop_Items.key))
    if key in Bind.Cancel:
        if selected_item_indexes:
            return ga.drop_items(selected_item_indexes)
