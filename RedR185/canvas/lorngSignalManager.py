# Author: Gregor Leban (gregor.leban@fri.uni-lj.si) modifications by Kyle R Covington and Anup Parikh
# Description:
#    manager, that handles correct processing of widget signals
#

import sys, time, OWGUI, os, redREnviron
#from orngCanvasItems import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
Single = 2
Multiple = 4

Default = 8
NonDefault = 16
class MyCanvasText(QGraphicsSimpleTextItem):
    def __init__(self, canvas, text, x, y, flags=Qt.AlignLeft, bold=0, show=1):
        QGraphicsSimpleTextItem.__init__(self, text, None, canvas)
        self.setPos(x,y)
        self.setPen(QPen(Qt.black))
        self.flags = flags
        if bold:
            font = self.font();
            font.setBold(1);
            self.setFont(font)
        if show:
            self.show()

    def paint(self, painter, option, widget = None):
        #painter.resetMatrix()
        painter.setPen(self.pen())
        painter.setFont(self.font())

        xOff = 0; yOff = 0
        rect = painter.boundingRect(QRectF(0,0,2000,2000), self.flags, self.text())
        if self.flags & Qt.AlignHCenter: xOff = rect.width()/2.
        elif self.flags & Qt.AlignRight: xOff = rect.width()
        if self.flags & Qt.AlignVCenter: yOff = rect.height()/2.
        elif self.flags & Qt.AlignBottom:yOff = rect.height()
        #painter.drawText(self.pos().x()-xOff, self.pos().y()-yOff, rect.width(), rect.height(), self.flags, self.text())
        painter.drawText(-xOff, -yOff, rect.width(), rect.height(), self.flags, self.text())
        
class SignalManager:
    widgets = []    # topologically sorted list of widgets
    links = {}      # dicionary. keys: widgetFrom, values: (widgetTo1, signalNameFrom1, signalNameTo1, enabled1), (widgetTo2, signalNameFrom2, signalNameTo2, enabled2)
    freezing = 0            # do we want to process new signal immediately
    signalProcessingInProgress = 0 # this is set to 1 when manager is propagating new signal values
    # loadSavedSession = False
    def __init__(self, *args):
        self.debugFile = None
        self.verbosity = 1 #orngDebugging.orngVerbosity
        self.stderr = sys.stderr
        
        self._seenExceptions = {}
    # add widget to list, ## should be removed and use the universal widget list
    def addWidget(self, widget):
        if self.verbosity >= 2:
            self.addEvent("added widget ", eventVerbosity = 2)

        if widget not in self.widgets:
            #self.widgets.insert(0, widget)
            self.widgets.append(widget)

    # remove widget from list ## should ref the universal widget list
    def removeWidget(self, widget):
        if self.verbosity >= 2:
            self.addEvent("remove widget ", eventVerbosity = 2)
        if widget in self.widgets:
            self.widgets.remove(widget)


    def fixPositionOfDescendants(self, widget):

        for link in self.links.get(widget, []):
            widgetTo = link[0]
            self.widgets.remove(widgetTo)
            self.widgets.append(widgetTo)
            self.fixPositionOfDescendants(widgetTo)

    
    def getChildern(self,theWidget):
        children = []
        # print 'getChildern\n'*5
        # print 'theWidget', theWidget
        # print self.links.keys()
        # print self.links.get(theWidget, [])
        for (widget, signalNameFrom, signalNameTo, enabled) in self.links.get(theWidget, []):
            # print _('widget'),widget
            children.append(widget)
            children.extend(self.getChildern(widget))
        return children

    def getParents(self,theWidget):
        parents = []
        for k, v in self.links.items():
            for (widget, signalNameFrom, signalNameTo, enabled) in v:
                if widget == theWidget:
                    parents.append(k)
                    parents.extend(self.getParents(k))
        return parents
         
    """
    def removeLink(self, widgetFrom, widgetTo, signalNameFrom, signalNameTo):
        if self.verbosity >= 2:
            self.addEvent("remove link", eventVerbosity = 2)
        # no need to update topology, just remove the link
        
        if self.links.has_key(widgetFrom):
            for (widget, signalFrom, signalTo, enabled) in self.links[widgetFrom]:
                if widget == widgetTo and signalFrom == signalNameFrom and signalTo == signalNameTo:
                    for key in widgetFrom.linksOut[signalFrom].keys():
                        widgetTo.updateNewSignalData(widgetFrom, signalNameTo, None, key, signalNameFrom)
                        print _('updating signal data')
                    self.links[widgetFrom].remove((widget, signalFrom, signalTo, enabled))
                    if not self.freezing and not self.signalProcessingInProgress: 
                        self.processNewSignals(widgetFrom)
                        #print _('processing signals')
        
        widgetTo.removeInputConnection(widgetFrom, signalNameTo)
    """

    # ############################################
    # ENABLE OR DISABLE LINK CONNECTION

    def setNeedAttention(self,firstWidget) :
        #index = self.widgets.index(firstWidget)
        # print 'setNeedAttention\n'*5
        # print _('firstWidget'), firstWidget
        children = self.getChildern(firstWidget)
        children.append(firstWidget)
        # print children
        #for i in range(index, len(self.widgets)):
        for i in children:
            # print _('propagating'), i.windowTitle(), i#, index
            if i.outputs != None and len(i.outputs) !=0 and not i.loadSavedSession:
                i.setInformation(id = 'attention', text = 'Widget needs attention.')
    
    """
    def processNewSignals(self, firstWidget):
        print 'processNewSignals'
        if len(self.widgets) == 0: 
            print _('No widgets'), self.widgets
            return
        if self.signalProcessingInProgress: 
            print _('processing in progress')
            return

        if firstWidget not in self.widgets:
            firstWidget = self.widgets[0]   # if some window that is not a widget started some processing we have to process new signals from the first widget
        
        # start propagating
        self.signalProcessingInProgress = 1
        
        # index = self.widgets.index(firstWidget)
        print 'self.getParents', self.getParents(firstWidget)
        children = self.getChildern(firstWidget)
        children.append(firstWidget)

        print _('children'), children
        for i in children:
            if i.needProcessing:
                print _('needs processing'), i
                try:
                    i.processSignals()  ## call process signals in the widgetSignals function.
                except:
                    type, val, traceback = sys.exc_info()
                    sys.excepthook(type, val, traceback)  # we pretend that we handled the exception, so that it doesn't crash canvas

        # we finished propagating
        self.signalProcessingInProgress = 0

    """
    """
    def existsPath(self, widgetFrom, widgetTo):
        # is there a direct link
        if not self.links.has_key(widgetFrom): return 0

        for (widget, signalFrom, signalTo, enabled) in self.links[widgetFrom]:
            if widget == widgetTo: return 1

        # is there a nondirect link
        for (widget, signalFrom, signalTo, enabled) in self.links[widgetFrom]:
            if self.existsPath(widget, widgetTo): return 1

        # there is no link...
        return 0
    """
    def refresh(self):
        for widget in self.widgets:
            widget.refresh()

# create a global instance of signal manager
globalSignalManager = SignalManager()


# #######################################
# # Signal dialog - let the user select active signals between two widgets, this is called when the connections are ambiguous.
# #######################################
class SignalDialog(QDialog):
    def __init__(self, canvasDlg, *args):
        #apply(QDialog.__init__,(self,) + args)
        QDialog.__init__(self,canvasDlg)
        self.canvasDlg = canvasDlg

        self.signals = []
        self._links = []
        self.allSignalsTaken = 0

        # GUI    ### canvas dialog that is shown when there are multiple possible connections.
        self.setWindowTitle(_('Connect Signals'))
        self.setLayout(QVBoxLayout())

        self.canvasGroup = OWGUI.widgetBox(self, 1)
        self.canvas = QGraphicsScene(0,0,1000,1000)
        self.canvasView = SignalCanvasView(self, self.canvasDlg, self.canvas, self.canvasGroup)
        self.canvasGroup.layout().addWidget(self.canvasView)

        buttons = OWGUI.widgetBox(self, orientation = "horizontal", sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed))

        self.buttonHelp = OWGUI.button(buttons, self, "&Help")
        buttons.layout().addStretch(1)
        self.buttonClearAll = OWGUI.button(buttons, self, "Clear &All", callback = self.clearAll)
        self.buttonOk = OWGUI.button(buttons, self, "&OK", callback = self.accept)
        self.buttonOk.setAutoDefault(1)
        self.buttonOk.setDefault(1)
        self.buttonCancel = OWGUI.button(buttons, self, "&Cancel", callback = self.reject)

    def clearAll(self):
        while self._links != []:
            self.removeLink(self._links[0][0], self._links[0][1])

    def setOutInWidgets(self, outWidget, inWidget):
        self.outWidget = outWidget
        self.inWidget = inWidget
        (width, height) = self.canvasView.addSignalList(outWidget, inWidget)
        self.canvas.setSceneRect(0, 0, width, height)
        self.resize(width+50, height+80)
        
        ## process the signals so that active connections are show.
        links = outWidget.instance().outputs.getSignalLinks(inWidget.instance())
        for (outName, inName) in links:
            self.addLink(outName, inName)
        #print _('Output Handler Returned the following links'), links

    def countCompatibleConnections(self, outputs, inputs, outInstance, inInstance, outType, inType):
        count = 0
        for outS in outputs:
            if outInstance.getOutputType(outS.name) == None: continue  # ignore if some signals don't exist any more, since we will report error somewhere else
            if outInstance.getOutputType(outS.name) == 'All': pass
            elif not issubclass(outInstance.getOutputType(outS.name), outType): continue
            for inS in inputs:
                if inInstance.getOutputType(inS.name) == None: continue  # ignore if some signals don't exist any more, since we will report error somewhere else
                if inInstance.getOutputType(inS.name) == 'All': 
                    count += 1
                    continue
                if type(inInstance.getOutputType(inS.name)) not in [list]:
                    if not issubclass(inType, inInstance.getInputType(inS.name)): continue
                    if issubclass(outInstance.getOutputType(outS.name), inInstance.getInputType(inS.name)): count+= 1
                else:
                    for i in type(inInstance.getOutputType(inS.name)):
                        if not issubclass(inType, i): continue
                        if issubclass(outInstance.getOutputType(outS.name), i): count+= 1
        return count

    def addLink(self, outName, inName):
        if (outName, inName) in self._links: 
            #print _('signal already in the links')
            return 1
        #print outName, inName, _('Names')
        # check if correct types
        outType = self.outWidget.instance().outputs.getSignal(outName)['signalClass']
        inType = self.inWidget.instance().inputs.getSignal(inName)['signalClass']
        if not outType or not inType:
            raise Exception, _('None sent as signal type')
            
            
        if not self.inWidget.instance().inputs.doesSignalMatch(inName, outType): 
            mb = QMessageBox("Failed to Connect", "Not valid connection.\nWould you like to force this connection anyway?\n\nTHIS MIGHT CAUSE ERRORS AND EVEN CRASH RED-R!!!", 
                QMessageBox.Information, QMessageBox.Ok | QMessageBox.Default, 
                QMessageBox.No | QMessageBox.Escape, QMessageBox.NoButton)
            if mb.exec_() == QMessageBox.No:
                return 0
            
        inSignal = None
        inputs = self.inWidget.instance().inputs.getAllInputs()
        for id, signal in inputs.items():
            if id == inName: inSignal = id

        # if inName is a single signal and connection already exists -> delete it
        for (outN, inN) in self._links:
            #print inSignal, inN, inName, self.inWidget.instance().inputs.getSignal(inSignal)['multiple']
            if inSignal and inN == inName and not self.inWidget.instance().inputs.getSignal(inSignal)['multiple']:
                self.removeLink(outN, inN)

        self._links.append((outName, inName))
        self.canvasView.addLink(outName, inName)
        return 1


    def removeLink(self, outName, inName): #removes from the list of instances
        res = QMessageBox.question(self.canvasView, 'Red-R Connections', 'Are you sure you want to remove that signal?\n\nThe downstream widget will recieve empty data.', QMessageBox.Yes | QMessageBox.No)
        if res == QMessageBox.Yes:
            self.outWidget.instance().outputs.removeSignal(self.inWidget.instance().inputs.getSignal(inName), outName)
            self.canvasView.removeLink(outName, inName)
            self._links.remove((outName, inName))

    def getLinks(self):
        return self._links
# this class is needed by signalDialog to show widgets and lines
class SignalCanvasView(QGraphicsView):
    def __init__(self, dlg, canvasDlg, *args):
        apply(QGraphicsView.__init__,(self,) + args)
        self.dlg = dlg
        self.canvasDlg = canvasDlg
        self.bMouseDown = False
        self.tempLine = None
        self.inWidget = None
        self.outWidget = None
        self.inWidgetIcon = None
        self.outWidgetIcon = None
        self.lines = []
        self.outBoxes = []
        self.inBoxes = []
        self.texts = []
        self.ensureVisible(0,0,1,1)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.setRenderHint(QPainter.Antialiasing)

    def addSignalList(self, outWidget, inWidget):
        self.scene().clear()
        outputs, inputs = outWidget.instance().outputs.getAllOutputs(), inWidget.instance().inputs.getAllInputs()
        outIcon, inIcon = QIcon(outWidget.widgetInfo.icon), QIcon(inWidget.widgetInfo.icon)
        self.lines = []
        self.outBoxes = []
        self.inBoxes = []
        self.texts = []
        xSpaceBetweenWidgets = 100  # space between widgets
        xWidgetOff = 10             # offset for widget position
        yWidgetOffTop = 10          # offset for widget position
        yWidgetOffBottom = 30       # offset for widget position
        ySignalOff = 10             # space between the top of the widget and first signal
        ySignalSpace = 50           # space between two neighbouring signals
        ySignalSize = 20            # height of the signal box
        xSignalSize = 20            # width of the signal box
        xIconOff = 10
        iconSize = 48

        count = max(len(inputs), len(outputs))
        height = max ((count)*ySignalSpace, 70)

        # calculate needed sizes of boxes to show text
        maxLeft = 0
        for i in inputs.keys():
            maxLeft = max(maxLeft, self.getTextWidth("("+inputs[i]['name']+")", 1))
            maxLeft = max(maxLeft, self.getTextWidth(unicode([unicode(a).split('.')[-1] for a in inputs[i]['signalClass']])))

        maxRight = 0
        for i in outputs.keys():
            maxRight = max(maxRight, self.getTextWidth("("+outputs[i]['name']+")", 1))
            maxRight = max(maxRight, self.getTextWidth(unicode(outputs[i]['signalClass']).split('.')[-1]))

        width = max(maxLeft, maxRight) + 70 # we add 70 to show icons beside signal names

        # show boxes
        brush = QBrush(QColor(60,150,255))
        self.outWidget = QGraphicsRectItem(xWidgetOff, yWidgetOffTop, width, height, None, self.dlg.canvas)
        self.outWidget.setBrush(brush)
        self.outWidget.setZValue(-100)

        self.inWidget = QGraphicsRectItem(xWidgetOff + width + xSpaceBetweenWidgets, yWidgetOffTop, width, height, None, self.dlg.canvas)
        self.inWidget.setBrush(brush)
        self.inWidget.setZValue(-100)
        
        canvasPicsDir  = os.path.join(redREnviron.directoryNames['canvasDir'], "icons")
        if os.path.exists(os.path.join(canvasPicsDir, "frame.png")):
            widgetBack = QPixmap(os.path.join(canvasPicsDir, "frame.png"))
        else:
            widgetBack = outWidget.imageFrame

        # if icons -> show them
        if outIcon:
            frame = QGraphicsPixmapItem(widgetBack, None, self.dlg.canvas)
            frame.setPos(xWidgetOff + xIconOff, yWidgetOffTop + height/2.0 - frame.pixmap().width()/2.0)
            self.outWidgetIcon = QGraphicsPixmapItem(outIcon.pixmap(iconSize, iconSize), None, self.dlg.canvas)
            self.outWidgetIcon.setPos(xWidgetOff + xIconOff, yWidgetOffTop + height/2.0 - self.outWidgetIcon.pixmap().width()/2.0)
        
        if inIcon:
            frame = QGraphicsPixmapItem(widgetBack, None, self.dlg.canvas)
            frame.setPos(xWidgetOff + xSpaceBetweenWidgets + 2*width - xIconOff - frame.pixmap().width(), yWidgetOffTop + height/2.0 - frame.pixmap().width()/2.0)
            self.inWidgetIcon = QGraphicsPixmapItem(inIcon.pixmap(iconSize, iconSize), None, self.dlg.canvas)
            self.inWidgetIcon.setPos(xWidgetOff + xSpaceBetweenWidgets + 2*width - xIconOff - self.inWidgetIcon.pixmap().width(), yWidgetOffTop + height/2.0 - self.inWidgetIcon.pixmap().width()/2.0)

        # show signal boxes and text labels
        #signalSpace = (count)*ySignalSpace
        signalSpace = height
        j = 0
        for i in outputs.keys():
            y = yWidgetOffTop + ((j+1)*signalSpace)/float(len(outputs)+1)
            box = QGraphicsRectItem(xWidgetOff + width, y - ySignalSize/2.0, xSignalSize, ySignalSize, None, self.dlg.canvas)
            box.setBrush(QBrush(QColor(0,0,255)))
            box.setZValue(200)
            self.outBoxes.append((outputs[i]['name'], box, i))

            self.texts.append(MyCanvasText(self.dlg.canvas, outputs[i]['name'], xWidgetOff + width - 5, y - 7, Qt.AlignRight | Qt.AlignVCenter, bold =1, show=1))
            self.texts.append(MyCanvasText(self.dlg.canvas, unicode(outputs[i]['signalClass']).split('.')[-1], xWidgetOff + width - 5, y + 7, Qt.AlignRight | Qt.AlignVCenter, bold =0, show=1))
            j += 1
        j = 0
        for i in inputs.keys():
            y = yWidgetOffTop + ((j+1)*signalSpace)/float(len(inputs)+1)
            box = QGraphicsRectItem(xWidgetOff + width + xSpaceBetweenWidgets - xSignalSize, y - ySignalSize/2.0, xSignalSize, ySignalSize, None, self.dlg.canvas)
            box.setBrush(QBrush(QColor(0,0,255)))
            box.setZValue(200)
            self.inBoxes.append((inputs[i]['name'], box, i))

            self.texts.append(MyCanvasText(self.dlg.canvas, inputs[i]['name'], xWidgetOff + width + xSpaceBetweenWidgets + 5, y - 7, Qt.AlignLeft | Qt.AlignVCenter, bold =1, show=1))
            self.texts.append(MyCanvasText(self.dlg.canvas, unicode([unicode(a).split('.')[-1] for a in inputs[i]['signalClass']]), xWidgetOff + width + xSpaceBetweenWidgets + 5, y + 7, Qt.AlignLeft | Qt.AlignVCenter, bold =0, show=1))
            j += 1
        self.texts.append(MyCanvasText(self.dlg.canvas, outWidget.caption, xWidgetOff + width/2.0, yWidgetOffTop + height + 5, Qt.AlignHCenter | Qt.AlignTop, bold =1, show=1))
        self.texts.append(MyCanvasText(self.dlg.canvas, inWidget.caption, xWidgetOff + width* 1.5 + xSpaceBetweenWidgets, yWidgetOffTop + height + 5, Qt.AlignHCenter | Qt.AlignTop, bold =1, show=1))

        return (2*xWidgetOff + 2*width + xSpaceBetweenWidgets, yWidgetOffTop + height + yWidgetOffBottom)

    def getTextWidth(self, text, bold = 0):
        temp = QGraphicsSimpleTextItem(text, None, self.dlg.canvas)
        if bold:
            font = temp.font()
            font.setBold(1)
            temp.setFont(font)
        temp.hide()
        return temp.boundingRect().width()

    # ###################################################################
    # mouse button was pressed
    def mousePressEvent(self, ev):
        #print _(' SignalCanvasView mousePressEvent')
        self.bMouseDown = 1
        point = self.mapToScene(ev.pos())
        activeItem = self.scene().itemAt(QPointF(ev.pos()))
        if type(activeItem) == QGraphicsRectItem and activeItem not in [self.outWidget, self.inWidget]:
            self.tempLine = QGraphicsLineItem(None, self.dlg.canvas)
            self.tempLine.setLine(point.x(), point.y(), point.x(), point.y())
            self.tempLine.setPen(QPen(QColor(0,255,0), 1))
            self.tempLine.setZValue(-300)
            
        elif type(activeItem) == QGraphicsLineItem:
            for (line, outName, inName, outBox, inBox) in self.lines:
                if line == activeItem:
                    self.dlg.removeLink(outName, inName)
                    return

    # ###################################################################
    # mouse button was released #########################################
    def mouseMoveEvent(self, ev):
        if self.tempLine:
            curr = self.mapToScene(ev.pos())
            start = self.tempLine.line().p1()
            self.tempLine.setLine(start.x(), start.y(), curr.x(), curr.y())
            self.scene().update()

    # ###################################################################
    # mouse button was released #########################################
    def mouseReleaseEvent(self, ev):
        if self.tempLine:  ## a line is on
            activeItem = self.scene().itemAt(QPointF(ev.pos()))  # what is the item at the active position??
            if type(activeItem) == QGraphicsRectItem:
                activeItem2 = self.scene().itemAt(self.tempLine.line().p1()) ## active item 2 is the item at the beginning of the line.
                if activeItem.x() < activeItem2.x(): outBox = activeItem; inBox = activeItem2
                else:                                outBox = activeItem2; inBox = activeItem
                outName = None; inName = None
                for (name, box, id) in self.outBoxes:
                    if box == outBox: outName = id
                for (name, box, id) in self.inBoxes:
                    if box == inBox: inName = id
                print outName, inName
                if outName != None and inName != None:
                    print _('adding link')
                    self.dlg.addLink(outName, inName)

            self.tempLine.hide()
            self.tempLine = None
            self.scene().update()


    def addLink(self, outName, inName):  ## makes the line that goes from one widget to the other on the canvas, outName and inName are the id's for the links
        #print _('Adding link in the canvas'), outName, inName
        outBox = None; inBox = None
        for (name, box, id) in self.outBoxes:
            if id == outName: outBox = box
        for (name, box, id) in self.inBoxes:
            if id == inName : inBox  = box
        if outBox == None or inBox == None:
            #print "error adding link. Data = ", outName, inName
            return
        line = QGraphicsLineItem(None, self.dlg.canvas)
        outRect = outBox.rect()
        inRect = inBox.rect()
        line.setLine(outRect.x() + outRect.width()-2, outRect.y() + outRect.height()/2.0, inRect.x()+2, inRect.y() + inRect.height()/2.0)
        line.setPen(QPen(QColor(0,255,0), 6))
        line.setZValue(100)
        self.scene().update()
        self.lines.append((line, outName, inName, outBox, inBox))


    def removeLink(self, outName, inName):  # removes the line on the canvas
        # res = QMessageBox.question(None, 'Red-R Connections', 'Are you sure you want to remove that link?\nThe downmtream widget will recieve No data.', QMessageBox.Yes, QMessageBox.No)
        
        # if res == QMessageBox.Yes:
            # self.dlg.
        for (line, outN, inN, outBox, inBox) in self.lines:
            if outN == outName and inN == inName:
                line.hide()
                self.lines.remove((line, outN, inN, outBox, inBox))
                self.scene().update()
                return



