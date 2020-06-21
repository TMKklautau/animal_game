import pandas as pd

class Data_module:
    '''Base data manipulation module'''
    mdl_type:str = 'base'

    def __init__(self):
        pass

class Csv_Data_module(Data_module):
    '''Csv using pandas data module'''
    mdl_type:str = 'Csv'

    def __init__(self):
        super().__init__()
        self._animals_df = pd.read_csv('./dataframes/csv/animals.csv')
        self._questions_df = pd.read_csv('./dataframes/csv/questions.csv')
