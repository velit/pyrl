from __future__ import absolute_import, division, print_function, unicode_literals

import pytest

from level_template import LevelTemplate
from rdg import generate_tilemap


def run_all():
    test_rdg_generation()


@pytest.mark.slow
def test_rdg_generation():

    for _ in range(300):
        lt = LevelTemplate()
        generate_tilemap(lt)
