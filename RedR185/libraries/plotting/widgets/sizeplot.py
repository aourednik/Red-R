"""
<name>Size Plot</name>
<tags>Plotting</tags>
<icon>plot.png</icon>
"""
from OWRpy import * 
import redRGUI 
from libraries.base.signalClasses.RVector import RVector as redRRVector
from libraries.base.qtWidgets.lineEdit import lineEdit
from libraries.base.qtWidgets.tabWidget import tabWidget
from libraries.base.qtWidgets.button import button
from libraries.base.qtWidgets.commitButton import commitButton as redRCommitButton

class sizeplot(OWRpy): 
    globalSettingsList = ['commit']
    def __init__(self, parent=None, signalManager=None):
        OWRpy.__init__(self)
        self.RFunctionParam_y = ''
        self.RFunctionParam_x = ''
        self.inputs.addInput('id0', 'y', redRRVector, self.processy)
        self.inputs.addInput('id1', 'x', redRRVector, self.processx)

        
        self.standardTab = self.controlArea
        self.RFunctionParamy_lineEdit =  lineEdit(self.standardTab,  label = "y:", text = '')
        self.RFunctionParamx_lineEdit =  lineEdit(self.standardTab,  label = "x:", text = '')
        self.RFunctionParamscale_lineEdit =  lineEdit(self.standardTab,  label = "scale:", text = '1')
        self.RFunctionParamsize_lineEdit =  lineEdit(self.standardTab,  label = "size:", text = 'c(1,4)')
        self.RFunctionParampow_lineEdit =  lineEdit(self.standardTab,  label = "pow:", text = '0.5')
        self.commit = redRCommitButton(self.bottomAreaRight, "Commit", callback = self.commitFunction,
        processOnInput=True)
    def processy(self, data):
        if not self.require_librarys(["plotrix"]):
            self.status.setText('R Libraries Not Loaded.')
            return
        if data:
            self.RFunctionParam_y=data.getData()
            #self.data = data
            if self.commit.processOnInput():
                self.commitFunction()
        else:
            self.RFunctionParam_y=''
    def processx(self, data):
        if not self.require_librarys(["plotrix"]):
            self.status.setText('R Libraries Not Loaded.')
            return
        if data:
            self.RFunctionParam_x=data.getData()
            #self.data = data
            if self.commit.processOnInput():
                self.commitFunction()
        else:
            self.RFunctionParam_x=''
    def commitFunction(self):
        if unicode(self.RFunctionParam_y) == '': return
        if unicode(self.RFunctionParam_x) == '': return
        injection = []
        if unicode(self.RFunctionParamy_lineEdit.text()) != '':
            string = 'y='+unicode(self.RFunctionParamy_lineEdit.text())+''
            injection.append(string)
        if unicode(self.RFunctionParamx_lineEdit.text()) != '':
            string = 'x='+unicode(self.RFunctionParamx_lineEdit.text())+''
            injection.append(string)
        if unicode(self.RFunctionParamscale_lineEdit.text()) != '':
            string = 'scale='+unicode(self.RFunctionParamscale_lineEdit.text())+''
            injection.append(string)
        if unicode(self.RFunctionParamsize_lineEdit.text()) != '':
            string = 'size='+unicode(self.RFunctionParamsize_lineEdit.text())+''
            injection.append(string)
        if unicode(self.RFunctionParampow_lineEdit.text()) != '':
            string = 'pow='+unicode(self.RFunctionParampow_lineEdit.text())+''
            injection.append(string)
        inj = ','.join(injection)
        self.Rplot('sizeplot(y='+unicode(self.RFunctionParam_y)+',x='+unicode(self.RFunctionParam_x)+','+inj+')')
        
    def getReportText(self, fileDir):
        if unicode(self.RFunctionParam_y) == '': return 'Nothing to plot from this widget'
        if unicode(self.RFunctionParam_x) == '': return 'Nothing to plot from this widget'
        
        self.R('png(file="'+fileDir+'/plot'+unicode(self.widgetID)+'.png")')
            
        injection = []
        if unicode(self.RFunctionParamy_lineEdit.text()) != '':
            string = 'y='+unicode(self.RFunctionParamy_lineEdit.text())+''
            injection.append(string)
        if unicode(self.RFunctionParamx_lineEdit.text()) != '':
            string = 'x='+unicode(self.RFunctionParamx_lineEdit.text())+''
            injection.append(string)
        if unicode(self.RFunctionParamscale_lineEdit.text()) != '':
            string = 'scale='+unicode(self.RFunctionParamscale_lineEdit.text())+''
            injection.append(string)
        if unicode(self.RFunctionParamsize_lineEdit.text()) != '':
            string = 'size='+unicode(self.RFunctionParamsize_lineEdit.text())+''
            injection.append(string)
        if unicode(self.RFunctionParampow_lineEdit.text()) != '':
            string = 'pow='+unicode(self.RFunctionParampow_lineEdit.text())+''
            injection.append(string)
        inj = ','.join(injection)
        self.R('sizeplot(y='+unicode(self.RFunctionParam_y)+',x='+unicode(self.RFunctionParam_x)+','+inj+')')
        self.R('dev.off()')
        text = 'The following plot was generated:\n\n'
        #text += '<img src="plot'+unicode(self.widgetID)+'.png" alt="Red-R R Plot" style="align:center"/></br>'
        text += '.. image:: '+fileDir+'/plot'+unicode(self.widgetID)+'.png\n    :scale: 50%%\n\n'
            
        return text
