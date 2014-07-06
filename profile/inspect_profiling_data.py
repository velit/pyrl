#!/usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals


import sys
import pstats

if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        p = pstats.Stats(arg)

        p.strip_dirs().sort_stats('cumulative').print_stats(20)
        p.strip_dirs().sort_stats('time').print_stats(20)
        p.sort_stats(-1).print_stats()
    else:
        print("This program requires an argument")
