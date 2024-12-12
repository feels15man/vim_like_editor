import pytest
from model.model import Model  
from controller.controller import Controller
from states.normal_state import NormalState
from view.view import View
from adapter.controller_adapter import ControllerAdapter
# from adapter.view_adapter import ViewAdapter

import curses


class MockViewAdapter:
    def initialize(self):
        pass



class MockControllerAdapter(ControllerAdapter):
    def __init__(self):
        super().__init__()
        self.curses = curses

    def initialize(self):
        pass

    def get_screen_size(self):
        return 10, 10


@pytest.fixture
def setup_environment():
    adapter_controller = MockControllerAdapter()
    adapter_controller.initialize()
    controller = Controller(adapter_controller)

    adapter_view = MockViewAdapter()
    view = View(adapter_view)

    editor = Model(controller, view)
    controller.set_model(editor)
    return editor, controller, view

def test_add_characters(setup_environment):
    editor, controller, _ = setup_environment

    controller.change_state(controller.available_states.insert_state(controller))
    controller.process_input(ord("a")) 
    controller.process_input(ord("b"))
    controller.process_input(ord("c"))
    assert editor.buffer[0].c_str() == "abc" 


def test_state_transitions(setup_environment):
    _, controller, _ = setup_environment

    controller.change_state(controller.available_states.command_state(controller))
    assert controller.state.__class__.__name__ == "CommandState"

    controller.change_state(controller.available_states.insert_state(controller))
    assert controller.state.__class__.__name__ == "InsertState"