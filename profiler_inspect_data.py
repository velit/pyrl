from __future__ import absolute_import, division, print_function, unicode_literals

#!/usr/bin/python

import sys
import pstats

if len(sys.argv) > 1:
    arg = sys.argv[1]
    p = pstats.Stats(arg)
    p.sort_stats(-1).print_stats()
    print("Cumulative stats")
    p.sort_stats('cumulative').print_stats()
else:
    print "This program requires an argument"
