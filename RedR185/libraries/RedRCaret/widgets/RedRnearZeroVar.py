"""
<name>nearZeroVar</name>
<author>Generated using Widget Maker written by Kyle R. Covington</author>
<description></description>
<RFunctions>caret:nearZeroVar</RFunctions>
<tags>Prototypes</tags>
<icon></icon>
"""
from OWRpy import * 
from libraries.base.qtWidgets.lineEdit import lineEdit as redRlineEdit 
from libraries.base.qtWidgets.radioButtons import radioButtons as redRradioButtons 
from libraries.base.qtWidgets.comboBox import comboBox as redRcomboBox 
from libraries.base.qtWidgets.checkBox import checkBox as redRcheckBox 
from libraries.base.qtWidgets.textEdit import textEdit as redRtextEdit 
import libraries.base.signalClasses as signals

class RedRnearZeroVar(OWRpy): 
	settingsList = []
	def __init__(self, parent=None, signalManager=None):
		OWRpy.__init__(self)
		self.setRvariableNames(["nearZeroVar"])
		self.data = {}
		self.RFunctionParam_x = ''
		self.inputs.addInput("x", "x", signals.RArbitraryList.RArbitraryList, self.processx)
		self.outputs.addOutput("nearZeroVar Output","nearZeroVar Output", signals.RArbitraryList.RArbitraryList)
		
		self.RFunctionParamfreqCut_lineEdit = redRlineEdit(self.controlArea, label = "freqCut:", text = '95/5')
		self.RFunctionParamuniqueCut_lineEdit = redRlineEdit(self.controlArea, label = "uniqueCut:", text = '10')
		redRCommitButton(self.bottomAreaRight, "Commit", callback = self.commitFunction)
	def processx(self, data):
		if not self.require_librarys(["caret"]):
			self.status.setText('R Libraries Not Loaded.')
			return
		if data:
			self.RFunctionParam_x=data.getData()
			#self.data = data
			self.commitFunction()
		else:
			self.RFunctionParam_x=''
	def commitFunction(self):
		if unicode(self.RFunctionParam_x) == '': return
		injection = []
		if unicode(self.RFunctionParamfreqCut_lineEdit.text()) != '':
			string = 'freqCut='+unicode(self.RFunctionParamfreqCut_lineEdit.text())+''
			injection.append(string)
		if unicode(self.RFunctionParamuniqueCut_lineEdit.text()) != '':
			string = 'uniqueCut='+unicode(self.RFunctionParamuniqueCut_lineEdit.text())+''
			injection.append(string)
		inj = ''.join(injection)
		self.R(self.Rvariables['nearZeroVar']+'<-nearZeroVar(x='+unicode(self.RFunctionParam_x)+','+inj+')')
		newData = signals.RArbitraryList.RArbitraryList(data = self.Rvariables["nearZeroVar"]) # moment of variable creation, no preexisting data set.  To pass forward the data that was received in the input uncomment the next line.
		#newData.copyAllOptinoalData(self.data)  ## note, if you plan to uncomment this please uncomment the call to set self.data in the process statemtn of the data whose attributes you plan to send forward.
		self.rSend("nearZeroVar Output", newData)