import const.game as GAME
import const.colors as COLOR

from level_file import LevelFile
from monster_file import MonsterFile
from char import Char

L0 = LevelFile(
		danger_level=1,
		#static_level=True,
		#use_dynamic_monsters=False,
)

L0.add_monster_file(MonsterFile("The Crone", Char('@', COLOR.PURPLE)))

#L0.add_walls()
#L0.passage_locations[GAME.PASSAGE_UP] = (15, 21)
#L0.passage_locations[GAME.PASSAGE_DOWN] = (19, 81)
#L0.tilefile = \
list(
"################################################################################################"
"##.####################################.........................######..................########"
"##.#...............................####......######################################.....########"
"##.#.......############################......#.................................####.....########"
"##.#.......#........................###......#.####################################.############"
"##.#.......#......#####################........#####################..........................##"
"##.#..............############################...............##########################.......##"
"##.#.......#......#####...................####.###################......#########.#####.......##"
"##.#.......#......#####...........############............########......#......##.#####.......##"
"##.#######.#......#####...........############.###################.............##.#####.......##"
"##.#######.##.#.#######.........................................##......#......##.#######.##.###"
"##.#######.##.#.#############.################################.###......#########.##.......#.###"
"#........#.##.#.#........................###.........#########.###......#########.##.......#.###"
"#........#.##.#.#.......#########.##########.........#.......#.###......##........##.......#.###"
"#..........##.#.#.......#.............######.........#.......#.###......#########.##.......#.###"
"#........#.##.#.#....<..#########.....######.........#.......#.#####.############.##.......#.###"
"##########.##.#.#.......#.......#.....######.........#.......#.###...........####.##.......#.###"
"###############.................##############.#######.......#.###...........####.##.......#.###"
"##.....########.#.......#.........................####.......#####...........####.####.#####.###"
"##.....##.....#.#.......################.#############.......#####...............>.......###.###"
"##.....##.......####################..........########.################.######...........###.###"
"#####.###.....######################....................................######...........#######"
"#...............................####..........##################################################"
"####################################.....................................................#######"
"################################################################################################"
"################################################################################################")

first = [
"ggggggggggggggggggggggggggggg",
"ggggggggggggggggggg#########w",
"ggggggggggggggggggg#====#...w",
"ggggggggggggggggggg#..../...w",
"ggg##ooo############....#####",
"ggg#.cc.===#==cc=../.==./.==#",
"ggg#S....../.......####/#...#",
"ggg#O--...p#--.cc..<###.#...#",
"ggg#F--.--p###/##=.####.#.|.#",
"ggg#A..###.#s..T#=.>#####|C|#",
"ggg#.c.#.#.#=.tU#=.######|A|#",
"ggg#cTc###.####B##.######|R|#",
"ggg#cAc==TV..###==.#====#|^|#",
"ggg#cBc....../...../....#...#",
"gggocLc......#=...#=....#...#",
"gggocEc..cc.-#=..=#=.---#...#",
"ggg#.c.==...-#=..=#=.BED#+++#",
"ggg###########=..=#=.---#gggg",
"ggggggggggggg#=--=#=....#gggg",
"gggggggggggggo=--=#=.---ogggg",
"ggggggggggggg#ooo####ooo#gggg",
"ggggggggggggggggggggggggggggg",
]
