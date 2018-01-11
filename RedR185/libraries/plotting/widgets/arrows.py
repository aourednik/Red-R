"""
<name>Arrow</name>
<tags>Plot Attributes</tags>
<icon>plot.png</icon>
"""
from OWRpy import * 
import redRGUI 
from libraries.plotting.signalClasses.RPlotAttribute import RPlotAttribute as redRRPlotAttribute
from libraries.base.qtWidgets.lineEdit import lineEdit
from libraries.base.qtWidgets.button import button
class arrows(OWRpy): 
    globalSettingsList = ['commit']
    def __init__(self, parent=None, signalManager=None):
        OWRpy.__init__(self)
        self.setRvariableNames(["arrows"])
        self.data = {}
        self.outputs.addOutput('id0', 'arrows Output', redRRPlotAttribute)

        self.standardTab = self.controlArea
        self.RFunctionParamx0_lineEdit =  lineEdit(self.standardTab,  label = "x0:", text = '')
        self.RFunctionParamy0_lineEdit =  lineEdit(self.standardTab,  label = "y0:", text = '')
        
        self.RFunctionParamx1_lineEdit =  lineEdit(self.standardTab,  label = "x1:", text = '')
        self.RFunctionParamy1_lineEdit =  lineEdit(self.standardTab,  label = "y1:", text = '')
        self.RFunctionParamcode_lineEdit =  lineEdit(self.standardTab,  label = "code:", text = '1')
        self.commit = redRCommitButton(self.bottomAreaRight, "Commit", callback = self.commitFunction)
    def commitFunction(self):
        if unicode(self.RFunctionParamx0_lineEdit.text()) == '':
            self.status.setText('No x0 specified')
            return
        if unicode(self.RFunctionParamx1_lineEdit.text()) == '':
            self.status.setText('No x1 specified')
            return
        if unicode(self.RFunctionParamy0_lineEdit.text()) == '':
            self.status.setText('No y0 specified')
            return
        if unicode(self.RFunctionParamy1_lineEdit.text()) == '':
            self.status.setText('No y1 specified')
            return
        injection = []
        if unicode(self.RFunctionParamy1_lineEdit.text()) != '':
            string = 'y1='+unicode(self.RFunctionParamy1_lineEdit.text())+''
            injection.append(string)
        if unicode(self.RFunctionParamy0_lineEdit.text()) != '':
            string = 'y0='+unicode(self.RFunctionParamy0_lineEdit.text())+''
            injection.append(string)
        if unicode(self.RFunctionParamx0_lineEdit.text()) != '':
            string = 'x0='+unicode(self.RFunctionParamx0_lineEdit.text())+''
            injection.append(string)
        if unicode(self.RFunctionParamcode_lineEdit.text()) != '':
            string = 'code='+unicode(self.RFunctionParamcode_lineEdit.text())+''
            injection.append(string)
        if unicode(self.RFunctionParamx1_lineEdit.text()) != '':
            string = 'x1='+unicode(self.RFunctionParamx1_lineEdit.text())+''
            injection.append(string)
        inj = ','.join(injection)
        
        newData = redRRPlotAttribute(data = 'arrows('+inj+')')# moment of variable creation, no preexisting data set.  To pass forward the data that was received in the input uncomment the next line.
        #newData.copyAllOptinoalData(self.data)  ## note, if you plan to uncomment this please uncomment the call to set self.data in the process statemtn of the data whose attributes you plan to send forward.
        self.rSend("id0", newData)
    def getReportText(self, fileDir):
        return 'This widget places arrows on existing plots by sending a plot attribute.  Please see those plots for more information about the arrows that were displayed.\n\n'
