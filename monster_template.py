from __future__ import absolute_import, division, print_function, unicode_literals

class MonsterTemplate(object):
    def __init__(self, name, char, speciation_lvl=0, extinction_lvl=0):
        self.name = name
        self.char = char
        self.speciation_lvl = speciation_lvl
        self.extinction_lvl = extinction_lvl
