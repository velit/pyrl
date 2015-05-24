from __future__ import absolute_import, division, print_function, unicode_literals


class CreatureTemplate(object):
    def __init__(self, name, char, speciation_lvl=0, extinction_lvl=0, coord=None):
        self.name = name
        self.char = char
        self.speciation_lvl = speciation_lvl
        self.extinction_lvl = extinction_lvl
        self.coord = coord

        self.base_strength     = 10
        self.base_dexterity    = 10
        self.base_endurance    = 10
        self.base_intelligence = 10
        self.base_perception   = 10
