"""
<name>bumpchart</name>
<tags>Plotting</tags>
<icon>plot.png</icon>
"""
from OWRpy import * 
import redRGUI 
from libraries.base.signalClasses.RDataFrame import RDataFrame as redRRDataFrame
from libraries.base.qtWidgets.lineEdit import lineEdit
from libraries.base.qtWidgets.tabWidget import tabWidget
from libraries.base.qtWidgets.button import button
from libraries.base.qtWidgets.commitButton import commitButton as redRCommitButton
class bumpchart(OWRpy): 
    globalSettingsList = ['commit']
    def __init__(self, parent=None, signalManager=None):
        OWRpy.__init__(self)
        self.RFunctionParam_y = ''
        self.inputs.addInput('id0', 'y', redRRDataFrame, self.processy)

        
        self.RFunctionParammar_lineEdit =  lineEdit(self.controlArea,  label = "mar:", text = 'c(2,8,5,8)')
        self.RFunctionParamlty_lineEdit =  lineEdit(self.controlArea,  label = "lty:", text = '1')
        self.RFunctionParamlabels_lineEdit =  lineEdit(self.controlArea,  label = "labels:", text = 'rownames(y)')
        self.RFunctionParamrank_lineEdit =  lineEdit(self.controlArea,  label = "rank:", text = 'TRUE')
        self.RFunctionParampch_lineEdit =  lineEdit(self.controlArea,  label = "pch:", text = '19')
        self.RFunctionParamtop_labels_lineEdit =  lineEdit(self.controlArea,  label = "top_labels:", text = 'colnames(y)')
        self.RFunctionParamcol_lineEdit =  lineEdit(self.controlArea,  label = "col:", text = 'par("fg")')
        self.RFunctionParamlwd_lineEdit =  lineEdit(self.controlArea,  label = "lwd:", text = '1')
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
    def commitFunction(self):
        if unicode(self.RFunctionParam_y) == '': return
        injection = []
        if unicode(self.RFunctionParammar_lineEdit.text()) != '':
            string = 'mar='+unicode(self.RFunctionParammar_lineEdit.text())+''
            injection.append(string)
        if unicode(self.RFunctionParamlty_lineEdit.text()) != '':
            string = 'lty='+unicode(self.RFunctionParamlty_lineEdit.text())+''
            injection.append(string)
        if unicode(self.RFunctionParamlabels_lineEdit.text()) != '':
            string = 'labels='+unicode(self.RFunctionParamlabels_lineEdit.text())+''
            injection.append(string)
        if unicode(self.RFunctionParamrank_lineEdit.text()) != '':
            string = 'rank='+unicode(self.RFunctionParamrank_lineEdit.text())+''
            injection.append(string)
        if unicode(self.RFunctionParampch_lineEdit.text()) != '':
            string = 'pch='+unicode(self.RFunctionParampch_lineEdit.text())+''
            injection.append(string)
        if unicode(self.RFunctionParamtop_labels_lineEdit.text()) != '':
            string = 'top.labels='+unicode(self.RFunctionParamtop_labels_lineEdit.text())+''
            injection.append(string)
        if unicode(self.RFunctionParamcol_lineEdit.text()) != '':
            string = 'col='+unicode(self.RFunctionParamcol_lineEdit.text())+''
            injection.append(string)
        if unicode(self.RFunctionParamlwd_lineEdit.text()) != '':
            string = 'lwd='+unicode(self.RFunctionParamlwd_lineEdit.text())+''
            injection.append(string)
        inj = ','.join(injection)
        self.R('y<-'+unicode(self.RFunctionParam_y))
        self.R('bumpchart(y='+unicode(self.RFunctionParam_y)+','+inj+')')
    def getReportText(self, fileDir):
        if unicode(self.RFunctionParam_y) == '': return 'Nothing to plot from this widget'
        
        self.R('png(file="'+fileDir+'/plot'+unicode(self.widgetID)+'.png")')
            
        injection = []
        if unicode(self.RFunctionParammar_lineEdit.text()) != '':
            string = 'mar='+unicode(self.RFunctionParammar_lineEdit.text())+''
            injection.append(string)
        if unicode(self.RFunctionParamlty_lineEdit.text()) != '':
            string = 'lty='+unicode(self.RFunctionParamlty_lineEdit.text())+''
            injection.append(string)
        if unicode(self.RFunctionParamlabels_lineEdit.text()) != '':
            string = 'labels='+unicode(self.RFunctionParamlabels_lineEdit.text())+''
            injection.append(string)
        if unicode(self.RFunctionParamrank_lineEdit.text()) != '':
            string = 'rank='+unicode(self.RFunctionParamrank_lineEdit.text())+''
            injection.append(string)
        if unicode(self.RFunctionParampch_lineEdit.text()) != '':
            string = 'pch='+unicode(self.RFunctionParampch_lineEdit.text())+''
            injection.append(string)
        if unicode(self.RFunctionParamtop_labels_lineEdit.text()) != '':
            string = 'top.labels='+unicode(self.RFunctionParamtop_labels_lineEdit.text())+''
            injection.append(string)
        if unicode(self.RFunctionParamcol_lineEdit.text()) != '':
            string = 'col='+unicode(self.RFunctionParamcol_lineEdit.text())+''
            injection.append(string)
        if unicode(self.RFunctionParamlwd_lineEdit.text()) != '':
            string = 'lwd='+unicode(self.RFunctionParamlwd_lineEdit.text())+''
            injection.append(string)
        inj = ','.join(injection)
        self.R('y<-'+unicode(self.RFunctionParam_y))
        self.R('bumpchart(y='+unicode(self.RFunctionParam_y)+','+inj+')')
        self.R('dev.off()')
        text = 'The following plot was generated:\n\n'
        #text += '<img src="plot'+unicode(self.widgetID)+'.png" alt="Red-R R Plot" style="align:center"/></br>'
        text += '.. image:: '+fileDir+'/plot'+unicode(self.widgetID)+'.png\n    :scale: 505%\n\n'
            
        return text
