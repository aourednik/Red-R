from PyQt4.QtCore import *
from PyQt4.QtGui import *
import os.path
import OWGUI
import redREnviron
from redRGUI import widgetState

import redRi18n
_ = redRi18n.get_(package = 'base')
dir = os.path.join(redREnviron.directoryNames["libraryDir"],'base','icons')

dlg_zoom = os.path.join(dir , "Dlg_zoom.png")
dlg_zoom_selection = os.path.join(dir ,  "Dlg_zoom_selection.png")
dlg_pan = os.path.join(dir , "Dlg_pan_hand.png")
dlg_select = os.path.join(dir , "Dlg_arrow.png")
dlg_rect = os.path.join(dir , "Dlg_rect.png")
dlg_poly = os.path.join(dir , "Dlg_poly.png")
dlg_zoom_extent = os.path.join(dir , "Dlg_zoom_extent.png")
dlg_undo = os.path.join(dir , "Dlg_undo.png")
dlg_clear = os.path.join(dir ,  "Dlg_clear.png")
dlg_send = os.path.join(dir ,  "Dlg_send.png")
dlg_browseRectangle = os.path.join(dir , "Dlg_browseRectangle.png")
dlg_browseCircle = os.path.join(dir ,  "Dlg_browseCircle.png")

dlg_zoom_selection = os.path.join(dir ,  "Dlg_zoom_selection.png")
dlg_pan = os.path.join(dir ,  "Dlg_pan_hand.png")
dlg_select = os.path.join(dir ,  "Dlg_arrow.png")
dlg_zoom_extent = os.path.join(dir ,  "dlg_zoom_extent.png")


def createButton(parent, text, action = None, icon = None, toggle = 0):
    btn = QToolButton(parent)
    btn.setMinimumSize(30,30)
    if parent.layout():
        parent.layout().addWidget(btn)
    btn.setCheckable(toggle)
    if action:
        parent.connect(btn, SIGNAL("clicked()"), action)
    if icon:
        btn.setIcon(icon)
    btn.setToolTip(text)
    return btn

class zoomSelectToolbar(QGroupBox,widgetState):
#                (tooltip, attribute containing the button, callback function, button icon, button cursor, toggle)
    IconSpace, IconZoom, IconPan, IconSelect, IconRectangle, IconPolygon, IconRemoveLast, IconRemoveAll, IconSendSelection, IconZoomExtent, IconZoomSelection = range(11)

    DefaultButtons = 1, 4, 5, 0, 6, 7, 8
    SelectButtons = 3, 4, 5, 0, 6, 7, 8
    NavigateButtons = 1, 9, 10, 0, 2

    def __init__(self, widget, parent, graph, autoSend = 0, 
    buttons = (1, 4, 5, 0, 6, 7), name = "Zoom / Select", exclusiveList = "__toolbars"):
        widgetState.__init__(self, widget,'zoomSelectToolbar',includeInReports=False)
        if not hasattr(zoomSelectToolbar, "builtinFunctions"):
            zoomSelectToolbar.builtinFunctions = \
                 (None,
                 (_("Zooming"), "buttonZoom", "activateZooming", QIcon(dlg_zoom), Qt.ArrowCursor, 1),
                 (_("Panning"), "buttonPan", "activatePanning", QIcon(dlg_pan), Qt.OpenHandCursor, 1),
                 (_("Selection"), "buttonSelect", "activateSelection", QIcon(dlg_select), Qt.CrossCursor, 1),
                 (_("Rectangle selection"), "buttonSelectRect", "activateRectangleSelection", QIcon(dlg_rect), Qt.CrossCursor, 1),
                 (_("Polygon selection"), "buttonSelectPoly", "activatePolygonSelection", QIcon(dlg_poly), Qt.CrossCursor, 1),
                 (_("Remove last selection"), "buttonRemoveLastSelection", "removeLastSelection", QIcon(dlg_undo), None, 0),
                 (_("Remove all selections"), "buttonRemoveAllSelections", "removeAllSelections", QIcon(dlg_clear), None, 0),
                 #("Send selections", "buttonSendSelections", "sendData", QIcon(dlg_send), None, 0),
                 (_("Zoom to extent"), "buttonZoomExtent", "zoomExtent", QIcon(dlg_zoom_extent), None, 0),
                 (_("Zoom selection"), "buttonZoomSelection", "zoomSelection", QIcon(dlg_zoom_selection), None, 0)
                )

        QGroupBox.__init__(self, name, parent)
        self.setLayout(QHBoxLayout())
        self.layout().setMargin(6)
        self.layout().setSpacing(4)
        if parent.layout():
            parent.layout().addWidget(self)

        self.graph = graph # save graph. used to send signals
        self.exclusiveList = exclusiveList

        self.widget = None
        self.functions = [type(f) == int and zoomSelectToolbar.builtinFunctions[f] or f for f in buttons]
        for b, f in enumerate(self.functions):
            if not f:
                self.layout().addSpacing(10)
            else:
                button = createButton(self, f[0], lambda x=b: self.action(x), f[3], toggle = f[5])
                setattr(self, f[1], button)
                if f[1] == "buttonSendSelections":
                    button.setEnabled(not autoSend)

        if not hasattr(widget, exclusiveList):
            setattr(widget, exclusiveList, [self])
        else:
            getattr(widget, exclusiveList).append(self)

        self.widget = widget    # we set widget here so that it doesn't affect the value of self.widget.toolbarSelection
        self.action(0)


    def action(self, b):
        f = self.functions[b]
        if not f:
            return

        if f[5]:
            if hasattr(self.widget, "toolbarSelection"):
                self.widget.toolbarSelection = b
            for tbar in getattr(self.widget, self.exclusiveList):
                for fi, ff in enumerate(tbar.functions):
                    if ff and ff[5]:
                        getattr(tbar, ff[1]).setChecked(self == tbar and fi == b)
        getattr(self.graph, f[2])()

        cursor = f[4]
        if not cursor is None:
            self.graph.setCursor(cursor)

    # for backward compatibility with a previous version of this class
    def actionZooming(self): self.action(0)
    def actionRectangleSelection(self): self.action(3)
    def actionPolygonSelection(self): self.action(4)