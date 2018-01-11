"""
<name>First Widget</name>
<description>Example for creating your first widget.</description>
<tags>Prototypes</tags>
"""

#OWRpy is the parent of all widgets. 
#Contains all the functionality for connecting the widget to the underlying R session.
from OWRpy import *


# our first widget. Must be a child of OWRpy class
# The class name must be the same as the file name
from libraries.base.qtWidgets.textEdit import textEdit
from libraries.base.qtWidgets.lineEdit import lineEdit
from libraries.base.qtWidgets.button import button
class firstWidget(OWRpy):
    
    def __init__(self, parent=None, signalManager=None):
        #must initalize the parent OWRpy class
        OWRpy.__init__(self)
        
        ### GUI ###
        #create input line
        self.lineEdit = lineEdit(self.controlArea, label = 'Line Edit')
        #create submit button
        self.button = button(self.controlArea,label='submit',callback=self.process)
        #create output area
        self.output = textEdit(self.controlArea,label='Output')
    
    # on click submit call this function
    def process(self):
        # get the user typed command
        userEnteredRcmd = unicode(self.lineEdit.text())
        # add the R code to capture the output to txt variable
        captureCmd  = 'txt<-capture.output(' + userEnteredRcmd +')'
        # execute the R code in the underlying R session. 
        #self.R is a functionality from OWRpy
        self.R(captureCmd, wantType = 'NoConversion')
        #format the txt variable for string output
        pasted = self.R('paste(txt, collapse = " \n")')
        #set the text in the output area
        self.output.setText(pasted)
        
        
