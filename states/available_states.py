from states.find_state import FindState
from states.insert_state import InsertState
from states.command_state import CommandState
from states.normal_state import NormalState
from states.help_state import HelpState


class AvailableStates():
    # normal_state = NormalState
    # find_state = FindState
    # insert_state = InsertState
    # command_state = CommandState

    def normal_state(self, controller):
        return NormalState(controller)
    
    def find_state(self, controller):
        return FindState(controller)

    def insert_state(self, controller):
        return InsertState(controller)

    def command_state(self, controller):
        return CommandState(controller)

    def help_state(self, controller):
        return HelpState(controller)

    def init_state(self):
        return self.normal_state()

    def find_state_obj(self):
        return FindState
     
    def command_state_obj(self):
        return CommandState

    def insert_state_obj(self):
        return InsertState
    
    def normal_state_obj(self):
        return NormalState

    def help_state_obj(self):
        return HelpState
