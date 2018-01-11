"""
<name>plot.mvrVal</name>
<author>Generated using Widget Maker written by Kyle R. Covington</author>
<description></description>
<RFunctions>pls:plot.mvrVal</RFunctions>
<tags>Prototypes</tags>
<icon></icon>
"""
from OWRpy import * 
import redRGUI 
import libraries.base.signalClasses as signals

from libraries.base.qtWidgets.comboBox import comboBox
from libraries.base.qtWidgets.button import button
class RedRplot_mvrVal(OWRpy): 
	settingsList = []
	def __init__(self, parent=None, signalManager=None):
		OWRpy.__init__(self)
		self.RFunctionParam_x = ''
		self.inputs.addInput('id0', 'x', redRRModelFit, self.processx)

		
		self.RFunctionParamtype_comboBox = comboBox(self.controlArea, label = "type:", items = ["'b',both","'l','lines'","'p',points"])
		self.RFunctionParamlegendpos_comboBox = comboBox(self.controlArea, label = "legendpos:", items = ["'topright'","'topleft'","'bottomright'","'bottomleft'"])
		redRCommitButton(self.bottomAreaRight, "Commit", callback = self.commitFunction)
	def processx(self, data):
		if not self.require_librarys(["pls"]):
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
		string = 'type='+unicode(self.RFunctionParamtype_comboBox.currentText()).split(',')[0]+''
		injection.append(string)
		string = 'legendpos='+unicode(self.RFunctionParamlegendpos_comboBox.currentText())+''
		injection.append(string)
		inj = ','.join(injection)
		self.Rplot('plot.mvrVal(x='+unicode(self.RFunctionParam_x)+','+inj+')')
