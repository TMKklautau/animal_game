class Ui_module:
    '''Base UI class'''
    mdl_type:str = 'base'

    def __init__(self):
        pass

    def present_text(self, text:str):
        #put raise errors here later
        pass

    def get_str_input(self) -> str:
        return(None)

class Cmd_Ui_module(Ui_module):
    '''Command line UI implementation'''
    mdl_type:str = 'Cmd'

    def __init__(self):
        super().__init__()

    def present_text(self, text:str):
        print(text)

    def get_input(self) -> str:
        return(str(input()))
