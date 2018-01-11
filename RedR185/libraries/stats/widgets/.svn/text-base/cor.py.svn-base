"""
<name>Correlation/Variance</name>
<tags>Stats</tags>
<icon>correlation.png</icon>
"""
#OWRpy is the parent of all widgets. 
#Contains all the functionality for connecting the widget to the underlying R session.
from OWRpy import *


# signalClasses classes contain the data that is passed between widgets. 
# In this case we are using the RDataFrame and RMatrix signals
from libraries.base.signalClasses.RDataFrame import RDataFrame as redRRDataFrame
from libraries.base.signalClasses.RMatrix import RMatrix as redRRMatrix


# our first widget. Must be a child of OWRpy class
# The wiget class name must be the same as the file name

## these are the imports of the qt widgets that are Red-R compliant.  Feel free to make your own widgets and use them.  You can even use Qt widgets directly, though this is not recomended as they may not work with loading and saving.
from libraries.base.qtWidgets.filterTable import filterTable as redRfilterTable
from libraries.base.qtWidgets.button import button
from libraries.base.qtWidgets.checkBox import checkBox
from libraries.base.qtWidgets.radioButtons import radioButtons
from libraries.base.qtWidgets.widgetBox import widgetBox
from libraries.base.qtWidgets.commitButton import commitButton as redRCommitButton

class cor(OWRpy):
    
    # a list of all the variables that need to be saved in the widget state file.
    # these varibles values will be shared between widgets
    globalSettingsList = ['commit']

    # Python init statement is the class constructor 
    # Here you put all the code that will run as soon as the widget is put on the canvas
    def __init__(self, parent=None, signalManager=None):
        #Here we init the parent class of our widget OWRpy.
        OWRpy.__init__(self)
        
        #create a R variable cor in the R session.  These variables will be in the R session to track the ouputs of functions that run in R.
        #the cor variable will not conflict with some other widgets cor function
        self.setRvariableNames(["cor"])
        
        # declare some variables we will use later
        self.RFunctionParam_y = None
        self.RFunctionParam_x = None
        
        # Define the inputs that this widget will accept
        # When data is received the three element in the tuple which is a function will be executed
        self.inputs.addInput('id0', 'x', redRRDataFrame, self.processx)
        self.inputs.addInput('id1', 'y', redRRDataFrame, self.processy)

        # Define the outputs of this widget
        self.outputs.addOutput('id0', 'cor Output', redRRMatrix)

        
        #START THE GUI LAYOUT
        area = widgetBox(self.controlArea,orientation='horizontal')       
        
        options = widgetBox(area,orientation='vertical')
        area.layout().setAlignment(options,Qt.AlignTop)
        
        # radioButtons are a type of qtWidget from the base package.  This widget will show radioButtons in a group.  Only one radio button may be selected at one time.  Buttons are declared using buttons = , the callback is the function that will be executed when the button selection changes.  setChecked sets a button to be checked by default.
        self.type = radioButtons(options,  label = "Perform", 
        buttons = ['Variance', 'Correlation', 'Covariance'],setChecked='Correlation',
        orientation='vertical',callback=self.changeType)
        
        self.methodButtons = radioButtons(options,  label = "Method", 
        buttons = ['pearson', 'kendall', 'spearman'],setChecked='pearson',
        orientation='vertical')

        self.useButtons =  radioButtons(options, label='Handing Missing Values', setChecked='everything',
        buttons = ["everything","all.obs", "complete.obs", "pairwise.complete.obs"],
        orientation='vertical')
        
        # the commit button is a special button that can be set to process on data input.  Widgets must be aware of these selections.  Clicking the commit button executes the callback which in this case executes the commitFunction.
        self.commit = redRCommitButton(self.bottomAreaRight, "Commit", callback = self.commitFunction,
        processOnInput=True)
        
        # this is a filter table designed to hold R data.  The name is Cor/Var for the report generation but the user will not see this label because displayLabel is set to False.
        self.RoutputWindow = redRfilterTable(area,label='Cor/Var', displayLabel=False,
        sortable=True,filterable=False)
    
    # execute this function when data in the X channel is received
    # The function will be passed the data
    def processx(self, signal):
        if signal:
            #if the signal exists get the data from it
            self.RFunctionParam_x=signal.getData()
            # if the checkbox is checked, immediately process the data
            if self.commit.processOnInput():
                self.commitFunction()
                
    # execute this function when data in the Y channel is received
    # does the same things as processX
    def processy(self, signal):
        if signal:
            self.RFunctionParam_y=signal.getData()
            if self.commit.processOnInput():
                self.commitFunction()
            
    # this function actually does the work in R 
    # its call by clicking the Commit button
    # or when data is received, if the checkbox is checked.
    def commitFunction(self):
        # The X data is required, if not received, do nothing
        if not self.RFunctionParam_x: 
            self.status.setText('X data is missing')
            return

        
        # START COLLECTION THE R PARAMETERS THAT WILL CREATE THE R CODE TO EXECUTE
        injection = []
        
        if self.type.getChecked() == 'Correlation':
            test = 'cor'
        elif self.type.getChecked() == 'Variance':
            test = 'var'
        elif self.type.getChecked() == 'Covariance':
            test = 'cov'
            
        if self.useButtons.getChecked():
            string = 'use=\''+unicode(self.useButtons.getChecked())+'\''
            injection.append(string)
        elif self.type.getChecked() == 'Variance':
            string = 'na.rm=TRUE'
            injection.append(string)
        
        if self.methodButtons.getChecked():
            string = 'method=\''+unicode(self.methodButtons.getChecked())+'\''
            injection.append(string)
            
        if self.RFunctionParam_y:
            injection.append('y='+unicode(self.RFunctionParam_y))

        # combine all the parameters in the a string    
        inj = ','.join(injection)
        
        # make the R call. The results will be saved in the 'cor' variable we declared earlier
        self.R(self.Rvariables['cor']+'<-'+test+'(x='+unicode(self.RFunctionParam_x)+','+inj+')')
        
        # visualize the data in a table
        self.RoutputWindow.clear()
        self.RoutputWindow.setRTable(self.Rvariables['cor'])
        
        # create a new signal of type RMatrix and load the results 
        newData = redRRMatrix(data = self.Rvariables["cor"]) 
        # send the signal forward
        self.rSend("id0", newData)
  
    
    # Based on the user selections some parameters is not valid. This is all documented in the R help for cor/var/cov
    # Here we are instructing the GUI to disable those parameters that are invalid. 
    def changeType(self):
        if self.type.getChecked() =='Variance':
            self.useButtons.setDisabled(True)
            self.methodButtons.setDisabled(True)
        else:    
            self.useButtons.setEnabled(True)
            self.methodButtons.setEnabled(True)

        if self.type.getChecked() =='Covariance':
            self.useButtons.disable(['pairwise.complete.obs'])
        elif self.type.getChecked() =='Correlation':
            self.useButtons.enable(['pairwise.complete.obs'])
    
    # getReportText returns a string of text in restructuredtext format that will be used to generate the report of the data.
    # We should send back a general representation of what happened in the widget to the user.
 
        
        
        
