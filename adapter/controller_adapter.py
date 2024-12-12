from adapter.curses_adapter import CursesAdapter
import curses
import curses.ascii


class ControllerAdapter(CursesAdapter):
    def __init__(self):
        self.stdscr = None
        self.curses = None

    def initialize(self):
        self.stdscr = curses.initscr()
        self.curses = curses
        self.curses.start_color()
        self.curses.cbreak()
        self.curses.noecho()
        self.stdscr.keypad(True)
        self.curses.curs_set(1)

    def move_cursor(self, y: int, x: int):
        self.stdscr.move(y, x)

    @property
    def key_down(self):
        return self.curses.KEY_DOWN

    @property
    def key_up(self):
        return self.curses.KEY_UP

    @property
    def key_left(self):
        return self.curses.KEY_LEFT

    @property
    def key_right(self):
        return self.curses.KEY_RIGHT

    @property
    def key_backspace(self):
        return self.curses.KEY_BACKSPACE

    @property
    def key_escape(self):
        return self.curses.ascii.ESC

    def get_key(self) -> int:
        return self.stdscr.getch()

    def get_screen_size(self):
        return self.stdscr.getmaxyx()

