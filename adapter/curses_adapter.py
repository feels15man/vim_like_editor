from abc import ABC 


class CursesAdapter(ABC):
    def draw_text(self, y: int, x: int, text: str):
        raise NotImplementedError("This method must be implemented in a subclass.")

    def refresh(self):
        raise NotImplementedError("This method must be implemented in a subclass.")

    def move_cursor(self, y: int, x: int):
        raise NotImplementedError("This method must be implemented in a subclass.")

    def clear_screen(self):
        raise NotImplementedError("This method must be implemented in a subclass.")

    def get_key(self) -> int:
        raise NotImplementedError("This method must be implemented in a subclass.")

    def cleanup(self):
        raise NotImplementedError("This method must be implemented in a subclass.")

    @property
    def key_down(self):
        raise NotImplementedError("This method must be implemented in a subclass.")

    @property
    def key_up(self):
        raise NotImplementedError("This method must be implemented in a subclass.")

    @property
    def key_left(self):
        raise NotImplementedError("This method must be implemented in a subclass.")

    @property
    def key_right(self):
        raise NotImplementedError("This method must be implemented in a subclass.")

    @property
    def key_backspace(self):
        raise NotImplementedError("This method must be implemented in a subclass.")

    @property
    def key_escape(self):
        raise NotImplementedError("This method must be implemented in a subclass.")

    def update_line(self, y: int, text: str):
        raise NotImplementedError("This method must be implemented in a subclass.")

    def get_screen_size(self):
        raise NotImplementedError("This method must be implemented in a subclass.")


