"""
Dialog to ask user to choose an item from a list.

C-Python TCL-TK Implementation

To test type in a console:
    from rmh.dialogs import chooseFromList_cpy
    chooseFromList_cpy.test()
"""

# -------------------------------- #

from ttk import Tkinter as tk
import ttk

try:
    import connect as rsl
except:
    print('No RayStation connection available using offline testing connection.')
    from rmh.test import rslOffline as rsl

# -------------------------------- #

DEFAULT_TITLE = 'Choose from list'
DEFAULT_PROMPT = 'Choose an item from the list and press OK'
DEFAULT_CHOICES_WIDTH = None

# -------------------------------- #

class ChooseFromListModel():
    
    def __init__(self, choiceList=None, prompt=DEFAULT_PROMPT, title=DEFAULT_TITLE, 
                    choicesWidth=DEFAULT_CHOICES_WIDTH):
        """
        Initialise the Gui Object
        """
        self.choice = None
        self.choiceList = choiceList
        self.prompt = prompt
        self.title = title
        self.app = None
        self.choicesWidth = choicesWidth
               
# -------------------------------- #

class ChooseFromListView(tk.Frame, object):
    
    def __init__(self, model, master=None):
        super(ChooseFromListView, self).__init__(master)
        self.pack()
        self.model = model
        self.master = master
        self.style()
        self.create_widgets(model)
        
    # -------------- #
    
    def create_widgets(self, model):
        """
        Create active widgets in the window
        """
        self.winfo_toplevel().title(self.model.title)
        
        self.lblPrompt = tk.Label(self)
        self.lblPrompt["text"] = self.model.prompt
        self.lblPrompt.pack(side="top", padx=5, pady=5)
        
        self.choicesBox = ttk.Combobox(self)
        self.choicesBox["values"] = self.model.choiceList
        self.choicesBox["textvariable"] = self.model.choice
        self.choicesBox["state"] = "readonly"
        if self.model.choicesWidth is not None:
            self.choicesBox["width"] = self.model.choicesWidth
        
        self.choicesBox.pack(side="top", padx=5, pady=5)
        
        self.createButtonFrame(model)
    
    # -------------- #
    
    def createButtonFrame(self, model):
        """
        Create a row of Cancel and OK buttons at the bottom of the window
        """
        self.btnFrame = tk.Frame(self)
        self.btnFrame.pack(side="bottom", padx=5, pady=5)
                
        self.btCancel = tk.Button(self.btnFrame)
        self.btCancel["text"] = "Cancel"
        self.btCancel["command"] = self.cancel_clicked
        #self.btCancel.config( height = 20, width = 80 )
        self.btCancel.pack(side="left")
        
        self.lblOkCanSpace = tk.Label(self.btnFrame)
        self.lblOkCanSpace["text"] = "  "
        self.lblOkCanSpace.pack(side="left", padx=5, pady=5)
        
        self.btOK = tk.Button(self.btnFrame)
        self.btOK["text"] = "OK"
        self.btOK["command"] = self.ok_clicked
        #self.btOK["width"] = 80
        #self.btOK["height"] = 20
        self.btOK.pack(side="left", padx=5, pady=5)

    # -------------- #
    
    def style(self):
        pass
        
    # -------------- #
    
    def cancel_clicked(self):
        """
        Cancel Clicked
        """
        self.model.choice = None
        self.master.eval('::ttk::CancelRepeat')
        self.master.destroy()
        
    # -------------- #
    
    def ok_clicked(self):
        """
        OK Clicked
        """
        self.model.choice = self.choicesBox.get()
        self.master.eval('::ttk::CancelRepeat')
        self.master.destroy()
        
# -------------------------------- #

def getChoiceFromList(choiceList=None, prompt=DEFAULT_PROMPT, title=DEFAULT_TITLE, 
                        choicesWidth=DEFAULT_CHOICES_WIDTH):
    """
    Ask user to enter their choice from the list and return it.

    choiceList should be a list of strings
    """
    d_Model = ChooseFromListModel(choiceList=choiceList, prompt=prompt, title=title, 
                            choicesWidth=choicesWidth)
    
    root = tk.Tk()
    view = ChooseFromListView(d_Model, master=root)
    view.mainloop()
    
    return d_Model.choice

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

