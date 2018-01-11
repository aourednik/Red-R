from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSvg import *
from redRGUI import widgetState
from libraries.base.qtWidgets.widgetBox import widgetBox
from libraries.base.qtWidgets.comboBox import comboBox
from libraries.base.qtWidgets.lineEdit import lineEdit 
from libraries.base.qtWidgets.button import button
from libraries.base.qtWidgets.listBox import listBox
from libraries.base.qtWidgets.spinBox import spinBox
import redREnviron, datetime, os, time

class graphicsViewSimple(QGraphicsView, widgetState):
    def __init__(self, parent, name = '', data = None):
        ## want to init a graphics view with a new graphics scene, the scene will be accessable through the widget.
        QGraphicsView.__init__(self, parent)
        self.controlArea = widgetBox(parent)
        self.topArea = widgetBox(self.controlArea)
        self.middleArea = widgetBox(self.controlArea)
        self.bottomArea = widgetBox(self.controlArea)
        self.middleArea.layout().addWidget(self)  # place the widget into the parent widget
        scene = QGraphicsScene()
        self.setScene(scene)
        self.parent = parent