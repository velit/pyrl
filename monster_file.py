from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

class MonsterFile(object):
    def __init__(self, name, char, speciation_lvl=0, extinction_lvl=0):
        self.name = name
        self.char = char
        self.speciation_lvl = speciation_lvl
        self.extinction_lvl = extinction_lvl
