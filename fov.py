import curses
from io import IO

# Multipliers for transforming coordinates to other octants:
mult = [[1,  0,  0, -1, -1,  0,  0,  1],
		[0,  1, -1,  0,  0, -1,  1,  0],
		[0,  1,  1,  0,  0, -1, -1,  0],
		[1,  0,  0,  1, -1,  0,  0, -1]]

# Algorithm by Bjorn Bergstrom bjorn.bergstrom@roguelikedevelopment.org Copyright 2001 
# http://roguebasin.roguelikedevelopment.org/index.php?title=FOV_using_recursive_shadowcasting
def _cast_light(level, cy, cx, row, start, end, radius, xx, xy, yx, yy):
	"Recursive lightcasting function"
	if start < end:
		return
	radius_squared = radius*radius
	for j in range(row, radius+1):
		dx, dy = -j-1, -j
		blocked = False
		while dx <= 0:
			dx += 1
			# Translate the dx, dy coordinates into map coordinates:
			X, Y = cx + dx * xx + dy * xy, cy + dx * yx + dy * yy
			# l_slope and r_slope store the slopes of the left and right
			# extremities of the square we're considering:
			l_slope, r_slope = (dx-0.5)/(dy+0.5), (dx+0.5)/(dy-0.5)
			if start < r_slope:
				continue
			elif end > l_slope:
				break
			else:
				# Our light beam is touching this square; light it:
				if dx*dx + dy*dy < radius_squared:
					level.visitSquare(Y, X)
				if blocked:
					# we're scanning a row of blocked squares:
					if not level.seeThrough(Y, X):
						new_start = r_slope
						continue
					else:
						blocked = False
						start = new_start
				else:
					if not level.seeThrough(Y, X) and j < radius:
						# This is a blocking square, start a child scan:
						blocked = True
						_cast_light(level, cy, cx, j+1, start, l_slope, radius, xx, xy, yx, yy)
						new_start = r_slope
		# Row is scanned; do next row unless last square was blocked:
		if blocked:
			break

def doFov(creature, level):
	"Calculate lit squares from the given location and radius"
	IO().clearLos()
	y,x = level.squares[creature].loc
	radius = creature.sight
	if radius != 0:
		level.visitSquare(y,x)
	for oct in range(8):
		_cast_light(level, y, x, 1, 1.0, 0.0, radius, mult[0][oct], mult[1][oct], mult[2][oct], mult[3][oct])
	IO().drawLos()
