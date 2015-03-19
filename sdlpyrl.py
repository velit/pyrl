#!/usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals

import main
from wrapper_libtcod import LibTCODWrapper


main.init_window_system(LibTCODWrapper())
main.start()
