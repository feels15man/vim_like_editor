# from normal_state import NormalState
# from insert_state import InsertState
# from find_state import FindState
# from command_state import CommandState
from MyString import MyString as MyString
from states.available_states import AvailableStates


class Controller():
    def __init__(self, adapter):
        # self.normal_state = NormalState(self)
        # self.insert_state = InsertState(self)
        # self.find_state = FindState(self)
        # self.command_state = CommandState(self)  # Н
        # self.state = AvailableStates.init_state()
        self.available_states = AvailableStates()
        self.state = self.available_states.normal_state(self)
        # self.state = self.normal_state
        self.search_type = None  # '/' или '?'
        self.adapter = adapter


    def set_model(self, model):
        self.model = model


    def change_state(self, state):
        self.state = state


    def process_input(self, ch=None):
        key = ch
        if not ch:
            key = self.adapter.get_key()
        result = self.state.process_input(key)

        if isinstance(self.state, (self.available_states.command_state_obj(), self.available_states.find_state_obj())):
        # if isinstance(self.state, (CommandState, FindState)):
            return result

        self.set_Text_View()

        return result


    def set_Text_View(self):
        term_height, term_width = self.adapter.get_screen_size()
        term_height -= 1  # Оставляем место для строки индикатора режима

        if self.model.cursor_y < self.model.scroll_offset:
            self.model.scroll_offset = self.model.cursor_y
        elif self.model.cursor_y >= self.model.scroll_offset + term_height:
            self.model.scroll_offset = self.model.cursor_y - term_height + 1

        max_scroll_offset = max(0, len(self.model.buffer) - term_height)
        self.model.scroll_offset = max(0, min(self.model.scroll_offset, max_scroll_offset))

        if self.model.cursor_x < self.model.horizontal_offset:
            self.model.horizontal_offset = self.model.cursor_x
        elif self.model.cursor_x >= self.model.horizontal_offset + term_width:
            self.model.horizontal_offset = self.model.cursor_x - term_width + 1

        self.model.scroll_offset = max(0, min(self.model.scroll_offset, max_scroll_offset))

        self.model.Text_String = [
            MyString(line.substr(self.model.horizontal_offset, min(line.length() - self.model.horizontal_offset,term_width-1)))
            if line.length() > self.model.horizontal_offset else MyString("")
            for line in self.model.buffer[self.model.scroll_offset:self.model.scroll_offset + term_height]
        ]
