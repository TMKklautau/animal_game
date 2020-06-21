import sys

import ui
import data
import logic

def main(args):
    _ui_module = ui.Cmd_Ui_module()
    _data_module = data.Csv_Data_module()
    _logic_module = logic.Logic_module(_ui_module, _data_module)
    _logic_module.start_execution()
if __name__ == '__main__':
    main(sys.argv[1:])
