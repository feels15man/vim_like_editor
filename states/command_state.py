from MyString import MyString
import os
from states.state import State


DIR = ""
class CommandState(State):
    def __init__(self, controller):
        self.controller = controller
        self.command_buffer = MyString("")  
        self.original_x = None
        self.original_y = None
        self.scroll_offset = None

    def process_input(self, key):
        if self.original_x == None:
            self.original_x = self.controller.model.cursor_x
            self.original_y = self.controller.model.cursor_y
            self.original_scroll_offset = self.controller.model.scroll_offset
            self.controller.model.cursor_y, _ = self.controller.adapter.get_screen_size()
            self.controller.model.cursor_y-=1
            self.controller.model.cursor_x = 1
            self.controller.model.scroll_offset = 0
        if key == self.controller.adapter.key_escape:  # Esc возвращает в NormalState
            self.controller.model.cursor_x = self.original_x
            self.controller.model.cursor_y = self.original_y
            self.controller.model.scroll_offset = self.original_scroll_offset
            self.original_x = None
            self.original_y = None
            self.original_scroll_offset = None
            self.controller.change_state(self.controller.available_states.normal_state(self.controller))
            self.controller.model.mode_string = MyString("-- NORMAL MODE --")
            self.command_buffer.clear()

        elif key == 10:  # Enter завершает ввод команды
            self.controller.change_state(self.controller.available_states.normal_state(self.controller))
            self.controller.model.mode_string = MyString("-- NORMAL MODE --")
            self.controller.model.cursor_x = self.original_x
            self.controller.model.cursor_y = self.original_y
            self.controller.model.scroll_offset = self.original_scroll_offset
            self.original_x = None
            self.original_y = None
            self.original_scroll_offset = None
            Status = self.execute_command(self.command_buffer.c_str())
            self.command_buffer.clear()
            if Status == 0:
                return False

        elif key in (self.controller.adapter.key_backspace, 127, 8):
            if self.command_buffer.length() > 0:
                self.command_buffer.erase(self.command_buffer.length() - 1, 1)
            self.controller.model.mode_string = MyString(f":{self.command_buffer.c_str()}") 
            if self.controller.model.cursor_x > 1:
                self.controller.model.cursor_x -= 1

        elif key >= 32 and key <= 255:
            self.command_buffer.append(1, chr(key))
            self.controller.model.mode_string = MyString(f":{self.command_buffer.c_str()}") 
            self.controller.model.cursor_x += 1

        if self.controller.model.status_message != None:
            self.controller.model.mode_string = MyString(
                f"{self.controller.model.status_message.c_str()}")
            self.controller.model.status_message = None
        return True


    def execute_command(self, command):
        try:
            parts = command.split()
            cmd = parts[0] if parts else ""

            if cmd == "o" and len(parts) > 1:  # Открыть файл
                filename = parts[1]
                self.open_file(filename)
                self.controller.model.cursor_x = 0
                self.controller.model.cursor_y = 0
                self.controller.model.scroll_offset = 0
            elif cmd == "x":  # Записать и выйти
                self.save_file(self.controller.model.filename)
                return False
            elif cmd == "w":  # Записать файл
                if len(parts) > 1:  # Сохранить как другой файл
                    filename = parts[1]
                    self.save_file(filename)
                else:  # Сохранить текущий файл
                    self.save_file(self.controller.model.filename)
                return True
            elif cmd == "q":  # Выйти
                if self.controller.model.changed_lines and not command.endswith("!"):
                    self.controller.model.status_message = MyString("Unsaved changes! Use :q! to force quit.")
                    return True
                else:
                    return False
            elif cmd == "q!":  # Выйти без сохранения
                return False
            elif cmd == "wq!":  # Сохранить и выйти
                self.save_file(self.controller.model.filename)
                return False
            elif cmd.isdigit():  # Переход на строку
                self.goto_line(int(cmd))
                return True
            elif cmd == "help":
                self.controller.change_state(self.controller.available_states.help_state(self.controller))
                
            else:
                self.controller.model.status_message = MyString(f"Unknown command: {command}")
                return True
        except Exception as e:
            self.controller.model.status_message = MyString(f"Error: {str(e)}")


    def open_file(self, filename):
        if os.path.exists(DIR + filename):
            with open(DIR + filename, 'r', encoding='utf-8') as file:
                self.controller.model.buffer = [MyString(line.rstrip('\n')) for line in file.readlines()]
            self.controller.model.filename = filename
            self.controller.model.cursor_x = 0
            self.controller.model.cursor_y = 0
            self.controller.model.changed_lines.clear()
            # self.controller.model.status_message = MyString(f"Opened file: {filename}")
        else:
            self.controller.model.status_message = MyString(f"File not found: {filename}")


    def save_file(self, filename):
        with open(DIR + filename, 'w', encoding='utf-8') as file:
            for line in self.controller.model.buffer:
                file.write(line.c_str() + '\n')
        self.controller.model.filename = filename
        self.controller.model.changed_lines.clear()
        self.controller.model.status_message = MyString(f"Saved file: {filename}")

    def goto_line(self, line_number):
        line_number = max(1, min(line_number, len(self.controller.model.buffer)))  # Ограничиваем диапазон
        self.controller.model.cursor_y = line_number - 1
        self.controller.model.cursor_x = 0
        self.controller.model.status_message = MyString(f"Moved to line: {line_number}")
