from adapter.curses_adapter import CursesAdapter
import curses


class ViewAdapter(CursesAdapter):
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

    def draw_text(self, y: int, x: int, text: str):
        self.stdscr.addstr(y, x, text)

    def refresh(self):
        self.stdscr.refresh()

    def move_cursor(self, y: int, x: int):
        self.stdscr.move(y, x)

    def clear_screen(self):
        self.stdscr.clear()

    def cleanup(self):
        if self.stdscr:
            self.curses.nocbreak()
            self.stdscr.keypad(False)
            self.curses.echo()
            self.curses.endwin()

    def update_line(self, y: int, text: str):
        self.stdscr.move(y, 0)
        self.stdscr.clrtoeol()
        self.stdscr.addstr(y, 0, text)

    def get_screen_size(self):
        return self.stdscr.getmaxyx()

    def close(self):
        self.curses.endwin()