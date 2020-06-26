import sys

import ui
import data
import logic

def main(args):
    '''Script entry point for the animal game

    Defined args:

    -uw : (update weights) recalculates the weights of the questions and sort the optimal question order for the first question
    -rnd : (randomize questions) randomizes the questions order, used to train questions with low percent of data
            and making the game non-linear after a database is optimized
    -pd : (print data) debug function to print the dataframes on the console, best used for small dataframes, for big ones the best is to acess it directly
    -sg : (skip game) used to perform the actions passed on the other arguments without starting the game after
    '''
    _ui_module = ui.Cmd_Ui_module()
    _data_module = data.Csv_Data_module()
    _logic_module = logic.Logic_module(_ui_module, _data_module)

    if('-uw' in args): #update weights
        _data_module.calculate_questions_weights()
    if('-rnd' in args): #randomize questions
        _data_module.randomize_questions()
    if('-pd' in args): #print data, used only for debugging goes against code modularity
        print(_data_module._animals_df)
        print(_data_module._questions_df)
    if('-sg' in args): #skip game
        return
    _logic_module.start_execution()

if __name__ == '__main__':
    main(sys.argv[1:])
