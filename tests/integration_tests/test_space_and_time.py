import logging
import time

from pyrl.engine import state_store
from pyrl.engine.creature.creature_picker import CreaturePicker
from pyrl.engine.creature.item import Weapon
from pyrl.engine.structures.dice import Dice
from pyrl.game_data.pyrl_creatures import PyrlCreature
from pyrl.game_data.pyrl_player import pyrl_player

def test_space_and_time() -> None:

    n = 10000

    player = pyrl_player()

    items_start = time.time()
    weapons = tuple(Weapon(f"Short Sword", i, Dice(1, 6, i)) for i in range(n))
    for weapon in weapons:
        player.inventory.bag_item(weapon)
    items_end = time.time()
    item_seconds = items_end - items_start

    creature_picker = CreaturePicker.using_speciation(PyrlCreature.templates(), area_level=20)

    creature_start = time.time()
    creatures = [creature_picker.spawn_random_creature() for _ in range(n)]
    creature_end = time.time()
    creature_seconds = creature_end - creature_start

    data = player, creatures
    state, compressed = state_store.pickle_data(data)
    assert len(state) < 5000000
    logging.info(f"{item_seconds=:.2} and {creature_seconds=:.2} to generate {n} instances")
    item_state, item_compressed = state_store.pickle_data(player)
    creature_state, creature_compressed = state_store.pickle_data(creatures)
    logging.info(f"{n} items and creatures store size: {state_store.compression_msg(state, compressed)}")
    logging.info(f"{n} items store size: {state_store.compression_msg(item_state, item_compressed)}")
    logging.info(f"{n} creatures store size: {state_store.compression_msg(creature_state, creature_compressed)}")
