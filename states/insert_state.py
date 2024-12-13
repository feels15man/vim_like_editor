from MyString import MyString
from states.state import State


class InsertState(State):
    def process_input(self, key):
        if key == self.controller.adapter.key_escape:  # Возврат в NormalState
            self.controller.model.mode_string = MyString(f"-- NORMAL MODE --\t\t {self.controller.model.command_buffer.c_str()}")
            self.controller.change_state(self.controller.available_states.normal_state(self.controller))
        elif key in (self.controller.adapter.key_backspace, 127, 8):  # Удаление символа
            self.handle_backspace()
        elif key == 10:  # Enter (перенос строки)
            self.insert_newline()
        elif key == 9:  # Tab key
            self.insert_tab()
        elif key in (self.controller.adapter.key_up,
                     self.controller.adapter.key_down,
                     self.controller.adapter.key_left,
                     self.controller.adapter.key_right):
            self.handle_navigation(key)  # Обработка навигации
        elif key >= 32 and key<=255:  # Символы (включая кириллицу)
            self.insert_character(chr(key))
        return True

    def handle_backspace(self):
        if self.controller.model.cursor_x > 0:
            line = self.controller.model.buffer[self.controller.model.cursor_y]
            line.erase(self.controller.model.cursor_x - 1, 1)
            self.controller.model.cursor_x -= 1
            self.controller.model.changed_lines.add(self.controller.model.cursor_y)
        elif self.controller.model.cursor_y > 0:
            current_line = self.controller.model.buffer.pop(self.controller.model.cursor_y)
            self.controller.model.cursor_y -= 1
            previous_line = self.controller.model.buffer[self.controller.model.cursor_y]
            self.controller.model.cursor_x = previous_line.length()
            previous_line.append(current_line.c_str())

    def insert_newline(self):
        current_line = self.controller.model.buffer[self.controller.model.cursor_y]

        if current_line.length() == 0:
            left_part = MyString("")
            right_part = MyString("")
        elif self.controller.model.cursor_x >= current_line.length():
            left_part = current_line.substr(0, current_line.length())
            right_part = MyString("")
        else:
            left_part = current_line.substr(0, self.controller.model.cursor_x)
            right_part = current_line.substr(self.controller.model.cursor_x)

        self.controller.model.buffer[self.controller.model.cursor_y] = left_part
        self.controller.model.buffer.insert(self.controller.model.cursor_y + 1, right_part)

        self.controller.model.cursor_y += 1
        self.controller.model.cursor_x = 0


    def insert_tab(self):
        tab_size = 4
        current_line = self.controller.model.buffer[self.controller.model.cursor_y]
        current_line.insert(self.controller.model.cursor_x, " " * tab_size)
        self.controller.model.cursor_x += tab_size

    def insert_character(self, char):
        line = self.controller.model.buffer[self.controller.model.cursor_y]
        line.insert(self.controller.model.cursor_x, char)
        self.controller.model.cursor_x += 1
    

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