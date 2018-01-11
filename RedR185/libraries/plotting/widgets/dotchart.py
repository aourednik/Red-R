"""
<name>Dot Chart</name>
<author>Generated using Widget Maker written by Kyle R. Covington</author>
<RFunctions>graphics:dotchart</RFunctions>
<tags>Plotting</tags>
<icon>plot.png</icon>
"""
from OWRpy import * 
import redRGUI 
from libraries.base.signalClasses.RMatrix import RMatrix as redRRMatrix
from libraries.base.signalClasses.RList import RList as redRList
from libraries.base.qtWidgets.comboBox import comboBox
from libraries.base.qtWidgets.lineEdit import lineEdit
from libraries.base.qtWidgets.button import button
from libraries.base.qtWidgets.commitButton import commitButton as redRCommitButton

class dotchart(OWRpy): 
    globalSettingsList = ['commit']
    def __init__(self, parent=None, signalManager=None):
        OWRpy.__init__(self)
        self.setRvariableNames(["dotchart"])
        self.data = {}
        self.RFunctionParam_x = ''
        self.labels = ''
        self.inputs.addInput('id0', 'Data', redRRMatrix, self.processx)
        self.inputs.addInput('id1', 'Labels', redRList, self.processLabels)
        
        self.standardTab = self.controlArea
        
        self.RFunctionParammain_lineEdit =  lineEdit(self.standardTab,  label = "Main Title:")
        self.RFunctionParamxlab_lineEdit =  lineEdit(self.standardTab,  label = "X Label:")
        self.RFunctionParamylab_lineEdit =  lineEdit(self.standardTab,  label = "Y Label:")
        self.labelNames = comboBox(self.standardTab, label = 'Label Data')
        self.commit = redRCommitButton(self.bottomAreaRight, "Commit", callback = self.commitFunction,
        processOnInput=True)

    def processx(self, data):
        if not self.require_librarys(["graphics"]):
            self.status.setText('R Libraries Not Loaded.')
            return
        if data:
            self.RFunctionParam_x=data.getData()
            #self.data = data
            if self.commit.processOnInput():
                self.commitFunction()
                
        else:
            self.RFunctionParam_x=''
    def processLabels(self, data):
        if data:
            self.labels = data.getData()
            self.labelNames.update(self.R('names('+self.labels+')'))
            self.commitFunction()
        else:
            self.labels = ''
            self.labelNames.clear()
    def commitFunction(self):
        if unicode(self.RFunctionParam_x) == '': return
        if not self.R('is.numeric('+unicode(self.RFunctionParam_x)+')'):
            self.status.setText('Data is not a numberic matrix, please remove text columns and process again')
            return
        injection = []
        if unicode(self.RFunctionParamxlab_lineEdit.text()) != '':
            string = ',xlab=\"'+unicode(self.RFunctionParamxlab_lineEdit.text())+'\"'
            injection.append(string)
        if self.labels != '':
            injection.append('labels = '+self.labels + '$' + unicode(self.labelNames.currentText()))
        if unicode(self.RFunctionParamylab_lineEdit.text()) != '':
            string = ',ylab=\"'+unicode(self.RFunctionParamylab_lineEdit.text())+'\"'
            injection.append(string)
        if unicode(self.RFunctionParammain_lineEdit.text()) != '':
            string = ',main=\"'+unicode(self.RFunctionParammain_lineEdit.text())+'\"'
            injection.append(string)
        inj = ''.join(injection)
        self.Rplot('dotchart(x='+unicode(self.RFunctionParam_x)+inj+')')
        
    def getReportText(self, fileDir):
        if unicode(self.RFunctionParam_x) == '': return 'Nothing to plot from this widget'
        
        self.R('png(file="'+fileDir+'/plot'+unicode(self.widgetID)+'.png")')
            
        injection = []
        if unicode(self.RFunctionParamxlab_lineEdit.text()) != '':
            string = 'xlab='+unicode(self.RFunctionParamxlab_lineEdit.text())+''
            injection.append(string)
        if unicode(self.labels) != '':
            string = 'labels='+self.labels+ '$' + unicode(self.labelNames.currentText())
            injection.append(string)
        if unicode(self.RFunctionParamylab_lineEdit.text()) != '':
            string = 'ylab='+unicode(self.RFunctionParamylab_lineEdit.text())+''
            injection.append(string)
        if unicode(self.RFunctionParammain_lineEdit.text()) != '':
            string = 'main='+unicode(self.RFunctionParammain_lineEdit.text())+''
            injection.append(string)
        inj = ','.join(injection)
        self.R('dotchart(x='+unicode(self.RFunctionParam_x)+','+inj+')')
        self.R('dev.off()')
        text = 'The following plot was generated:\n\n'
        #text += '<img src="plot'+unicode(self.widgetID)+'.png" alt="Red-R R Plot" style="align:center"/></br>'
        text += '.. image:: '+fileDir+'/plot'+unicode(self.widgetID)+'.png\n    :scale: 50%%\n\n'
            
        return text
