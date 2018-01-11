"""
<name>Scatterplot</name>
<tags>Plotting, Subsetting</tags>
<icon>scatterplot.png</icon>
"""

from OWRpy import *
import OWGUI
import redRGUI 
import re
import textwrap
from libraries.base.signalClasses.RDataFrame import RDataFrame as redRRDataFrame

from PyQt4.QtGui import *

from libraries.base.qtWidgets.checkBox import checkBox
from libraries.plotting.qtWidgets.redRGraph import redRGraph
from libraries.base.qtWidgets.comboBox import comboBox
from libraries.base.qtWidgets.button import button
from libraries.base.qtWidgets.textEdit import textEdit
from libraries.base.qtWidgets.groupBox import groupBox
from libraries.base.qtWidgets.separator import separator
from libraries.base.qtWidgets.widgetBox import widgetBox
from libraries.base.qtWidgets.zoomSelectToolbar import zoomSelectToolbar

class RedRScatterplot(OWRpy):
    globalSettingsList = ['commitOnInput', 'plotOnInput']
    def __init__(self, parent=None, signalManager=None):

        OWRpy.__init__(self)
        self.setRvariableNames(['Plot','paint','selected'])
        self.inputs.addInput('id0', 'x', redRRDataFrame, self.gotX)

        self.outputs.addOutput('id0', 'Scatterplot Output', redRRDataFrame)

        self.data = None
        self.parent = None
        self.dataParent = None
        
        # GUI
        area = widgetBox(self.controlArea,orientation='horizontal')
        
        options= widgetBox(area,orientation='vertical')
        options.setMaximumWidth(250)
        # options.setMinimumWidth(250)
        options.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        dataSelection = groupBox(options,orientation='vertical')
        self.xColumnSelector = comboBox(dataSelection, label = 'X data', items=[],callback=self.onSourceChange)
        self.yColumnSelector = comboBox(dataSelection, label = 'Y data', items=[],callback=self.onSourceChange)
        self.paintCMSelector = comboBox(dataSelection, label = 'Color Points By:', items = [''],callback=self.onSourceChange)
        
        # plot area
        plotarea = groupBox(area, label = "Graph")
        plotarea.setSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.MinimumExpanding)
        #plotarea.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.graph = redRGraph(plotarea,label='Scatter Plot', displayLabel=False,
        onSelectionCallback=self.onSelectionCallback)

        #plotarea.layout().addWidget(self.graph)
        #self.zoomSelectToolbarBox = groupBox(self.GUIDialog, label = "Plot Tool Bar")
        
        separator(options,height=8)
        buttonBox = groupBox(options,orientation='vertical')
        
        box1 = widgetBox(buttonBox,orientation='horizontal')
        box1.layout().setAlignment(Qt.AlignRight)
        self.plotOnInput = checkBox(box1, label='commit', displayLabel=False,
        buttons = ['Plot on Change'],
        toolTips = ['Whenever X, Y or color data source changes plot the results.'])
        button(box1, label = "Plot", callback = self.plot, toolTip = 'Plot the data.')
        
        box2 = widgetBox(buttonBox,orientation='horizontal')  
        box2.layout().setAlignment(Qt.AlignRight)
        
        self.commitOnInput = checkBox(box2, label='commit', displayLabel=False,
        buttons = ['Commit on Selection'],
        toolTips = ['Whenever this selection changes, send data forward.'])
        button(box2, label = "Select", callback = self.sendMe, toolTip = 'Subset the data according to your selection.')

        separator(options,height=8)
        self.zoomSelectToolbar = zoomSelectToolbar(self, options, self.graph)
        self.paintLegend = textEdit(options,label='Legend')
        
        # self.R('data <- data.frame(a=rnorm(1000),b=rnorm(1000))')
        # data = redRRDataFrame(data = 'data', parent = None) 
        # self.graph.resize(350, 350)
        # self.gotX(data)
        
        
    def showSelected(self):
        if self.data == None:
            self.status.setText('No Data')
            return
            
        xData = self.data.getData()[unicode(self.xColumnSelector.currentText())]
        yData = self.data.getData()[unicode(self.yColumnSelector.currentText())]
        selected, unselected = self.graph.getSelectedPoints(xData = xData, yData = yData)
        
        ## use the selected and unselected lists to generate the new dict.
        newData = {}
        for key in self.data.getData().keys():
            newData[key] = []
            for i in range(len(selected)):
                if selected[i]:
                    newData[key].append(self.data.getData()[key][i])
                    
        sendData = signals.StructuredDict(data = newData, parent = self.data.getData(), keys = self.data.getItem('keys'))
        self.rSend("id0", newData)
        self.sendRefresh()
        
    def gotX(self, data):
        if data:
            self.dataParent = data
            self.data = data.getData()
            colnames = self.R('colnames(%s)' % self.data)
            keys = ['']
            keys += colnames
            self.paintCMSelector.update(keys)
            
            ## might be good to limit the user to selecting only those indicies that have numeric values
            self.xColumnSelector.update(colnames)
            self.yColumnSelector.update(colnames)
            self.plot()
        else:
            self.data = None
            self.xData = []
            self.yData = []
            self.graph.clear()
    
    def onSourceChange(self):
        if 'Plot on Change' in self.plotOnInput.getChecked():
            self.plot()
        
    def plot(self, newZoom = True):
        xCol = self.xColumnSelector.currentText()
        yCol = self.yColumnSelector.currentText()
        paintClass = self.paintCMSelector.currentText()
        self.xData = []
        self.yData = []
        if xCol == yCol: return
        self.graph.setXaxisTitle(xCol)
        self.graph.setYLaxisTitle(yCol)
        self.graph.setShowXaxisTitle(True)
        self.graph.setShowYLaxisTitle(True)
        self.graph.clear()
        # there is a paintclass selected so we should paint on the levels of the paintclass
        subset = []
        d = self.data
        self.paintLegend.clear()
        if paintClass in self.R('colnames('+self.data+')'): 
            self.R(self.Rvariables['paint'] + ' <-as.factor('+self.data+'[,\''+paintClass+'\'])')
            levels = self.R('levels('+self.Rvariables['paint']+')', wantType = 'list')
            #print vectorClass
            if len(levels) > 50:
                runMe = QMessageBox.information(None, 'RedRWarning', 'You are asking to paint on more than 50 colors.\nRed-R supports a limited number of colors in this plot widget.\nIt is unlikely that you will be able to interperte this data\nand plotting may take a very long time.\nAre you sure you want to plot this???', QMessageBox.Yes, QMessageBox.No)
                if runMe == QMessageBox.No: return
                
            for level in levels:
                subset.append((level, self.data+'[,\''+paintClass+'\'] == "'+level + '"'))

            if self.R('sum(is.na('+self.data+'[,\''+paintClass+'\']))') > 0:
                subset.append(('NA', 'is.na('+self.data+'[,\''+paintClass+'\'])'))
                levels.append('NA')
        else:
            self.R(self.Rvariables['paint']+'<-TRUE')
            levels = ['ALL']
            subset.append(('ALL','TRUE'))
            
        pc = 0
        xDataClass = self.R('class('+self.data+'[,\''+unicode(xCol)+'\'])', silent = True)
        yDataClass = self.R('class('+self.data+'[,\''+unicode(yCol)+'\'])', silent = True)
        self.paintLegend.insertHtml('<h5>Color Legend</h5>')
        self.paintLegend.insertHtml('<table class="reference" cellspacing="0" border="1" width="100%"><tr><th align="left" width="25%">Color</th><th align="left" width="75%">Group Name</th></tr>')
        for (p, subset) in subset:
            print p
            if p in ['NA','ALL']:
                pc=0
            else:
                pc = levels.index(p)+1
                
            lColor = self.setColor(pc)
            
            self.paintLegend.insertHtml('<tr><td width = "25%" bgcolor="'+lColor+'">&nbsp;</td><td width = "75%">'+p+'</td></tr>')
            # generate the subset
            # check if the column is a factor
            # print '|#| '+unicode(self.forceXNumeric.getChecked())
            
            # if xDataClass in ['factor'] and 'Force Numeric' not in self.forceXNumeric.getChecked():
                # print 'Setting xData as factor'
                # xData = self.R('match('+self.data+'['+subset+',\''+unicode(xCol)+'\'], levels('+self.data+'[,\''+unicode(xCol)+'\']))', wantType = 'list', silent = True)
            # else:
            xData = self.R('as.numeric('+self.data+'['+subset+',\''+unicode(xCol)+'\'])', wantType = 'list')

            # if yDataClass in ['factor'] and 'Force Numeric' not in self.forceYNumeric.getChecked():
                # print 'Setting yData as factor'
                # yData = self.R('match('+self.data+'['+subset+',\''+unicode(yCol)+'\'], levels('+self.data+'[,\''+unicode(yCol)+'\']))', wantType = 'list', silent = True)
            # else:
            yData = self.R('as.numeric('+self.data+'['+subset+',\''+unicode(yCol)+'\'])', wantType = 'list')

            # print xData
            # print yData
            
            if len(xData) == 0 or len(yData) == 0: continue
            self.graph.points("MyData", xData = xData, yData = yData, brushColor = pc, penColor=pc)
            self.xData += xData
            self.yData += yData
        self.paintLegend.insertHtml('</table>')
        
        ## make a fake call to the zoom to repaint the points and to add some interest to the graph
        # if newZoom and 'Reset Zoom On Selection' in self.replotCheckbox.getChecked():
        self.graph.setNewZoom(float(min(self.xData)), float(max(self.xData)), float(min(self.yData)), float(max(self.yData)))
            
        self.graph.replot()
        
    def asNumeric(self, listItems):
        ## convert a list to a numeric list
        newList = []
        for i in listItems:
            try:
                newList.append(float(i))
            except:
                newList.append(None)
                
        return newList
    def onSelectionCallback(self):
        if 'Commit on Selection' in self.commitOnInput.getChecked():
            self.sendMe()
   
    def sendMe(self):
        xCol = unicode(self.xColumnSelector.currentText())
        yCol = unicode(self.yColumnSelector.currentText())

        xData = self.R('as.numeric('+self.data+'[,"'+unicode(xCol)+'"])', wantType = 'list')
        yData = self.R('as.numeric('+self.data+'[,"'+unicode(yCol)+'"])', wantType = 'list')
        
        selected, unselected = self.graph.getSelectedPoints(xData = xData, yData = yData)
        # print selected
        # print unselected
        index = []
        for x in selected:
            if x ==1: index.append('T')
            else: index.append('F')
            
        index = 'c('+','.join(index) + ')'
        self.R('%s<-%s[%s,]' % (self.Rvariables['selected'],self.data,index),silent=True)
        if self.dataParent:
            data = redRRDataFrame(data = self.Rvariables['selected'], parent = self.dataParent.getDataParent()) 
            data.copyAllOptionalData(self.dataParent)
        else:
            data = redRRDataFrame(data = self.Rvariables['selected']) 
        self.rSend("id0", data)
        #self.sendRefresh()
        
    def loadCustomSettings(self, settings = None):
        # custom function to replot the data that is in the scatterplot
        self.plot()
    def setColor(self, colorint):
        # import colorsys
        # N = 50
        # HSV_tuples = [(x*1.0/N, 0.5, 0.5) for x in range(N)]
        # RGB_tuples = map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples)
        # return RGB_tuples[colorint]
        
        if colorint == 0 or colorint == 'FALSE':
            return '#000000'
        elif colorint == 1 or colorint == 'TRUE':
            return '#ff0000'
        elif colorint == 2:
            return '#00ff00'
        elif colorint == 3:
            return '#0000ff'
        elif colorint == 4:
            return '#ffff00'
        elif colorint == 5:
            return '#a0a0a4'
        elif colorint == 6:
            return '#ff00ff'
        elif colorint == 7:
            return '#00ffff'
        elif colorint == 8:
            return '#000080'
        elif colorint == 9:
            return '#800000'
        
        else:
            return self.setColor(colorint - 10) # run back through the levels and reduce by 5, the colors cycle every 5
            
    def getReportText(self, fileDir):
        return 'Please see the Red-R .rrs file or the users notes for more information on how this widget was used.\n\n'