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

    def get_question_text_by_index(self, index: int) -> str:
        return None

    def get_question_id_by_index(self, index: int) -> str:
        return None

    def remove_animals_by_question_index_value(self, question_index: int, value: int):
        pass

    def check_only_one_valid_animal_by_question_index(self, question_index: int) -> (bool, str):
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

    def calculate_questions_weights(self):
        pass

    def randomize_questions(self):
        pass

class Csv_Data_module(Data_module):
    '''Csv using pandas data module'''
    mdl_type:str = 'Csv'

    def __init__(self):
        super().__init__()
        self._animals_df = pd.read_csv('./dataframes/csv/animals.csv', index_col=0)
        self._questions_df = pd.read_csv('./dataframes/csv/questions.csv', index_col=0)

    def reset_animals_to_disk_version(self):
        self._animals_df = pd.read_csv('./dataframes/csv/animals.csv', index_col=0)

    def is_animal_present(self, name: str) -> bool:
        return not (self._animals_df.loc[self._animals_df.name == name].empty)

    def get_number_of_questions(self) -> int:
        return len(self._questions_df)

    def get_question_text_by_index(self, index: int) -> str:
        return self._questions_df.loc[index, 'text']

    def get_question_id_by_index(self, index: int) -> str:
        return self._questions_df.loc[index, 'id']

    def remove_animals_by_question_index_value(self, question_index:int, value: int):
        self._animals_df = self._animals_df[~(self._animals_df[self._questions_df.loc[question_index].id] == value)]

    def check_only_one_valid_animal_by_question_index(self, question_index: int) -> (int, str):
        number_of_valids = len(self._animals_df[self._questions_df.loc[question_index].id].dropna())
        if number_of_valids == 1:
            return number_of_valids, self._animals_df.loc[self._animals_df[self._questions_df.loc[question_index].id].notnull(), 'name'].item();
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
            aux_id = 'q'+str(self._questions_df.order.max()+1)
            self._questions_df = self._questions_df.append({'id':aux_id, 'text':text, 'order':self._questions_df.order.max()+1, 'weight':0}, ignore_index=True)
            self._animals_df[aux_id] = np.nan
            return aux_id

    def save_animals_to_disk(self):
        self._animals_df.to_csv('./dataframes/csv/animals.csv')

    def save_questions_to_disk(self):
        self._questions_df.to_csv('./dataframes/csv/questions.csv')

    def calculate_questions_weights(self):
        for row in self._questions_df.index:
            aux = self._animals_df.loc[:,self._questions_df.loc[row].id]
            self._questions_df.loc[row,'weight'] = (1 - abs(len(aux.loc[aux == 1]) - len(aux.loc[aux == 0]))/len(aux.dropna())) * (len(aux.dropna())/len(aux))
            self._questions_df = self._questions_df.sort_values('weight', ascending=False).reset_index(drop=True)
            self.save_questions_to_disk()

    def randomize_questions(self):
        self._questions_df = self._questions_df.sample(frac=1).reset_index(drop=True)
