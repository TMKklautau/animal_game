import pandas as pd

class Data_module:
    '''Base data manipulation module'''
    mdl_type:str = 'base'

    def __init__(self):
        pass

    def get_number_of_questions(self) -> int:
        return None

    def get_question_text_by_order(self, order_index: int) -> str:
        return None

    def remove_animals_by_question_order_value(self, question_order: int, value: int):
        pass

    def check_only_one_valid_animal_by_question_order(self, question_order: int) -> (bool, str):
        return None, None

class Csv_Data_module(Data_module):
    '''Csv using pandas data module'''
    mdl_type:str = 'Csv'

    def __init__(self):
        super().__init__()
        self._animals_df = pd.read_csv('./dataframes/csv/animals.csv', index_col=0)
        self._questions_df = pd.read_csv('./dataframes/csv/questions.csv', index_col=0)

    def get_number_of_questions(self) -> int:
        return len(self._questions_df)

    def get_question_text_by_order(self, order_index: int) -> str:
        return self._questions_df.loc[order_index, 'text']

    def remove_animals_by_question_order_value(self, question_order:int, value: int):
        self._animals_df = self._animals_df[~(self._animals_df[self._questions_df.loc[question_order].id] == value)]

    def check_only_one_valid_animal_by_question_order(self, question_order: int) -> (bool, str):
        if int(self._animals_df[self._questions_df.loc[question_order].id].sum()) == 1:
            return True , self._animals_df.loc[self._animals_df[self._questions_df.loc[question_order].id] == 1, 'name'].item();
        else:
            return False, None;
