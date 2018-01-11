"""
<name>Read Files</name>
<tags>Data Input</tags>
<icon>readfile.png</icon>
"""

from OWRpy import *
import redRGUI 
import re
import textwrap
import cPickle
import pickle
import types
import redRReports

import libraries.base.signalClasses.RDataFrame as rdf

from libraries.base.qtWidgets.scrollArea import scrollArea
from libraries.base.qtWidgets.checkBox import checkBox
from libraries.base.qtWidgets.comboBox import comboBox
from libraries.base.qtWidgets.button import button
from libraries.base.qtWidgets.textEdit import textEdit
from libraries.base.qtWidgets.radioButtons import radioButtons
from libraries.base.qtWidgets.widgetLabel import widgetLabel
from libraries.base.qtWidgets.fileNamesComboBox import fileNamesComboBox
from libraries.base.qtWidgets.groupBox import groupBox
from libraries.base.qtWidgets.lineEdit import lineEdit
from libraries.base.qtWidgets.widgetBox import widgetBox
import redRi18n
_ = redRi18n.get_(package = 'base')
class readFile(OWRpy):
    
    globalSettingsList = ['filecombo','path']
    def __init__(self, parent=None, signalManager=None):

        OWRpy.__init__(self)
        self.path = os.path.abspath('/')
        self.colClasses = []
        self.myColClasses = []
        self.colNames = []
        self.dataTypes = []
        self.useheader = 1
        
        #set R variable names        
        self.setRvariableNames(['dataframe_org','dataframe_final','filename', 'parent'])
        
        #signals
        self.outputs.addOutput('od1', _('Output Data'), rdf.RDataFrame) #[("data.frame", rdf.RDataFrame)]
        #GUI
        area = widgetBox(self.controlArea,orientation='horizontal',alignment=Qt.AlignTop)       
        #area.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding ,QSizePolicy.MinimumExpanding))
        #area.layout().setAlignment(Qt.AlignTop)
        options = widgetBox(area,orientation='vertical')
        options.setMaximumWidth(300)
        # options.setMinimumWidth(300)
        options.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        #area.layout().setAlignment(options,Qt.AlignTop)
        
        
        self.browseBox = groupBox(options, label=_("Load File"), 
        addSpace = True, orientation='vertical')
        box = widgetBox(self.browseBox,orientation='horizontal')
        self.filecombo = fileNamesComboBox(box, label=_('Files'), displayLabel=False,
        orientation='horizontal',callback=self.scanNewFile)
        self.filecombo.setSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.Minimum)
        button(box, label = _('Browse'), callback = self.browseFile)
        
        self.fileType = radioButtons(options, label=_('File Type'),
        buttons = [_('Text'), _('Excel')], setChecked=_('Text'),callback=self.scanNewFile,
        orientation='horizontal')
        self.fileType.setSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.Minimum)
        self.fileType.hide()

        
        self.delimiter = radioButtons(options, label=_('Column Seperator'),
        buttons = [_('Tab'), _('Comma'), _('Space'),_('Other')], setChecked=_('Tab'),callback=self.scanNewFile,
        orientation='horizontal')
        
        self.otherSepText = lineEdit(self.delimiter.box,label=_('Seperator'), displayLabel=False,
        text=';',width=20,orientation='horizontal')
        QObject.connect(self.otherSepText, SIGNAL('textChanged(const QString &)'), self.otherSep)
        
        self.headersBox = groupBox(options, label=_("Row and Column Names"), 
        addSpace = True, orientation ='horizontal')

        self.hasHeader = checkBox(self.headersBox,label=_('Column Header'), displayLabel=False, 
        buttons = [_('Column Headers')],setChecked=[_('Column Headers')],
        toolTips=[_('a logical value indicating whether the file contains the names of the variables as its first line. If missing, the value is determined from the file format: header is set to TRUE if and only if the first row contains one fewer field than the number of columns.')],
        orientation='vertical',callback=self.scanNewFile)
        
        self.rowNamesCombo = comboBox(self.headersBox,label=_('Select Row Names'), 
        orientation='vertical',callback=self.scanFile)
        #self.rowNamesCombo.setMaximumWidth(250)        
        
        self.otherOptionsBox = groupBox(options, label=_("Other Options"), 
        addSpace = True, orientation ='vertical')
        # box.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        split = widgetBox(self.otherOptionsBox,orientation='horizontal')
        # split.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.otherOptions = checkBox(split,label=_('Options'), displayLabel=False,
        buttons=['fill','strip.white','blank.lines.skip',
        'allowEscapes','StringsAsFactors'],
        setChecked = ['blank.lines.skip'],
        toolTips = [_('logical. If TRUE then in case the rows have unequal length, blank fields are implicitly added.'),
        _('logical. Used only when sep has been specified, and allows the unicodeipping of leading and trailing white space from character fields (numeric fields are always unicodeipped). '),
        _('logical: if TRUE blank lines in the input are ignored.'),
        _('logical. Should C-style escapes such as \n be processed or read verbatim (the default)? '),
        _('logical: should character vectors be converted to factors?')],
        orientation='vertical',callback=self.scanFile)
        # box.layout().addWidget(self.otherOptions,1,1)
        box2 = widgetBox(split,orientation='vertical')
        #box2.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        split.layout().setAlignment(box2,Qt.AlignTop)
        self.quote = lineEdit(box2,text='"',label=_('Quote:'), width=50, orientation='horizontal')
        self.decimal = lineEdit(box2, text = '.', label = _('Decimal:'), width = 50, orientation = 'horizontal', toolTip = _('Decimal sign, some countries may want to use the \'.\''))
        
        self.numLinesScan = lineEdit(box2,text='10',label=_('# Lines to Preview:'), 
        toolTip=_('The maximum number of rows to read in while previewing the file. Negative values are ignored.'), 
        width=50,orientation='horizontal')
        self.numLinesReads = lineEdit(box2,text='-1',label=_('# Lines to Read:'), 
        toolTip=_('Number of lines to read from file. Read whole file if 0 or negative values.'), 
        width=50,orientation='horizontal')

        self.numLinesSkip = lineEdit(box2,text='0',label=_('# Lines to Skip:'),
        toolTip=_("The number of lines of the data file to skip before beginning to read data."), 
        width=50,orientation='horizontal')
        
        holder = widgetBox(options,orientation='horizontal')
        clipboard = button(holder, label = _('Load Clipboard'), 
        toolTip = _('Load the file from the clipboard, you can do this if\ndata has been put in the clipboard using the copy command.'), 
        callback = self.loadClipboard)
        rescan = button(holder, label = _('Rescan File'),toolTip=_("Preview a small portion of the file"),
        callback = self.scanNewFile)
        load = button(holder, label = _('Load File'),toolTip=_("Load the file into Red-R"),
        callback = self.loadFile)
        holder.layout().setAlignment(Qt.AlignRight)

        self.FileInfoBox = groupBox(options, label = _("File Info"), addSpace = True)       
        self.infob = widgetLabel(self.FileInfoBox, label='')
        self.infob.setWordWrap(True)
        self.infoc = widgetLabel(self.FileInfoBox, label='')
        self.FileInfoBox.setHidden(True)
        
        
        self.tableArea = widgetBox(area)
        self.tableArea.setMinimumWidth(500)
        #self.tableArea.setHidden(True)
        self.tableArea.setSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.MinimumExpanding)

        self.scanarea = textEdit(self.tableArea,label= _('File Preview'),includeInReports=False)
        self.scanarea.setLineWrapMode(QTextEdit.NoWrap)
        self.scanarea.setReadOnly(True)
        self.scroll = scrollArea(self.tableArea);
        
        self.columnTypes = widgetBox(self,orientation=QGridLayout(),margin=10);
        self.scroll.setWidget(self.columnTypes)
        #self.columnTypes.layout().setSizeConstraint(QLayout.SetMinAndMaxSize)
        self.columnTypes.setMinimumWidth(460)
        self.columnTypes.layout().setSizeConstraint(QLayout.SetMinimumSize)
        self.columnTypes.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding ,QSizePolicy.MinimumExpanding ))
        self.columnTypes.layout().setAlignment(Qt.AlignTop | Qt.AlignLeft)
        #self.setFileList()
        import sys
        if sys.platform=="win32":
            self.require_librarys(['RODBC'])
            self.setForExcel()
        ##self.require_librarys(['ff'])
    # def rep(self):
        # for x in range(10):
            # self.loadFile()

    def setForExcel(self):
        self.fileType.show()
    def otherSep(self,text):
        self.delimiter.setChecked('other')
        
    def loadCustomSettings(self,settings):
        # import pprint
        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(settings)
        # print settings['colClasses']['pythonObject']
        # self.colClasses = settings['colClasses']['pythonObject']
        # self.colNames = settings['colNames']['pythonObject']
        # self.myColClasses = settings['myColClasses']['list']
        if not self.filecombo.getCurrentFile():
            widgetLabel(self.browseBox,label=_('The loaded file is not found on your computer.\nBut the data saved in the Red-R session is still available.')) 
        # print '#############################', self.colClasses
        # print '#############################', self.colNames
        # print '#############################', self.myColClasses #, settings['myColClasses']['list']
        for i in range(len(self.colClasses)):
            s = radioButtons(self.columnTypes,label=self.colNames[i],displayLabel=False,
            buttons = ['factor','numeric','character','integer','logical'], 
            orientation = 'horizontal', callback = self.updateColClasses)
            
            s.setChecked(self.myColClasses[i])
            if not self.filecombo.getCurrentFile():
                s.setEnabled(False)
            q = widgetLabel(self.columnTypes,label=self.colNames[i])
            self.columnTypes.layout().addWidget(s.controlArea, i, 1)
            self.columnTypes.layout().addWidget(q.controlArea, i, 0)
        
    
    def browseFile(self): 
        print self.path
        fn = QFileDialog.getOpenFileName(self, _("Open File"), self.path,
        "Text file (*.txt *.csv *.tab *.xls);; All Files (*.*)")
        #print unicode(fn)
        if fn.isEmpty(): return
        fn = unicode(fn)
        # print type(fn), fn
        
        self.path = os.path.split(fn)[0]
        self.filecombo.addFile(fn)
        self.saveGlobalSettings()
        self.scanNewFile()

    def scanNewFile(self):
        self.removeInformation()
        self.removeWarning()
        
        if self.fileType.getChecked() == _('Excel'):
            self.delimiter.setDisabled(True)
            self.otherOptionsBox.setDisabled(True)
            self.headersBox.setDisabled(True)
            self.columnTypes.setDisabled(True)
        else:
            self.delimiter.setEnabled(True)
            self.otherOptionsBox.setEnabled(True)
            self.headersBox.setEnabled(True)
            self.columnTypes.setEnabled(True)
        
        for i in self.columnTypes.findChildren(QWidget):
            i.setHidden(True)
          
        self.rowNamesCombo.clear()
        self.colClasses = []
        self.colNames = []
        self.dataTypes = []
        
        self.loadFile(scan=True)
    
    def updateColClasses(self):
        self.myColClasses = []
        for i in self.dataTypes:
            self.myColClasses.append(unicode(i[1].getCheckedId()))
        # print '#####################myColClasses' , self.myColClasses
        self.loadFile(scan=True)
    def scanFile(self):
        self.loadFile(scan=True)

    def loadClipboard(self):
        self.loadFile(scan = 'clipboard')
    
    def loadFile(self,scan=False):
        #print scan
        fn = self.filecombo.getCurrentFile()
        if not fn and not scan == 'clipboard':
            print _('No file selected')
            return
        if not scan =='clipboard':
            self.R('%s <- "%s"' % (self.Rvariables['filename'] , fn)) 
            
            # if os.path.basename(self.recentFiles[self.filecombo.currentIndex()]).split('.')[1] == 'tab':
                # self.delimiter.setChecked('Tab')
            # elif os.path.basename(self.recentFiles[self.filecombo.currentIndex()]).split('.')[1] == 'csv':
                # self.delimiter.setChecked('Comma')
            if self.delimiter.getCheckedId() =='Tab':
                sep  = '\t'
            elif self.delimiter.getCheckedId() =='Comma':
                sep  = ','
            elif self.delimiter.getCheckedId() =='Space':
                sep  = ' '
            elif self.delimiter.getCheckedId() == 'other':
                sep = unicode(self.otherSepText.text())
                
            otherOptions = ''
            for i in self.otherOptions.getCheckedIds():
                otherOptions += unicode(i) + '=TRUE,' 
            
        if 'Column Headers' in self.hasHeader.getChecked():
            header = 'TRUE'
        else:
            header = 'FALSE'
        
        
        if scan and scan != 'clipboard':
            nrows = unicode(self.numLinesScan.text())
            processing=False
        else:
            if int(self.numLinesReads.text()) > 0:
                nrows = unicode(self.numLinesReads.text())
            else:
                nrows = '-1'
            processing=True
        
        
        
        if self.rowNamesCombo.currentIndex() not in [0,-1]:
            self.rownames = self.rowNamesCombo.currentText()
            param_name = '"' + self.rownames + '"'
        else:
            param_name = 'NULL' 
            self.rownames = 'NULL'
        
        cls = []
        for i,new,old in zip(xrange(len(self.myColClasses)),self.myColClasses,self.colClasses):
            if new != old:
                cls.append(self.dataTypes[i][0] + '="' + new + '"')
        
        if len(cls) > 0:
            ccl = 'c(' + ','.join(cls) + ')'
        else:
            ccl = 'NA'
        Runicode = 'None'
        try:
            if self.fileType.getChecked() == _('Excel'):
                Runicode = '%s <- sqlQuery(channel, "select * from [%s]",max=%s)' % (self.Rvariables['dataframe_org'], table,nrows)
                self.R('channel <- odbcConnectExcel(%s)' %(self.Rvariables['filename']))
                table = self.R('sqlTables(channel)$TABLE_NAME[1]')
                if not scan:
                    nrows = '0'
                self.R(RStr,
                processingNotice=processing, wantType = 'NoConversion')
            elif scan == 'clipboard':
                self.R(self.Rvariables['filename']+'<-\'clipboard\'', wantType = 'NoConversion')
                RStr = self.Rvariables['dataframe_org'] + '<- read.table("clipboard", fill = TRUE)'
                self.R(RStr, processingNotice=processing, wantType = 'NoConversion')
                print 'scan was to clipboard'
                self.commit()
            else:
                print 
                RStr = self.Rvariables['dataframe_org'] + '<- read.table(' + self.Rvariables['filename'] + ', header = '+header +', sep = "'+sep +'",quote="' + unicode(self.quote.text()).replace('"','\\"') + '", colClasses = '+ ccl +', row.names = '+param_name +',skip='+unicode(self.numLinesSkip.text())+', nrows = '+nrows +',' + otherOptions + 'dec = \''+unicode(self.decimal.text())+'\')'
                #print '####################', processing
                self.R(RStr, processingNotice=processing, wantType = 'NoConversion')
                
        except:
            import redRLog
            redRLog.log(redRLog.REDRCORE, redRLog.ERROR,redRLog.formatException())
            self.rowNamesCombo.setCurrentIndex(0)
            self.updateScan()
            return
        
        if scan:
            self.updateScan()
        else:
            self.commit()

    def updateScan(self):
        if self.rowNamesCombo.count() == 0:
            self.colNames = self.R('colnames(' + self.Rvariables['dataframe_org'] + ')',wantType='list')
            self.rowNamesCombo.clear()
            self.rowNamesCombo.addItem('NULL','NULL')
            for x in self.colNames:
                self.rowNamesCombo.addItem(x,x)
        self.scanarea.clear()
        # print self.R(self.Rvariables['dataframe_org'])
        # return
        
        data = self.R('rbind(colnames(' + self.Rvariables['dataframe_org'] 
        + '), as.matrix(' + self.Rvariables['dataframe_org'] + '))',wantType='list')
        rownames = self.R('rownames(' + self.Rvariables['dataframe_org'] + ')',wantType='list')
        #print data
        txt = self.html_table(data,rownames)
        # print 'paste(capture.output(' + self.Rvariables['dataframe_org'] +'),collapse="\n")'
        # try:
            #txt = self.R('paste(capture.output(' + self.Rvariables['dataframe_org'] +'),collapse="\n")',processingNotice=True, showException=False)
        # txt = self.R(self.Rvariables['dataframe_org'],processingNotice=True, showException=False)
        
        self.scanarea.setText(txt)
        # except:
            # QMessageBox.information(self,'R Error', _("Try selected a different Column Seperator."), 
            # QMessageBox.Ok + QMessageBox.Default)
            # return
            
        
        try:
            if len(self.colClasses) ==0:
                self.colClasses = self.R('as.vector(sapply(' + self.Rvariables['dataframe_org'] + ',class))',wantType='list')
                self.myColClasses = self.colClasses
                # print '@@@@@@@@@@@@@@@@@@@@@@@@@', self.myColClasses
            if len(self.dataTypes) ==0:
                types = ['factor','numeric','character','integer','logical']
                self.dataTypes = []
                
                for k,i,v in zip(range(len(self.colNames)),self.colNames,self.myColClasses):
                    s = radioButtons(self.columnTypes,label=i,displayLabel=False,
                    buttons=types,orientation='horizontal',callback=self.updateColClasses)
                    
                    # print k,i,unicode(v)
                    if unicode(v) in types:
                        s.setChecked(unicode(v))
                    else:
                        s.addButton(unicode(v))
                        s.setChecked(unicode(v))
                    label = widgetLabel(None,label=i)
                    self.columnTypes.layout().addWidget(label.controlArea,k,0)
                    self.columnTypes.layout().addWidget(s.controlArea,k,1)
                    
                    self.dataTypes.append([i,s])
        except:
            import redRLog
            redRLog.log(redRLog.REDRCORE, redRLog.ERROR,redRLog.formatException())
            self.scanarea.clear()
            self.scanarea.setText(_('Problem reading or scanning the file.  Please check the file integrity and try again.'))
        
        # print self.getReportText('./')
          
    def html_table(self,lol,rownames):
        s = '<table border="1" cellpadding="3">'
        s+= _('  <tr><td>Rownames</td><td><b>')
        s+= '    </b></td><td><b>'.join(lol[0])
        s+= '  </b></td></tr>'
        
        for row, sublist in zip(rownames,lol[1:]):
            s+= '  <tr><td><b>' +row + '</b></td><td>'
            s+= '    </td><td>'.join(sublist)
            s+= '  </td></tr>'
        s+= '</table>'
        return s
        
    def updateGUI(self):
        dfsummary = self.R('dim('+self.Rvariables['dataframe_org'] + ')', wantType='list',silent=True)
        self.infob.setText(self.R(self.Rvariables['filename']))
        self.infoc.setText(_("Rows: %(ROWS)s\nColumns: %(COLS)s") % {'ROWS':unicode(dfsummary[0]), 'COLS':unicode(dfsummary[1])})
        self.FileInfoBox.setHidden(False)
    def commit(self):
        self.updateGUI()
        sendData = rdf.RDataFrame(data = self.Rvariables['dataframe_org'], parent = self.Rvariables['dataframe_org'])
        self.rSend("od1", sendData)
    
  