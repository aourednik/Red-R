## redRGUI Graphics View.  A graphics view used for graphing R graphs, this should be as general as possible with an eye to some degree of automation in assignment of items.  

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSvg import *
from redRGUI import widgetState
from libraries.base.qtWidgets.widgetBox import widgetBox
from libraries.base.qtWidgets.groupBox import groupBox
from libraries.base.qtWidgets.comboBox import comboBox
from libraries.base.qtWidgets.lineEdit import lineEdit 
from libraries.base.qtWidgets.button import button
from libraries.base.qtWidgets.listBox import listBox
from libraries.base.qtWidgets.spinBox import spinBox
import RSession, redREnviron, datetime, os, time
import redRi18n
_ = redRi18n.get_(package = 'base')
class graphicsView(QGraphicsView, widgetState):
    def __init__(self, parent,label=_('Graph'), displayLabel=True,includeInReports=True, name = '', data = None):
        ## want to init a graphics view with a new graphics scene, the scene will be accessable through the widget.
        self.R = RSession.Rcommand
        self.require_librarys = RSession.require_librarys
        widgetState.__init__(self,parent,label,includeInReports)
        
        QGraphicsView.__init__(self, self.controlArea)
        if displayLabel:
            self.controlArea = groupBox(self.controlArea,label=label, orientation='vertical')
        else:
            self.controlArea = widgetBox(self.controlArea,orientation='vertical')
        
        #self.controlArea = widgetBox(parent)
        self.topArea = widgetBox(self.controlArea)
        self.middleArea = widgetBox(self.controlArea)
        self.bottomArea = widgetBox(self.controlArea)
        self.middleArea.layout().addWidget(self)  # place the widget into the parent widget
        scene = QGraphicsScene()
        self.setScene(scene)
        self.parent = self.controlArea
        self.widgetSelectionRect = None
        self.mainItem = None
        self.query = ''
        self.function = 'plot'
        self.data = data
        self.layers = []
        self._bg = None
        self._cex = None
        self._cexAxis = None
        self._cexLab = None
        self._cexMain = None
        self._cexSub = None
        self._col = None
        self._colAxis = None
        self._colMain = None
        self._colSub = None
        self._family = None
        self._fg = None
        self._lty = None
        self._lwd = None
        self._legendNames = None
        self._legendLocation = 'bottomleft'
        self._pch = None
        self.colorList = ['#000000', '#ff0000', '#00ff00', '#0000ff']
        self._replotAfterChange = True
        self._dheight = 4
        self._dwidth = 4
        self.image = 'plot'+unicode(time.time()) # the base file name without an extension
        self.imageFileName = ''
        self.currentScale = 1
        
        ## bottom menu bar
        self.menuBar = QMenuBar(self.bottomArea)
        self.bottomArea.layout().addWidget(self.menuBar)
        
        self.menuParameters = QMenu(_('Parameters'), self)
        colors = self.menuParameters.addMenu(_('Colors'))
        colors.addAction(_('Set Plotting Colors'), self.setPlotColors)
        colors.addAction(_('Set Axis Colors'), self.setAxisColors)
        colors.addAction(_('Set Label Colors'), self.setLabelColors)
        colors.addAction(_('Set Main Title Color'), self.setTitleColors)
        colors.addAction(_('Set Subtitle Color'), self.setSubtitleColors)
        colors.addAction(_('Set Forground Color'), self.setForgroundColors)
        colors.addAction(_('Set Background Color'), self.setBackgroundColors)
        
        font = self.menuParameters.addMenu(_('Font'))
        ffa = font.addMenu(_('Set Font Family'))
        
        legend = self.menuParameters.addMenu(_('Legend'))
        ll = legend.addMenu(_('Legend Location'))
        ll.addAction(_('Set to bottom right'), lambda x = 'bottomright': self._setLegendLocation(x))
        ll.addAction(_('Set to bottom left'), lambda x = 'bottomleft': self._setLegendLocation(x))
        ll.addAction(_('Set to top right'), lambda x = 'topleft': self._setLegendLocation(x))
        ll.addAction(_('Set to top left'), lambda x = 'topright': self._setLegendLocation(x))
        fontComboAction = QWidgetAction(font)
        self.fontCombo = comboBox(None, items = ['serif', 'sans', 'mono'], label='fonts', displayLabel=False,
            #'HersheySerif', 'HersheySans', 'HersheyScript',
            #'HersheyGothicEnglish', 'HersheyGothicGerman', 'HersheyGothicItalian', 'HersheySymbol', 'HersheySansSymbol'], 
            callback = self.setFontFamily)
        fontComboAction.setDefaultWidget(self.fontCombo)
        ffa.addAction(fontComboAction)
        #font.addAction(_('Set Font Magnification'), self.setFontMagnification)
        wb = widgetBox(None)
        self.fontMag = spinBox(wb, label = 'Font Magnification:', min = 0, max = 500, value = 100) #, callback = self.setFontMagnification)
        QObject.connect(self.fontMag, SIGNAL('editingFinished ()'), self.setFontMagnification) ## must define ourselves because the function calls the attribute and this causes an error in Qt
        magAction = QWidgetAction(font)
        magAction.setDefaultWidget(wb)
        font.addAction(magAction)
        
        self.menuParameters.setToolTip(_('Set the parameters of the rendered image.\nThese parameters are standard graphics parameters which may or may not be applicable or rendered\ndepending on the image type and the settings of the plotting widget.'))
        fa = font.addMenu(_('Font Attributes'))
        lines = self.menuParameters.addMenu(_('Lines'))
        lines.addAction(_('Set Line Type'), self.setLineType)
        lines.addAction(_('Set Line Width'), self.setLineWidth)
        points = self.menuParameters.addMenu(_('Points'))
        points.addAction(_('Set Point Characters'), self.setPointCharacters)
        
        self.imageParameters = QMenu(_('Image'), self)
        type = self.imageParameters.addMenu(_('Type'))
        type.addAction(_('Set Image Vector Graphics'), self.setImageSVG).setToolTip(_('Renders the image using vector graphics which are scaleable and zoomable,\nbut may not show all graphical options such as forground color changes.'))
        type.addAction(_('Set Image Bitmap Graphics'), self.setImagePNG).setToolTip(_('Redners the image using bitmap graphics which will become distorted on zooming,\nbut will show all graphical options.'))
        #type.addAction(_('Set Image JPEG'), self.setImageJPEG)
        type.setToolTip(_('Changes the plotting type of the rendered image.\nDifferent image types may enable or disable certain graphics parameters.'))
        
        self.fileParameters = QMenu(_('File'), self)
        save = self.fileParameters.addMenu(_('Save'))
        save.addAction(_('Bitmap'), self.saveAsBitmap)
        save.addAction(_('PDF'), self.saveAsPDF)
        save.addAction(_('Post Script'), self.saveAsPostScript)
        save.addAction(_('JPEG'), self.saveAsJPEG)
        
        printScene = self.fileParameters.addAction(_('Print'), self.printMe)
        
        self.menuBar.addMenu(self.fileParameters)
        self.menuBar.addMenu(self.menuParameters)
        #self.menuBar.addMenu(self.imageParameters)
        
        ### lower Line Edit
        self.extrasLineEdit = lineEdit(self.bottomArea, label = _('Advanced plotting parameters'), 
            toolTip = _('Add extra parameters to the main plot.\nPlease see documentation for more details about parameters.'), callback = self.replot)
        
        ### right click menu
        self.menu = QMenu(self)
        save = self.menu.addMenu(_('Save As'))
        save.addAction(_('Bitmap'))
        save.addAction(_('PDF'))
        save.addAction(_('Post Script'))
        save.addAction(_('JPEG'))
        self.menu.addAction(_('Copy'))
        self.menu.addAction(_('Fit In Window'))
        self.menu.addAction(_('Zoom Out'))
        self.menu.addAction(_('Zoom In'))
        self.menu.addAction(_('Undock'))
        self.menu.addAction(_('Redock'))
        self.dialog = QDialog()
        self.dialog.setWindowTitle(_('Red-R Graphics View') + name)
        self.dialog.setLayout(QHBoxLayout())
        
        self.standardImageType = 'svg'
        self.plotExactlySwitch = False ## a switch that can be activated to allow plotting exactly as the plot is sent, no function generation will be performed and all attribute alteration will be disabled
        QObject.connect(self.dialog, SIGNAL('finished(int)'), self.dialogClosed)
    ################################
    ####  Menu Actions         #####
    ################################
    def dialogClosed(self, int):
        self.backToParent()
    def setImageSVG(self):
        self.setStandardImageType('svg')
    def setImagePNG(self):
        self.setStandardImageType('png')
    def setImageJPEG(self):
        self.setStandardImageType('jpeg')
    def setStandardImageType(self, it):
        self.standardImageType = it
    def setPlotColors(self):
        colorDialog = colorListDialog(data = self.data)
        colorDialog.setColors(self.colorList)
        colorDialog.exec_()
        self._col = 'c('+','.join([unicode(a) for a in colorDialog.listOfColors])+')'
        self.colorList = colorDialog.listOfColors
        if self._col == 'c()':
            self._col = 'c("#FFFFFF")'
        colorDialog.hide()
        if self._replotAfterChange:
            self.replot()
    def setAxisColors(self):
        colorDialog = QColorDialog(self)
        self._colAxis = unicode(colorDialog.getColor().name())
        colorDialog.hide()
        if self._replotAfterChange:
            self.replot()
    def setBackgroundColors(self):
        colorDialog = QColorDialog(self)
        self._bg = unicode(colorDialog.getColor().name())
        colorDialog.hide()
        if self._replotAfterChange:
            self.replot()
    def setExtrasLineEditEnabled(self, enabled):
        if enabled:
            self.extrasLineEdit.show()
        else:
            self.extrasLineEdit.hide()
    def setFontFamily(self):
        self._family = unicode(self.fontCombo.currentText())
        if self._replotAfterChange:
            self.replot()
    def setFontMagnification(self):
        print self.fontMag.value()
        print float(self.fontMag.value())/100
        if float(self.fontMag.value())/100 > 0:
            self._cex = float(self.fontMag.value())/100
        else:
            self._cex = 1
        if self._replotAfterChange:
            self.replot()
    def setForgroundColors(self):
        colorDialog = QColorDialog(self)
        self._forgroundColor = unicode(colorDialog.getColor().name())
        colorDialog.hide()
        if self._replotAfterChange:
            self.replot()
    def setLabelColors(self):
        colorDialog = QColorDialog(self)
        self._labelColors = unicode(colorDialog.getColor().name())
        colorDialog.hide()
        if self._replotAfterChange:
            self.replot()
    def setTitleColors(self):
        colorDialog = QColorDialog(self)
        self._titleColors = unicode(colorDialog.getColor().name())
        colorDialog.hide()
        if self._replotAfterChange:
            self.replot()
    def setSubtitleColors(self):
        colorDialog = QColorDialog(self)
        self._subtitleColors = unicode(colorDialog.getColor().name())
        colorDialog.hide()
        if self._replotAfterChange:
            self.replot()
    def setLineType(self):
        ltd = lineTypeDialog(self)
        if ltd.exec_() != QDialog.Accepted: 
            print _('Not accepted')
            return
        self._lty = 'c('+','.join(ltd.ltys)+')'
        print self._lty
        if self._replotAfterChange:
            self.replot()
    def setLineWidth(self):
        pass
        if self._replotAfterChange:
            self.replot()
    def setPointCharacters(self):
        ### set a list of point characters to be plotted.  these should be of the form of either a character or an integer for plotting
        
        if self._replotAfterChange:
            self.replot()
    def plotExactly(self, logic = True):
        self.plotExactlySwitch = logic
        if logic:
            self.menuParameters.setEnabled(False)
        else:
            self.menuParameters.setEnabled(True)

    
    ##########################
    ## Interaction Functions #
    ##########################
    def clear(self):
        if self.scene():
            self.scene().clear()
        else:
            print _('loading scene')
            scene = QGraphicsScene()
            self.setScene(scene)
        
    def toClipboard(self):
        QApplication.clipboard().setImage(self.returnImage())
    def saveAsPDF(self):
        print _('save as pdf')
        qname = QFileDialog.getSaveFileName(self, _("Save Image"), redREnviron.directoryNames['documentsDir'] + "/Image-"+unicode(datetime.date.today())+".pdf", "PDF Document (.pdf)")
        if qname.isEmpty(): return
        qname = unicode(qname)
        self.saveAs(unicode(qname), 'pdf')
    def saveAsPostScript(self):
        print _('save as post script')
        qname = QFileDialog.getSaveFileName(self, _("Save Image"), redREnviron.directoryNames['documentsDir'] + "/Image-"+unicode(datetime.date.today())+".eps", "Post Script (.eps)")
        if qname.isEmpty(): return
        qname = unicode(qname)
        self.saveAs(unicode(qname), 'ps')
    def saveAsBitmap(self):
        print _('save as bitmap')
        qname = QFileDialog.getSaveFileName(self, _("Save Image"), redREnviron.directoryNames['documentsDir'] + "/Image-"+unicode(datetime.date.today())+".bmp", "Bitmap (.bmp)")
        if qname.isEmpty(): return
        qname = unicode(qname)
        self.saveAs(unicode(qname), 'bmp')
    def saveAsJPEG(self):
        print _('save as jpeg')
        qname = QFileDialog.getSaveFileName(self, _("Save Image"), redREnviron.directoryNames['documentsDir'] + "/Image-"+unicode(datetime.date.today())+".jpg", "JPEG Image (.jpg)")
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
                if unicode(action.text()) == _('Copy'):
                    self.toClipboard()
                elif unicode(action.text()) == _('Zoom Out'):
                    self.scale(0.80, 0.80)
                elif unicode(action.text()) == _('Zoom In'):
                    self.scale(1.50, 1.50)
                elif unicode(action.text()) == _('Undock'):
                    ## want to undock from the widget and make an independent viewing dialog.
                    self.dialog.layout().addWidget(self.controlArea)
                    self.dialog.show()
                elif unicode(action.text()) == _('Redock'):
                    self.parent.layout().addWidget(self.controlArea)
                    self.dialog.hide()
                elif unicode(action.text()) == _('Fit In Window'):
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
        print _('Addign Image')
        if not self.scene():
            print _('loading scene')
            scene = QGraphicsScene()
            self.setScene(scene)
            print self.image
        if imageType == None:
            imageType = image.split('.')[-1]
        if imageType not in ['svg', 'png', 'jpeg']:
            self.clear()
            print imageType, _('Error occured')
            raise Exception, _('Image type specified is not a valid type for this widget.')
        if imageType == 'svg':
            self.convertSVG(unicode(os.path.join(redREnviron.directoryNames['tempDir'], image)).replace('\\', '/')) ## handle the conversion to glyph free svg
            mainItem = QGraphicsSvgItem(unicode(os.path.join(redREnviron.directoryNames['tempDir'], image)).replace('\\', '/'))
        elif imageType in ['png', 'jpeg']:
            mainItem = QGraphicsPixmapItem(QPixmap(os.path.join(redREnviron.directoryNames['tempDir'], image.replace('\\', '/'))))
        else:
            raise Exception, 'Image type %s not specified in a plotting method' % imageType
            #mainItem = QGraphicsPixmapItem(QPixmap(image))
        print mainItem
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
            print _('Error in saving image in graphicsView')
            return ''
        
        text = '.. image:: %s\n    :scale: 50%%\n\n' % imageFile
        
        return {self.widgetName:{'includeInReports':self.includeInReports,'text':text}}        
        
    def saveAs(self, fileName, imageType):
        if self.query == '': return
        if imageType == 'pdf':
            self.R('pdf(file = \'%s\')' % fileName.replace('\\', '/'), wantType = 'NoConversion')
        elif imageType == 'ps':
            self.R('postscript(file = \'%s\')' % fileName.replace('\\', '/'), wantType = 'NoConversion')
        elif imageType == 'bmp':
            self.R('bmp(file = \'%s\')' % fileName.replace('\\', '/'), wantType = 'NoConversion')
        elif imageType == 'jpeg':
            self.R('jpeg(file = \'%s\')' % fileName.replace('\\', '/'), wantType = 'NoConversion')
        
        if not self.plotExactlySwitch:
            self.extras = self._setParameters()
            if unicode(self.extrasLineEdit.text()) != '':
                self.extras += ', '+unicode(self.extrasLineEdit.text())
            if self.extras != '':
                fullquery = '%s(%s, %s)' % (self.function, self.query, self.extras)
            else:
                fullquery = '%s(%s)' % (self.function, self.query)
        else:
            query = self.query
        self.R(query, wantType = 'NoConversion')
        for l in self.layers:
            self.R(l, wantType = 'NoConversion')
        
        self.R('dev.off()', wantType = 'NoConversion')
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
             self.parent.status.setText(_('No legend names specified. Can\'t make the legend'))
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
        self.R(function, wantType = 'NoConversion')
    def setLegendNames(self, parameter):
        ## sets the legend to plot the names as the set parameter.  This can come from either a call to the widget through it's own interface or through the widget.
        self._legendNames = parameter
    def _setLegendLocation(self, location):
        self._legendLocation = location
    def _setParameters(self):
        inj = ''
        injection = []
        if self._bg:
            injection.append('bg = \'%s\'' % self._bg)
        if self._cex:
            injection.append('cex = %s' % self._cex)
        if self._cexAxis:
            injection.append('cex.axis = %s' % self._cexAxis)
        if self._cexLab:
            injection.append('cex.lab = %s' % self._cexLab)
        if self._cexMain:
            injection.append('cex.main = %s' % self._cexMain)
        if self._cexSub:
            injection.append('cex.sub = %s' % self._cexSub)
        if self._col:
            injection.append('col = %s' % self._col)
        if self._colAxis:
            injection.append('col.axis = \'%s\'' % self._colAxis)
        if self._colMain:
            injection.append('col.main = \'%s\'' % self._colMain)
        if self._colSub:
            injection.append('col.sub = \'%s\'' % self._colSub)
        if self._family:
            injection.append('family = \'%s\'' % self._family)
        if self._fg:
            injection.append('fg = \'%s\'' % self._fg)
        if self._lty:
            injection.append('lty = %s' % self._lty)
        if self._lwd:
            injection.append('lwd = %s' % self._lwd)
        inj = ','.join(injection)
        print inj
        #self.R('par('+inj+')')
        return inj
    def _startRDevice(self, dwidth, dheight, imageType):
        if imageType not in ['svg', 'png', 'jpeg']:
            imageType = 'png'
        
        # fileName = redREnviron.directoryNames['tempDir']+'/plot'+unicode(self.widgetID).replace('.', '_')+'.'+imageType
        # fileName = fileName.replace('\\', '/')
        self.imageFileName = unicode(self.image).replace('\\', '/')+'.'+unicode(imageType)
        # print '###################### filename' , self.imageFileName
        if imageType == 'svg':
            self.require_librarys(['Cairo'])
            self.R('CairoSVG(file=\''+unicode(os.path.join(redREnviron.directoryNames['tempDir'], self.imageFileName).replace('\\', '/'))+'\', width = '
                +unicode(dheight)+', height = '+unicode(dheight)
                +')', wantType = 'NoConversion')
            
        if imageType == 'png':
            self.R('png(file=\''+unicode(os.path.join(redREnviron.directoryNames['tempDir'], self.imageFileName).replace('\\', '/'))+'\', width = '
                +unicode(dheight*100)+', height = '+unicode(dheight*100)
                +')', wantType = 'NoConversion')
        elif imageType == 'jpeg':
            self.R('jpeg(file=\''+unicode(os.path.join(redREnviron.directoryNames['tempDir'], self.imageFileName).replace('\\', '/'))+'\', width = '
                +unicode(dheight*100)+', height = '+unicode(dheight*100)
                +')', wantType = 'NoConversion')
                
    def plot(self, query, function = 'plot', dwidth=6, dheight=6, data = None, legend = False):
        ## performs a quick plot given a query and an imageType
        self.plotMultiple(query, function = function, dwidth = dwidth, dheight = dheight, layers = [], data = data, legend = legend)
            

    def plotMultiple(self, query, function = 'plot', dwidth = 6, dheight = 6, layers = [], data = None, legend = False):
        ## performs plotting using multiple layers, each layer should be a query to be executed in RSession
        self.data = data
        self.function = function
        self.query = query
        self._startRDevice(dwidth, dheight, self.standardImageType)
        
        if not self.plotExactlySwitch:
            self.extras = self._setParameters()
            if unicode(self.extrasLineEdit.text()) != '':
                self.extras += ', '+unicode(self.extrasLineEdit.text())
            if self.extras != '':
                fullquery = '%s(%s, %s)' % (function, query, self.extras)
            else:
                fullquery = '%s(%s)' % (function, query)
        else:
            fullquery = self.query
        
        try:
            self.R(fullquery, wantType = 'NoConversion')
        
            
            print fullquery
            if len(layers) > 0:
                for l in layers:
                    self.R(l, wantType = 'NoConversion')
            if legend:
                self._setLegend()
            fileName = unicode(self.imageFileName)
            print fileName
        except Exception as inst:
            self.R('dev.off()', wantType = 'NoConversion') ## we still need to turn off the graphics device
            print _('Plotting exception occured')
            raise Exception(unicode(inst))
        self.R('dev.off()', wantType = 'NoConversion')
        self.clear()
        fileName = unicode(self.imageFileName)
        print fileName
        self.addImage(fileName)
        self.layers = layers
        self._dwidth = dwidth
        self._dheight = dheight
        self.fitInView(self.mainItem.boundingRect(), Qt.KeepAspectRatio)
    def setExtrasLineEditEnabled(self, enabled = True):
        
        self.extrasLineEdit.enabled(enabled)
        if enabled:
            self.extrasLineEdit.show()
        else:
            self.extrasLineEdit.hide()
    def setReplotAfterChange(self, replot = True):
        if replot:
            self._replotAfterChange = True
        else:
            self._replotAfterChange = False
    def replot(self):
        if self.query == '': return ## no plot can be generated.
        self._startRDevice(self._dwidth, self._dheight, self.standardImageType)
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
        
        
        self.R(fullquery, wantType = 'NoConversion')
        if len(self.layers) > 0:
            for l in self.layers:
                self.R(l, wantType = 'NoConversion')
        self.R('dev.off()', wantType = 'NoConversion')
        self.clear()
        fileName = unicode(self.imageFileName)
        self.addImage(fileName)
    def printMe(self):
        printer = QPrinter()
        printDialog = QPrintDialog(printer)
        if printDialog.exec_() == QDialog.Rejected: 
            print _('Printing Rejected')
            return
        painter = QPainter(printer)
        self.scene().render(painter)
        painter.end()
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
        print _('getting DOM model')
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
                print i, nl[i], _('error')
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
    def __init__(self, parent = None, layout = 'vertical', title = _('Color List Dialog'), data = ''):
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
        self.colorList = listBox(leftBox, label = _('Color List'))
        button(leftBox, label = _('Add Color'), callback = self.addColor)
        button(leftBox, label = _('Remove Color'), callback = self.removeColor)
        button(leftBox, label = _('Clear Colors'), callback = self.colorList.clear)
        button(mainArea, label = _('Finished'), callback = self.accept)
        # attribute list
        self.attsList = listBox(rightBox, label = _('Data Parameters'), callback = self.attsListSelected)
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

class lineTypeDialog(dialog):
    def __init__(self, parent = None, layout = 'vertical', title = _('Line Type Dialog')):
        dialog.__init__(self, parent = parent, layout = layout, title = title)
        
        ## add a set of line types that can be shown in R and allow the user to pick them
        self.linesListBox = listBox(self, label = 'Line types:', items = ['________', '- - - -', '........', '_._._._.', '__ __ __', '__.__.__.'], callback = self.setLineTypes)
        self.linesListBox.setSelectionMode(QAbstractItemView.MultiSelection)
        button(self, _("Done"), callback = self.accept)
    def setLineTypes(self):
        numbers = []
        for item in self.linesListBox.selectedItems():
            if unicode(item.text()) == '________':
                numbers.append('1')
            elif unicode(item.text()) == '- - - -':
                numbers.append('2')
            elif unicode(item.text()) == '........':
                numbers.append('3')
            elif unicode(item.text()) == '_._._._.':
                numbers.append('4')
            elif unicode(item.text()) == '__ __ __':
                numbers.append('5')
            elif unicode(item.text()) == '__.__.__.':
                numbers.append('6')
        print numbers
        self.ltys = numbers
            