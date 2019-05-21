"""
Dialog to ask user to choose an item from a list.

IronPython WPF Implementation

To test type in a console:
    from rmh.dialogs import chooseFromList_ipy
    chooseFromList_ipy.test()
"""

# ------------------------------------- #
import wpf, clr, sys, os

clr.AddReference("System.Windows.Forms")

import System
from System.Windows import HorizontalAlignment
from System.Windows.Controls import StackPanel, Button, Label, TextBox, ComboBox

try:
    import connect as rsl
except:
    print('No RayStation connection available using offline testing connection.')
    from rmh.test import rslOffline as rsl


# ------------------------------------- #
# -------------- GUI Code ------------- #
# ------------------------------------- #

GUI_XAML_FILE = os.path.join( os.path.split(os.path.realpath(__file__))[0], "chooseFromList_ipy.xaml") 
DEFAULT_TITLE = 'Choose from list'
DEFAULT_PROMPT = 'Choose an item from the list and press OK'

class ChooseFromListDialog(System.Windows.Window):
    # ------------------ #

    def getChoice(self):
        return self.choice
  
    # ------------------ #
  
    def __init__(self, choiceList=None, prompt=DEFAULT_PROMPT, title=DEFAULT_TITLE):
        """
        Display the dialog to allow user to choose an item from a list
        
        Dialog Intended appearance:
          ----------------------------
          Title
          Prompt
          [listOfChoices]
          
             <OK-Btn>
          ----------------------------
        """
        self.choice = None
        
        wpf.LoadComponent(self, GUI_XAML_FILE)
        
        self.Title = title
        self.lblPrompt.Content = prompt
      
        self.choicesBox.ItemsSource = choiceList
    
    # ------------------ #

    # Eventhandler
    def ok_clicked(self, sender, event):
        """
        Close dialog
        """
        self.choice = self.choicesBox.Text
        if len(self.choice) == 0:
            self.choice = None
        
        self.Close()
  
    # ------------------ #
  
    def cancel_clicked(self, sender, event):
        """
        Close dialog
        """
        self.choice = None
        self.Close()
    
# ------------------------------------------- #

def getChoiceFromList(choiceList=None, prompt=DEFAULT_PROMPT, title=DEFAULT_TITLE):
    """
    Ask user to enter their choice from the list and return it.

    choiceList should be a list of strings
    """
    dialog = ChooseFromListDialog(choiceList=choiceList, prompt=prompt, title=title)
    dialog.ShowDialog()

    return dialog.getChoice()
  
# ------------------------------------------- #

def chooseRoi(prompt='Choose an ROI and press OK', title='Choose an ROI'):
    """
    Ask user to select an ROI from the ROIs in the active patient
    """
    case = rsl.get_current('Case')
    roiNames = [ roi.Name for roi in case.PatientModel.RegionsOfInterest ]
    return getChoiceFromList(choiceList=roiNames, prompt=prompt, title=title)
  
# ------------------------------------------- #

def choosePoi(prompt='Choose a Point and press OK', title='Choose a POI'):
    """
    Ask user to select an POI from the POIs in the active patient
    """
    case = rsl.get_current('Case')
    poiNames = [ poi.Name for poi in case.PatientModel.PointsOfInterest ]
    return getChoiceFromList(choiceList=poiNames, prompt=prompt, title=title)
  
# ------------------------------------------- #


def chooseImage(prompt='Choose an Image and press OK', title='Choose an Image'):
    """
    Ask user to select an Image from the Images in the active patient
    """
    case = rsl.get_current('Case')
    imageNames = [ img.Name for img in case.Examinations ]
    return getChoiceFromList(choiceList=imageNames, prompt=prompt, title=title)

# ------------------------------------------- #

def choosePlan(prompt='Choose a Plan and press OK', title='Choose a Plan'):
    """
    Ask user to select an Image from the Images in the active patient
    """
    case = rsl.get_current('Case')
    planNames = [ pln.Name for pln in case.TreatmentPlans ]
    return getChoiceFromList(choiceList=planNames, prompt=prompt, title=title)

# ------------------------------------------- #
 
def test():
    choice = getChoiceFromList(['Item 1', 'Item 2', 'Item 3'])
    print('User entered : %s' % (choice))
  
# ------------------------------------------- #
  
if __name__ == '__main__':
  test()
