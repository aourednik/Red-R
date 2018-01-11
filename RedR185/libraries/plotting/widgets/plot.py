"""
<name>Generic Plot</name>
<author>Generated using Widget Maker written by Kyle R. Covington</author>
<description>Generic plot is the basis of most RedR plotting.  This accepts fits, data tables, or other RedR outputs and attempts to plot them.  However, there is no guarantee that your data will plot correctly.</description>
<tags>Plotting</tags>
<icon>plot.png</icon>
<inputWidgets></inputWidgets>
<outputWidgets></outputWidgets>

"""
from OWRpy import * 
from libraries.base.signalClasses.RVariable import RVariable as redRRVariable
from libraries.plotting.signalClasses.RPlotAttribute import RPlotAttribute as redRRPlotAttribute
from libraries.base.qtWidgets.lineEdit import lineEdit
from libraries.base.qtWidgets.button import button
from libraries.base.qtWidgets.graphicsView import graphicsView as redRGraphicsView
from libraries.base.qtWidgets.SearchDialog import SearchDialog
class plot(OWRpy): 
    def __init__(self, parent=None, signalManager=None):
        OWRpy.__init__(self)
        self.data = None
        self.RFunctionParam_x = ''
        self.plotAttributes = {}
        self.saveSettingsList = ['plotArea', 'data', 'RFunctionParam_x', 'plotAttributes']
        self.inputs.addInput('id0', 'x', redRRVariable, self.processx)

        
        box = OWGUI.widgetBox(self.controlArea, "Widget Box")
        self.RFunctionParam_main = lineEdit(box, label = 'Main Title:')
        self.plotArea = redRGraphicsView(self.controlArea)
        redRCommitButton(self.bottomAreaRight, "Commit", callback = self.commitFunction)
        # button(self.bottomAreaRight, 'Inspect Plot', callback = self.InspectPlot)
    # def InspectPlot(self):
        # fn = QFileDialog.getOpenFileName(self, "Open File", '~',
        # "Text file (*.png);; All Files (*.*)")
        # print str(fn)
        # if fn.isEmpty(): return
        # self.plotArea.addImage(str(fn))
    def processx(self, data):
        if data:
            self.data = data
            self.RFunctionParam_x=data.getData()
            self.commitFunction()
        else:
            self.clearPlots()
    def commitFunction(self):
        #if self.RFunctionParam_y == '': return
        if self.RFunctionParam_x == '': return
        injection = []
        if str(self.RFunctionParam_main.text()) != '':
            injection.append('main = "'+str(self.RFunctionParam_main.text())+'"')
        if injection != []:
            inj = ','+','.join(injection)
        else: inj = ''
        
        self.plotArea.plot(query = str(self.RFunctionParam_x)+inj, data = self.RFunctionParam_x)
    
    def clearPlots(self):
        self.plotArea.clear()
