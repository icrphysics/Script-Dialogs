# Script-Dialogs
Example Simple Ironpython and C-Python script dialogs

## ChooseFromList 
The ChooseFromList dialog allows user to select a single item from a list. 
It is called by

```python
import chooseFromList
answer = chooseFromList.getChoiceFromList(choiceList, prompt, title)
```
- choiceList should be a list of strings
- prompt is a string displayed as a dialog prompt
- title is a string displayed as the window title

- answer is a string chosen from choiceList or None if user clicked Cancel

see chooseFromList.test() for more example syntax

Shortcut functions are availble for common choices:
- chooseFromList.chooseRoi() : Choose from the ROIs present in the current case
- chooseFromList.choosePoi() : Choose from the POIs present in the current case
- chooseFromList.chooseImage() : Choose from the Examinations present in the current case
- chooseFromList.choosePlan() : Choose from the Plans present in the current case

## ChooseMultipleFromList 
The ChooseMultipleFromList dialog allows user to select multiple items from from a list. 
It is called by

```python
import chooseMultipleFromList
answers = chooseMultipleFromList.getChoicesFromList(choiceList, prompt, title)
```

- choiceList should be a list of strings displayed as options with tickboxes
- prompt is a string displayed as a dialog prompt
- title is a string displayed as the window title

- answer is a list of strings chosen from choiceList or None if user clicked Cancel

see chooseMultipleFromList.test() for more example syntax

Shortcut functions are availble for common choices:
- chooseMultipleFromList.chooseRois() : Choose from the ROIs present in the current case
- chooseMultipleFromList.choosePois() : Choose from the POIs present in the current case
- chooseMultipleFromList.chooseImages() : Choose from the Examinations present in the current case
- chooseMultipleFromList.choosePlans() : Choose from the Plans present in the current case
- chooseMultipleFromList.chooseBeams() : Choose from the Beams present in the current beamset

## C-python and IronPython

Both dialogs will work in C-Python and Ironpython.

### ChooseFromList
chooseFromList.py references two independant child scripts:
* chooseFromList_ipy  A dialog designed for IronPython that displays the window using the .NET WPF library
* chooseFromList_cpy  A dialog designed for C-Python that displays the window using the ttk library

### ChooseMultipleFromList
chooseMultipleFromList.py has one single script that uses the C-Python dotnet library and different 
WPF commands to make the WPF window work in both IronPython and C-Python
