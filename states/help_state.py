from MyString import MyString as MyString
from states.state import State


class HelpState(State):
    def __init__(self, controller):
        super().__init__(controller)
        self.old_text = self.controller.model.buffer.copy()
        self.old_file = self.controller.model.filename
        self.controller.model.filename = None
        self.controller.model.buffer = [
            MyString("Hello, this is help page")
        ]

    def process_input(self, key):
        if key == self.controller.adapter.key_escape: 
            self.quit()
        elif key in (self.controller.adapter.key_up,
                     self.controller.adapter.key_down,
                     self.controller.adapter.key_left,
                     self.controller.adapter.key_right):
            self.handle_navigation(key)  # Обработка навигации
        return True


    def handle_navigation(self, key):
        if key == self.controller.adapter.key_up:
            if self.controller.model.cursor_y > 0:
                self.controller.model.cursor_y -= 1
                self.controller.model.cursor_x = min(self.controller.model.cursor_x,
                                               len(self.controller.model.buffer[self.controller.model.cursor_y]))
        elif key == self.controller.adapter.key_down:
            if self.controller.model.cursor_y < len(self.controller.model.buffer) - 1:
                self.controller.model.cursor_y += 1
                self.controller.model.cursor_x = min(self.controller.model.cursor_x,
                                               len(self.controller.model.buffer[self.controller.model.cursor_y]))
        elif key == self.controller.adapter.key_left:
            if self.controller.model.cursor_x > 0:
                self.controller.model.cursor_x -= 1

        elif key == self.controller.adapter.key_right:
            if self.controller.model.cursor_x < len(self.controller.model.buffer[self.controller.model.cursor_y]):
                self.controller.model.cursor_x += 1


    def quit(self):
        self.controller.model.filename = self.old_file
        self.controller.model.buffer = self.old_text
        self.controller.change_state(self.controller.available_states.normal_state(self.controller))