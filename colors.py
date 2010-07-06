import curses

for x in range(7):
	curses.init_pair(x+1, x, 0)

color = {}

color["brown"] = curses.color_pair(4) | curses.A_DIM

color["grey"] = curses.color_pair(0)
color["normal"] = curses.color_pair(0)
color["black_on_black"] = curses.color_pair(1)
color["red"] = curses.color_pair(2)
color["green"] = curses.color_pair(3)
color["yellow"] = curses.color_pair(4)
color["blue"] = curses.color_pair(5)
color["purple"] = curses.color_pair(6)
color["cyan"] = curses.color_pair(7)

color["white"] = curses.color_pair(0) | curses.A_BOLD
color["black"] = curses.color_pair(1) | curses.A_BOLD
color["light_red"] = curses.color_pair(2) | curses.A_BOLD
color["light_green"] = curses.color_pair(3) | curses.A_BOLD
color["light_yellow"] = curses.color_pair(4) | curses.A_BOLD
color["light_blue"] = curses.color_pair(5) | curses.A_BOLD
color["light_purple"] = curses.color_pair(6) | curses.A_BOLD
color["light_cyan"] = curses.color_pair(7) | curses.A_BOLD

color["normal"] = curses.A_NORMAL
color["blink"] = curses.A_BLINK
color["bold"] = curses.A_BOLD
color["dim"] = curses.A_DIM
color["reverse"] = curses.A_REVERSE
color["standout"] = curses.A_STANDOUT
color["underline"] = curses.A_UNDERLINE
