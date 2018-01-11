## Math widget.  Performs math on a column of a data table (RDataFrame).  Math functions can be added as the user wishes but many functions should already be present.  Note that if the widget fails you will get a message indicating that your function is unknown.

"""
<name>Math</name>
<tags>Data Manipulation</tags>
"""
from OWRpy import * 
import redRGUI 
from libraries.base.signalClasses.RDataFrame import RDataFrame as redRRDataFrame
from libraries.base.qtWidgets.button import button
from libraries.base.qtWidgets.groupBox import groupBox
from libraries.base.qtWidgets.widgetLabel import widgetLabel
from libraries.base.qtWidgets.dialog import dialog
from libraries.base.qtWidgets.filterTable import filterTable as redRfilterTable
from libraries.base.qtWidgets.lineEdit import lineEdit
from libraries.base.qtWidgets.listBox import listBox
from libraries.base.qtWidgets.widgetBox import widgetBox
import redRi18n
_ = redRi18n.get_(package = 'base')
class mathWidget(OWRpy): 
    settingsList = []
    def __init__(self, parent=None, signalManager=None):
        OWRpy.__init__(self)
        
        self.setRvariableNames(['math'])
        
        self.counter = 1
        self.functionsList = ['log2', 'log10', 'add', 'subtract', 'multiply', 'divide', 'match', 'as.numeric', 'as.character', 'exp', 'logicAND', 'logicOR', 'toDateTime (MDY)', 'toDateTime (DMY)', 'toDateTime (YMD)']
        
        self.inputs.addInput('id0', _('Data Frame'), redRRDataFrame, self.gotData)

        self.outputs.addOutput('id0', _('Data Frame'), redRRDataFrame)

        #GUI#
        
        mainArea = widgetBox(self.controlArea, orientation = 'horizontal')
        leftArea = groupBox(mainArea, label = _('Table View'))
        rightArea = groupBox(mainArea, label = _('Math Box'))
        
        self.table = redRfilterTable(leftArea,label= _('Data Table'), displayLabel=False,
        filterable=False,sortable=False)
        
        self.functionLineEdit = lineEdit(rightArea, label = _('Function Search or Run'), 
        callback = self.functionDone)
        QObject.connect(self.functionLineEdit, SIGNAL('textChanged(const QString&)'), 
        lambda s: self.textChanged(s))
        
        self.functionListBox = listBox(rightArea, label= _('List of Functions'),displayLabel=False,
        includeInReports=False,
        items = self.functionsList, callback = self.funcionPressed)
        
        #self.helpButton = button(rightArea, label = 'Help') #, toolTip = 'Press this then select a function from the list for help.')
        self.dialog = dialog(self)
        self.dialogTopArea = groupBox(self.dialog, label = _('Left Side'))
        self.dialogTopLineEdit = lineEdit(self.dialogTopArea, label = _('Constant'), toolTip = _('Must be a number'))
        self.dialogTopListBox = listBox(self.dialogTopArea, label = _('Columns'), toolTip = _('Select one of the columns'), callback = self.dialogTopLineEdit.clear)
        
        self.dialogLabel = widgetLabel(self.dialog)
        
        self.dialogBottomArea = groupBox(self.dialog, label = _('Right Side'))
        self.dialogBottomLineEdit = lineEdit(self.dialogBottomArea, label = _('Constant'), 
        toolTip = _('Must be a number'))
        self.dialogBottomListBox = listBox(self.dialogBottomArea, label = _('Columns'), 
        toolTip = _('Select one of the columns'), callback = self.dialogBottomLineEdit.clear)
        redRCommitButton(self.dialog, label = _('Done'), callback = self.functionCommit)
        self.dialog.hide()
    def gotData(self, data):
        if data:
            self.R(self.Rvariables['math'] + '<-' + data.getData(), wantType = 'NoConversion')
            self.data = self.Rvariables['math']
            self.table.setRTable(data.getData())
            self.dialogBottomListBox.update(self.R('colnames('+self.data+')', wantType = 'list'))
            self.dialogTopListBox.update(self.R('colnames('+self.data+')', wantType = 'list'))
        else:
            self.table.clear()
            
    def textChanged(self, s):
        print s
        self.functionListBox.scrollToItem(self.functionListBox.findItems(s, Qt.MatchStartsWith)[0])
        
    def functionDone(self):
        text = unicode(self.functionLineEdit.text())
        self.executeFunction(text)
        
    def funcionPressed(self):
        text = unicode(self.functionListBox.selectedItems()[0].text())
        self.executeFunction(text)
        
    def executeFunction(self, text):
        if text in ['log10', 'log2', 'as.numeric', 'as.character', 'exp']:
            self.dialogBottomArea.hide()
            self.dialog.show()
        else:
            self.dialogBottomArea.show()
            self.dialog.show()
        self.dialogLabel.setText(text)
    def functionCommit(self):
        try:
            if unicode(self.dialogTopLineEdit.text()) != '':
                topText = unicode(self.dialogTopLineEdit.text())
                try:
                    a = float(topText)
                except:
                    self.status.setText(_('Top Text Area Does Not Contain A Number'))
                    return 
            else:
                topText = self.data+'$'+unicode(self.dialogTopListBox.selectedItems()[0].text())
                
            if self.dialogBottomArea.isVisible():
                if unicode(self.dialogBottomLineEdit.text()) != '':
                    bottomText = unicode(self.dialogBottomLineEdit.text())
                    try:
                        if unicode(self.dialogLabel.text()) not in ['match']:
                            a = float(bottomText)
                    except:
                        self.status.setText(_('Top Text Area Does Not Contain A Number'))
                        return
                else:
                    bottomText = self.data+'$'+unicode(self.dialogBottomListBox.selectedItems()[0].text())
                    
            function = unicode(self.dialogLabel.text())
            
            if function in ['log10', 'log2', 'as.numeric', 'as.character', 'exp']:
                try:
                    self.R(self.data+'$'+function+unicode(self.counter)+'<-'+function+'('+topText+')', wantType = 'NoConversion')
                    self.table.setRTable(self.data)
                    self.counter += 1
                except:
                    self.status.setText(_('An error occured in your function'))
            elif function in ['toDateTime (MDY)', 'toDateTime(YMD)', 'toDateTime(DMY)']:
                if function == 'toDateTime (MDY)':
                    self.R(self.data+'$dateAsMDY'+unicode(self.counter)+'<-strptime('+topText+', "%m/%d/%y")', wantType = 'NoConversion')
                elif function == 'toDateTime (YMD)':
                    self.R(self.data+'$dateAsMDY'+unicode(self.counter)+'<-strptime('+topText+', "%y/%m/%d")', wantType = 'NoConversion')
                elif function == 'toDateTime (DMY)':
                    self.R(self.data+'$dateAsMDY'+unicode(self.counter)+'<-strptime('+topText+', "%d/%m/%y")', wantType = 'NoConversion')
            elif function in ['match']:
                try:
                    self.R(self.data+'$'+function+unicode(self.counter)+'<-'+function+'('+topText+', '+bottomText+')', wantType = 'NoConversion')
                    self.table.setRTable(self.data)
                    self.counter += 1
                except:
                    self.status.setText(_('An error occured in your function'))
            else:
                if function == 'add':
                    try:
                        self.R(self.data+'$'+'plus_'+unicode(self.counter)+'<-'+topText+' + '+bottomText, wantType = 'NoConversion')
                        self.table.setRTable(self.data)
                    except:
                        self.status.setText(_('An error occured in your function'))
                elif function == 'subtract':
                    try:
                        self.R(self.data+'$'+'minus_'+unicode(self.counter)+'<-'+topText+' - '+bottomText, wantType = 'NoConversion')
                        self.table.setRTable(self.data)
                    except:
                        self.status.setText(_('An error occured in your function'))
                elif function == 'multiply':
                    try:
                        self.R(self.data+'$'+'times_'+unicode(self.counter)+'<-as.numeric('+topText+') * as.numeric('+bottomText+')', wantType = 'NoConversion')
                        self.table.setRTable(self.data)
                    except:
                        self.status.setText(_('An error occured in your function'))
                elif function == 'divide':
                    try:
                        self.R(self.data+'$'+'divide_'+unicode(self.counter)+'<-as.numeric('+topText+') / as.numeric('+bottomText+')', wantType = 'NoConversion')
                        self.table.setRTable(self.data)
                    except:
                        self.status.setText(_('An error occured in your function'))
                elif function == 'logicAND':
                    try:
                        self.R(self.data+'$'+'logic_AND'+unicode(self.counter)+'<-'+topText+'&'+bottomText, wantType = 'NoConversion')
                    except:
                        self.status.setText(_('An error occured in your function'))
                elif function == 'logicOR':
                    try:
                        self.R(self.data+'$'+'logic_OR'+unicode(self.counter)+'<-'+topText+'|'+bottomText, wantType = 'NoConversion')
                    except:
                        self.status.setText(_('An error occured in your function'))
                self.counter += 1
            self.dialogBottomListBox.update(self.R('colnames('+self.data+')', wantType = 'list'))
            self.dialogTopListBox.update(self.R('colnames('+self.data+')', wantType = 'list'))
            newData = redRRDataFrame(data = self.data, parent = self.data)
            self.rSend("id0", newData)
            self.dialog.hide()
        except:
            self.status.setText(_('An error occured in your function'))