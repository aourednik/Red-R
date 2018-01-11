## redRGUI Graphics View.  A graphics view used for graphing R graphs, this should be as general as possible with an eye to some degree of automation in assignment of items.  

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from redRGUI import widgetState
import redRi18n
_ = redRi18n.get_(package = 'base')
class graphicsScene(QGraphicsView, widgetState):
    def __init__(self, parent, image = None):
        ## want to init a graphics view with a new graphics scene, the scene will be accessable through the widget.
        QGraphicsView.__init__(self, QGraphicsScene(), parent)
        parent.layout().addWidget(self)  # place the widget into the parent widget
        
        if image:
            ## there is an image and we should set that into the graphics scene
            if self.scene:
                self.scene.addItem(QGraphicsPixmapItem(QPixmap(image)))
            else:
                print _('Error, no scene initialized')
                raise Exception
    def clear(self):
        self.scene.clear()
        
    def addImage(self, image):
        ## add an image to the view
        self.scene.addItem(QGraphicsPixmapItem(QPixmap(image)))
    def getSettings(self):
        # print _('in widgetLabel getSettings')
        r = {'text':None}
        # print r
        return r
    def loadSettings(self,data):
        # print _('in widgetLabel loadSettings')
        # print data
        #self.setText(data['text'])
        pass
    def getReportText(self, fileDir):
        #return ''
        pass
        