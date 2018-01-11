"""
<name>Heatmap2</name>
<description>Makes heatmaps of data.  This data should be in the form of a data table and should contain only numeric data, no text.  </description>
<tags>Prototypes</tags>
<author>Anup Parikh (anup@red-r.org) and Kyle R Covington (kyle@red-r.org)</author>
<RFunctions>stats:heatmap</RFunctions>
<icon>heatmap.png</icon>
"""

from OWRpy import *
from libraries.base.signalClasses.RMatrix import RMatrix as redRRMatrix

from libraries.base.qtWidgets.separator import separator
from libraries.base.qtWidgets.checkBox import checkBox
from libraries.base.qtWidgets.comboBox import comboBox
from libraries.base.qtWidgets.button import button
from libraries.base.qtWidgets.spinBox import spinBox
from libraries.base.qtWidgets.radioButtons import radioButtons
from libraries.base.qtWidgets.widgetLabel import widgetLabel
from libraries.base.qtWidgets.groupBox import groupBox
from libraries.base.qtWidgets.lineEdit import lineEdit
from libraries.base.qtWidgets.widgetBox import widgetBox
from libraries.base.qtWidgets.graphicsView import graphicsView

class heatmap2(OWRpy):
    globalSettingsList = ['plotOnConnect','imageWidth','imageHeight']
    
    def __init__(self, parent=None, signalManager=None):
        OWRpy.__init__(self)
        
        self.setRvariableNames(['heatsubset'])
        self.plotOnConnect = 0
        self.plotdata = ''
        self.rowvChoice = None
        
        self.inputs.addInput('id0', 'Expression Matrix', redRRMatrix, self.processMatrix)

        
        #GUI
        mainArea = widgetBox(self.controlArea,orientation='horizontal')
        #mainArea.setMaximumWidth(300)
        options = widgetBox(mainArea,orientation='vertical')
        options.setMaximumWidth(175)
        options.setMinimumWidth(175)
        dendrogramsBox = groupBox(options, label='Calculate dendrogram ', orientation='vertical')
        self.notice = widgetLabel(dendrogramsBox,label='The data set has > 1000 rows.\nClustering on rows will likely fail.')
        self.notice.setHidden(True)
        self.dendrogramOptions = checkBox(dendrogramsBox,
        buttons = ['Rows', 'Columns'], setChecked=['Rows', 'Columns'], orientation='horizontal',
        callback=self.dendrogramChanged)
        
        functions = widgetBox(dendrogramsBox,orientation='vertical')
        self.distOptions = lineEdit(functions,label='Distance Function:', text='dist', orientation='vertical')
        self.hclustOptions = lineEdit(functions,label='Clustering Function:',text='hclust', 
        orientation='vertical')
        #self.reorderOptions = lineEdit(functions,label='Reorder Function:', text='reorder.dendrogram')
        
        
        self.scaleOptions = radioButtons(options,label='Scale',  buttons=['row','column','none'],
        setChecked='row',orientation='horizontal')
        
        otherOptions = groupBox(options,label='Other Options')
        self.narmOptions = checkBox(otherOptions, buttons = ['Remove NAs'], setChecked=['Remove NAs'])
        # self.showDendroOptions = checkBox(otherOptions,buttons=['Show dendrogram '], setChecked=['Show dendrogram '])
        
        self.colorTypeCombo = comboBox(otherOptions, label = 'Color Type:', 
        items = ['rainbow', 'heat.colors', 'terrain.colors', 'topo.colors', 'cm.colors'],callback=self.colorTypeChange)
        self.startSaturation = spinBox(otherOptions, label = 'Starting Saturation', min = 0, max = 100)
        self.endSaturation = spinBox(otherOptions, label = 'Ending Saturation', min = 0, max = 100)
        self.endSaturation.setValue(30)
        separator(otherOptions,height=10)

        self.imageWidth = spinBox(otherOptions, label = 'Image Width', min = 1, max = 1000)
        self.imageWidth.setValue(4)
        self.imageHeight = spinBox(otherOptions, label = 'Image Height', min = 1, max = 1000)
        self.imageHeight.setValue(4)
        
        
        self.notice2 = widgetLabel(options,label='The input matrix is not numeric.')
        self.notice2.setHidden(True)
        self.buttonsBox = widgetBox(options,orientation='horizontal')
        self.buttonsBox.layout().setAlignment(Qt.AlignRight)
        self.plotOnConnect = checkBox(self.buttonsBox, buttons=['Plot on Connect'])
        button(self.buttonsBox, label = "Plot", callback=self.makePlot)
        
        
        #self.gview1 = graphicsView(mainArea)
        
    def dendrogramChanged(self):
        if len(self.dendrogramOptions.getChecked()) > 0:
            self.hclustOptions.setEnabled(True)
            self.distOptions.setEnabled(True)
        else:
            self.hclustOptions.setDisabled(True)
            self.distOptions.setDisabled(True)
           
    def colorTypeChange(self):
        if self.colorTypeCombo.currentText() =='rainbow':
            self.startSaturation.setEnabled(True)
            self.endSaturation.setEnabled(True)
        else:
            self.startSaturation.setDisabled(True)
            self.endSaturation.setDisabled(True)
        
    def processMatrix(self, data):
        if not data:
            return 
        self.plotdata = data.getData()
        
        if not self.R('is.numeric(%s)' % self.plotdata):
            self.buttonsBox.setDisabled(True)
            self.notice2.setHidden(False)
        else:
            self.buttonsBox.setEnabled(True)
            self.notice2.setHidden(True)
            
        if self.R('nrow(%s)' % self.plotdata)  >1000:
            self.notice.setHidden(False)
            
            self.dendrogramOptions.setChecked(['Columns']) 
        else:
            self.notice.setHidden(True)
        if 'Plot on Connect'  in self.plotOnConnect.getChecked():
            self.makePlot()

    def makePlot(self):
        if self.plotdata == '': return
        options = {}

        colorType = unicode(self.colorTypeCombo.currentText())
        if colorType == 'rainbow':
            start = float(float(self.startSaturation.value())/100)
            end = float(float(self.endSaturation.value())/100)
            # print start, end
            col = 'rev(rainbow(50, start = '+unicode(start)+', end = '+unicode(end)+'))'
        else:
            col = colorType+'(50)'
        
        options['col'] = col    
        
        if 'Rows' in self.dendrogramOptions.getChecked():
            options['Rowv'] = 'NULL'
        else:
            options['Rowv'] = 'NA'
        if 'Columns' in self.dendrogramOptions.getChecked():
            options['Colv'] = 'NULL'
        else:
            options['Colv'] = 'NA'
            
        options['hclustfun'] = self.hclustOptions.text()
        #options['reorderfun'] = self.reorderOptions.text()
        options['distfun'] = self.distOptions.text()
        
        options['scale'] = '"%s"' % self.scaleOptions.getChecked()
        
        if 'Remove NAs' in self.narmOptions.getChecked():
            options['na.rm'] = 'TRUE'
        else:
            options['na.rm'] = 'FALSE'
        # if 'Show dendrogram' in self.showDendroOptions.getChecked():
            # options['keep.dendro'] = 'TRUE'
        # else:
            # options['keep.dendro'] = 'FALSE'
            
        text = ''
        for k,v in options.items():
            text += '%s=%s,' % (k,v)
        # self.gview1.plot(function = 'heatmap', query = self.plotdata + ',' + text, dwidth=self.imageHeight.value(), dheight=self.imageWidth.value())

        self.R('heatmap(%s, %s)' % (self.plotdata,text), wantType = 'NoConversion')
        
