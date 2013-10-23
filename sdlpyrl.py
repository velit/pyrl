#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import main
import wrapper_libtcod

ROOT_WIN = 0
wrapper_libtcod.init(ROOT_WIN)
main.init_window_system(wrapper_libtcod)
main.start()
