"""
Dialog to ask user to choose an item from a list.

To test type in a console:
    from rmh.dialogs import chooseFromList
    chooseFromList.test()
"""

import platform

if platform.python_implementation() != "IronPython":
    from rmh.dialogs.chooseFromList_cpy import *
else:
    from rmh.dialogs.chooseFromList_ipy import *
