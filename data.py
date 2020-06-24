import pandas as pd
import numpy as np

class Data_module:
    '''Base data manipulation module'''
    mdl_type:str = 'base'

    def __init__(self):
        pass

    def reset_animals_to_disk_version(self):
        pass

    def is_animal_present(self, name:str) -> bool:
        return None

    def get_number_of_questions(self) -> int:
        return None

    def get_question_text_by_order(self, order_index: int) -> str:
        return None

    def get_question_id_by_order(self, order_index: int) -> str:
        return None

    def remove_animals_by_question_order_value(self, question_order: int, value: int):
        pass

    def check_only_one_valid_animal_by_question_order(self, question_order: int) -> (bool, str):
        return None, None

    def update_animal_with_dict(self, animal_data: dict):
        pass

    def add_animal_with_dict(self, animal_data: dict):
        pass

    def add_question_with_text(self, text: str) -> str:
        return None

    def save_animals_to_disk(self):
        pass

    def save_questions_to_disk(self):
        pass

class Csv_Data_module(Data_module):
    '''Csv using pandas data module'''
    mdl_type:str = 'Csv'

    def __init__(self):
        super().__init__()
        self._animals_df = pd.read_csv('./dataframes/csv/animals.csv', index_col=0)
        self._questions_df = pd.read_csv('./dataframes/csv/questions.csv', index_col=0)
        print(self._animals_df)
        print(self._questions_df)

    def reset_animals_to_disk_version(self):
        self._animals_df = pd.read_csv('./dataframes/csv/animals.csv', index_col=0)

    def is_animal_present(self, name: str) -> bool:
        return not (self._animals_df.loc[self._animals_df.name == name].empty)

    def get_number_of_questions(self) -> int:
        return len(self._questions_df)

    def get_question_text_by_order(self, order_index: int) -> str:
        return self._questions_df.loc[order_index, 'text']

    def get_question_id_by_order(self, order_index: int) -> str:
        return self._questions_df.loc[order_index, 'id']

    def remove_animals_by_question_order_value(self, question_order:int, value: int):
        self._animals_df = self._animals_df[~(self._animals_df[self._questions_df.loc[question_order].id] == value)]

    def check_only_one_valid_animal_by_question_order(self, question_order: int) -> (int, str):
        number_of_valids = len(self._animals_df[self._questions_df.loc[question_order].id].dropna())
        if number_of_valids == 1:
            return number_of_valids, self._animals_df.loc[self._animals_df[self._questions_df.loc[question_order].id].notnull(), 'name'].item();
        else:
            return number_of_valids, None;

    def update_animal_with_dict(self, animal_data: dict):
        aux_series = pd.Series(animal_data)
        self._animals_df.loc[self._animals_df.name == animal_data['name'], aux_series.index] = aux_series.values

    def add_animal_with_dict(self, animal_data: dict):
        self._animals_df = self._animals_df.append(animal_data, ignore_index=True)

    def add_question_with_text(self, text:str) -> str:
        if(not self._questions_df.loc[self._questions_df.text == text].empty):
            return self._questions_df.loc[self._questions_df.text == text, 'id'].item()
        else:
            #the id management can cause problems if a question is removed, need to think of something better
            aux_id = 'q'+str(len(self._questions_df.id))
            self._questions_df = self._questions_df.append({'id':aux_id, 'text':text, 'order':len(self._questions_df.id)}, ignore_index=True)
            self._animals_df[aux_id] = np.nan
            return aux_id

    def save_animals_to_disk(self):
        self._animals_df.to_csv('./dataframes/csv/animals.csv')

    def save_questions_to_disk(self):
        self._questions_df.to_csv('./dataframes/csv/questions.csv')
