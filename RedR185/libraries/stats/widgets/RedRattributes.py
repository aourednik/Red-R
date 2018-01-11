"""
<name>Attributes</name>
<author>Generated using Widget Maker written by Kyle R. Covington</author>
<description></description>
<RFunctions>base:attributes</RFunctions>
<tags>Stats</tags>
<icon></icon>
"""
from OWRpy import * 
import redRGUI 
import libraries.base.signalClasses as signals
import libraries.base.signalClasses.RVariable.RVariable as redRRVariable


from libraries.base.qtWidgets.textEdit import textEdit
from libraries.base.qtWidgets.button import button
class RedRattributes(OWRpy): 
	settingsList = []
	def __init__(self, parent=None, signalManager=None):
		OWRpy.__init__(self)
		self.setRvariableNames(["attributes"])
		self.data = {}
		self.RFunctionParam_obj = ''
		self.inputs.addInput('id0', 'obj', redRRVariable, self.processobj)

		
		redRCommitButton(self.bottomAreaRight, "Commit", callback = self.commitFunction)
		self.RoutputWindow = textEdit(self.controlArea, label = "R Output Window")
	def processobj(self, data):
		if not self.require_librarys(["base"]):
			self.status.setText('R Libraries Not Loaded.')
			return
		if data:
			self.RFunctionParam_obj=data.getData()
			#self.data = data
			self.commitFunction()
		else:
			self.RFunctionParam_obj=''
	def commitFunction(self):
		if unicode(self.RFunctionParam_obj) == '': return
		injection = []
		inj = ','.join(injection)
		self.R(self.Rvariables['attributes']+'<-attributes(obj='+unicode(self.RFunctionParam_obj)+','+inj+')')
		self.R('txt<-capture.output('+self.Rvariables['attributes']+')')
		self.RoutputWindow.clear()
		tmp = self.R('paste(txt, collapse ="\n")')
		self.RoutputWindow.insertHtml('<br><pre>'+tmp+'</pre>')
