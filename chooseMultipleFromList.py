"""
Dialog to ask user to choose multiple items from a list.

To test type in a console:
from rmh.dialogs import chooseMultipleFromList
chooseMultipleFromList.test()
"""

# ------------------------------------- #
import clr, sys, os

clr.AddReference("System.Windows.Forms")

import System
from System.Windows import HorizontalAlignment, Thickness
from System.Windows.Controls import StackPanel, Button, Label, TextBox, CheckBox, Grid, ColumnDefinition, RowDefinition

from System.Windows.Markup import XamlReader
from System.IO import StreamReader
from System.Windows import Application, Window, LogicalTreeHelper
from System.Threading import Thread, ThreadStart, ApartmentState

try:
    import connect as rsl
except:
    print('No RayStation connection available using offline testing connection.')
    from rmh.test import rslOffline as rsl

# ------------------------------------- #
# -------------- GUI Code ------------- #
# ------------------------------------- #

GUI_XAML_FILE = os.path.join( os.path.split(os.path.realpath(__file__))[0], "chooseMultipleFromList.xaml") 
DEFAULT_TITLE = 'Choose from list'
DEFAULT_PROMPT = 'Choose items from the list and press OK'
CHOOSE_MULTIPLE_FROM_LIST_APPLICATION = None

# ------------------------------------- #

class ChooseFromListModel():
    
    def __init__(self, choiceList=None, prompt=DEFAULT_PROMPT, title=DEFAULT_TITLE, alignChoices=None):
        """
        Initialise the Gui Object
        """
        self.choices = None
        self.choiceList = choiceList
        self.prompt = prompt
        self.title = title
        self.alignChoices = alignChoices
        
# ------------------------------------- #

class ChooseFromListView(System.Windows.Window):
    
    def __init__(self, model):
        """
        Display the GUI using data in the model class
        """
        self.model = model
        
        stream = StreamReader(os.path.join(os.path.dirname(__file__),GUI_XAML_FILE))
        self.window = XamlReader.Load(stream.BaseStream)
        
        self.window.Title = self.model.title
        
        self.lblPrompt = LogicalTreeHelper.FindLogicalNode(self.window, "lblPrompt")
        self.lblPrompt.Content = self.model.prompt
      
        self.choicesGrid = LogicalTreeHelper.FindLogicalNode(self.window, "choicesGrid")
        self.choicesChk = System.Array.CreateInstance(CheckBox, len(self.model.choiceList))
        self.choicesLabels = System.Array.CreateInstance(Label, len(self.model.choiceList))
        
        for ii, choiceName in enumerate(self.model.choiceList):
            self.choicesGrid.RowDefinitions.Add(RowDefinition())
            
            self.choicesLabels[ii] = Label()
            self.choicesLabels[ii].Content = choiceName
            self.choicesLabels[ii].SetValue(Grid.RowProperty, ii)
            self.choicesLabels[ii].SetValue(Grid.ColumnProperty, 0)
            
            if self.model.alignChoices.lower() == 'left':
                self.choicesLabels[ii].HorizontalAlignment = HorizontalAlignment.Left
            else:    
                self.choicesLabels[ii].HorizontalAlignment = HorizontalAlignment.Right
            self.choicesGrid.Children.Add(self.choicesLabels[ii])
      
            self.choicesChk[ii] = CheckBox()
            self.choicesChk[ii].Margin = Thickness(7.0, 7.0, 2.0, 2.0)
            self.choicesChk[ii].SetValue(Grid.RowProperty, ii)
            self.choicesChk[ii].SetValue(Grid.ColumnProperty, 1)
            self.choicesChk[ii].HorizontalAlignment = HorizontalAlignment.Left
            self.choicesGrid.Children.Add(self.choicesChk[ii])
            
        self.btCancel = LogicalTreeHelper.FindLogicalNode(self.window, "btCancel")
        self.btCancel.Click += self.cancel_clicked
        self.btOK = LogicalTreeHelper.FindLogicalNode(self.window, "btOK")
        self.btOK.Click += self.ok_clicked

        self.window.Show()
        self.window.Closed += lambda s,e: self.window.Dispatcher.InvokeShutdown()
        System.Windows.Threading.Dispatcher.Run()
                
    # ------------------ #
    
    def ok_clicked(self, sender, event):
        """
        Close dialog
        """
        self.model.choices = [chLbl.Content for chLbl, chk in zip(self.choicesLabels, self.choicesChk) 
									if chk.IsChecked]
        if len(self.model.choices) == 0:
            self.model.choices = None
    
        self.Close()
        
    # ------------------ #
  
    def cancel_clicked(self, sender, event):
        """
        Close dialog
        """
        self.model.choices = None
        self.Close()
        
    # ------------------ #
    
    def Close(self):
        """
        On call to close close the window 
        """
        self.window.Close()
        
# ------------------------------------------- #

def getChoicesFromList(choiceList=None, prompt=DEFAULT_PROMPT, title=DEFAULT_TITLE, alignChoices=None):
    """
    Ask user to enter their choices from the list and return it.
  
    choiceList should be a list of strings
    """
    if alignChoices is None:
        alignChoices = 'left'
    
    choiceData = ChooseFromListModel(choiceList=choiceList, prompt=prompt, 
                                title=title, alignChoices=alignChoices)
    
    thread = Thread(ThreadStart(lambda: ChooseFromListView(choiceData)))
    thread.SetApartmentState(ApartmentState.STA)
    thread.Start()
    thread.Join()
    
    return choiceData.choices
    
# ------------------------------------------- #

def chooseRois(prompt='Select ROIs and press OK', title='Choose from ROIs'):
    """
    Ask user to select an ROI from the ROIs in the active patient
    """
    case = rsl.get_current('Case')
    roiNames = [ roi.Name for roi in case.PatientModel.RegionsOfInterest ]
    return getChoicesFromList(choiceList=roiNames, prompt=prompt, title=title)
  
# ------------------------------------------- #

def chooseImages(prompt='Select Images and press OK', title='Choose from Images'):
    """
    Ask user to select an Image from the Images in the active patient
    """
    case = rsl.get_current('Case')
    imageNames = [ img.Name for img in case.Examinations ]
    return getChoicesFromList(choiceList=imageNames, prompt=prompt, title=title)

# ------------------------------------------- #

def choosePlans(prompt='Select Plans and press OK', title='Choose from Plans'):
    """
    Ask user to select an Image from the Images in the active patient
    """
    case = rsl.get_current('Case')
    planNames = [ pln.Name for pln in case.TreatmentPlans ]
    return getChoicesFromList(choiceList=planNames, prompt=prompt, title=title)

# ------------------------------------------- #
	
def chooseBeams(prompt='Select Beams and press OK', title='Choose from Beams'):
    """
    Ask user to select an Image from the Images in the active patient
    """
    bs = rsl.get_current('BeamSet')
    beamNames = [ bm.Name for bm in bs.Beams ]
    return getChoicesFromList(choiceList=beamNames, prompt=prompt, title=title)
	
# ------------------------------------------- #
 
def test():
    choice = getChoicesFromList(['Item 1', 'Item 2', 'Item 3'])
    print('User entered : %s' % (choice))
    
# ------------------------------------------- #
  
if __name__ == '__main__':
    test()
