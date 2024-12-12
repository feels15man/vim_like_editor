from MyString import MyString
from states.state import State

class FindState(State):
    def __init__(self, controller):
        super().__init__(controller)
        self.original_x = None
        self.original_y = None
        self.scroll_offset = None

    def process_input(self, key):
        if self.original_x == None:
            self.original_x = self.controller.model.cursor_x
            self.original_y = self.controller.model.cursor_y
            self.original_scroll_offset = self.controller.model.scroll_offset
            self.controller.model.cursor_y, _ = self.controller.adapter.get_screen_size()
            self.controller.model.cursor_y -= 1
            self.controller.model.cursor_x = 1
            self.controller.model.scroll_offset = 0

        if key == self.controller.adapter.key_escape:  # Возврат в NormalState
            self.controller.model.cursor_x = self.original_x
            self.controller.model.cursor_y = self.original_y
            self.controller.model.scroll_offset = self.original_scroll_offset
            self.original_x = None
            self.original_y = None
            self.original_scroll_offset = None
            self.controller.model.mode_string = MyString(f"-- NORMAL MODE --\t\t {self.controller.model.command_buffer.c_str()}")
            # self.controller.change_state(self.controller.normal_state)
            self.controller.change_state(self.controller.available_states.normal_state(self.controller))
        elif key == 10:  # Enter
            query = self.controller.model.find_buffer
            # Выполняем поиск всех вхождений строки
            self.controller.model.search_results=self.find_all(query, 1 if self.controller.search_type == '/' else -1)

            self.controller.model.cursor_x = self.original_x
            self.controller.model.cursor_y = self.original_y
            self.controller.model.scroll_offset = self.original_scroll_offset
            self.original_x = None
            self.original_y = None
            self.original_scroll_offset = None

            # Если поиск назад, меняем индекс текущего результата
            if self.controller.search_type == '?':
                # self.controller.model.search_results.reverse()

                self.controller.model.search_index = len(self.controller.model.search_results)-1
            else:
                self.controller.model.search_index = 0
            # Перемещаемся к первому результату, если он есть
            if self.controller.model.search_results == [ ]:
                self.controller.model.status_message = MyString("Pattern not found")
            else:
                self.controller.model.status_message = MyString(f"Found: {query}")
                y, x = self.controller.model.search_results[self.controller.model.search_index]
                self.controller.model.cursor_y = y
                self.controller.model.cursor_x = x

            # Возврат в NormalState
            # self.controller.change_state(self.controller.normal_state)
            self.controller.change_state(self.controller.available_states.normal_state(self.controller))
        elif key in (self.controller.adapter.key_backspace, 127, 8):
            if self.controller.model.find_buffer.length() > 0:
                self.controller.model.find_buffer.erase(self.controller.model.find_buffer.length() - 1, 1)
                self.controller.model.mode_string = MyString(f"{self.controller.search_type}{self.controller.model.find_buffer.c_str()}")
                if self.controller.model.cursor_x > 1:
                    self.controller.model.cursor_x -= 1
            return True
        else:
            if key >= 0 and key <= 255:
                self.controller.model.find_buffer.append(1, chr(key))
                self.controller.model.mode_string = MyString(f"{self.controller.search_type}{self.controller.model.find_buffer.c_str()}")
                self.controller.model.cursor_x += 1
        if self.controller.model.status_message != None:
            self.controller.model.mode_string = MyString(
                f"{self.controller.model.status_message.c_str()}")
            self.controller.model.status_message = None

        return True

    def find_all(self, query, direction=1):
        results = []  # Список координат совпадений
        query_str = query.c_str()

        # Если строка поиска пуста, возвращаем пустой список
        if not query_str:
            return results

        if direction == 1:  # Поиск вперёд ('/')
            for y, line in enumerate(self.controller.model.buffer[self.original_y:],
                                     start=self.original_y):
                # Для текущей строки начинаем с позиции курсора, иначе с начала строки
                line = line.c_str()
                start_pos = self.original_y if y == self.original_y else 0
                if start_pos >= len(line):  # Если курсор за пределами строки
                    continue  # Пропускаем строку

                x = start_pos
                while x < len(line):
                    pos = line.find(query_str, x)
                    if pos == -1:
                        break
                    results.append((y, pos))
                    x = pos + 1  # Двигаем курсор вперёд
        else:  # Поиск назад ('?')
            for y, line in reversed(
                    list(enumerate(self.controller.model.buffer[: self.original_y + 1]))):
                line = line.c_str()
                # Для текущей строки начинаем с позиции курсора, иначе с конца строки
                end_pos = self.original_x if y == self.original_y else line.length() - 1
                if end_pos < 0:  # Если курсор перед началом строки
                    continue  # Пропускаем строку

                x = 0
                while x < end_pos:
                    pos = line.find(query_str, x)
                    if pos == -1:
                        break
                    if pos <= end_pos:
                        results.append((y, pos))
                    x = pos + 1  # Двигаем курсор вперёд

        # Возвращаем отсортированный список
        return sorted(results)

