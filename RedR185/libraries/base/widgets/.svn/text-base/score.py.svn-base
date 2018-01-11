"""
<name>Score</name>
<author>Generated using Widget Maker written by Kyle R. Covington, other improvements by Kyle R Covington</author>
<description>Scores samples based on a scoring matrix.  First merges the data by the row names and extracts only those row names that are in the scoring matrix.  Also any NA values are removed prior to scoring.  Several scoring options are available and include; multiplication (values are multiplied and summed to generate a score for every sample for every level of the scoring matrix), correlation (identical to correlation / variance widget).</description>
<RFunctions></RFunctions>
<tags>Data Classification</tags>
<icon>default.png</icon>
"""
from OWRpy import * 
from libraries.base.qtWidgets.lineEdit import lineEdit as redRlineEdit 
from libraries.base.qtWidgets.radioButtons import radioButtons as redRradioButtons 
from libraries.base.qtWidgets.comboBox import comboBox as redRcomboBox 
from libraries.base.qtWidgets.checkBox import checkBox as redRcheckBox 
from libraries.base.qtWidgets.textEdit import textEdit as redRtextEdit 
from libraries.base.qtWidgets.listBox import listBox as redRlistBox
from libraries.base.qtWidgets.spinBox import spinBox as redRspinBox
from libraries.base.qtWidgets.filterTable import filterTable as redRfilterTable
import libraries.base.signalClasses as signals
import redRi18n
_ = redRi18n.get_(package = 'base')
class score(OWRpy): 
    settingsList = []
    def __init__(self, signalManager = None):
        OWRpy.__init__(self)
        
        
        self.setRvariableNames(['score', 'mergedmatrix', 'mergedvals', 'tempmerge'])
        self.data = {}
        self.RFunctionParam_data = ''
        self.RFunctionParam_score = ''
        self.inputs.addInput("data", _("Sample Data"), signals.RDataFrame.RDataFrame, self.processdata)
        self.inputs.addInput("scoremat", _("Scoring Matrix"), signals.RDataFrame.RDataFrame, self.processscores)
        self.outputs.addOutput("fscoremat",_("Sored Samples"), signals.RDataFrame.RDataFrame)
        self.outputs.addOutput("maxScore", _("Max Scored Class"), signals.RVector.RVector)

        wb = redRwidgetBox(self.controlArea, orientation = 'horizontal')
        self.scoremethod = redRcomboBox(wb, label = _('Scoring Method'), items = [_('Multiplication'), _('Correlation')], callback = self.commitFunction)
        redRCommitButton(self.bottomAreaRight, _("Commit"), callback = self.commitFunction)
        self.RoutputWindow = redRfilterTable(wb,label=_('Scores'), displayLabel=False,
            sortable=True,filterable=False)
            
    def processdata(self, data):
        if data:
            self.RFunctionParam_data=data.getData()
            self.commitFunction()
        else:
            self.RFunctionParam_data=''
            
    def processscores(self, data):
        if data:
            self.RFunctionParam_score = data.getData()
            self.commitFunction()
        else:
            self.RFunctionParam_score = ''
    def commitFunction(self):
        if unicode(self.RFunctionParam_data) == '': return
        if unicode(self.RFunctionParam_score) == '': return
        self.RoutputWindow.clear()
        
        ## first merge the data so that the scores and the data are in the same register, this will usually happen on naturally but we can't be sure of that.
        
        self.R('%s<-merge(%s, %s, by.x=0, by.y=0)' % (self.Rvariables['tempmerge'], self.RFunctionParam_score, self.RFunctionParam_data), wantType = 'NoConversion')
        self.R('%s<-%s[,c(\"%s\")]' % (self.Rvariables['mergedvals'], self.Rvariables['tempmerge'], '\",\"'.join(self.R('colnames(%s)' % self.RFunctionParam_data, wantType = 'NoConversion'))), wantType = 'NoConversion')
        self.R('%s<-%s[,c(\"%s\")]' % (self.Rvariables['mergedmatrix'], self.Rvariables['tempmerge'], '\",\"'.join(self.R('colnames(%s)' % self.RFunctionParam_score, wantType = 'NoConversion'))), wantType = 'NoConversion')
        
        ## now make the matrixes
        if unicode(self.scoremethod.currentText()) == _('Multiplication'):
            ## for each col in the samples we need to multiply the cols in the score matrix and save the result.
            self.R(self.Rvariables['score']+'<-as.data.frame(t(data.matrix('+self.Rvariables['mergedmatrix']+')) %*% data.matrix('+ self.Rvariables['mergedvals'] + '))', wantType = 'NoConversion')
            
        elif unicode(self.scoremethod.currentText()) == _('Correlation'):
            # perform cor and show the results
            self.R('%s<-as.data.frame(cor(data.matrix(%s), data.matrix(%s)))' % (self.Rvariables['score'], self.Rvariables['mergedmatrix'], self.Rvariables['mergedvals']), wantType = 'NoConversion')
        self.RoutputWindow.setRTable(self.Rvariables['score'])
        newScores = signals.RDataFrame.RDataFrame(data = self.Rvariables['score'])
        self.rSend('fscoremat', newScores)
            
        
        
        