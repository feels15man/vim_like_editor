from MyString import MyString as MyString
from states.state import State
# from available_states import AvailableStates


class NormalState(State):
    def __init__(self, controller):
        super().__init__(controller)
    def process_input(self, key):
        if key == self.controller.adapter.key_escape:  # Завершение работы
            return False
        if self.controller.model.command_buffer.c_str() == "r":
            self.replace_character(key)
            self.clear_buffer()
            return True
        if key == ord('i') and self.controller.model.command_buffer.c_str() != "d":  # Переход в режим вставки
            self.controller.change_state(self.controller.available_states.insert_state(self.controller))
            return True
        if key == ord('a') and self.controller.model.command_buffer.c_str() != "d":  # Переход в режим вставки
            self.controller.model.cursor_x += 1
            self.controller.change_state(self.controller.available_states.insert_state(self.controller))
            return True
        elif key == ord('/'):  # Переход в режим поиска вперед
            self.controller.model.mode_string = MyString("/")
            self.controller.model.search_results = []
            self.controller.model.find_buffer.clear()
            self.controller.search_type = '/'
            # self.controller.change_state(self.controller.find_state)
            self.controller.change_state(self.controller.available_states.find_state(self.controller))
            return True
        elif key == ord('?'):  # Переход в режим поиска назад
            self.controller.model.mode_string = MyString(f"?")
            self.controller.model.search_results = []
            self.controller.model.find_buffer.clear()
            self.controller.search_type = '?'
            # self.controller.change_state(self.controller.find_state)
            self.controller.change_state(self.controller.available_states.find_state(self.controller))
            return True
        # Ввод текста в начале строки (I)
        elif key == ord('I'):
            # self.controller.model.mode_string =  MyString("-- INSERT MODE --")
            self.controller.model.cursor_x = 0  # Перемещаем курсор в начало строки
            # self.controller.change_state(self.controller.insert_state)
            self.controller.change_state(self.controller.available_states.insert_state(self.controller))
            return True

        # Ввод текста в конце строки (A)
        elif key == ord('A'):
            # self.controller.model.mode_string =  MyString("-- INSERT MODE --")
            self.controller.model.cursor_x = len(self.controller.model.buffer[self.controller.model.cursor_y])  # Конец строки
            # self.controller.change_state(self.controller.insert_state)
            self.controller.change_state(self.controller.available_states.insert_state(self.controller))
            return True

        # Удалить содержимое строки и начать ввод (S)
        elif key == ord('S'):
            # self.controller.model.mode_string =  MyString("-- INSERT MODE --")
            self.controller.model.buffer[self.controller.model.cursor_y] = MyString("")  # Удаляем содержимое строки
            self.controller.model.cursor_x = 0  # Перемещаем курсор в начало строки
            # self.controller.change_state(self.controller.insert_state)
            self.controller.change_state(self.controller.available_states.insert_state(self.controller))
            return True
        elif key == ord(':'):  # Ввод команды
            # self.controller.change_state(self.controller.command_state)
            self.controller.change_state(self.controller.available_states.command_state(self.controller))
            self.controller.model.mode_string = MyString(":")
            return True
  
        elif key in (self.controller.adapter.key_up,
                   self.controller.adapter.key_down,
                   self.controller.adapter.key_left,
                   self.controller.adapter.key_right):
            self.handle_navigation(key)  # Обработка навигации


        # Добавление символа в `command_buffer`
        # key = str(chr(key))
        string = self.controller.model.command_buffer.c_str()
        if key >= 32 and key <= 255:
            self.controller.model.command_buffer.append(1, chr(key))
        string = self.controller.model.command_buffer.c_str()
        # Проверка команд
        # Проверка команд
        if self.controller.model.command_buffer.c_str() == "yy":  # Копирование текущей строки
            self.copy_current_line()
            self.clear_buffer()
        elif self.controller.model.command_buffer.c_str() == "yw":  # Копирование текущего слова
            self.copy_current_word()
            self.clear_buffer()
        elif self.controller.model.command_buffer.c_str() == "p":  # Вставка содержимого буфера
            self.paste_after_cursor()
            self.clear_buffer()
        elif self.controller.model.command_buffer.c_str() == "0" or self.controller.model.command_buffer.c_str() == "^":  # Перемещение в начало строки
            self.move_to_start_of_line()
            self.clear_buffer()
        elif self.controller.model.command_buffer.c_str() == "$":  # Перемещение в конец строки
            self.move_to_end_of_line()
            self.clear_buffer()
        elif self.controller.model.command_buffer.c_str() == "x":  # Удаление символа после курсора
            self.delete_char()
            self.clear_buffer()
        elif self.controller.model.command_buffer.c_str()== "G":  # Переход в конец файла
            self.move_to_end_of_file()
            self.clear_buffer()
        elif self.controller.model.command_buffer.c_str() == "r":
            pass
        elif self.controller.model.command_buffer.c_str() == "gg":  # Переход в начало файла
            self.handle_gg()
            self.clear_buffer()
        elif self.controller.model.command_buffer.c_str() == "dd":  # Удаление строки
            self.handle_dd()
            self.clear_buffer()
        elif self.controller.model.command_buffer.c_str() == "diw":  # Удаление текущего слова
            self.delete_current_word()
            self.clear_buffer()
        elif key == ord('G') and self.controller.model.command_buffer.substr(0, self.controller.model.command_buffer.length() - 1).c_str().isdigit():  # Перемещение на строку N
            self.move_to_line_by_number()
            self.clear_buffer()
        elif self.controller.model.command_buffer.c_str() == "w":  # Перемещение к следующему слову
            self.move_to_next_word()
            self.clear_buffer()
        elif self.controller.model.command_buffer.c_str() == "b":  # Перемещение к предыдущему слову
            self.move_to_previous_word()
            self.clear_buffer()
        elif self.controller.model.command_buffer.c_str() == 'n':  # Повторить предыдущий поиск
            if not self.move_to_next_result():
                self.controller.model.status_message = "Pattern not found"
            self.clear_buffer()
        elif self.controller.model.command_buffer.c_str() == 'N':  # Повторить поиск в обратном направлении
            if not self.move_to_previous_result():
                self.controller.model.status_message = "Pattern not found"
            self.clear_buffer()
        else:
            # Проверка, начинается ли `command_buffer` с допустимой команды
            valid_lengths = {
                "d": 1,
                "g": 2,
                "di": 2,
                "y": 1,
                # Числовые команды: длина буфера для N G должна быть от 1 до 10
                **{str(i): 10 for i in range(10)}
            }

            # Проверяем длину и содержание буфера
            valid = False
            for prefix, max_length in valid_lengths.items():
                if self.controller.model.command_buffer.c_str().startswith(prefix) and\
                        len(self.controller.model.command_buffer) <= max_length:
                    valid = True
                    break
            if self.controller.model.command_buffer.c_str()[:-1].isdigit():
                # Если она заканчивается на G — это допустимая команда
                if self.controller.model.command_buffer.c_str().endswith("G"):
                    valid = True
                elif not self.controller.model.command_buffer.c_str()[-1].isdigit():
                    valid = False
            if not valid:
                self.clear_buffer()  # Если команда не соответствует, очищаем буфер
        if self.controller.model.status_message != None:
            self.controller.model.mode_string = MyString(
                f"{self.controller.model.status_message.c_str()}")
            self.controller.model.status_message = None
        else:
            # self.controller.model.mode_string = MyString(f"-- NORMAL MODE --\t\t {self.controller.model.command_buffer.c_str()}")
            pass
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


    def clear_buffer(self):
        self.controller.model.command_buffer.clear()

    # Команды навигации
    def move_to_start_of_line(self):
        self.controller.model.cursor_x = 0

    def move_to_end_of_line(self):
        self.controller.model.cursor_x = len(self.controller.model.buffer[self.controller.model.cursor_y])

    def move_to_end_of_file(self):
        self.controller.model.cursor_y = len(self.controller.model.buffer) - 1
        self.controller.model.cursor_x = 0

    def move_to_line_by_number(self):
        # Преобразование содержимого `command_buffer` в строку
        command = self.controller.model.command_buffer.c_str()

        # Проверка на наличие числового значения в `command_buffer`
        if command[:-1].isdigit():
            line_number = int(command[:-1])  # Извлекаем число
            self.controller.model.cursor_y = min(len(self.controller.model.buffer) - 1, line_number - 1)
            self.controller.model.cursor_x = 0
        else:
            # Если в буфере нет допустимого числа, очищаем буфер
            self.clear_buffer()

    # Команды для работы со словами
    def move_to_next_word(self):
        while self.controller.model.cursor_y < len(self.controller.model.buffer):
            line = self.controller.model.buffer[self.controller.model.cursor_y]
            cursor_x = self.controller.model.cursor_x

            # Пропускаем пробелы в текущей строке
            while cursor_x < len(line) and line.c_str()[cursor_x].isspace():
                cursor_x += 1

            if cursor_x < len(line):
                # Пропускаем символы текущего слова
                while cursor_x < len(line) and not line.c_str()[cursor_x].isspace():
                    cursor_x += 1
                self.controller.model.cursor_x = cursor_x
                return


            # Если достигнут конец строки, переходим на следующую строку
            if self.controller.model.cursor_y == len(self.controller.model.buffer) - 1:
                return
            self.controller.model.cursor_y += 1
            self.controller.model.cursor_x = 0

            # Если строка пустая, считаем её словом
            if self.controller.model.cursor_y < len(self.controller.model.buffer) and not self.controller.model.buffer[
                self.controller.model.cursor_y]:
                return

    def move_to_previous_word(self):
        while self.controller.model.cursor_y >= 0:
            line = self.controller.model.buffer[self.controller.model.cursor_y]
            cursor_x = self.controller.model.cursor_x

            # Если курсор в начале строки, переходим на предыдущую строку
            if cursor_x == 0:
                self.controller.model.cursor_y -= 1
                if self.controller.model.cursor_y >= 0:
                    line = self.controller.model.buffer[self.controller.model.cursor_y]
                    cursor_x = len(line)

                    # Если строка пустая, считаем её словом
                    if not line:
                        self.controller.model.cursor_x = 0
                        return
                    else:
                        self.controller.model.cursor_x=cursor_x
                continue

            # Пропускаем пробелы в текущей строке (идём назад)
            while cursor_x > 0 and line.c_str()[cursor_x - 1].isspace():
                cursor_x -= 1

            # Пропускаем символы текущего слова (идём назад)
            while cursor_x > 0 and not line.c_str()[cursor_x - 1].isspace():
                cursor_x -= 1

            self.controller.model.cursor_x = cursor_x
            return
        self.controller.model.cursor_y = 0
        return


    # Команды редактирования
    def delete_char(self):
        line = self.controller.model.buffer[self.controller.model.cursor_y]
        if self.controller.model.cursor_x < line.length():  # Проверяем, находится ли курсор перед концом строки
            line.erase(self.controller.model.cursor_x, 1)  # Удаляем символ на позиции cursor_x
            self.controller.model.changed_lines.add(self.controller.model.cursor_y)  # Отмечаем строку как изменённую


    def delete_current_word(self):
        line = self.controller.model.buffer[self.controller.model.cursor_y]
        start = self.controller.model.cursor_x
        end = self.controller.model.cursor_x

        # Найти начало текущего слова
        while start > 0 and not line.substr(start - 1, 1).c_str().isspace():
            start -= 1

        # Найти конец текущего слова
        while end < line.length() and not line.substr(end, 1).c_str().isspace():
            end += 1

        # Удалить слово
        line.erase(start, end - start)

        # Обновить положение курсора
        self.controller.model.cursor_x = start

        # Пометить строку как изменённую
        self.controller.model.changed_lines.add(self.controller.model.cursor_y)

    # Обработка сложных многобуквенных команд
    def handle_gg(self):
        self.controller.model.cursor_y = 0
        self.controller.model.cursor_x = 0

    def handle_dd(self):
        # Удаляем текущую строку
        self.controller.model.buffer.pop(self.controller.model.cursor_y)

        # Если буфер пустой, добавляем пустую строку
        if not self.controller.model.buffer:
            self.controller.model.buffer=[MyString("")]

        # Помечаем текущую строку и все строки ниже как изменённые
        self.update_lines_from(self.controller.model.cursor_y)

        # Обновляем положение курсора
        self.controller.model.cursor_y = min(self.controller.model.cursor_y, len(self.controller.model.buffer) - 1)
        self.controller.model.cursor_x = min(self.controller.model.cursor_x, len(self.controller.model.buffer[self.controller.model.cursor_y]))

    def update_lines_from(self, start_line):
        for i in range(start_line, len(self.controller.model.buffer)):
            self.controller.model.changed_lines.add(i)

    def copy_current_line(self):
        self.controller.model.clipboard = self.controller.model.buffer[self.controller.model.cursor_y]
        # print(f"Copied line: {self.controller.model.clipboard.c_str()}")  # Для отладки
        self.controller.model.status_message = MyString(f"Copied line: {self.controller.model.clipboard.c_str()}")

    def copy_current_word(self):
        line = self.controller.model.buffer[self.controller.model.cursor_y]
        start = self.controller.model.cursor_x
        end = self.controller.model.cursor_x

        # # Найти начало текущего слова
        # while start > 0 and not line.substr(start - 1, 1).c_str().isspace():
        #     start -= 1

        # Найти конец текущего слова
        while end < line.length() and not line.substr(end, 1).c_str().isspace():
            end += 1

        self.controller.model.clipboard = line.substr(start, end - start)
        print(f"Copied word: {self.controller.model.clipboard.c_str()}")  # Для отладки

    def paste_after_cursor(self):
        if not self.controller.model.clipboard:
            return  # Если буфер пустой, ничего не делать

        line = self.controller.model.buffer[self.controller.model.cursor_y]

        # Убедимся, что индекс не выходит за пределы строки
        insert_position = min(self.controller.model.cursor_x + 1, line.length())

        # Вставляем содержимое буфера в строку
        line.insert(insert_position, self.controller.model.clipboard.c_str())

        # Обновляем курсор, перемещая его в конец вставленного текста
        self.controller.model.cursor_x = insert_position + self.controller.model.clipboard.length()

        # Помечаем строку как изменённую
        self.controller.model.changed_lines.add(self.controller.model.cursor_y)

    def replace_character(self, key):
        if self.controller.model.cursor_x < len(self.controller.model.buffer[self.controller.model.cursor_y]):
            line = self.controller.model.buffer[self.controller.model.cursor_y]
            # Заменяем символ под курсором
            line.erase(self.controller.model.cursor_x, 1)
            line.insert(self.controller.model.cursor_x, chr(key))
            self.controller.model.changed_lines.add(self.controller.model.cursor_y)


    def move_to_next_result(self):
        if not self.controller.model.search_results:
            return False

        self.controller.model.search_index = (self.controller.model.search_index + 1) % len(self.controller.model.search_results)
        y, x = self.controller.model.search_results[self.controller.model.search_index]
        self.controller.model.cursor_y = y
        self.controller.model.cursor_x = x
        return True

    def move_to_previous_result(self):
        if not self.controller.model.search_results:
            return False

        self.controller.model.search_index = (self.controller.model.search_index - 1) % len(self.controller.model.search_results)
        y, x = self.controller.model.search_results[self.controller.model.search_index]
        self.controller.model.cursor_y = y
        self.controller.model.cursor_x = x
        return True

