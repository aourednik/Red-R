"""
<name>save</name>
<tags>View Data</tags>
"""
from OWRpy import * 
from libraries.base.qtWidgets.lineEdit import lineEdit as redRlineEdit 
from libraries.base.qtWidgets.radioButtons import radioButtons as radioButtons 
from libraries.base.qtWidgets.comboBox import comboBox as redRcomboBox 
from libraries.base.qtWidgets.checkBox import checkBox as redRcheckBox 
from libraries.base.qtWidgets.textEdit import textEdit as redRtextEdit 
from libraries.base.qtWidgets.textEdit import textEdit as redRtextEdit 
from libraries.base.qtWidgets.widgetBox import widgetBox as widgetBox 
from libraries.base.qtWidgets.groupBox import groupBox as groupBox 
from libraries.base.qtWidgets.commitButton import commitButton as commitButton 
import libraries.base.signalClasses as signals
import redRi18n
_ = redRi18n.get_(package = 'base')
class RedRsave(OWRpy): 
    globalSettingsList = ['path','commit']
    def __init__(self, parent=None, signalManager=None):
        OWRpy.__init__(self)
        self.path = os.path.abspath('/')

        self.data = None
        self.inputs.addInput("list", _("R Data"), signals.RVariable.RVariable, self.processlist)
        
        self.fileType = radioButtons(self.controlArea, label=_('Save File Type'),
        buttons = [_('Text'), _('R Data File')], setChecked=_('Text'), orientation='horizontal',callback=self.selectFileType)
        
        self.rDataFileOptions = widgetBox(self.controlArea, orientation='vertical')
        self.varName = redRlineEdit(self.rDataFileOptions,label=_("Variable Name"))        
        self.textFileOptions = widgetBox(self.controlArea, orientation='vertical')
        self.rDataFileOptions.setDisabled(True)
        self.delimiter = radioButtons(self.textFileOptions, label=_('Column Seperator'),
        buttons = {'\t':_('Tab'), ' ':_('Space'), ',':_('Comma'), '?':_('Other')}, setChecked='\t', orientation='horizontal')
        self.otherSepText = redRlineEdit(self.delimiter.box,label=_('Seperator'), displayLabel=False,
        text=';',width=20,orientation='horizontal')
        QObject.connect(self.otherSepText, SIGNAL('textChanged(const QString &)'), lambda: self.delimiter.setChecked('Other'))
        
        
        twoColHolder = groupBox(self.textFileOptions,label=_('File Options'), orientation='horizontal')
        colOne = widgetBox(twoColHolder)
        colTwo = widgetBox(twoColHolder)

        self.fileOptions = redRcheckBox(colOne,label=_('Options'), displayLabel=False,
        buttons=[_('append'),_('quote'),_('row.names'),_('col.names')],
        setChecked = [_('quote'),_('col.names')],
        toolTips = [_('If TRUE, the output is appended to the file.'),
        _(' If TRUE, any character or factor columns will be surrounded by double quotes.'),
        _('a logical value indicating whether the row names of data are to be written.'),
        _('a logical value indicating whether the column names of data are to be written.')],
        orientation='vertical')

        self.eolChr = redRlineEdit(colTwo,label=_('End of line Chr:'),text='\\n',width=50)
        self.naStr = redRlineEdit(colTwo,label=_('Missing Value String:'),text='NA',width=50)
        self.decStr = redRlineEdit(colTwo,label=_('Decimel point Chr:'),text='.',width=50)

        self.qmethod = radioButtons(self.textFileOptions,label=_('Deal with embedded double quote characters '), 
        buttons=[_('escape'),_('double')],
        setChecked=_('escape'),orientation='horizontal')
        
        
        self.browseBox = groupBox(self.controlArea, label=_("Save File"), 
        addSpace = True, orientation='vertical')
        
        box = widgetBox(self.browseBox,orientation='horizontal')
        self.fileLocation = redRlineEdit(box, label=_('File Location'), displayLabel=False, orientation='horizontal')
        
        redRbutton(box, label = _('Browse'), callback = self.browseFile)

        self.commit = commitButton(self.bottomAreaRight, _("Save"), callback = self.commitFunction,processOnInput=True)
    def selectFileType(self):
        if self.fileType.getChecked() ==_('Text'):
            self.textFileOptions.setEnabled(True)
            self.rDataFileOptions.setDisabled(True)
        else:
            self.textFileOptions.setDisabled(True)
            self.rDataFileOptions.setEnabled(True)
            
    def browseFile(self): 
        print self.path
        if self.fileType.getChecked() == _('Text'):
            fn = QFileDialog.getSaveFileName(self, _("Open File"), self.path,
            "Text file (*.txt *.csv *.tab);; All Files (*.*)")
        else:
            fn = QFileDialog.getSaveFileName(self, _("Open File"), self.path,
            "R Data File (*.RData *.rda);; All Files (*.*)")
            
        #print unicode(fn)
        if fn.isEmpty(): return
        fn = unicode(fn)
        self.path = os.path.split(fn)[0]
        # print type(fn), fn
        self.fileLocation.setText(fn)
        
        
    def processlist(self, data):
        if data:
            self.data=data.getData()
            self.varName.setText(self.data)
        else:
            self.data = None
    def commitFunction(self):
        if not self.data or self.fileLocation.text() =='': return
        
        print self.fileType.getChecked(), self.fileType.getChecked() == _('R Data File')
        if self.fileType.getChecked() == _('R Data File'):
           self.R('%s <- %s' %  (unicode(self.varName.text()),self.data))
           self.R('save(%s,file="%s")' % (unicode(self.varName.text()),unicode(self.fileLocation.text())))
        else:
            options = []
            if self.delimiter.getChecked() == _('Tab'): #'tab'
                sep = '\\t'
            elif self.delimiter.getChecked() == _('Space'):
                sep = ' '
            elif self.delimiter.getChecked() == _('Comma'):
                sep = ','
            elif self.delimiter.getChecked() == _('Other'):
                sep = unicode(self.otherSepText.text())

            options.append('sep="%s"' % sep)
            
            options.append('file="'+unicode(self.fileLocation.text())+'"')
          
            for i in self.fileOptions.getChecked():
                options.append(unicode(i) + '=TRUE') 
            for i in self.fileOptions.getUnchecked():
                options.append(unicode(i) + '=FALSE') 
      
            options.append('eol="%s"' % unicode(self.eolChr.text()))
            options.append('na="%s"' % unicode( self.naStr.text()) )
            options.append('dec="%s"' % unicode(self.decStr.text()))
        
            self.R('write.table(%s,%s)' % (self.data, ','.join(options)))
        # index = 0
        # items = []
        # for i in [unicode(a) for (k, a) in self.RFunctionParam_list.items()]:
            # self.R('temp%s<-%s' % (unicode(index), (i)), wantType = 'NoConversion')
            
            # items.append('temp%s' % unicode(index))
            # index += 1
        # self.R('save('+unicode(','.join(items))+','+inj+')', wantType = 'NoConversion')
        # for i in items:
            # self.R('rm(%s)' % i, wantType = 'NoConversion')