from observer.observer import Observer


class View(Observer):
    def __init__(self, adapter):
        self.adapter = adapter
        self.scroll_offset = 0


    def update(self, subject):
        self.update_text(subject)
        self.update_status_bar(subject)
        self.update_cursor(subject)


    def update_text(self, subject):
        term_height, term_width = self.adapter.get_screen_size()
        term_height -= 1 

        visible_lines = subject.Text_String

        for line_index in range(term_height):
            if line_index < len(visible_lines):
                text = visible_lines[line_index].c_str()[:term_width] 
            elif not isinstance(subject.controller.state, subject.controller.available_states.help_state_obj()):
                text = "~"
            else:
                text = ""

            self.adapter.update_line(line_index, text)
        mode_with_command = subject.mode_string.c_str()
        self.adapter.update_line(term_height, mode_with_command) 


    def update_cursor(self, subject):
        term_height, _ = self.adapter.get_screen_size()
        term_height -= 1  # Учитываем строку индикатора режима

        screen_cursor_y = subject.cursor_y - subject.scroll_offset
        screen_cursor_x = subject.cursor_x - subject.horizontal_offset
        self.adapter.move_cursor(screen_cursor_y,screen_cursor_x)
        self.adapter.refresh()

    def update_status_bar(self, subject):
        height, width = self.adapter.get_screen_size()
        controller = subject.controller
        text = ''
        # set up text mode
        if subject.status_message:
            text = subject.status_message
        elif isinstance(controller.state, controller.available_states.command_state_obj()):
            text = subject.mode_string.c_str()
        elif isinstance(controller.state, controller.available_states.insert_state_obj()):
            # text += f"INSERT -- {subject.command_buffer.c_str():^} {subject.cursor_y + 1:>}/{len(subject.buffer):>}"
            # text += '-- INSERT --'
            tmp = int(width - 12 - 20)
            text += f"-- INSERT --{' ' * tmp}{subject.cursor_y + 1}/{len(subject.buffer)}"
            # for _ in range(width - len(text) - 9):
            #     text += ' '
            # text += f'{subject.cursor_y + 1}/{len(subject.buffer)}'
        elif isinstance(controller.state, controller.available_states.normal_state_obj()):
            tmp = int((width - 12 - len(subject.command_buffer.c_str())) / 2 )
            text += f"-- NORMAL --{' ' * tmp}{subject.command_buffer.c_str()}\
            {subject.cursor_y + 1}/{len(subject.buffer)}"
            # text += 'NORMAL --'
            # for _ in range(width - len(text) - 9):
            #     text += ' '
            # text += f'{subject.cursor_y + 1}/{len(subject.buffer)}'
        elif isinstance(controller.state, controller.available_states.find_state_obj()):
            # text += 'FIND --'
            text = subject.mode_string.c_str()
        # mode_with_command = subject.mode_string.c_str()
        self.adapter.update_line(height - 1, text) 
        return
