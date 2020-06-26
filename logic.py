import ui
import data

class Logic_module:
    '''logic components'''
    # see use case and latter decide if logic should be a singleton, even if it goes against the python way

    def __init__(self, ui_module: ui.Ui_module, data_module: data.Data_module):
        self._ui_module = ui_module
        self._data_module = data_module

    def start_execution(self):
        '''Starts the game execution
        '''
        self._ui_module.present_text('Think of an animal, then judge the facts about it with yes or no:')

        name, answers_dict, number_of_valids = self._discover_animal_with_simplified_order()

        if(name):
            answer = self._ui_module.get_delimited_input_with_text('Is the animal a ' + name + '? (y/n)', ('y','n','q'))
            if answer == 'q':
                return
            elif answer == 'y':
                self._animal_found(name, answers_dict)
            elif answer == 'n':
                self._animal_not_found(answers_dict)

        elif(number_of_valids):
            self._ambiguous_animal_found(answers_dict, number_of_valids)
        elif(answers_dict):
            self._animal_not_found(answers_dict)

    def _ambiguous_animal_found(self, answers_dict: dict, number_of_valids: int):
        '''Resolves case when more than one animal have the same values, are the only ones remaining and there is no more questions to differenciate then.

        Args:
            answers_dict (dict): a dict with the mapping of values to questions id who set the dataframe to this position
            number_of_valids (int): the number of animals with identical values left

        '''
        name_aux = self._ui_module.get_free_input_with_text\
                        ('There are ' + str(number_of_valids) + ' animals in my database that matches yours description, what is the name of the one you are thinking?').lower()
        if(name_aux == 'q'):
            return
        text_aux = self._ui_module.get_free_input_with_text('Complete this blank space with an fact about your animal: Your animal ________ . ')
        if(text_aux == 'q'):
            return
        id_aux = self._data_module.add_question_with_text(text_aux)
        answers_dict[id_aux] = 1
        if(self._data_module.is_animal_present(name_aux)):
            self._animal_found(name_aux, answers_dict)
        else:
            answers_dict['name'] = name_aux
            self._data_module.add_animal_with_dict(answers_dict)
            self._data_module.save_animals_to_disk()
        self._data_module.save_questions_to_disk()

    def _animal_found(self, name: str, answers_dict: dict):
        '''Resolves the case when the animal was found, or by process of elimination or by input of the user

        Args:
            name (str): the name of the animal
            answers_dict (dict): a dict with the mapping of values to questions id who set the dataframe to this position

        '''
        answers_dict['name'] = name;
        self._data_module.update_animal_with_dict(answers_dict)
        self._data_module.save_animals_to_disk()

    def _animal_not_found(self, answers_dict:dict):
        '''Resolves the case when the animal could not be found by process of elimination

        Args:
            answers_dict (dict): a dict with the mapping of values to questions id who set the dataframe to this position

        '''
        name_aux = self._ui_module.get_free_input_with_text\
                        ('Sorry the animal you are thinking is not on my database or I dont have enough information on it to give a definitive answer, what is the animal?').lower()
        if(name_aux == 'q'):
            return
        if(self._data_module.is_animal_present(name_aux)):
            self._animal_found(name_aux, answers_dict)
        else:
            answers_dict['name'] = name_aux
            self._data_module.add_animal_with_dict(answers_dict)
            self._data_module.save_animals_to_disk()


    def get_sup_modules_types(self):
        '''Resturn the suport modules types associated with the logic module

        Returns:
            tuple of str : contains id of the ui and data module
        '''
        return (self._ui_module.mdl_type, self._data_module.mdl_type)

    def _discover_animal_with_simplified_order(self) -> (str,dict,int):
        '''Tries to discover the user's animal by process of elimination using a simplified ordering by weight
        The ordering only uses the weights of the questions calculated using the full dataframe, so only the first question for sure at it's best position

        Returns:
            str: the name of the animal chosen by the user, only returned if only one value with complete information is found at the end of the elimination process
            dict: a dict with the mapping of values to questions id who set the dataframe to this position
            int: the number of animals that the dataframe has complete information that can be the one chosen by the user
        '''
        answers_dict = {}
        for question_index in range(self._data_module.get_number_of_questions()):

            answer = self._ui_module.get_delimited_input_with_text('Your animal ' + self._data_module.get_question_text_by_index(question_index) + '. (y/n)', ('y','n','q'))
            if answer == 'q':
                self._data_module.reset_animals_to_disk_version()
                return None, None, None;
            else:
                self._data_module.remove_animals_by_question_index_value(question_index, 0 if answer == 'y' else 1)
                answers_dict[self._data_module.get_question_id_by_index(question_index)] = 1 if answer == 'y' else 0

            number_of_valids, name = self._data_module.check_only_one_valid_animal_by_question_index(question_index)

            if(number_of_valids == 1):
                self._data_module.reset_animals_to_disk_version()
                return name, answers_dict, number_of_valids;

        self._data_module.reset_animals_to_disk_version()
        return None, answers_dict, number_of_valids;
