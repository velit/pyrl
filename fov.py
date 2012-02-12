# Multipliers for transforming coordinates to other octants:
from __future__ import division
_mult = ((1, 0, 0, -1, -1, 0, 0, 1),
		(0, 1, -1, 0, 0, -1, 1, 0),
		(0, 1, 1, 0, 0, -1, -1, 0),
		(1, 0, 0, 1, -1, 0, 0, -1))

def get_light_set(visibility_func, coord, sight):
	y, x = coord
	light_set = set([(y, x)])
	for oct in xrange(8):
		_shadow_cast(light_set, visibility_func, y, x, 1, 1.0, 0.0, sight,
				_mult[0][oct], _mult[1][oct], _mult[2][oct], _mult[3][oct])
	return light_set

# Algorithm by Bjorn Bergstrom bjorn.bergstrom@roguelikedevelopment.org
# Copyright 2001
# http://roguebasin.roguelikedevelopment.org/index.php?title=FOV_using_recursive_shadowcasting

def _shadow_cast(light_set, visibility_func, cy, cx, row, start, end, r, xx, xy, yx, yy):
	"""Recursive lightcasting function"""
	if start < end:
		return
	radius_squared = r * r
	for j in xrange(row, r + 1):
		dx, dy = 0 - 1 - j, 0 - j
		blocked = False
		while dx <= 0:
			dx += 1
			# Translate the dx, dy coordinates into map coordinates:
			X, Y = cx + dx * xx + dy * xy, cy + dx * yx + dy * yy
			# l_slope and r_slope store the slopes of the left and right
			# extremities of the square we're considering:
			l_slope, r_slope = (dx - 0.5) / (dy + 0.5), (dx + 0.5) / (dy - 0.5)
			if start < r_slope:
				continue
			elif end > l_slope:
				break
			else:
				# Our light beam is touching this square; light it:
				if dx * dx + dy * dy <= radius_squared:
					light_set.add((Y, X))
				if blocked:
					# we're scanning a row of blocked squares:
					if not visibility_func((Y, X)):
						new_start = r_slope
						continue
					else:
						blocked = False
						start = new_start
				else:
					if not visibility_func((Y, X)) and j < r:
						# This is a blocking square, start a child scan:
						blocked = True
						_shadow_cast(light_set, visibility_func, cy, cx, j + 1, start, l_slope, r, xx, xy, yx, yy)
						new_start = r_slope
		# Row is scanned; do next row unless last square was blocked:
		if blocked:
			break
