class Ui_module:
    '''Base UI class'''
    mdl_type:str = 'base'

    def __init__(self):
        pass

    def present_text(self, text:str):
        '''Present text to user without receiving input

        Args:
            text (str): the text to be presented
        '''
        pass

    def get_str_input(self) -> str:
        '''Receive input from user on the str format without presenting a text

        Returns:
            str: input from user
        '''
        return(None)

    def get_delimited_input_with_text(self, text:str, values:tuple) -> str:
        '''Present text to user and waits for a delimited input

        Args:
            text (str): the text to be presented
            values (tuple): tuple of values accepted as input

        Returns:
            str: input from user
        '''
        return(None)

    def get_free_input_with_text(self, text:str) -> str:
        '''Present text to user and receive input

        Args:
            text (str): the text to be presented

        Returns:
            str: input from user
        '''
        return(None)

class Cmd_Ui_module(Ui_module):
    '''Command line UI implementation'''
    mdl_type:str = 'Cmd'

    def __init__(self):
        super().__init__()

    def present_text(self, text:str):
        print('------------------------')
        print(text)

    def get_input(self) -> str:
        return(str(input()))

    def get_delimited_input_with_text(self, text:str, values:tuple) -> str:
        print('------------------------')
        print(text)
        answer_aux = str(input())
        while answer_aux not in values:
            print('Not a valid answer, insert a valid one')
            answer_aux = str(input())
        return answer_aux

    def get_free_input_with_text(self, text:str) -> str:
        print('------------------------')
        print(text)
        return str(input())
