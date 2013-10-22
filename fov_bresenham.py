from generic_algorithms import bresenham

_mult = (
        (0, 0, 1, 1, 0, 0, -1, -1),
        (1, 1, 0, 0, -1, -1, 0, 0),
        (-1, -1, -1, 0, 1, 1, 1, 0),
        (-1, 0, 1, 1, 1, 0, -1, -1),
)

def get_light_set(visibility_func, start_coord, sight):
    light_set = set()
    sight_squared = sight * sight
    start_y, start_x = start_coord
    for octant in xrange(8):
        mult_y_i = _mult[0][octant]
        mult_x_i = _mult[1][octant]
        mult_y_s = _mult[2][octant]
        mult_x_s = _mult[3][octant]
        for i in range(sight):
            for y, x in bresenham(start_coord, (start_y + sight * mult_y_s + i * mult_y_i,
                                                start_x + sight * mult_x_s + i * mult_x_i)):
                if sight_squared < ((start_y - y) ** 2 + (start_x - x) ** 2):
                    break
                if (y, x) not in light_set:
                    light_set.add((y, x))
                if not visibility_func((y, x)):
                    break
    return light_set
