"""
<name>image</name>
<tags>Plotting</tags>
<icon>plot.png</icon>
"""
from OWRpy import * 
import redRGUI 
from libraries.base.signalClasses.RMatrix import RMatrix as redRRMatrix
from libraries.base.qtWidgets.button import button
from libraries.base.qtWidgets.checkBox import checkBox as redRCheckBox

class image(OWRpy): 
    globalSettingsList = ['commitButton']
    def __init__(self, parent=None, signalManager=None):
        OWRpy.__init__(self)
        self.RFunctionParam_x = ''
        self.inputs.addInput('id0', 'x', redRRMatrix, self.processx)

        self.commitButton = redRCommitButton(self.bottomAreaRight, "Commit", callback = self.commitFunction,
        processOnInput=True)
    def processx(self, data):
        if data:
            self.RFunctionParam_x=data.getData()
            if not self.R('is.numeric('+self.RFunctionParam_x+')', silent=True):
                self.status.setText('Data not numeric')
                self.commitButton.setDisabled(True)
                return
            else:
                self.status.setText('')
                self.commitButton.setEnabled(True)
                
            if self.commitButton.processOnInput():
                self.commitFunction()
        else:
            self.RFunctionParam_x=''
    def commitFunction(self):
        if unicode(self.RFunctionParam_x) == '': return
        self.Rplot('image(x='+unicode(self.RFunctionParam_x)+')')
def getReportText(self, fileDir):
        if unicode(self.RFunctionParam_x) == '': return 'Nothing to plot from this widget'
        
        self.R('png(file="'+fileDir+'/plot'+unicode(self.widgetID)+'.png")')
        self.Rplot('image(x='+unicode(self.RFunctionParam_x)+')')
        self.R('dev.off()')
        text = 'The following plot was generated:\n\n'
        #text += '<img src="plot'+unicode(self.widgetID)+'.png" alt="Red-R R Plot" style="align:center"/></br>'
        text += '.. image:: '+fileDir+'/plot'+unicode(self.widgetID)+'.png\n    :scale: 50%%\n\n'
            
        return text
