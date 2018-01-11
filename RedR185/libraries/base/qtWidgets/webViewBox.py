from redRGUI import widgetState
from libraries.base.qtWidgets.widgetBox import widgetBox
from libraries.base.qtWidgets.widgetLabel import widgetLabel

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtWebKit
import redRi18n
_ = redRi18n.get_(package = 'base')
class webViewBox(QtWebKit.QWebView,widgetState):
    def __init__(self,widget,label=None, displayLabel=True,includeInReports=True, 
    url=None,orientation='vertical', followHere = False):
        widgetState.__init__(self,widget,label,includeInReports)
        QtWebKit.QWebView.__init__(self,self.controlArea)
        
        if displayLabel:
            hb = widgetBox(self.controlArea,orientation=orientation)
            widgetLabel(hb, label)
            hb.layout().addWidget(self)
        else:
            self.controlArea.layout().addWidget(self)
    
        self.page().setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)
        if not followHere:
            self.connect(self, SIGNAL('linkClicked(QUrl)'), self.followLink)
        if url:
            try:
                self.load(QUrl(url))
            except: pass 
    
    def followLink(self, url):
        import webbrowser
        #print unicode(url)
        #print url.toString()
        webbrowser.open_new_tab(url.toString())

    def sizeHint(self):
        return QSize(10,10)

