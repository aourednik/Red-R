"""
<name>Load R Session</name>
<tags>R</tags>
"""
from OWRpy import * 
import redRGUI
from libraries.base.signalClasses.REnvironment import REnvironment as redRREnvironment

from libraries.base.qtWidgets.button import button
from libraries.base.qtWidgets.commitButton import commitButton
from libraries.base.qtWidgets.groupBox import groupBox
from libraries.base.qtWidgets.widgetLabel import widgetLabel
from libraries.base.qtWidgets.fileNamesComboBox import fileNamesComboBox
from libraries.base.qtWidgets.listBox import listBox
from libraries.base.qtWidgets.widgetBox import widgetBox
import redRi18n
_ = redRi18n.get_(package = 'base')
class RLoader(OWRpy): 
    globalSettingsList = ['filecombo','path']

    def __init__(self, parent=None, signalManager=None):
        OWRpy.__init__(self)
        self.outputs.addOutput('id0', _('R Session'), redRREnvironment)

        # print os.path.abspath('/')
        self.path = os.path.abspath('/')
        self.setRvariableNames(['sessionEnviron'])
        
        
        gbox = groupBox(self.controlArea,orientation='vertical',label=_('Select R session'))
        
        box = widgetBox(gbox,orientation='horizontal')
        self.filecombo = fileNamesComboBox(box,label=_('Session File'), displayLabel=False,
        orientation='vertical')
        self.filecombo.setSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.Maximum)

        button(box, label=_('Browse'), callback = self.browseFile)
        self.commit = commitButton(gbox, label=_('Load Session'), callback = self.loadSession,
        alignment=Qt.AlignRight)
        #gbox.layout().setAlignment(self.commit,Qt.AlignRight)
        
        self.infoa = widgetLabel(self.controlArea, '')
        self.varBox = listBox(self.controlArea, label = _('Variables'))
        self.varBox.hide()
        self.infob = widgetLabel(self.controlArea, '')
    
    def browseFile(self): 
        fn = QFileDialog.getOpenFileName(self, _("Open File"), self.path, "R save file (*.RData *.rda);; All Files (*.*)")
        if fn.isEmpty(): return
        fn = unicode(fn)
        self.path = os.path.split(unicode(fn))[0]
        self.filecombo.addFile(fn)
        self.saveGlobalSettings()
        
    def loadSession(self, file = None):
        # open a dialog to pick a file and load it.
        self.R(self.Rvariables['sessionEnviron']+'<-new.env()', wantType = 'NoConversion') # make a new environment for the data
        file = self.filecombo.getCurrentFile()
        
        if not file: return
        self.R('load(\''+file+'\', '+self.Rvariables['sessionEnviron']+')', wantType = 'NoConversion') #load the saved session into a protective environment
        
        
        self.infoa.setText(_('Data loaded from %s') % unicode(file))
        self.varBox.show()
        dataList = self.R('local(ls(), '+self.Rvariables['sessionEnviron']+')', wantType = 'list')
        self.varBox.update(dataList)
        self.infob.setText(_('Please use the R Variable Separator widget to extract your data.'))
        newData = redRREnvironment(data = self.Rvariables['sessionEnviron'])
        self.rSend('id0', newData)
        #self.status.setText('Data sent.')
        
    def customWidgetDelete(self):
        self.R('if(exists("' + self.Rvariables['sessionEnviron'] + '")) { local(rm(ls()), envir = ' + self.Rvariables['sessionEnviron'] + ')}', wantType = 'NoConversion')