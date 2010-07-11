def swap(y, x):
	return x, y

def bresenham(y0, x0, y1, x1, includelast=True):
	steep = abs(x1 - x0) > abs(y1 - y0)
	if steep:
		y0, x0 = swap(y0, x0)
		y1, x1 = swap(y1, x1)
	if y0 > y1:
		y0, y1 = swap(y0, y1)
		x0, x1 = swap(x0, x1)
	deltay = y1 - y0
	deltax = abs(x1 - x0)
	error = deltay / 2
	x = x0
	xstep = 1 if x0 < x1 else -1
	for y in range(y0, y1+includelast):
		yield (x, y) if steep else (y, x)
		error -= deltax
		if error < 0:
			x += xstep
			error += deltay
