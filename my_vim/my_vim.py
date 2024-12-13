from controller.controller import Controller
from view.view import View
from adapter.controller_adapter import ControllerAdapter
from adapter.view_adapter import ViewAdapter
from model.model import Model

class MyVIM():
    
    def run(self):
        adapter_controller = ControllerAdapter()
        adapter_controller.initialize()
        controller = Controller(adapter_controller)

        adapter_view = ViewAdapter()
        adapter_view.initialize()
        view = View(adapter_view)

        editor = Model(controller, view)
        controller.set_model(editor)
        try:
            while True:
                editor.notify_observers()
                if not controller.process_input():
                    break
        except Exception as ex:
            with open("log.txt", "w") as f:
                print(ex, file=f)
            # input()
        finally:
            adapter_view.cleanup()


# if __name__ == "__main__":
#     adapter_controller = ControllerAdapter()
#     adapter_controller.initialize()
#     controller = Controller(adapter_controller)

#     adapter_view = ViewAdapter()
#     adapter_view.initialize()
#     view = View(adapter_view)

#     editor = Model(controller, view)
#     controller.set_model(editor)
#     controller.set_Text_View()
#     try:
#        while True:
#             editor.notify_observers()
#             if not controller.process_input():
#                 break
#     except Exception as ex:
#         with open("log.txt", "w") as f:
#             print(ex, file=f)
#         # input()
#     finally:
#         adapter_view.cleanup()
