import ui
import data

class Logic_module:
    '''logic components'''
    # see use case and latter decide if logic should be a singleton, even if it goes against the python way

    def __init__(self, ui_module: ui.Ui_module, data_module: data.Data_module):
        self._ui_module = ui_module
        self._data_module = data_module

    def start_execution(self):
        self._ui_module.present_text('Think of an animal, then press Enter to continue:')
        self._ui_module.get_input()

    def get_sup_modules_types(self):
        return(self._ui_module.mdl_type, self._data_module.mdl_type)
