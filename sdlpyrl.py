#!/usr/bin/env python2
from __future__ import absolute_import, division, print_function, unicode_literals

import main
from io_wrappers.libtcod import LibTCODWrapper


main.init_window_system(LibTCODWrapper())
main.start()
