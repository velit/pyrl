from __future__ import absolute_import, division, print_function, unicode_literals

import random

import path
from config.debug import Debug
from enums.level_locations import LevelLocation
from creature.creature import Creature
from creature.actions import Action, Multiplier, Cost
from enums.directions import Dir
from generic_algorithms import bresenham, cross_product, get_vector, add_vector
from generic_structures import List2D
from turn_scheduler import TurnScheduler


class Level(object):

    def __init__(self, world_loc, level_template):
        self.world_loc = world_loc
        self.rows = level_template.rows
        self.cols = level_template.cols
        self.danger_level = level_template.danger_level
        self.passage_locations = level_template.passage_locations
        self.passage_destination_infos = level_template.passage_destination_infos
        self.tiles = List2D(level_template.tilemap, self.cols)
        #self.visible_change_observers = []
        self.modified_locations = set()
        self.turn_scheduler = TurnScheduler()
        self.creatures = {}

        for monster_file in level_template.static_monster_templates:
            self.add_creature(Creature(monster_file))

        if level_template.use_dynamic_monsters:
            self.creature_spawn_list = level_template.get_dynamic_monster_spawn_list()

            for _ in range(level_template.dynamic_monster_amount):
                monster_file = random.choice(self.creature_spawn_list)
                self.add_creature(Creature(monster_file))

    def legal_coord(self, coord, direction=(0, 0)):
        return (0 <= (coord[0] + direction[0]) < self.rows) and (0 <= (coord[1] + direction[1]) < self.cols)

    def get_free_coord(self):
        while True:
            coord = random.randrange(self.rows), random.randrange(self.cols)
            if self.is_passable(coord):
                return coord

    def get_coord_iter(self):
        for y in range(self.rows):
            for x in range(self.cols):
                yield y, x

    def get_exit(self, coord):
        return self.tiles[coord].exit_point

    def get_creature(self, coord):
        return self.creatures[coord]

    def get_visible_char(self, coord):
        if self.has_creature(coord):
            return self.get_creature(coord).char
        else:
            return self.tiles[coord].visible_char

    def get_memory_char(self, coord):
        return self.tiles[coord].memory_char

    def get_visible_data(self, coord_set):
        for coord in coord_set:
            yield coord, self.get_visible_char(coord)

    def get_wallhack_data(self, coord_set):
        for coord in coord_set:
            if self.has_creature(coord):
                char = self.get_creature(coord).char
            else:
                char = self.get_memory_char(coord)
            yield coord, char

    def get_memory_data(self, coord_set):
        for coord in coord_set:
            yield coord, self.get_memory_char(coord)

    def get_passage_coord(self, passage):
        if passage == LevelLocation.Passage_Random:
            return self.get_free_coord()
        else:
            return self.passage_locations[passage]

    def get_destination_info(self, passage):
        return self.passage_destination_infos[passage]

    def get_last_pathable_coord(self, coord_start, coord_end):
        last = coord_start
        for coord in bresenham(coord_start, coord_end):
            if self.is_pathable(coord):
                last = coord
            else:
                break
        return last

    def get_neighbor_coords_and_costs(self, coord):
        for direction in self.get_passable_neighbors(coord):
            neighbor_coord = add_vector(coord, direction)
            multiplier = self.movement_multiplier(coord, direction)
            yield neighbor_coord, round(multiplier * Cost.Move.value)

    def get_passable_neighbors(self, coord):
        for direction in Dir.All:
            neighbor_coord = add_vector(coord, direction)
            if self.legal_coord(neighbor_coord) and self.tiles[neighbor_coord].is_passable:
                yield direction

    def has_creature(self, coord):
        return coord in self.creatures

    def has_exit(self, coord):
        return self.tiles[coord].exit_point is not None

    def is_passable(self, coord):
        if self.has_creature(coord):
            return False
        else:
            return self.tiles[coord].is_passable

    def is_pathable(self, coord):
        return self.tiles[coord].is_passable

    def is_see_through(self, coord):
        return self.tiles[coord].is_see_through

    def pop_modified_locations(self):
        mod_locs = self.modified_locations
        self.modified_locations = set()
        return mod_locs

    def check_los(self, coordA, coordB):
        return not (any(not self.is_see_through(coord) for coord in bresenham(coordA, coordB)) and
                    any(not self.is_see_through(coord) for coord in bresenham(coordB, coordA)))

    def distance_heuristic(self, coordA, coordB):
        return round(path.heuristic(coordA, coordB, Cost.Move.value, Multiplier.Diagonal))

    def movement_multiplier(self, coord, direction):
        origin_multiplier = self.tiles[coord].movement_multiplier
        target_coord = add_vector(coord, direction)
        target_multiplier = self.tiles[target_coord].movement_multiplier

        tile_multiplier = (origin_multiplier + target_multiplier) / 2

        if direction in Dir.Orthogonals:
            return tile_multiplier * Multiplier.Orthogonal
        elif direction in Dir.Diagonals:
            return tile_multiplier * Multiplier.Diagonal
        elif direction == Dir.Stay:
            return tile_multiplier * Multiplier.Stay
        else:
            raise ValueError("Invalid direction: {}".format(direction))

    # nudge_coord nudges towards a line between end_coord and nudge_coord
    def _a_star_heuristic(self, start_coord, end_coord, nudge_coord):
        cost = self.distance_heuristic(start_coord, end_coord)
        if Debug.cross:
            cost += cross_product(start_coord, end_coord, nudge_coord) / Debug.cross_mod
        return cost

    def path(self, start_coord, goal_coord):
        return path.path(start_coord, goal_coord, self.get_neighbor_coords_and_costs, self._a_star_heuristic)

    def look_information(self, coord):
        #if coord in creature.visited_locations:
        information = "{}x{} ".format(*coord)
        if self.has_creature(coord):
            c = self.get_creature(coord)
            msg = "{} hp:{}/{} sight:{} armor:{} dr:{} ar:{} attack:{}D{}+{}"
            information += msg.format(c.name, c.hp, c.max_hp, c.sight, c.armor,
                                      c.defense_rating, c.attack_rating, *c.get_damage_info())
            if hasattr(c, "target_coord"):
                information += " target:{}".format(c.target_coord)
            if hasattr(c, "chase_vector"):
                information += " direction:{}".format(c.chase_vector)
        else:
            information += self.tiles[coord].name
        return information
        #else:
        #   return "You don't know anything about this place."

    def add_creature_to_passage(self, creature, passage, turnscheduler_add=False):
        self.add_creature(creature, coord=self.get_passage_coord(passage),
                          turnscheduler_add=turnscheduler_add)

    def add_creature(self, creature, coord=None, turnscheduler_add=True):
        if coord is None:
            coord = self.get_free_coord()
        elif self.has_creature(coord):
            blocking_creature = self.creatures[coord]
            self.move_creature(blocking_creature, self.get_free_coord())
        self.creatures[coord] = creature
        self.modified_locations.add(coord)
        creature.coord = coord
        creature.level = self

        if turnscheduler_add:
            self.turn_scheduler.add(creature, creature.action_cost(Action.Move))

    def remove_creature(self, creature, turnscheduler_remove=True):
        coord = creature.coord
        del self.creatures[coord]
        self.modified_locations.add(coord)
        creature.coord = None
        creature.level = None
        if turnscheduler_remove:
            self.turn_scheduler.remove(creature)

    def move_creature(self, creature, new_coord):
        self.modified_locations.add(creature.coord)
        self.modified_locations.add(new_coord)
        del self.creatures[creature.coord]
        self.creatures[new_coord] = creature
        creature.coord = new_coord

    def move_creature_to_dir(self, creature, direction):
        target_coord = add_vector(creature.coord, direction)
        self.move_creature(creature, target_coord)

    def swap_creature(self, creatureA, creatureB):
        self.modified_locations.add(creatureA.coord)
        self.modified_locations.add(creatureB.coord)
        self.creatures[creatureA.coord] = creatureB
        self.creatures[creatureB.coord] = creatureA
        creatureA.coord, creatureB.coord = creatureB.coord, creatureA.coord

    def creature_can_reach(self, creature, target_coord):
        if creature.coord == target_coord:
            return True
        else:
            vector = get_vector(creature.coord, target_coord)
            if vector in Dir.All:
                return True
            else:
                return False

    def creature_can_move(self, creature, direction):
        if direction not in Dir.AllPlusStay:
            raise ValueError("Illegal movement direction: {}".format(direction))
        elif direction == Dir.Stay:
            return True
        elif self.legal_coord(creature.coord, direction):
            coord = add_vector(creature.coord, direction)
            return self.is_passable(coord)
        else:
            return False

    def creature_has_sight(self, creature, target_coord):
        cy, cx = creature.coord
        ty, tx = target_coord
        if (cy - ty) ** 2 + (cx - tx) ** 2 <= creature.sight ** 2:
            return self.check_los(creature.coord, target_coord)
        else:
            return False
