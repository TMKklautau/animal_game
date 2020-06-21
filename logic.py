import ui
import data

class Logic_module:
    '''logic components'''
    # see use case and latter decide if logic should be a singleton, even if it goes against the python way

    def __init__(self, ui_module: ui.Ui_module, data_module: data.Data_module):
        self._ui_module = ui_module
        self._data_module = data_module

    def start_execution(self):

        #move the next 2 lines to ui module later
        self._ui_module.present_text('Think of an animal, then press Enter to continue:')
        self._ui_module.get_input()

        flag, name = self._discover_animal()

        if(flag):
            #move nexts lines to ui module later
            self._ui_module.present_text('Is the animal a ' + name + '?')

        else:
            self._ui_module.present_text('Sorry the animal you are thinking is not on my database, what was it?')

    def get_sup_modules_types(self):
        return(self._ui_module.mdl_type, self._data_module.mdl_type)

    def _discover_animal(self) -> (bool, str):

        for question_order_index in range(self._data_module.get_number_of_questions()):

            #move this to ui module, as its ui dependent
            self._ui_module.present_text('Does your animal ' + self._data_module.get_question_text_by_order(question_order_index) + '? (y/n)')
            answer = self._ui_module.get_input()
            while answer not in ('y','n','q'):
                self._ui_module.present_text('Not a valid answer, insert a valid one')
                answer = self._ui_module.get_input()
            #end of block to pass to ui module

            if answer == 'q':
                break
            else:
                self._data_module.remove_animals_by_question_order_value(question_order_index, 0 if answer == 'y' else 1)

            flag, name = self._data_module.check_only_one_valid_animal_by_question_order(question_order_index)

            if(flag):
                return True, name;

        return False, None;
