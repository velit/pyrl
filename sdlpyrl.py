#!/usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals

import main
import wrapper_libtcod


ROOT_WIN = 0
wrapper_libtcod.init(ROOT_WIN)
main.init_window_system(wrapper_libtcod)
main.start()
