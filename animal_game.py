import sys

import ui
import data
import logic

def main(args):
    '''Script entry point for the animal game

    Defined args:

    -uw : (update weights) recalculates the weights of the questions and sort the optimal question order for the first question
            using will set simplified search if the game is played right after
    -rnd : (randomize questions) randomizes the questions order, used to train questions with low percent of data
            and making the game non-linear after a database is optimized
            using will set simplified search if the game is played right after
    -pd : (print data) debug function to print the dataframes on the console, best used for small dataframes, for big ones the best is to acess it directly
    -rt : (rebuild tree) rebuilds the binary search tree
    -ss : (simplified search) sets simplified search for the game played this session
    -sg : (skip game) used to perform the actions passed on the other arguments without starting the game after
    '''
    _ui_module = ui.Cmd_Ui_module()
    _data_module = data.Csv_Data_module()
    _logic_module = logic.Logic_module(_ui_module, _data_module)

    simplified_search = 0

    if('-uw' in args): #update weights
        _data_module.calculate_questions_weights()
        _data_module.save_questions_to_disk()
        simplified_search = 1
    if('-rnd' in args): #randomize questions
        _data_module.randomize_questions()
        simplified_search = 1
    if('-pd' in args): #print data, used only for debugging goes against code modularity
        print(_data_module._animals_df)
        print(_data_module._questions_df)
        print(_data_module._bst_df)
    if('-rt' in args):
        _data_module.build_new_bst()
    if('-ss' in args):
        simplified_search = 1
    if('-sg' in args): #skip game
        return
    _logic_module.start_execution(simplified_search)

if __name__ == '__main__':
    main(sys.argv[1:])
