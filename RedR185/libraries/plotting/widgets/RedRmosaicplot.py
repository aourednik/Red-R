"""
<name>mosaicplot</name>
<author>Generated using Widget Maker written by Kyle R. Covington</author>
<description>Generates a mosaic plot given a table whose columns contain labels or factors representing the classes of the rows.  For example; subjects could be classified as male/female and blue/brown/black/green/purple eyecolor.  No continuous data should be sent to this widget and should be removed using a selection widget prior to attaching the signal.</description>
<RFunctions>:mosaicplot</RFunctions>
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

class RedRmosaicplot(OWRpy): 
	settingsList = []
	def __init__(self, parent=None, signalManager=None):
		OWRpy.__init__(self)
		self.RFunctionParam_x = ''
		self.inputs.addInput("x", "x", signals.RDataFrame.RDataFrame, self.processx)
		
		self.RFunctionParammain_lineEdit = redRlineEdit(self.controlArea, label = "Main Title:", text = '')
		self.RFunctionParamxlab_lineEdit = redRlineEdit(self.controlArea, label = "X label:", text = '')
		self.RFunctionParamylab_lineEdit = redRlineEdit(self.controlArea, label = "Y label:", text = '')
		self.plotArea = redRgraphicsView(self.controlArea)
		redRCommitButton(self.bottomAreaRight, "Commit", callback = self.commitFunction)
	def processx(self, data):
		if data:
			self.RFunctionParam_x=data.getData()
			#self.data = data
			self.commitFunction()
		else:
			self.RFunctionParam_x=''
	def commitFunction(self):
		if unicode(self.RFunctionParam_x) == '': return
		injection = []
		if unicode(self.RFunctionParamxlab_lineEdit.text()) != '':
			string = 'xlab=\''+unicode(self.RFunctionParamxlab_lineEdit.text())+'\''
			injection.append(string)
		if unicode(self.RFunctionParamylab_lineEdit.text()) != '':
			string = 'ylab=\''+unicode(self.RFunctionParamylab_lineEdit.text())+'\''
			injection.append(string)
		if unicode(self.RFunctionParammain_lineEdit.text()) != '':
			string = 'main=\''+unicode(self.RFunctionParammain_lineEdit.text())+'\''
			injection.append(string)
		inj = ','.join(injection)
		self.plotArea.plot('x=table('+unicode(self.RFunctionParam_x)+'),'+inj, function = 'mosaicplot')