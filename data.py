import pandas as pd
import numpy as np
import os

class Data_module:
    '''Base data manipulation module'''
    mdl_type:str = 'base'

    def __init__(self):
        pass

    def reset_animals_to_disk_version(self):
        '''Reloads the database part with animals with the version on persistent storage

        '''
        pass

    def reset_questions_to_disk_version(self):
        pass

    def is_animal_present(self, name:str) -> bool:
        '''Verifies if an animal's name is present on the database

        Args:
            name (str): the name to check

        '''
        return None

    def get_number_of_questions(self) -> int:
        '''Returns the number of questions present in the database

        Returns:
            int: the number of questions

        '''
        return None

    def get_question_text_by_index(self, index: int) -> str:
        '''Returns the text of the question associated with the passed index

        Args:
            index (int): index of the question to return the text

        Returns:
            str: text of the question requested

        '''
        return None

    def get_question_id_by_index(self, index: int) -> str:
        '''Returns the id of the question associated with the passed index

        Args:
            index (int): index of the question to return the id

        Returns:
            str: id of the question requested

        '''
        return None

    def remove_animals_by_question_index_value(self, question_index: int, value: int):
        '''Removes all animals that have the value on the question (animals without information on the passed question will not be removed)

        Args:
            question_index (int): the index of the question to use
            value (int): the value to remove

        '''
        pass

    def check_only_one_valid_animal_by_question_index(self, question_index: int) -> (int, str):
        '''Returns the number of animals with info on the question present on the state of the database

        Args:
            question_index (int): the index of the question to use

        Returns:
            int: the number of animals with info on the passed question present on the state of the database
            str: the name of the animal with info on the passed question (Returns None if no animal has info, or if there is more than 1 animal)

        '''
        return None, None

    def update_animal_with_dict(self, animal_data: dict):
        '''Updates the database with the animal with the info contained on the passed dict (name needed for on the passed dict for index)

        Args:
            animal_data (dict): data of the animal to update

        '''
        pass

    def add_animal_with_dict(self, animal_data: dict):
        '''Adds an animal with the data passed on the dict (name obrigatory)

        Args:
            animal_data (dict): data of the animal to add

        '''
        pass

    def add_question_with_text(self, text: str) -> str:
        '''Adds a question with the text passed

        Args:
            text (str): text of the question to be added

        '''
        return None

    def save_animals_to_disk(self):
        '''Saves the state of the loaded animals database to permanent storage

        '''
        pass

    def save_questions_to_disk(self):
        '''Saves the state of the loaded questions database to permanent storage

        '''
        pass

    def calculate_questions_weights(self):
        '''Changes the order of the questions using a weight system
        (the weight is the percent of animals with data times the difference between the 2 options, so weight correlates with the number of removed options if a question is presented)

        '''
        pass

    def randomize_questions(self):
        '''Changes the order of the questions randomly

        '''
        pass

    def build_new_bst(self, depth:int = -1):
        '''Builds new binary search tree for preprocessing the best question order with the data on dik

        Args:
            depth (int) = -1: max depth on the tree, if negative the tree indexes all possibilities

        '''
        pass

    def get_question_id_list(self) -> list:
        '''Returns a list with all ids on the questions database

        Returns:
            List: list of ids

        '''
        return None

    def get_node_from_index(self, index:int) -> dict:
        '''Returns a dict with the node information associated with the passed index

        Args:
            index (int): index of the node to return

        Returns:
            dict: node information

        '''
        return None

    def get_question_index_from_id(self, question_id:str) -> int:
        '''Returns the index of a question with the passed id

        Args:
            question_id (str): id to search

        Returns:
            int :index of the question found

        '''
        return None

class Csv_Data_module(Data_module):
    '''Csv using pandas data module'''
    mdl_type:str = 'Csv'

    def __init__(self):
        super().__init__()
        self._animals_df = pd.read_csv(os.path.join(os.path.dirname(__file__),'dataframes/csv/animals.csv'), index_col=0)
        self._questions_df = pd.read_csv(os.path.join(os.path.dirname(__file__),'dataframes/csv/questions.csv'), index_col=0)
        self._bst_df = pd.read_csv(os.path.join(os.path.dirname(__file__),'dataframes/csv/bst.csv'), index_col=0)

    def reset_animals_to_disk_version(self):
        self._animals_df = pd.read_csv(os.path.join(os.path.dirname(__file__),'dataframes/csv/animals.csv'), index_col=0)

    def reset_questions_to_disk_version(self):
        self._questions_df = pd.read_csv(os.path.join(os.path.dirname(__file__),'dataframes/csv/questions.csv'), index_col=0)

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
        #put check for name != null later
        aux_series = pd.Series(animal_data)
        self._animals_df.loc[self._animals_df.name == animal_data['name'], aux_series.index] = aux_series.values

    def add_animal_with_dict(self, animal_data: dict):
        #put check for name != null later
        self._animals_df = self._animals_df.append(animal_data, ignore_index=True)

    def add_question_with_text(self, text:str) -> str:
        if(not self._questions_df.loc[self._questions_df.text == text].empty):
            return self._questions_df.loc[self._questions_df.text == text, 'id'].item()
        else:
            aux_id = 'q'+str(self._questions_df.order.max()+1)
            self._questions_df = self._questions_df.append({'id':aux_id, 'text':text, 'order':self._questions_df.order.max()+1, 'weight':0}, ignore_index=True)
            self._animals_df[aux_id] = np.nan
            return aux_id

    def save_animals_to_disk(self):
        self._animals_df.to_csv(os.path.join(os.path.dirname(__file__),'dataframes/csv/animals.csv'))

    def save_questions_to_disk(self):
        self._questions_df.to_csv(os.path.join(os.path.dirname(__file__),'dataframes/csv/questions.csv'))

    def calculate_questions_weights(self):
        self._calculate_questions_weights_from_snapshot(self._questions_df, self._animals_df)
        self._questions_df = self._sort_questions_by_weight(self._questions_df)

    def _calculate_questions_weights_from_snapshot(self, aux_questions_df:pd.DataFrame, aux_animals_df:pd.DataFrame):
        for row in aux_questions_df.index:
            aux = aux_animals_df.loc[:,aux_questions_df.loc[row].id]
            if(len(aux.dropna()) > 0):
                aux_questions_df.loc[row,'weight'] = (1 - abs(len(aux.loc[aux == 1]) - len(aux.loc[aux == 0]))/len(aux.dropna())) * (len(aux.dropna())/len(aux))
            else:
                aux_questions_df.loc[row,'weight'] = 0

    def _sort_questions_by_weight(self, aux_questions_df:pd.DataFrame) -> pd.DataFrame:
        return aux_questions_df.sort_values('weight', ascending=False).reset_index(drop=True)

    def randomize_questions(self):
        self._questions_df = self._questions_df.sample(frac=1).reset_index(drop=True)

    def build_new_bst(self, depth:int = -1):

        if((depth < 0) | (depth > len(self._questions_df))):
            depth = len(self._questions_df)

        self.calculate_questions_weights()
        self._bst_df = self._bst_df[0:0]
        self._bst_df = self._bst_df.append({'parent':-1,'y_child':-1,'n_child':-1,'question':self._questions_df.loc[0,'id']}, ignore_index=True)

        aux_animals_snap = self._animals_df.copy()
        aux_questions_snap = self._questions_df.copy()

        aux_animals_snap_0 = aux_animals_snap[~(aux_animals_snap[aux_questions_snap.loc[0,'id']] == 0)]
        aux_animals_snap_1 = aux_animals_snap[~(aux_animals_snap[aux_questions_snap.loc[0,'id']] == 1)]
        aux_questions_snap = aux_questions_snap[1:]

        self._bst_df.loc[0,'y_child'] =  self._build_new_bst_recursive(depth, 1, 0, aux_questions_snap, aux_animals_snap_1)
        self._bst_df.loc[0,'n_child'] =  self._build_new_bst_recursive(depth, 1, 0, aux_questions_snap, aux_animals_snap_0)

        self._bst_df.to_csv(os.path.join(os.path.dirname(__file__),'dataframes/csv/bst.csv'))

    def _build_new_bst_recursive(self, max_depth:int, current_depth:int, parent_index:int, arg_questions_df_snapshot:pd.DataFrame, arg_animals_df_snapshot:pd.DataFrame) -> int:

        if(max_depth<=current_depth):
            return -1

        aux_questions_snap = arg_questions_df_snapshot.copy()
        aux_animals_snap = arg_animals_df_snapshot.copy()

        self._calculate_questions_weights_from_snapshot(aux_questions_snap, aux_animals_snap)
        aux_questions_snap = self._sort_questions_by_weight(aux_questions_snap)

        my_index = len(self._bst_df)

        self._bst_df = self._bst_df.append({'parent':parent_index, 'y_child':-1, 'n_child':-1, 'question':aux_questions_snap.loc[0,'id']}, ignore_index=True)

        aux_animals_snap_0 = aux_animals_snap[~(aux_animals_snap[aux_questions_snap.loc[0,'id']] == 0)]
        aux_animals_snap_1 = aux_animals_snap[~(aux_animals_snap[aux_questions_snap.loc[0,'id']] == 1)]
        aux_questions_snap = aux_questions_snap[1:]

        self._bst_df.loc[my_index,'y_child'] =  self._build_new_bst_recursive(max_depth, current_depth+1, my_index, aux_questions_snap, aux_animals_snap_1)
        self._bst_df.loc[my_index,'n_child'] =  self._build_new_bst_recursive(max_depth, current_depth+1, my_index, aux_questions_snap, aux_animals_snap_0)

        return my_index

    def get_question_id_list(self) -> list:
        return self._questions_df.id.to_list()

    def get_node_from_index(self, index:int) -> dict:
        return self._bst_df.loc[index].to_dict()

    def get_question_index_from_id(self, question_id:str) -> int:
        return self._questions_df[self._questions_df.id == question_id].index[0]

