import curses

d = {}

for x in range(7):
	curses.init_pair(x+1, x, 0)

brown = curses.color_pair(4) | curses.A_DIM

grey = curses.color_pair(0)
black_on_black = curses.color_pair(1)
red = curses.color_pair(2)
green = curses.color_pair(3)
yellow = curses.color_pair(4)
blue = curses.color_pair(5)
purple = curses.color_pair(6)
cyan = curses.color_pair(7)

white = curses.color_pair(0) | curses.A_BOLD
black = curses.color_pair(1) | curses.A_BOLD
light_red = curses.color_pair(2) | curses.A_BOLD
light_green = curses.color_pair(3) | curses.A_BOLD
light_yellow = curses.color_pair(4) | curses.A_BOLD
light_blue = curses.color_pair(5) | curses.A_BOLD
light_purple = curses.color_pair(6) | curses.A_BOLD
light_cyan = curses.color_pair(7) | curses.A_BOLD

normal = curses.A_NORMAL
blink = curses.A_BLINK
bold = curses.A_BOLD
dim = curses.A_DIM
reverse = curses.A_REVERSE
standout = curses.A_STANDOUT
underline = curses.A_UNDERLINE

d["brown"] = brown
d["grey"] = grey
d["black_on_black"] = black_on_black
d["red"] = red
d["green"] = green
d["yellow"] = yellow
d["blue"] = blue
d["purple"] = purple
d["cyan"] = cyan
d["white"] = white
d["black"] = black
d["light_red"] = light_red
d["light_green"] = light_green
d["light_yellow"] = light_yellow
d["light_blue"] = light_blue
d["light_purple"] = light_purple
d["light_cyan"] = light_cyan
d["normal"] = normal
d["blink"] = blink
d["bold"] = bold
d["dim"] = dim
d["reverse"] = reverse
d["standout"] = standout
d["underline"] = underline
