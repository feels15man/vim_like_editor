from abc import ABC, abstractmethod


class State(ABC):
    def __init__(self, controller):
        self.controller = controller


    @abstractmethod
    def process_input(self, key):
        pass