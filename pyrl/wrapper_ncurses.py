from const.game import NCURSES, SCREEN_ROWS, SCREEN_COLS
import const.keys as KEY
import const.colors as COLOR
import curses
import curses.ascii


class Curses256ColorDict(dict):

    CURSES_ATTR = {
        COLOR.BASE_RED: 124,
        COLOR.BASE_GREEN: 34,
        COLOR.BASE_BLUE: 21,
        COLOR.BASE_PURPLE: 129,
        COLOR.BASE_CYAN: 37,
        COLOR.BASE_YELLOW: 227,
        COLOR.BASE_BROWN: 130,

        COLOR.BASE_DARK_BLUE: 19,
        COLOR.BASE_DARK_BROWN: 94,

        COLOR.BASE_LIGHT_RED: 203,
        COLOR.BASE_LIGHT_GREEN: 83,
        COLOR.BASE_LIGHT_BLUE: 63,
        COLOR.BASE_LIGHT_PURPLE: 207,
        COLOR.BASE_LIGHT_CYAN: 87,

        COLOR.BASE_WHITE: 231,
        COLOR.BASE_LIGHT: 253,
        COLOR.BASE_NORMAL: curses.COLOR_WHITE,
        COLOR.BASE_LIGHT_GRAY: 248,
        COLOR.BASE_GRAY: 245,
        COLOR.BASE_DARK_GRAY: 242,
        COLOR.BASE_DARK: 239,
        COLOR.BASE_DARKER: 236,
        COLOR.BASE_DARKEST: 233,
        COLOR.BASE_BLACK: 16,
    }

    def __init__(self):
        dict.__init__(self)
        # 0 is hard-coded to be curses.NORMAL in curses
        self.pair_nr = 1

    def __getitem__(self, key):
        try:
            return dict.__getitem__(self, key)
        except KeyError:
            fg, bg = key
            curses.init_pair(self.pair_nr, self.CURSES_ATTR[fg], self.CURSES_ATTR[bg])
            color_pair = curses.color_pair(self.pair_nr)
            self[key] = color_pair
            self.pair_nr += 1
            return color_pair


class CursesColorDict(dict):

    CURSES_ATTR = {
        COLOR.BASE_BLACK: curses.COLOR_BLACK,
        COLOR.BASE_RED: curses.COLOR_RED,
        COLOR.BASE_GREEN: curses.COLOR_GREEN,
        COLOR.BASE_BROWN: curses.COLOR_YELLOW,
        COLOR.BASE_BLUE: curses.COLOR_BLUE,
        COLOR.BASE_PURPLE: curses.COLOR_MAGENTA,
        COLOR.BASE_CYAN: curses.COLOR_CYAN,
        COLOR.BASE_GRAY: curses.COLOR_WHITE,

        COLOR.BASE_DARK_BLUE: curses.COLOR_BLUE,
        COLOR.BASE_DARK_BROWN: curses.COLOR_YELLOW,

        COLOR.BASE_LIGHT_RED: curses.COLOR_RED,
        COLOR.BASE_LIGHT_GREEN: curses.COLOR_GREEN,
        COLOR.BASE_YELLOW: curses.COLOR_YELLOW,
        COLOR.BASE_LIGHT_BLUE: curses.COLOR_BLUE,
        COLOR.BASE_LIGHT_PURPLE: curses.COLOR_MAGENTA,
        COLOR.BASE_LIGHT_CYAN: curses.COLOR_CYAN,

        COLOR.BASE_WHITE: curses.COLOR_WHITE,
        COLOR.BASE_LIGHT: curses.COLOR_WHITE,
        COLOR.BASE_NORMAL: curses.COLOR_WHITE,
        COLOR.BASE_LIGHT_GRAY: curses.COLOR_WHITE,
        COLOR.BASE_GRAY: curses.COLOR_WHITE,
        COLOR.BASE_DARK_GRAY: curses.COLOR_WHITE,
        COLOR.BASE_DARK: curses.COLOR_BLACK,
        COLOR.BASE_DARKER: curses.COLOR_BLACK,
        COLOR.BASE_DARKEST: curses.COLOR_BLACK,
    }

    BASIC_COLORS = {COLOR.BASE_NORMAL, COLOR.BASE_WHITE, COLOR.BASE_BLACK, COLOR.BASE_RED,
            COLOR.BASE_GREEN, COLOR.BASE_BLUE, COLOR.BASE_PURPLE, COLOR.BASE_CYAN,
            COLOR.BASE_BROWN, COLOR.BASE_DARK_GRAY, COLOR.BASE_GRAY, COLOR.BASE_LIGHT_GRAY}

    def __init__(self):
        dict.__init__(self)
        # 0 is hard-coded to be NORMAL
        self.pair_nr = 1

    def __getitem__(self, key):
        try:
            return dict.__getitem__(self, key)
        except KeyError:
            fg, bg = key
            curses.init_pair(self.pair_nr, self.CURSES_ATTR[fg], self.CURSES_ATTR[bg])
            if fg not in self.BASIC_COLORS:
                color_pair = curses.color_pair(self.pair_nr) | curses.A_BOLD
            else:
                color_pair = curses.color_pair(self.pair_nr)
            self[key] = color_pair
            self.pair_nr += 1
            return color_pair


CURSES_COLOR = None
CURSES_KEYS = {
    curses.ascii.CR: KEY.ENTER,
    curses.ascii.TAB: KEY.TAB,
    curses.ascii.SP: KEY.SPACE,
    curses.ascii.ESC: KEY.ESC,
    curses.KEY_UP: KEY.UP,
    curses.KEY_DOWN: KEY.DOWN,
    curses.KEY_LEFT: KEY.LEFT,
    curses.KEY_RIGHT: KEY.RIGHT,
    curses.KEY_HOME: KEY.HOME,
    curses.KEY_END: KEY.END,
    curses.KEY_NPAGE: KEY.PAGE_DOWN,
    curses.KEY_PPAGE: KEY.PAGE_UP,
    curses.KEY_A1: KEY.NUMPAD_7,
    curses.KEY_A3: KEY.NUMPAD_9,
    curses.KEY_B2: KEY.NUMPAD_5,
    curses.KEY_C1: KEY.NUMPAD_1,
    curses.KEY_C3: KEY.NUMPAD_3,
    curses.KEY_IC: KEY.INSERT,
    curses.KEY_DC: KEY.DELETE,
    curses.KEY_BACKSPACE: KEY.BACKSPACE,
    curses.KEY_FIND: KEY.NUMPAD_7,
    curses.KEY_SELECT: KEY.NUMPAD_1,
    curses.KEY_F1: KEY.F1,
    curses.KEY_F2: KEY.F2,
    curses.KEY_F3: KEY.F3,
    curses.KEY_F4: KEY.F4,
    curses.KEY_F5: KEY.F5,
    curses.KEY_F6: KEY.F6,
    curses.KEY_F7: KEY.F7,
    curses.KEY_F8: KEY.F8,
    curses.KEY_F9: KEY.F9,
    curses.KEY_F10: KEY.F10,
    curses.KEY_F11: KEY.F11,
    curses.KEY_F12: KEY.F12,
    curses.KEY_RESIZE: KEY.WINDOW_RESIZE,
}
ROOT_WIN = None

def init(root_window):
    global CURSES_COLOR, ROOT_WIN

    curses.curs_set(0)
    curses.nonl()

    ROOT_WIN = root_window
    if curses.COLORS == 256:
        CURSES_COLOR = Curses256ColorDict()
    else:
        CURSES_COLOR = CursesColorDict()
    _window_resized()

def init_handle(window):
    window.keypad(True)

# Writing to the last cell of a window raises an exception because
# the automatic cursor move to the next cell is illegal. The +1 fixes that.
def new_window(size):
    rows, columns = size
    window = curses.newpad(rows + 1, columns)
    init_handle(window)
    return window

def _window_resized():
    rows, cols = get_dimensions(ROOT_WIN)
    while rows < SCREEN_ROWS or cols < SCREEN_COLS:
        message = "Game needs at least a screen size of {}x{} while the current size is {}x{}. " \
                "Please resize the screen or press Q to quit immediately."
        addstr(ROOT_WIN, 0, 0, message.format(SCREEN_COLS, SCREEN_ROWS, rows, cols))
        if get_key(ROOT_WIN) == "Q":
            exit()
        rows, cols = get_dimensions(ROOT_WIN)

def flush():
    curses.doupdate()

def get_root_window():
    return ROOT_WIN

def suspend():
    curses.def_prog_mode()
    curses.reset_shell_mode()
    curses.endwin()

def resume():
    curses.reset_prog_mode()

def addch(window, y, x, char):
    symbol, color = char
    window.addch(y, x, symbol, CURSES_COLOR[color])

def addstr(window, y, x, string, color=None):
    if color is None:
        window.addstr(y, x, string)
    else:
        window.addstr(y, x, string, CURSES_COLOR[color])

def draw(window, char_payload_sequence):
    f = window.addch
    COLOR_LOOKUP = CURSES_COLOR
    for y, x, (symbol, color) in char_payload_sequence:
        f(y, x, symbol, COLOR_LOOKUP[color])

def draw_reverse(window, char_payload_sequence):
    f = window.addch
    COLOR_LOOKUP = CURSES_COLOR
    for y, x, (symbol, (fg, bg)) in char_payload_sequence:
        f(y, x, symbol, COLOR_LOOKUP[bg, fg])

def _esc_key_handler(window, ch):
    if ch == curses.ascii.ESC:
        window.nodelay(True)
        second_ch = window.getch()
        window.nodelay(False)
        if second_ch != curses.ERR:
            return curses.ascii.alt(second_ch)
    return ch

def _interpret_ch(ch):
    if ch == curses.KEY_RESIZE:
        _window_resized()
    if ch in CURSES_KEYS:
        return CURSES_KEYS[ch]
    ch = curses.ascii.unctrl(ch)
    if '^' in ch:
        return ch.lower()
    else:
        return ch

def get_key(window):
    return _interpret_ch(_esc_key_handler(window, window.getch()))

def check_key(window):
    window.nodelay(True)
    ch = window.getch()
    window.nodelay(False)
    if ch == curses.ERR:
        return KEY.NO_INPUT
    else:
        return _interpret_ch(_esc_key_handler(window, ch))

def clear(window):
    window.erase()

def blit(window, size, screen_position):
    screen_rows, screen_cols = get_dimensions(ROOT_WIN)
    if screen_rows < SCREEN_ROWS or screen_cols < SCREEN_COLS:
        _window_resized()
    rows, cols = size
    y, x = screen_position
    window.noutrefresh(0, 0, y, x, y + rows - 1, x + cols - 1)

def get_dimensions(window):
    rows, columns = window.getmaxyx()
    return rows, columns

def move(window, y, x):
    window.move(y, x)

def get_cursor_pos(window):
    return window.getyx()

def get_implementation():
    return NCURSES
