"""
<name>aaa</name>
<tags>Plotting</tags>
<icon>plot.png</icon>
"""
from OWRpy import * 
import redRGUI
from libraries.base.signalClasses.RVariable import RVariable as redRRVariable
from libraries.plotting.signalClasses.RPlotAttribute import RPlotAttribute as redRRPlotAttribute

from libraries.base.qtWidgets.lineEdit import lineEdit
from libraries.base.qtWidgets.button import button
from libraries.base.qtWidgets.widgetBox import widgetBox
from libraries.base.qtWidgets.commitButton import commitButton as redRCommitButton
#from libraries.plotting.qtWidgets.graphicsView2 import graphicsView2 as redRGraphicsView
from libraries.base.qtWidgets.SearchDialog import SearchDialog

class aplot(OWRpy): 
    globalSettingsList= ['commit']
    def __init__(self, parent=None, signalManager=None):
        OWRpy.__init__(self)
        self.data = None
        self.RFunctionParam_x = ''
        self.plotAttributes = {}
        self.saveSettingsList = ['plotArea', 'data', 'RFunctionParam_x', 'plotAttributes']
        self.inputs.addInput('id0', 'x', redRRVariable, self.processx)

        # self.R('data <- iris')
        # self.RFunctionParam_x = 'data'
        self.data = 'iris'
        self.plotArea = graphicsView2(self.controlArea,label='Plot', displayLabel=False)
        self.plotArea.hideTab('Points/Lines')
        
        self.plotArea.setCustomPlot(self.updatePlot)
        
        self.plotControls = self.plotArea.createTab('Barplot')
        imageBox = self.plotArea.createControlGroup('Barplot',label='Barplot')
        
        self.namesCombo = comboBox(imageBox,label='Group Name')
        self.heightCombo = listBox(self.plotControls,label='Heights',selectionMode=QAbstractItemView.ExtendedSelection)
        
        self.commit = redRCommitButton(self.bottomAreaRight, "Commit", callback = self.commitFunction,
        processOnInput=True)
        
        
    def show(self):
        OWRpy.show(self)
        self.namesCombo.update(self.R('colnames(iris)'))
        self.heightCombo.update(self.R('colnames(iris)'))
        
        # self.plotArea.plot(query = 'iris$Sepal.Width', function='barplot', data = 'iris')
    def processx(self, data):
        if data:
            self.data = data
            self.RFunctionParam_x=data.getData()
            if self.commit.processOnInput():
                self.commitFunction()
        else:
            self.clearPlots()
    def updatePlot(self):
        injection = []
        injection.append('names.arg = %s$%s' % (self.data,self.namesCombo.currentId()))
        injection.append('height = %s[,c("%s")]' % (self.data, '","'.join(self.heightCombo.selectedIds())))
        self.plotArea.plot(query = ','.join(injection), function='barplot', data = self.data)    
    def commitFunction(self):
        self.updatePlot()
        #if self.RFunctionParam_y == '': return
        # if self.RFunctionParam_x == '': return
        # injection = []
        # if unicode(self.RFunctionParam_main.text()) != '':
            # injection.append('main = "'+unicode(self.RFunctionParam_main.text())+'"')
        # if injection != []:
            # inj = ','+','.join(injection)
        # else: inj = ''
        # injection.append('names.arg = %s$%s' % (self.data,self.namesCombo.currentId()))
        # injection.append('height = %s[,c("%s")]' % (self.data, '","'.join(self.heightCombo.selectedIds())))
        
        # self.plotArea.plot(query = ','.join(injection), function='barplot', data = self.data)
    def getReportText(self, fileDir):
        ## print the plot to the fileDir and then send a text for an image of the plot
        if self.RFunctionParam_x != '':
            self.R('png(file="'+fileDir+'/plot'+unicode(self.widgetID)+'.png")')
            if self.RFunctionParam_x == '': return 'Nothing to plot from this widget'
            injection = []
            if unicode(self.RFunctionParam_main.text()) != '':
                injection.append('main = "'+unicode(self.RFunctionParam_main.text())+'"')
            if injection != []:
                inj = ','+','.join(injection)
            else: inj = ''

            self.R('plot('+unicode(self.RFunctionParam_x)+inj+')')
            for name in self.plotAttributes.keys():
                if self.plotAttributes[name] != None:
                    self.R(self.plotAttributes[name])
            self.R('dev.off()')
            text = 'The following plot was generated:\n\n'
            #text += '<img src="plot'+unicode(self.widgetID)+'.png" alt="Red-R R Plot" style="align:center"/></br>'
            text += '.. image:: '+fileDir+'/plot'+unicode(self.widgetID)+'.png\n    :scale: 50%%\n\n'
        else:
            text = 'Nothing to plot from this widget'
            
        return text
    def clearPlots(self):
        self.plotArea.clear()

        
## redRGUI Graphics View.  A graphics view used for graphing R graphs, this should be as general as possible with an eye to some degree of automation in assignment of items.  

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSvg import *
from redRGUI import widgetState
from libraries.base.qtWidgets.widgetBox import widgetBox
from libraries.base.qtWidgets.groupBox import groupBox
from libraries.base.qtWidgets.comboBox import comboBox
from libraries.base.qtWidgets.lineEdit import lineEdit 
from libraries.base.qtWidgets.widgetLabel import widgetLabel 
from libraries.base.qtWidgets.button import button
from libraries.base.qtWidgets.tabWidget import tabWidget
from libraries.base.qtWidgets.listBox import listBox
from libraries.base.qtWidgets.spinBox import spinBox
from libraries.base.qtWidgets.textEdit import textEdit
from libraries.base.qtWidgets.checkBox import checkBox
import RSession, redREnviron, datetime, os, time
    

class graphicsView2(QGraphicsView, widgetState):
    def __init__(self, parent,label=None, displayLabel=True,includeInReports=True, name = '', data = None):
        ## want to init a graphics view with a new graphics scene, the scene will be accessable through the widget.
        widgetState.__init__(self,parent,label,includeInReports)
        
        QGraphicsView.__init__(self, self.controlArea)
        # if displayLabel:
            # self.controlArea = groupBox(parent,label=label, orientation='vertical')
        # else:
            # self.controlArea = widgetBox(parent,orientation='vertical')
        
        #self.controlArea = widgetBox(parent)
        self.topArea = widgetBox(self.controlArea,
        sizePolicy = QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Maximum),includeInReports=False)
        self.middleArea = widgetBox(self.controlArea)
        self.bottomArea = widgetBox(self.controlArea,includeInReports=False)
        
        self.middleArea.layout().addWidget(self)  # place the widget into the parent widget
        scene = QGraphicsScene()
        self.setScene(scene)
        self.parent = parent
        self.data = data
        
        self.widgetSelectionRect = None
        self.mainItem = None
        self.query = ''
        self.function = 'plot'
        self.layers = []
        self.image = 'plot'+unicode(time.time()) # the base file name without an extension
        self.imageFileName = ''
        self.currentScale = 1
        self.customPlotFunction = None
        self.controlGroups = {}
        self.tabs = {}
    ################################
    ####   Themes              #####
    ################################
        
        
        self.options = {
            'device': {
                'Rcall': 'Cairo',
                'parameters': {
                    'type':{
                            'default':'svg',
                            'qtWidget': 'imageType'
                        }
                    ,'dpi':{
                            'default':'75',
                            'qtWidget': 'dpi'
                        }
                    ,'bg': {
                            'default':'#FFFFFF', 
                            'color': '#FFFFFF',
                            'qtWidget':'bgColor'
                            
                            }
                    ,'height': {
                            'default':400, 
                            'qtWidget': 'dheight'
                            }
                    ,'width': {
                            'default':400, 
                            'qtWidget': 'dwidth'
                            }
                    ,'units': {
                            'default':'px', 
                            'qtWidget': 'units'
                            }
                    }
                }
            ,'main': {
                'Rcall': 'plot',
                'parameters': {
                    'col': {
                        'default':None, 
                        'qtWidget':'colorSeries',
                        'series': '',
                        'seriesLen': 0,
                        'getFunction': self.getColorSeries,
                        'setFunction': self.setColorSeries,
                        }
                    ,'lty': {
                        'default':None, 
                        'qtWidget':'linesListBox',
                        'getFunction': self.getLineTypes,
                        'setFunction': self.setLineTypes,
                        }
                    ,'lwd': {
                        'default':None, 
                        'qtWidget':'lineWidth'
                        }
                    ,'pch': {
                        'default':None, 
                        'qtWidget':'pointListBox',
                        'getFunction': self.getLineTypes,
                        'setFunction': self.setLineTypes,
                        }
                    ,'xlim': {
                        'default':None, 
                        'qtWidget':['xstart','xend'],
                        'getFunction': self.getLimits,
                        'setFunction': self.setLimits,                    
                    }
                    ,'ylim': {
                        'default':None, 
                        'qtWidget':['ystart','yend'],
                        'getFunction': self.getLimits,
                        'setFunction': self.setLimits,                    
                    }
                }
            },
            'title': {
                'Rcall': 'title',
                'parameters': {
                    'main': {
                          'default':"Title", 
                          'qtWidget':'mainTitle' 
                          }
                    ,'xlab': {
                        'default':"XLab", 
                        'qtWidget':'xLab'
                        }
                    ,'ylab': {
                        'default':"YLab", 
                        'qtWidget':'yLab'
                        }   
                    ,'col.main': {
                          'default':'#000000', 
                          'qtWidget':'titleColor' 
                          }
                    ,'col.sub': {
                          'default':'#000000', 
                          'qtWidget':'subColor' 
                          }
                    ,'col.lab': {
                          'default':'#000000', 
                          'qtWidget':'labColor' 
                          }                        
                }
            },
            'par': {
                'Rcall':'par',
                'parameters': {
                    'cex.axis': {
                          'default':1, 
                          'qtWidget':'axisFont' 
                          }
                    ,'cex.lab': {
                          'default':1, 
                          'qtWidget':'labFont' 
                          }
                    ,'cex': {
                          'default':1, 
                          'qtWidget':'plotFont' 
                          }
                    ,'cex.main': {
                          'default':1, 
                          'qtWidget':'mainFont' 
                          }
                    ,'cex.sub': {
                          'default':1, 
                          'qtWidget':'subFont' 
                          }
                    ,'col.axis': {
                          'default':'#000000', 
                          'qtWidget':'axisColor' 
                          }
                    # ,'family': {
                          # 'default':'serif', 
                          # 'qtWidget':'fontCombo' 
                          # }
                }
            }
        }
        # ,'fg' : None
        # ,'legendNames' : None
        # ,'legendLocation' : "'bottomleft'"
        # }
        
        self.optionWidgets = {}
        self.colorList = ['#000000', '#ff0000', '#00ff00', '#0000ff']       


    ################################
    ####   Setup Tabs          #####
    ################################
        self.graphicOptionsButton = button(self.topArea,label='Graphic Options',
        toggleButton = True,callback=self.displayGraphicOptions)
        self.graphicOptionsWidget = widgetBox(self.topArea)
        self.tabWidget = tabWidget(self.graphicOptionsWidget)
        self.tabWidget.setFixedHeight(180)
        hbox = widgetBox(self.graphicOptionsWidget,orientation='horizontal',alignment= Qt.AlignLeft)
        self.resizeCheck = checkBox(hbox,label='resize',displayLabel=False,buttons={'true':'Resize Image'},setChecked='true')
        button(hbox,label='Update Graphic', alignment=Qt.AlignLeft, callback=self.updatePlot)
        
        self.createTab('General')
        self.createTab('Points/Lines')
        self.createTab('Advanced')

    ################################
    ####   Advanced Tabs       #####
    ################################
        imageBox = self.createControlGroup('Advanced',label='Image Properties')
        self.optionWidgets['extrasLineEdit'] = lineEdit(imageBox, label = 'Advanced plotting parameters', 
        orientation='horizontal',
        toolTip = 'Add extra parameters to the main plot.\nPlease see documentation for more details about parameters.')
        
        self.optionWidgets['onlyAdvanced'] = checkBox(imageBox,
        buttons=['Only use the advanced options here'],
        label='advancedOnly',displayLabel=False)

    ################################
    ####   First Tabs          #####
    ################################
        imageBox = self.createControlGroup('General',label='Image Properties')
        # imageBox = groupBox(firstTab,label='Image Properties', orientation='vertical',
        # sizePolicy = QSizePolicy(QSizePolicy.Maximum ,QSizePolicy.Minimum))
        
        self.optionWidgets['imageType'] = comboBox(imageBox,label='Image Type',items=['svg','png'])
        self.optionWidgets['imageType'].setSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.Minimum)
        
        hbox = widgetBox(imageBox,orientation='horizontal')
        self.optionWidgets['dheight'] = spinBox(hbox, label = 'Height', min = 1, max = 5000, value = 400)
        self.optionWidgets['dwidth'] = spinBox(hbox, label = 'Width', min = 1, max = 5000, value = 400)
        hbox = widgetBox(imageBox,orientation='horizontal')
        self.optionWidgets['units'] = comboBox(hbox,label='units',items=[('px','Pixel'),('in','Inches')])
        self.optionWidgets['dpi'] = comboBox(hbox,label='DPI',items=['75','100','150','auto'],editable=True)
        
        
        labelBox = self.createControlGroup('General',label='Labels')
        
        self.optionWidgets['mainTitle'] = lineEdit(labelBox,label='Main Title')
        self.optionWidgets['xLab'] = lineEdit(labelBox,label='X Axis Label')        
        self.optionWidgets['yLab'] = lineEdit(labelBox,label='Y Axis Label')

        
        fontBox = self.createControlGroup('General',label='Sizes')
        fontColumnBox = widgetBox(fontBox,orientation='horizontal')
        fontColumn1 = widgetBox(fontColumnBox,orientation='vertical')
        fontColumn2 = widgetBox(fontColumnBox,orientation='vertical')
        
        #self.optionWidgets['fontCombo'] = comboBox(fontColumn1, items = ['serif', 'sans', 'mono'], label='Font Family')
        
        self.optionWidgets['lineWidth'] = spinBox(fontColumn1,label='Point/Line Size',decimals=2,min=1,max=50)
        self.optionWidgets['plotFont'] = spinBox(fontColumn1, label = 'Plot Text Size',decimals=2, min = 1, max = 50)
        self.optionWidgets['axisFont'] = spinBox(fontColumn1, label = 'Axis Text Size',decimals=2, min = 1, max = 50)
        self.optionWidgets['mainFont'] = spinBox(fontColumn2, label = 'Title Text Size',decimals=2, min = 1, max = 50)
        self.optionWidgets['subFont'] = spinBox(fontColumn2, label = 'Subtitle Text Size',decimals=2, min = 1, max = 50)
        self.optionWidgets['labFont'] = spinBox(fontColumn2, label = ' XY Label Text Size',decimals=2, min = 1, max = 50)
        
        limitBox = self.createControlGroup('General',label='Limits')
        col2Box = widgetBox(limitBox,orientation='horizontal')
        column1 = widgetBox(col2Box,orientation='vertical')
        column2 = widgetBox(col2Box,orientation='vertical')

        self.optionWidgets['xstart'] = lineEdit(column1,label='X Start', width=40)
        self.optionWidgets['xend'] = lineEdit(column2,label='X End', width=40)
        self.optionWidgets['ystart'] = lineEdit(column1,label='Y Start', width=40)
        self.optionWidgets['yend'] = lineEdit(column2,label='Y End', width=40)
        

    
    ################################
    ####   Second Tabs         #####
    ################################
        colorBox = self.createControlGroup('Points/Lines',label='Colors')
        hbox = widgetBox(colorBox,orientation='horizontal')

        self.optionWidgets['colorSeries'] = comboBox(hbox,label='Generate Colors Series',orientation='vertical',
        items = ['select','rainbow','heat.colors','terrain.colors','topo.colors','cm.colors'])
        self.optionWidgets['colorSeriesLen'] = spinBox(hbox,label='Length of Series',displayLabel=False, min=0, max=500)
        hbox.layout().setAlignment(self.optionWidgets['colorSeriesLen'].controlArea, Qt.AlignBottom)
        
        self.optionWidgets['bgColor'] = ColorIcon(colorBox,label='Background')

        #self.optionWidgets['customColors'] = button(colorBox,label='Custom Plot Colors',callback=self.setPlotColors)
        colorBox2 = self.createControlGroup('Points/Lines',label='More Colors')
        
        # colorColumnBox = widgetBox(colorBox2,orientation='horizontal')
        # colorColumn1 = widgetBox(colorColumnBox,orientation='vertical')
        # colorColumn2 = widgetBox(colorColumnBox,orientation='vertical')
      
         
        self.optionWidgets['titleColor'] = ColorIcon(colorBox2,label='Title')
        self.optionWidgets['subColor'] = ColorIcon(colorBox2,label='Subtitle')
        self.optionWidgets['labColor'] = ColorIcon(colorBox2,label='Subtitle')
        self.optionWidgets['axisColor'] = ColorIcon(colorBox2,label='Axis')
        
        lineBox = self.createControlGroup('Points/Lines',label='Lines')
       
        self.optionWidgets['linesListBox'] = listBox(lineBox, label = 'Line types', displayLabel=False,
        selectionMode = QAbstractItemView.ExtendedSelection,
        items = [(1,'________'), (2,'- - - -'), (3,'........'), (4,'_._._._.'), 
        (5,'__ __ __'), (6,'__.__.__.')])
        
        
        
        pointBox = self.createControlGroup('Points/Lines',label='Points')
        
        items = []
        for i in range(1,26):
            items.append((i-1,QListWidgetItem(QIcon(os.path.join(redREnviron.directoryNames['picsDir'],
            'R icon (%d).png' %i)),'')))
        
        for i in range(32,128):
            items.append((i-1,'%s' % (chr(i))))
            
        self.optionWidgets['pointListBox'] = listBox(pointBox, label = 'Line types', displayLabel=False,
        selectionMode = QAbstractItemView.ExtendedSelection, items = items)
        


        self.setTheme(self.options)
    ################################
    ### right click menu     #######
    ################################
        self.menu = QMenu(self)
        save = self.menu.addMenu('Save As')
        save.addAction('Bitmap')
        save.addAction('PDF')
        save.addAction('Post Script')
        save.addAction('JPEG')
        self.menu.addAction('Copy')
        self.menu.addAction('Fit In Window')
        self.menu.addAction('Zoom Out')
        self.menu.addAction('Zoom In')
        self.menu.addAction('Undock')
        self.menu.addAction('Redock')
        
        self.dialog = QDialog()
        self.dialog.setWindowTitle('Red-R Graphics View' + name)
        self.dialog.setLayout(QHBoxLayout())
        
        self.standardImageType = 'svg'
        QObject.connect(self.dialog, SIGNAL('finished(int)'), self.dialogClosed)



    def createTab(self,label):
        a = self.tabWidget.createTabPage(label)
        b = widgetBox(a,orientation='horizontal',alignment=Qt.AlignLeft | Qt.AlignTop)
        self.tabs[label] = b
        self.controlGroups[label] = {}
        return b
    def createControlGroup(self,tab,label):
        imageBox = groupBox(self.tabs[tab],label=label, orientation='vertical',
        sizePolicy = QSizePolicy(QSizePolicy.Maximum ,QSizePolicy.Minimum))
        self.controlGroups[label] = imageBox
        return imageBox
    def hideTab(self,label):
        for x in range(len(self.tabs.keys())):
            if self.tabWidget.tabText(x) == label:
                self.tabWidget.removeTab(x)
                return
    def showTab(self,label):
        self.tabWidget.insertTab(-1,self.tabs[label],label)
    def hideControlGroup(self,label):
        self.controlGroups[label].hide()
    def showControlGroup(self,label):
        self.controlGroups[label].show()
        
    ################################
    #### Plot Option Widgets   #####
    ################################
    
    def displayGraphicOptions(self):
        if self.graphicOptionsButton.isChecked():
            self.graphicOptionsWidget.show()
        else:
            self.graphicOptionsWidget.hide()
    
    def setTheme(self,options):
        for Rcall,parameters in self.options.items():
            for k,v in parameters['parameters'].items():
                #call function to collect data  
                if 'setFunction' in v.keys():
                    v['setFunction'](self.options[Rcall]['parameters'][k])
                else:
                    self.setOptions(self.options[Rcall]['parameters'][k])
        
        
    ################################
    ####  Tab Actions         #####
    ################################
    
    def setPlotColors(self):
        colorDialog = colorListDialog(data = self.data)
        colorDialog.setColors(self.colorList)
        colorDialog.exec_()
        self.options['col']['value'] = 'c('+','.join([unicode(a) for a in colorDialog.listOfColors])+')'
        self.colorList = colorDialog.listOfColors
        if self.options['col']['value'] == 'c()':
           self.options['col']['value'] = 'c("#FFFFFF")'
        colorDialog.hide()

    def setColorSeries(self,options):
        self.optionWidgets['colorSeries'].setCurrentId(options['series'])
        self.optionWidgets['colorSeriesLen'].setValue(options['seriesLen'])
        
    def getColorSeries(self,options):
        #print options
        if self.optionWidgets['colorSeries'].currentId() == 'select':
            options['value'] = None
        else:
            series = self.optionWidgets['colorSeries'].currentId()
            options['value'] = '%s(%d)' % (series,self.optionWidgets['colorSeriesLen'].value())
    
    def setOptions(self,options):
        if 'default' not in options.keys() or options['default'] == None: return
        
        qtWidget = self.optionWidgets[options['qtWidget']]
        if isinstance(qtWidget,ColorIcon):
            qtWidget.color = options['default']
            qtWidget.updateColor()
        elif isinstance(qtWidget,lineEdit):
            qtWidget.setText(options['default'])
        elif isinstance(qtWidget,comboBox):
            qtWidget.setCurrentId(options['default'])
        elif isinstance(qtWidget,spinBox):
            qtWidget.setValue(options['default'])
            
    def updateOptions(self,options):
        qtWidget = self.optionWidgets[options['qtWidget']]
        
        if isinstance(qtWidget,ColorIcon):
            options['value'] = "'%s'" % self.optionWidgets[options['qtWidget']].color
        if isinstance(qtWidget,lineEdit):
            #if qtWidget.text() =='': return
            try:
                options['value'] = "%f" % float(qtWidget.text())
            except:
                options['value'] = "'%s'" % qtWidget.text()
        elif isinstance(qtWidget,comboBox):
            if qtWidget.currentId() =='': 
                options['value'] = None
                return 
            try:
                options['value'] = "%f" % float(qtWidget.currentId())
            except:
                options['value'] = "'%s'" % qtWidget.currentId()
                
        elif isinstance(qtWidget,spinBox):
            if qtWidget.value() =='':
                options['value'] = None
                return 

            options['value'] = qtWidget.value()
    
    def getLimits(self,options):
        start = self.optionWidgets[options['qtWidget'][0]].text()
        end = self.optionWidgets[options['qtWidget'][1]].text()
        options['value'] = 'c(%s,%s)' % (start,end)
    def setLimits(self,options):
        pass
    def getLineTypes(self,options):
        qtWidget = self.optionWidgets[options['qtWidget']]
        # print qtWidget.selectedIds()
        if len(qtWidget.selectedIds()):
            options['value'] = 'c('+','.join([unicode(x) for x in qtWidget.selectedIds()])+')'
        
    def setLineTypes(self,options):
        if 'default' not in options.keys() or options['default'] == None: return
        qtWidget = self.optionWidgets[options['qtWidget']]
        qtWidget.setSelectedIds(options['default'])
        
    ##############################
    ### Plotting #################\
    ##############################
    def _setLegend(self):
        ## we want to make a legend that will appear on the plot.  legend(x, y = NULL, legend, fill = NULL, col = par("col"),
                   # border="black", lty, lwd, pch,
                   # angle = 45, density = NULL, bty = "o", bg = par("bg"),
                   # box.lwd = par("lwd"), box.lty = par("lty"), box.col = par("fg"),
                   # pt.bg = NA, cex = 1, pt.cex = cex, pt.lwd = lwd,
                   # xjust = 0, yjust = 1, x.intersp = 1, y.intersp = 1,
                   # adj = c(0, 0.5), text.width = NULL, text.col = par("col"),
                   # merge = do.lines && has.pch, trace = FALSE,
                   # plot = TRUE, ncol = 1, horiz = FALSE, title = NULL,
                   # inset = 0, xpd, title.col = text.col)
        if not self._legendNames:
            self.parent.status.setText('No legend names specified. Can\'t make the legend')
        function = 'legend(x=\''+self._legendLocation+'\', legend = '+self._legendNames
        if self._col:
            function += ', col = '+self._col
        if self._lty:
            function += ', lty = '+self._lty
        if self._lwd:
            function += ', lwd = '+self._lwd
        if self._pch:
            function += ', pch = '+self._pch
        function += ')'
        self.R(function)
    def setLegendNames(self, parameter):
        ## sets the legend to plot the names as the set parameter.  This can come from either a call to the widget through it's own interface or through the widget.
        self._legendNames = parameter
    def _setLegendLocation(self, location):
        self._legendLocation = location
    def _getParameters(self):
        # import pprint
        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(self.options)

        injection = {}
        for Rcall,parameters in self.options.items():
            injection[Rcall] = []
            for k,v in parameters['parameters'].items():
                #call function to collect data  
                if 'getFunction' in v.keys():
                    v['getFunction'](self.options[Rcall]['parameters'][k])
                else:
                    self.updateOptions(self.options[Rcall]['parameters'][k])
                print Rcall,k
                if 'value' in v.keys() and v['value'] not in [None,'']:
                    injection[Rcall].append('%s = %s' % (k,v['value']))
            
        # pp.pprint(self.options)            
        return injection            
        
    def _startRDevice(self, parameters):
        if imageType not in ['svg', 'png', 'jpeg']:
            imageType = 'png'
        
        # fileName = redREnviron.directoryNames['tempDir']+'/plot'+unicode(self.widgetID).replace('.', '_')+'.'+imageType
        # fileName = fileName.replace('\\', '/')
        self.imageFileName = unicode(self.image).replace('\\', '/')+'.'+unicode(imageType)
        file = unicode(os.path.join(redREnviron.directoryNames['tempDir'], self.imageFileName).replace('\\', '/'))
        # print '###################### filename' , self.imageFileName
        if imageType == 'svg':
            self.require_librarys(['Cairo'])
            self.R('CairoSVG(file="%s",%s)' % ( file, ','.join(parameters)))
            
        if imageType == 'png':
            self.R('png(file="%s",%s)' % ( file, ','.join(parameters)))

        elif imageType == 'jpeg':
            self.R('jpeg(file="%s",%s)' % ( file, ','.join(parameters)))
                
    def plot(self, query, function = 'plot', parameters=None,data=None):
        ## performs a quick plot given a query and an imageType
        self.data = data
        self.function = function
        self.query = query
        self.layers = []
           
        self.plotMultiple()
    def setCustomPlot(self,plotFun):
        self.customPlotFunction = plotFun
    def updatePlot(self):
        if self.customPlotFunction:
            self.customPlotFunction()
        else:
            self.plotMultiple()
            
    def plotMultiple(self):
        ## performs plotting using multiple layers, each layer should be a query to be executed in RSession
        self.parameters = self._getParameters()
        # import pprint
        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(self.parameters)

        #self._startRDevice(self.parameters['device'])
        self.require_librarys(['Cairo'])
        
        self.imageFileName = unicode(self.image)+'.'+unicode(self.options['device']['parameters']['type']['value'][1:-1])
        file = unicode(os.path.join(redREnviron.directoryNames['tempDir'], self.imageFileName).replace('\\', '/'))

        self.R('Cairo(onefile=F, file="%s",%s,%s)' % ( file, ','.join(self.parameters['device']), ','.join(self.parameters['par'])))
        self.R('par(%s)' % (','.join(self.parameters['par'])))
        
        
        self.extras = ','.join(self.parameters['main'])
        if unicode(self.optionWidgets['extrasLineEdit'].text()) != '':
            self.extras += ', '+unicode(self.optionWidgets['extrasLineEdit'].text())
        if self.extras != '':
            fullquery = '%s(%s, %s)' % (self.function, self.query, self.extras)
        else:
            fullquery = '%s(%s)' % (self.function, self.query)
        
        try:
            self.R(fullquery)
            self.R('title(%s)' % (','.join(self.parameters['title'])))
            # if len(self.layers) > 0:
                # for l in self.layers:
                    # self.R(l)
            # if self.legend:
                # self._setLegend()
        except Exception as inst:
            self.R('dev.off()') ## we still need to turn off the graphics device
            print 'Plotting exception occured'
            raise Exception(unicode(inst))
            
        self.R('dev.off()')
        self.clear()
        self.addImage(file)
        self.fitInView(self.mainItem.boundingRect(), Qt.KeepAspectRatio)
    def resizeEvent(self,ev):
        if self.mainItem and 'true' in self.resizeCheck.getCheckedIds():
            self.fitInView(self.mainItem.boundingRect(), Qt.KeepAspectRatio)
        
    def setExtrasLineEditEnabled(self, enabled = True):
        
        self.extrasLineEdit.enabled(enabled)
        if enabled:
            self.extrasLineEdit.show()
        else:
            self.extrasLineEdit.hide()
    def printMe(self):
        printer = QPrinter()
        printDialog = QPrintDialog(printer)
        if printDialog.exec_() == QDialog.Rejected: 
            print 'Printing Rejected'
            return
        painter = QPainter(printer)
        self.scene().render(painter)
        painter.end()    
    

    #########################
    ## R session functions ##
    #########################
    def R(self, query):
        return RSession.Rcommand(query = query)
    def require_librarys(self, libraries):
        return RSession.require_librarys(libraries)
        
    ##########################
    ## Interaction Functions #
    ##########################
    def clear(self):
        if self.scene():
            self.scene().clear()
        else:
            print 'loading scene'
            scene = QGraphicsScene()
            self.setScene(scene)
    def dialogClosed(self, int):
        self.backToParent()

    def toClipboard(self):
        QApplication.clipboard().setImage(self.returnImage())
    def saveAsPDF(self):
        print 'save as pdf'
        qname = QFileDialog.getSaveFileName(self, "Save Image", redREnviron.directoryNames['documentsDir'] + "/Image-"+unicode(datetime.date.today())+".pdf", "PDF Document (.pdf)")
        if qname.isEmpty(): return
        qname = unicode(qname)
        self.saveAs(unicode(qname), 'pdf')
    def saveAsPostScript(self):
        print 'save as post script'
        qname = QFileDialog.getSaveFileName(self, "Save Image", redREnviron.directoryNames['documentsDir'] + "/Image-"+unicode(datetime.date.today())+".eps", "Post Script (.eps)")
        if qname.isEmpty(): return
        qname = unicode(qname)
        self.saveAs(unicode(qname), 'ps')
    def saveAsBitmap(self):
        print 'save as bitmap'
        qname = QFileDialog.getSaveFileName(self, "Save Image", redREnviron.directoryNames['documentsDir'] + "/Image-"+unicode(datetime.date.today())+".bmp", "Bitmap (.bmp)")
        if qname.isEmpty(): return
        qname = unicode(qname)
        self.saveAs(unicode(qname), 'bmp')
    def saveAsJPEG(self):
        print 'save as jpeg'
        qname = QFileDialog.getSaveFileName(self, "Save Image", redREnviron.directoryNames['documentsDir'] + "/Image-"+unicode(datetime.date.today())+".jpg", "JPEG Image (.jpg)")
        if qname.isEmpty(): return
        qname = unicode(qname)
        self.saveAs(unicode(qname), 'jpeg')
    def backToParent(self):
        self.parent.layout().addWidget(self.controlArea)
        self.dialog.hide()
    def mousePressEvent(self, mouseEvent):
        
        if mouseEvent.button() == Qt.RightButton:
            # remove the selection rect
            if self.widgetSelectionRect:
                self.widgetSelectionRect.hide()
                self.widgetSelectionRect = None
            
            # show the action menu
            newCoords = QPoint(mouseEvent.globalPos())
            action = self.menu.exec_(newCoords)
            if action:
                if unicode(action.text()) == 'Copy':
                    self.toClipboard()
                elif unicode(action.text()) == 'Zoom Out':
                    self.scale(0.80, 0.80)
                elif unicode(action.text()) == 'Zoom In':
                    self.scale(1.50, 1.50)
                elif unicode(action.text()) == 'Undock':
                    ## want to undock from the widget and make an independent viewing dialog.
                    self.dialog.layout().addWidget(self.controlArea)
                    self.dialog.show()
                elif unicode(action.text()) == 'Redock':
                    self.parent.layout().addWidget(self.controlArea)
                    self.dialog.hide()
                elif unicode(action.text()) == 'Fit In Window':
                    print self.mainItem.boundingRect()
                    self.fitInView(self.mainItem.boundingRect(), Qt.KeepAspectRatio)
                elif unicode(action.text()) == 'Bitmap':
                    self.saveAsBitmap()
                elif unicode(action.text()) == 'PDF':
                    self.saveAsPDF()
                elif unicode(action.text()) == 'Post Script':
                    self.saveAsPostScript()
                elif unicode(action.text()) == 'JPEG':
                    self.saveAsJPEG()
        else:
            self.mouseDownPosition = self.mapToScene(mouseEvent.pos())
            self.widgetSelectionRect = QGraphicsRectItem(QRectF(self.mouseDownPosition, self.mouseDownPosition), None, self.scene())
            self.widgetSelectionRect.setZValue(-100)
            self.widgetSelectionRect.show()
    def mouseMoveEvent(self, ev):
        point = self.mapToScene(ev.pos())

        if self.widgetSelectionRect:
            self.widgetSelectionRect.setRect(QRectF(self.mouseDownPosition, point))            

        self.scene().update()
    def mouseReleaseEvent(self, ev):
        point = self.mapToScene(ev.pos())
        if self.widgetSelectionRect:
            self.fitInView(self.widgetSelectionRect.rect(), Qt.KeepAspectRatio)
            self.widgetSelectionRect.hide()
            self.widgetSelectionRect = None
            
        self.scene().update()

    def returnImage(self):
        ## generate a rendering of the graphicsView and return the image
        
        size = self.scene().sceneRect().size()
        image = QImage(int(self.scene().width()), int(self.scene().height()), QImage.Format_ARGB32_Premultiplied)
        painter = QPainter(image)
        self.scene().render(painter)
        painter.end()
        return image
        
    def addImage(self, image, imageType = None):
        ## add an image to the view
        #self.image = os.path.abspath(image)
        #print self.image
        # print 'Addign Image'
        if not self.scene():
            # print 'loading scene'
            scene = QGraphicsScene()
            self.setScene(scene)
            print self.image
        if imageType == None:
            imageType = image.split('.')[-1]
        if imageType not in ['svg', 'png', 'jpeg']:
            self.clear()
            print imageType, 'Error occured'
            raise Exception, 'Image type specified is not a valid type for this widget.'
        if imageType == 'svg':
            self.convertSVG(image) ## handle the conversion to glyph free svg
            mainItem = QGraphicsSvgItem(image)
        elif imageType in ['png', 'jpeg']:
            mainItem = QGraphicsPixmapItem(QPixmap(image))
        else:
            raise Exception, 'Image type %s not specified in a plotting method' % imageType
        #print mainItem
        self.scene().addItem(mainItem)
        self.mainItem = mainItem
        
        
    def getSettings(self):
        print '#################in getSettings'
        r = {'image':self.imageFileName, 'query':self.query, 'function':self.function, 'addSettings':self.extrasLineEdit.getSettings()}
        
        print r
        return r
    def loadSettings(self,data):
        # print '@@@@@@@@@@@@@@@@@in loadSettings'
        # print data
        
        self.query = data['query']
        self.function = data['function']
        self.extrasLineEdit.loadSettings(data['addSettings'])
        self.addImage(data['image'])
    def getReportText(self, fileDir):
        
        image = self.returnImage()
        image = image.scaled(1000,1000, Qt.KeepAspectRatio)
        imageFile = os.path.join(fileDir, self.image + '.png').replace('\\', '/')
        if not image.save(imageFile):
            print 'Error in saving image in graphicsView'
            return ''
        
        text = '.. image:: %s\n    :scale: 50%%\n\n' % imageFile
        
        return {self.widgetName:{'includeInReports':self.includeInReports,'text':text}}  
        
    def saveAs(self, fileName, imageType):
        if self.query == '': return
        if imageType == 'pdf':
            self.R('pdf(file = \'%s\')' % fileName.replace('\\', '/'))
        elif imageType == 'ps':
            self.R('postscript(file = \'%s\')' % fileName.replace('\\', '/'))
        elif imageType == 'bmp':
            self.R('bmp(file = \'%s\')' % fileName.replace('\\', '/'))
        elif imageType == 'jpeg':
            self.R('jpeg(file = \'%s\')' % fileName.replace('\\', '/'))
        
        if not self.plotExactlySwitch:
            self.extras = self._setParameters()
            if unicode(self.extrasLineEdit.text()) != '':
                self.extras += ', '+unicode(self.extrasLineEdit.text())
            if self.extras != '':
                fullquery = '%s(%s, %s)' % (self.function, self.query, self.extras)
            else:
                fullquery = '%s(%s)' % (self.function, self.query)
        else:
            fullquery = self.query
        self.R(fullquery)
        for l in self.layers:
            self.R(l)
        
        self.R('dev.off()')

    ###########
    ## Convert an SVG for pyqt
    ###########
    def convertSVG(self, file):
        print file
        dom = self._getsvgdom(file)
        #print dom
        self._switchGlyphsForPaths(dom)
        self._commitSVG(file, dom)
    def _commitSVG(self, file, dom):
        f = open(file, 'w')
        dom.writexml(f)
        f.close()
    def _getsvgdom(self, file):
        print 'getting DOM model'
        import xml.dom
        import xml.dom.minidom as mini
        f = open(file, 'r')
        svg = f.read()
        f.close()
        dom = mini.parseString(svg)
        return dom
    def _getGlyphPaths(self, dom):
        symbols = dom.getElementsByTagName('symbol')
        glyphPaths = {}
        for s in symbols:
            pathNode = [p for p in s.childNodes if 'tagName' in dir(p) and p.tagName == 'path']
            glyphPaths[s.getAttribute('id')] = pathNode[0].getAttribute('d')
        return glyphPaths
    def _switchGlyphsForPaths(self, dom):
        glyphs = self._getGlyphPaths(dom)
        use = self._getUseTags(dom)
        for glyph in glyphs.keys():
            #print glyph
            nl = self.makeNewList(glyphs[glyph].split(' '))
            u = self._matchUseGlyphs(use, glyph)
            for u2 in u:
                #print u2, 'brefore'
                self._convertUseToPath(u2, nl)
                #print u2, 'after'
            
    def _getUseTags(self, dom):
        return dom.getElementsByTagName('use')
    def _matchUseGlyphs(self, use, glyph):
        matches = []
        for i in use:
            #print i.getAttribute('xlink:href')
            if i.getAttribute('xlink:href') == '#'+glyph:
                matches.append(i)
        #print matches
        return matches
    def _convertUseToPath(self, use, strokeD):
        ## strokeD is a list of lists of strokes to make the glyph
        newD = self.nltostring(self.resetStrokeD(strokeD, use.getAttribute('x'), use.getAttribute('y')))
        use.tagName = 'path'
        use.removeAttribute('xlink:href')
        use.removeAttribute('x')
        use.removeAttribute('y')
        use.setAttribute('style', 'fill: rgb(0%,0%,0%); stroke-width: 0.5; stroke-linecap: round; stroke-linejoin: round; stroke: rgb(0%,0%,0%); stroke-opacity: 1;stroke-miterlimit: 10; ')
        use.setAttribute('d', newD)
    def makeNewList(self, inList):
        i = 0
        nt = []
        while i < len(inList):
            start = i + self.listFind(inList[i:], ['M', 'L', 'C', 'Z'])
            end = start + self.listFind(inList[start+1:], ['M', 'L', 'C', 'Z', '', ' '])
            nt.append(inList[start:end+1])
            i = end + 1
        return nt
    def listFind(self, x, query):
        for i in range(len(x)):
            if x[i] in query:
                return i
        return len(x)
    def resetStrokeD(self, strokeD, x, y):
        nsd = []
        for i in strokeD:
            nsd.append(self.resetXY(i, x, y))
        return nsd
    def resetXY(self, nl, x, y): # convert a list of strokes to xy coords
        nl2 = []
        for i in range(len(nl)):
            if i == 0:
                nl2.append(nl[i])
            elif i%2: # it's odd
                nl2.append(float(nl[i]) + float(x))
            elif not i%2: # it's even
                nl2.append(float(nl[i]) + float(y))
            else:
                print i, nl[i], 'error'
        return nl2
    def nltostring(self, nl): # convert a colection of nl's to a string
        col = []
        for l in nl:
            templ = []
            for c in l:
                templ.append(unicode(c))
            templ = ' '.join(templ)
            col.append(templ)
        return ' '.join(col)
        
    
class colorListDialog(QDialog):
    def __init__(self, parent = None, layout = 'vertical', title = 'Color List Dialog', data = ''):
        QDialog.__init__(self, parent)
        self.setWindowTitle(title)
        if layout == 'horizontal':
            self.setLayout(QHBoxLayout())
        else:
            self.setLayout(QVBoxLayout())
        
        self.listOfColors = []
        self.controlArea = widgetBox(self)
        mainArea = widgetBox(self.controlArea, 'horizontal')
        leftBox = widgetBox(mainArea)
        rightBox = widgetBox(mainArea)
        ## GUI
        
        # color list
        self.colorList = listBox(leftBox, label = 'Color List')
        button(leftBox, label = 'Add Color', callback = self.addColor)
        button(leftBox, label = 'Remove Color', callback = self.removeColor)
        button(leftBox, label = 'Clear Colors', callback = self.colorList.clear)
        button(mainArea, label = 'Finished', callback = self.accept)
        # attribute list
        self.attsList = listBox(rightBox, label = 'Data Parameters', callback = self.attsListSelected)
        if data:
            names = self.R('names('+data+')')
            print names
            self.attsList.update(names)
        self.data = data
    def attsListSelected(self):
        ## return a list of numbers coresponding to the levels of the data selected.
        self.listOfColors = self.R('as.numeric(as.factor('+self.data+'$'+unicode(self.attsList.selectedItems()[0].text())+'))')
        
    def addColor(self):
        colorDialog = QColorDialog(self)
        color = colorDialog.getColor()
        colorDialog.hide()
        newItem = QListWidgetItem()
        newItem.setBackgroundColor(color)
        self.colorList.addItem(newItem)
        
        self.processColors()
    def removeColor(self):
        for item in self.colorList.selectedItems():
            self.colorList.removeItemWidget(item)
            
        self.processColors()
    def setColors(self, colorList):
        self.colorList.clear()
        try:
            for c in colorList:
                col = QColor()
                col.setNamedColor(unicode(c))
                newItem = QListWidgetItem()
                newItem.setBackgroundColor(col)
                self.colorList.addItem(newItem)
        except:
            pass # it might happen that we can't show the colors that's not good but also not disasterous either.
    def processColors(self):
        self.listOfColors = []
        for item in self.colorList.items():
            self.listOfColors.append('"'+unicode(item.backgroundColor().name())+'"')
    def R(self, query):
        return RSession.Rcommand(query = query)

class dialog(QDialog):
    def __init__(self, parent, layout = 'vertical',title=None):
        QDialog.__init__(self,parent)
        self.ltys = []
        self.parent = parent
        if title:
            self.setWindowTitle(title)
        if layout == 'horizontal':
            self.setLayout(QHBoxLayout())
        else:
            self.setLayout(QVBoxLayout())


class ColorIcon(QToolButton):
    def __init__(self, parent, label):
        box = widgetBox(parent,orientation='horizontal')       
        a = widgetLabel(box,label=label)
        QToolButton.__init__(self, box)
        box.layout().addWidget(self)
        # if not color:
        self.color = '#000000'
        # else:
            # self.color = color
            
        self.setMaximumSize(20,20)
        self.connect(self, SIGNAL("clicked()"), self.showColorDialog)
        # self.updateColor()

    def updateColor(self):
        pixmap = QPixmap(16,16)
        painter = QPainter()
        painter.begin(pixmap)
        painter.setPen(QPen(QColor(self.color)))
        painter.setBrush(QBrush(QColor(self.color)))
        painter.drawRect(0, 0, 16, 16);
        painter.end()
        self.setIcon(QIcon(pixmap))
        self.setIconSize(QSize(16,16))


    def drawButtonLabel(self, painter):
        painter.setBrush(QBrush(QColor(self.color)))
        painter.setPen(QPen(QColor(self.color)))
        painter.drawRect(3, 3, self.width()-6, self.height()-6)

    def showColorDialog(self):
        color = QColorDialog.getColor(QColor(self.color), self)
        if color.isValid():
            self.color = color.name()
            self.updateColor()
            self.repaint()
