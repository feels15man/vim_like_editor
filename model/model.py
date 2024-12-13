from MyString import MyString as MyString
from observer.observer import Subject


class Model(Subject):
    def __init__(self, controller, view):
        super().__init__()  
        self.controller = controller
        self.view = view
        self.buffer = [MyString("")]
        self.cursor_x = 0
        self.cursor_y = 0
        self.changed_lines = set()
        self.command_buffer = MyString("")  
        self.clipboard = MyString("")  
        self.add_observer(self.view)
        self.scroll_offset = 0
        self.horizontal_offset = 0
        self.last_mode_line = None

        self.search_results = []  
        self.search_index = -1  
        self.find_buffer = MyString("")

        self.status_message = None

        self.mode_string = MyString("-- NORMAL MODE --")
        self.Text_String = MyString("")
        self.filename = None