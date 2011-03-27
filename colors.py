import curses

d = {}


def init_colors():
	for x in range(7):
		curses.init_pair(x + 1, x, 0)

	d["brown"] = curses.color_pair(4) | curses.A_DIM

	d["grey"] = curses.color_pair(0)
	d["black_on_black"] = curses.color_pair(1)
	d["red"] = curses.color_pair(2)
	d["green"] = curses.color_pair(3)
	d["yellow"] = curses.color_pair(4)
	d["blue"] = curses.color_pair(5)
	d["purple"] = curses.color_pair(6)
	d["cyan"] = curses.color_pair(7)

	d["white"] = curses.color_pair(0) | curses.A_BOLD
	d["black"] = curses.color_pair(1) | curses.A_BOLD
	d["light_red"] = curses.color_pair(2) | curses.A_BOLD
	d["light_green"] = curses.color_pair(3) | curses.A_BOLD
	d["light_yellow"] = curses.color_pair(4) | curses.A_BOLD
	d["light_blue"] = curses.color_pair(5) | curses.A_BOLD
	d["light_purple"] = curses.color_pair(6) | curses.A_BOLD
	d["light_cyan"] = curses.color_pair(7) | curses.A_BOLD

	d["normal"] = curses.A_NORMAL

	_temp = {}
	for key, value in d.items():
		_temp[key + "r"] = value | curses.A_REVERSE
	d.update(_temp)

	d["blink"] = curses.A_BLINK
	d["bold"] = curses.A_BOLD
	d["dim"] = curses.A_DIM
	d["reverse"] = curses.A_REVERSE
	d["standout"] = curses.A_STANDOUT
	d["underline"] = curses.A_UNDERLINE
