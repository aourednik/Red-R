# Author: Gregor Leban (gregor.leban@fri.uni-lj.si) modifications by Kyle R Covington and Anup Parikh
# Description:
#    handling the mouse events inside documents
#
import orngCanvasItems
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import redRObjects, redRLog
import redRi18n
# def _(a):
    # return a
_ = redRi18n.Coreget_()
        
class SchemaView(QGraphicsView):
    def __init__(self, doc, name, *args):
        apply(QGraphicsView.__init__,(self,) + args)
        self.doc = doc
        self.name = name
        self.bWidgetDragging = False               # are we currently dragging a widget
        self.movingWidget = None
        self.mouseDownPosition = QPointF(0,0)
        self.tempLine = None
        self.widgetSelectionRect = None
        self.selectedLine = None
        self.tempWidget = None
        self.setRenderHint(QPainter.Antialiasing)
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.ensureVisible(0,0,1,1)

        # create popup menus
        self.linePopup = QMenu(_("Link"), self)
        self.lineEnabledAction = self.menupopupLinkEnabledID = self.linePopup.addAction( _("Enabled"),  self.toggleEnabledLink)
        self.lineEnabledAction.setCheckable(1)
        self.linePopup.addSeparator()
        self.linePopup.addAction(_("Reset Signals"), self.resetLineSignals)
        self.linePopup.addAction(_("Remove"), self.deleteSelectedLine)
        self.linePopup.addSeparator()
        self.setAcceptDrops(1)
        self.controlHeld = False

    # ###########################################
    # drag and drop events. You can open a document by dropping it on the canvas
    # ###########################################
    def containsOWSFile(self, name):
        name = name.strip("\x00")
        return name.lower().endswith(".rrs")

    def dragEnterEvent(self, ev):
        if self.containsOWSFile(unicode(ev.mimeData().data("FileName"))):
            ev.accept()
        else: ev.ignore()
                
    def dragMoveEvent(self, ev):
        if self.containsOWSFile(unicode(ev.mimeData().data("FileName"))):
            ev.setDropAction(Qt.MoveAction)
            ev.accept()
        else:
            ev.ignore()

    def dropEvent(self, ev):
        name = unicode(ev.mimeData().data("FileName"))
        if self.containsOWSFile(name):
            name = name.strip("\x00")
            self.doc.loadDocument(name)
            ev.accept()
        else:
            ev.ignore()

    # ###########################################
    # POPUP MENU - WIDGET actions
    # ###########################################

    # popMenuAction - user selected to show active widget
    def openActiveWidget(self):
        #if not self.tempWidget or self.tempWidget.instance == None: return
        # widgets = self.getSelectedWidgets()
        # if len(widgets) != 1: return
        # widget = widgets[0]
        # print 'Showing widget instance.', widget.instance().widgetID
        # widget.instance().show()
        self.tempWidget.instance().show()  ## simplified for showing the widget that was clicked.
        if self.tempWidget.instance().isMinimized():  # if widget is minimized, show its normal size
            self.tempWidget.instance().showNormal()

    # popMenuAction - user selected to rename active widget
    def renameActiveWidget(self):
        widgets = self.getSelectedWidgets()
        if len(widgets) != 1: return
        widget = widgets[0]

        exName = unicode(widget.caption)
        (newName, ok) = QInputDialog.getText(self, _("Rename Widget"), _("Enter new name for the '%s' widget:") % exName, QLineEdit.Normal, exName)
        newName = unicode(newName)
        if ok and newName != exName:
            for w in self.doc.widgets():
                if w != widget and w.caption == newName:
                    QMessageBox.information(self, _('Red-R Canvas'), _('Unable to rename widget. An instance with that name already exists.'))
                    return
            widget.updateText(newName)
            widget.instance().setWindowTitle(newName)

    # popMenuAction - user selected to delete active widget
    def removeActiveWidget(self):
        #print "Trying to remove the widget"
        res = QMessageBox.question(self.doc.canvasDlg, _('Red-R Canvas Remove Widget'), _('Are you sure you want to remove selected widget(s)?  This will remove the downstream data.'), QMessageBox.Yes | QMessageBox.No)
        if res != QMessageBox.Yes: return
        if self.doc.signalManager.signalProcessingInProgress:
            QMessageBox.information( self, _("Red-R Canvas"), _("Unable to remove widgets while signal processing is in progress. Please wait."))
            return

        selectedWidgets = self.getSelectedWidgets()
        #print selectedWidgets
        if selectedWidgets == []:
            selectedWidgets = [self.tempWidget]

        for item in selectedWidgets:
            #print item
            self.doc.removeWidget(item)

        self.scene().update()
        self.tempWidget = None
        self.doc.canvasDlg.widgetPopup.setEnabled(len(self.getSelectedWidgets()) == 1)

    # ###########################################
    # POPUP MENU - LINKS actions
    # ###########################################

    # popMenuAction - enable/disable link between two widgets
    def toggleEnabledLink(self):
        if self.selectedLine != None:
            #oldEnabled = self.doc.signalManager.getLinkEnabled(self.selectedLine.outWidget.instance, self.selectedLine.inWidget.instance)
            
            # we enable or disable all of the links simultaneously (only way to do it with this interface.
            self.selectedLine.outWidget.instance.outputs.setSignalEnabled(self.selectedLine.inWidget.instance, not self.selectedLine.outWidget.instance.outputs.isSignalEnabled(self.selectedLine.inWidget.instance))
            #self.doc.signalManager.setLinkEnabled(self.selectedLine.outWidget.instance, self.selectedLine.inWidget.instance, not oldEnabled)
            self.selectedLine.updateTooltip()
            self.selectedLine.inWidget.updateTooltip()
            self.selectedLine.outWidget.updateTooltip()

    # popMenuAction - delete selected link
    def deleteSelectedLine(self):
        if not self.selectedLine: return
        if self.doc.signalManager.signalProcessingInProgress:
             QMessageBox.information( self, _("Red-R Canvas"), _("Unable to remove connection while signal processing is in progress. Please wait."))
             return
        self.deleteLine(self.selectedLine)
        self.selectedLine = None
        self.scene().update()

    def deleteLine(self, line):
        if line != None:
            redRObjects.removeLineInstance(line)

    # resend signals between two widgets. receiving widget will process the received data
    def resendSignals(self):
        if self.selectedLine != None:
            self.doc.signalManager.setLinkEnabled(self.selectedLine.outWidget.instance, self.selectedLine.inWidget.instance, 1, justSend = 1)

    def resetLineSignals(self):
        if self.selectedLine:
            self.doc.resetActiveSignals(self.selectedLine.outWidget, self.selectedLine.inWidget, enabled = True)
            self.selectedLine.inWidget.updateTooltip()
            self.selectedLine.outWidget.updateTooltip()
            self.selectedLine.updateTooltip()

    def unselectAllWidgets(self):
        for k, items in redRObjects.getIconsByTab().items():
            #print k
            for item in items:
                #print item
                item.setSelected(0)
        self.scene().update()
    def selectAllWidgets(self):
        for k, items in redRObjects.getIconsByTab().items():
            for item in items:
                item.setSelected(1)
        self.scene().update()
    def getItemsAtPos(self, pos, itemType = None):
        if type(pos) == QPointF:
            pos = QGraphicsRectItem(QRectF(pos, QSizeF(1,1)))
        items = self.scene().collidingItems(pos)
        if itemType != None:
            items = [item for item in items if isinstance(item, itemType)]
        return items

    # ###########################################
    # MOUSE events
    # ###########################################

    # mouse button was pressed
    def keyPressEvent(self, ev):
        if ev.key() == Qt.Key_Control:
            self.controlHeld = True
    def keyReleaseEvent(self, ev):
        if ev.key() == Qt.Key_Control:
            self.controlHeld = False
    def mousePressEvent(self, ev):
        self.scene().update()
        self.mouseDownPosition = self.mapToScene(ev.pos())
        
        if self.widgetSelectionRect:
            self.widgetSelectionRect.hide()
            self.widgetSelectionRect = None
        if not self.controlHeld:
            self.unselectAllWidgets()  ## should clear the selections ahead of time KRC
        # do we start drawing a connection line
        if ev.button() == Qt.LeftButton:
            widgets = [item for item in self.doc.widgets() if item.mouseInsideRightChannel(self.mouseDownPosition)] + [item for item in self.doc.widgets() if item.mouseInsideLeftChannel(self.mouseDownPosition)]           
            if widgets:
                self.tempWidget = widgets[0]
                if not self.doc.signalManager.signalProcessingInProgress:   # if we are processing some signals, don't allow to add lines
                    self.unselectAllWidgets()
                    self.tempLine = orngCanvasItems.TempCanvasLine(self.doc.canvasDlg, self.scene())
                    if self.tempWidget.getDistToLeftEdgePoint(self.mouseDownPosition) < self.tempWidget.getDistToRightEdgePoint(self.mouseDownPosition):
                        self.tempLine.setEndWidget(self.tempWidget)
                        for widget in self.doc.widgets():
                            widget.canConnect(widget, self.tempWidget)
                    else:
                        self.tempLine.setStartWidget(self.tempWidget)
                        for widget in self.doc.widgets():
                            widget.canConnect(self.tempWidget, widget)
                                                        
                self.scene().update()
                self.doc.canvasDlg.widgetPopup.setEnabled(len(self.getSelectedWidgets()) == 1)
                return
            
        activeItem = self.scene().itemAt(self.mouseDownPosition)
        if not activeItem:
            self.tempWidget = None
            self.widgetSelectionRect = QGraphicsRectItem(QRectF(self.mouseDownPosition, self.mouseDownPosition), None, self.scene())
            self.widgetSelectionRect.setZValue(-100)
            self.widgetSelectionRect.show()
            self.unselectAllWidgets()
            for k, v in redRObjects.getIconsByTab().items():
                for i in v:
                    i.setPossibleConnection(False)
        # we clicked on a widget or on a line
        else:
            #redRLog.log(redRLog.REDRCORE, redRLog.DEBUG, _('Active item %s') % activeItem)
            if type(activeItem) in [orngCanvasItems.CanvasWidget]:# if we clicked on a widget          
                #print activeItem, _('An item was clicked')
                self.tempWidget = activeItem

                ## if it was a ghost widget we need to do something
                # print type(self.tempWidget)
                
                # if isinstance(self.tempWidget, orngCanvasItems.GhostWidget) and self.tempWidget.ghost:
                    # self.tempWidget.convertToCanvasWidget()
                # did we click inside the boxes to draw connections
                if ev.button() == Qt.LeftButton:
                    self.bWidgetDragging = True
                    if self.doc.ctrlPressed:
                        activeItem.setSelected(not activeItem.isSelected())
                    elif activeItem.isSelected() == 0:
                        self.unselectAllWidgets()
                        activeItem.setSelected(1) # set the active widget to be selected

                    for w in self.getSelectedWidgets():
                        w.savePosition()
                        w.setAllLinesFinished(False)

                # is we clicked the right mouse button we show the popup menu for widgets
                elif ev.button() == Qt.RightButton:
                    self.unselectAllWidgets()
                    activeItem.setSelected(1)
                    self.doc.canvasDlg.widgetPopup.popup(ev.globalPos())
                else:
                    self.unselectAllWidgets()

            # if we right clicked on a line we show a popup menu
            elif type(activeItem) == orngCanvasItems.CanvasLine and ev.button() == Qt.RightButton:
                self.unselectAllWidgets()
                self.selectedLine = activeItem
                self.lineEnabledAction.setChecked(self.selectedLine.getEnabled())
                self.linePopup.popup(ev.globalPos())
            else:
                self.unselectAllWidgets()

        self.doc.canvasDlg.widgetPopup.setEnabled(len(self.getSelectedWidgets()) == 1)
        self.scene().update()


    # mouse button was pressed and mouse is moving ######################
    def mouseMoveEvent(self, ev):
        point = self.mapToScene(ev.pos())

        if self.bWidgetDragging:
            for item in self.getSelectedWidgets():
                newPos = item.oldPos + (point-self.mouseDownPosition)
                item.setCoords(newPos.x(), newPos.y())

        elif self.tempLine:
            self.tempLine.updateLinePos(point)

        elif self.widgetSelectionRect:
            self.widgetSelectionRect.setRect(QRectF(self.mouseDownPosition, point))            

            

        self.scene().update()


    # mouse button was released #########################################
    def mouseReleaseEvent(self, ev):
        point = self.mapToScene(ev.pos())
        if self.widgetSelectionRect:
            # select widgets in rectangle
            widgets = self.getItemsAtPos(self.widgetSelectionRect, orngCanvasItems.CanvasWidget)
            for widget in self.doc.widgets():
                widget.setSelected(widget in widgets)
            self.widgetSelectionRect.hide()
            self.widgetSelectionRect = None

        # if we are moving a widget
        if self.bWidgetDragging:
            validPos = True
            for item in self.getSelectedWidgets():
                items = self.scene().collidingItems(item)
                validPos = validPos and (self.findItemTypeCount(items, orngCanvasItems.CanvasWidget) == 0)

            for item in self.getSelectedWidgets():
                if not validPos:
                    item.restorePosition()
                item.updateTooltip()
                item.setAllLinesFinished(True)


        # if we are drawing line
        elif self.tempLine:
            # show again the empty input/output boxes
            for widget in self.doc.widgets():
              widget.resetLeftRightEdges()      
            
            start = self.tempLine.startWidget or self.tempLine.widget  ## marks the starting of the tempLine
            end = self.tempLine.endWidget or self.tempLine.widget       ## marks the ending of the tempLine
            self.tempLine.hide()
            self.tempLine = None

            # we must check if we have really connected some output to input
            if start and end and start != end:
                if self.doc.signalManager.signalProcessingInProgress:
                     QMessageBox.information( self, _("Red-R Canvas"), _("Unable to connect widgets while signal processing is in progress. Please wait."))
                else:
                    self.doc.addLine(start, end)
            else:
                state = [self.doc.widgets()[i].widgetInfo.name for i in range(min(len(self.doc.widgets()), 5))]
                #predictedWidgets = orngHistory.predictWidgets(state, 20)

                newCoords = QPoint(ev.globalPos())
                self.doc.widgetPopupMenu.updateMenu()
                action = self.doc.widgetPopupMenu.exec_(newCoords- QPoint(0, self.doc.widgetPopupMenu.categoriesYOffset))
                if action and hasattr(action, "widgetInfo"):
                    xOff = -48 * bool(end)
                    newWidget = self.doc.addWidget(action.widgetInfo, point.x()+xOff, point.y()-24)
                    if newWidget != None:
                        nw = redRObjects.getWidgetByIDActiveTabOnly(newWidget)
                        if self.doc.signalManager.signalProcessingInProgress:
                            QMessageBox.information( self, _("Red-R Canvas"), _("Unable to connect widgets while signal processing is in progress. Please wait."))
                        else:
                            self.doc.addLine(start or nw, end or nw)

        elif ev.button() == Qt.RightButton:
            activeItem = self.scene().itemAt(point)
            diff = self.mouseDownPosition - point
            if not activeItem and (diff.x()**2 + diff.y()**2) < 25:     # if no active widgets and we pressed and released mouse at approx same position
                newCoords = QPoint(ev.globalPos())
                self.doc.widgetPopupMenu.showAllWidgets()
                state = [self.doc.widgets()[i].widgetInfo.name for i in range(min(len(self.doc.widgets()), 5))]
                #predictedWidgets = orngHistory.predictWidgets(state, 20)
                #self.doc.widgetPopupMenu.updatePredictedWidgets(predictedWidgets, 'inputClasses')
                self.doc.widgetPopupMenu.updateMenu()
                height = sum([self.doc.widgetPopupMenu.actionGeometry(action).height() for action in self.doc.widgetPopupMenu.actions()])
                action = self.doc.widgetPopupMenu.exec_(newCoords - QPoint(0, self.doc.widgetPopupMenu.categoriesYOffset))
                if action and hasattr(action, "widgetInfo"):
                    newWidget = self.doc.addWidget(action.widgetInfo, point.x(), point.y())
                    

        self.scene().update()
        self.bWidgetDragging = False
        self.doc.canvasDlg.widgetPopup.setEnabled(len(self.getSelectedWidgets()) == 1)

    def mouseDoubleClickEvent(self, ev):
        point = self.mapToScene(ev.pos())
        activeItem = self.scene().itemAt(point)
        if type(activeItem) in [orngCanvasItems.CanvasWidget]:        # if we clicked on a widget
            #print activeItem, _('Item double clicked')
            self.tempWidget = activeItem
            self.openActiveWidget()
        elif type(activeItem) == orngCanvasItems.CanvasLine:
            if self.doc.signalManager.signalProcessingInProgress:
                QMessageBox.information( self, _("Orange Canvas"), _("Please wait until Orange finishes processing signals."))
                return
            self.doc.resetActiveSignals(activeItem.outWidget, activeItem.inWidget, enabled = activeItem.outWidget.instance().outputs.isSignalEnabled(activeItem.inWidget.instance()))
            activeItem.inWidget.updateTooltip()
            activeItem.outWidget.updateTooltip()
            activeItem.updateTooltip()

    # ###########################################
    # Functions for processing events
    # ###########################################

    def progressBarHandler(self, widgetInstance, value):
        for widget in self.doc.widgets():
            if widget.instance() == widgetInstance:
                widget.setProgressBarValue(value)
                qApp.processEvents()        # allow processing of other events
                return

    def processingHandler(self, widgetInstance, value):
        for widget in self.doc.widgets():
            if widget.instance() == widgetInstance:
                widget.setProcessing(value)
                self.repaint()
                widget.update()
                return
              
    # ###########################################
    # misc functions regarding item selection
    # ###########################################

    # return a list of widgets that are currently selected
    def getSelectedWidgets(self):
        return [widget for widget in self.doc.widgets() if widget.isSelected()]

    # return number of items in "items" of type "type"
    def findItemTypeCount(self, items, Type):
        return sum([type(item) == Type for item in items])


