from redRGUI import widgetState
from libraries.base.qtWidgets.widgetBox import widgetBox
from libraries.base.qtWidgets.groupBox import groupBox
from libraries.base.qtWidgets.widgetLabel import widgetLabel
from libraries.base.qtWidgets.button import button

import redRReports
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import redRi18n
_ = redRi18n.get_(package = 'base')
class textEdit(QTextEdit,widgetState):
    def __init__(self,widget,html='',label=None, displayLabel=True,includeInReports=True, 
    orientation='vertical', alignment=None, editable=True, printable=False,clearable=False,**args):

        widgetState.__init__(self,widget, label,includeInReports)

        QTextEdit.__init__(self,self.controlArea)
        self.label = label
        if displayLabel:
            self.hb = groupBox(self.controlArea,label=label,orientation=orientation)
        else:
            self.hb = widgetBox(self.controlArea,orientation=orientation)

        self.hb.layout().addWidget(self)
        if alignment:
            self.controlArea.layout().setAlignment(self.hb,alignment)
        if printable:
            button(self.hb, _("Print"), self.printMe)
        if clearable:
            button(self.hb, _("Clear"), callback = self.clear)
        if not editable:
            self.setReadOnly(True)
        self.setFontFamily('Courier')
        self.insertHtml(html)
        
        
    def sizeHint(self):
        return QSize(10,10)
    def setCursorToEnd(self):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.setTextCursor(cursor)
    def getSettings(self):
        # print _('in textEdit getSettings')
        r = {'text': self.toHtml()}
        # print r['text']
        return r
    def loadSettings(self,data):
        self.clear()
        self.insertHtml(data['text'])
        # self.setEnabled(data['enabled'])
    def toPlainText(self):
        return unicode(QTextEdit.toPlainText(self))
    def getReportText(self,fileDir):
        limit = min(100000,len(self.toPlainText()))
        return {self.widgetName:{'includeInReports': self.includeInReports, 'type': 'litralBlock',
        'text': self.toPlainText()[0:limit], 'numChrLimit': limit}}
        
    def printMe(self):
        printer = QPrinter()
        printDialog = QPrintDialog(printer)
        if printDialog.exec_() == QDialog.Rejected: 
            print _('Printing Rejected')
            return
        self.print_(printer)
        
