from __future__ import annotations

from collections.abc import Callable

from pyrl.engine.behaviour.coordinates import bresenham
from pyrl.engine.enums.directions import Coord

IsVisible = Callable[[Coord], bool]

class ShadowCast:

    # Multipliers for transforming coordinates to other octants:
    _mult = (
            (1, 0, 0, -1, -1, 0, 0, 1),
            (0, 1, -1, 0, 0, -1, 1, 0),
            (0, 1, 1, 0, 0, -1, -1, 0),
            (1, 0, 0, 1, -1, 0, 0, -1),
    )

    @classmethod
    def get_light_set(cls, visible: IsVisible, coord: Coord, sight: int,
                      max_rows: int, max_cols: int) -> set[Coord]:
        y, x = coord
        light_set: set[Coord] = set()
        light_set.add(coord)
        for octant in range(8):
            cls._shadow_cast(light_set, visible, y, x, 1, 1.0, 0.0, sight, max_rows, max_cols,
                             cls._mult[0][octant], cls._mult[1][octant], cls._mult[2][octant], cls._mult[3][octant])
        return light_set

    # Based on an algorithm by Bjorn Bergstrom bjorn.bergstrom@roguelikedevelopment.org
    # http://roguebasin.roguelikedevelopment.org/index.php?title=FOV_using_recursive_shadowcasting
    @classmethod
    def _shadow_cast(cls, light_set: set[Coord], visible: IsVisible, cy: int, cx: int, row: int, start: float,
                     end: float, radius: int, max_rows: int, max_cols: int, xx: int, xy: int, yx: int, yy: int) -> None:
        """Recursive lightcasting function."""
        if start < end:
            return
        radius_squared = radius * radius
        for j in range(row, radius + 1):
            dx = -j - 1
            dy = -j
            blocked = False
            while dx <= 0:
                dx += 1
                # Translate the dx, dy coordinates into map coordinates:
                map_x = cx + dx * xx + dy * xy
                map_y = cy + dx * yx + dy * yy

                # Don't try to compute outside of the map
                if 0 <= map_y < max_rows and 0 <= map_x < max_cols:
                    # l_slope and r_slope store the slopes of the left and right
                    # extremities of the square we're considering:
                    l_slope = (dx - 0.5) / (dy + 0.5)
                    r_slope = (dx + 0.5) / (dy - 0.5)

                    if end > l_slope:
                        break
                    if start >= r_slope:
                        # Our light beam is touching this square; light it:
                        if dx * dx + dy * dy <= radius_squared:
                            light_set.add((map_y, map_x))

                        if blocked:
                            # we're scanning a row of blocked squares:
                            if not visible((map_y, map_x)):
                                new_start = r_slope
                            else:
                                blocked = False
                                start = new_start  # pyright: ignore [reportPossiblyUnboundVariable]
                        else:
                            if not visible((map_y, map_x)) and j < radius:
                                # This is a blocking square, start a child scan:
                                blocked = True
                                cls._shadow_cast(light_set, visible, cy, cx, j + 1, start, l_slope, radius,
                                                 max_rows, max_cols, xx, xy, yx, yy)
                                new_start = r_slope

            # Row is scanned; do next row unless last square was blocked:
            if blocked:
                break

class Bresenham:

    _mult = (
            (0, 0, 1, 1, 0, 0, -1, -1),
            (1, 1, 0, 0, -1, -1, 0, 0),
            (-1, -1, -1, 0, 1, 1, 1, 0),
            (-1, 0, 1, 1, 1, 0, -1, -1),
    )

    @classmethod
    def get_light_set(cls, visibility: IsVisible, start_coord: Coord, sight: int) -> set[Coord]:
        light_set: set[Coord] = set()
        sight_squared = sight * sight
        start_y, start_x = start_coord
        for octant in range(8):
            mult_y_i = cls._mult[0][octant]
            mult_x_i = cls._mult[1][octant]
            mult_y_s = cls._mult[2][octant]
            mult_x_s = cls._mult[3][octant]
            for i in range(sight):
                for y, x in bresenham(start_coord, (start_y + sight * mult_y_s + i * mult_y_i,
                                                    start_x + sight * mult_x_s + i * mult_x_i)):
                    if sight_squared < ((start_y - y) ** 2 + (start_x - x) ** 2):
                        break
                    if (y, x) not in light_set:
                        light_set.add((y, x))
                    if not visibility((y, x)):
                        break
        return light_set
