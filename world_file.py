import const.game as GAME
import const.maps as MAP

from level_file import LevelFile


class LevelNotFound(Exception):
    pass


class WorldFile(object):

    def __init__(self):
        self.level_files = {}
        self.level_passageways = {}
        self.dungeon_lengths = {}

        self.add_dungeon(GAME.DUNGEON)
        self.add_level(GAME.DUNGEON, MAP.L0)
        for x in xrange(GAME.LEVELS_PER_DUNGEON - 1):
            self.add_level(GAME.DUNGEON)

    def add_dungeon(self, dungeon_key):
        self.dungeon_lengths[dungeon_key] = 1

    def add_level(self, dungeon_key, level_file=None):
        level_i = self.dungeon_lengths[dungeon_key]
        if level_file is None:
            self.level_files[dungeon_key, level_i] = LevelFile(level_i)
        else:
            self.level_files[dungeon_key, level_i] = level_file
        self.level_passageways[dungeon_key, level_i] = {GAME.PASSAGE_UP: GAME.UP,
                                                        GAME.PASSAGE_DOWN: GAME.DOWN}
        self.dungeon_lengths[dungeon_key] += 1

    def get_level_file(self, world_loc):
        try:
            return self.level_files[world_loc]
        except KeyError:
            raise LevelNotFound("Nonexistant level key: {}".format(world_loc))

    def pop_level_file(self, world_loc):
        try:
            level_file = self.level_files[world_loc]
        except KeyError:
            raise LevelNotFound("Nonexistant level key: {}".format(world_loc))
        else:
            del self.level_files[world_loc]
            return level_file

    def get_passage_info(self, world_loc, passage):
        return self.level_passageways[world_loc][passage]
