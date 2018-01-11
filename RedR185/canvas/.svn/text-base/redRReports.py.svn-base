import datetime, os, re
import redREnviron
from docutils.core import publish_string
from docutils.writers.odf_odt import Writer, Reader
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import shutil, redRLog

from libraries.base.qtWidgets.widgetBox import widgetBox as redRWidgetBox
from libraries.base.qtWidgets.groupBox import groupBox as redRGroupBox
from libraries.base.qtWidgets.widgetLabel import widgetLabel as redRwidgetLabel
from libraries.base.qtWidgets.listBox import listBox as redRlistBox
from libraries.base.qtWidgets.button import button as redRbutton
from libraries.base.qtWidgets.dialog import dialog as redRdialog
from libraries.base.qtWidgets.treeWidgetItem import treeWidgetItem as redRtreeWidgetItem
from libraries.base.qtWidgets.treeWidget import treeWidget as redRtreeWidget
from libraries.base.qtWidgets.lineEdit import lineEdit
import redRi18n
# def _(a):
    # return a
_ = redRi18n.Coreget_()
def createTable(arrayOfArray,tableName='', columnNames=None):
    # print len(arrayOfArray), len(arrayOfArray[0]), arrayOfArray
    if not arrayOfArray  or len(arrayOfArray) == 0 or len(arrayOfArray[0]) == 0:
        return '';
    if columnNames:
        headers = '  :header: "' + '","'.join(columnNames) + '"'
    else:
        headers = '';

    body = ''
    toAppend = []
    for row in arrayOfArray:
        formatted = []
        for cell in row:
            if type(cell) is not str:
                cell = unicode(cell)
            # cant have any double quotes inside cell text
            if re.search('.. csv-table::|.. image::|::', cell):
                toAppend.append([row[0],cell])
                formatted.append(_('See Below'))
            else:
                cell = cell.replace('"','""')
                formatted.append(cell)

        body += '  "' + '","'.join(formatted) + '"\n'

    body += '\n\n'
    for x in toAppend:
        body += x[0] + '\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n'
        body += x[1] + '\n\n'
        
    text = """
.. csv-table:: %s
%s

%s

""" % (tableName, headers, body)
    return text
    
def createLitralBlock(text):
    if text =='':
        return ''
    else:
        return "::\n\n  " + re.sub(r'\n','\n  ', text)

class reports(QWizard):
    def __init__(self,parent, schema):
        self.schema = schema
        
        QWizard.__init__(self, parent)
        self.setWindowTitle(_('Generate Report'))

        self.selectElements = QWizardPage()
        self.selectElements.setLayout(QVBoxLayout())

        self.selectElements.setTitle(_('Create A Report'))
        self.selectElements.setSubTitle(_('Select the widgets to include in this report.'))
        
        #mainWidgetBox = redRWidgetBox(self.selectElements)

        self.topWidgetBox = redRWidgetBox(self.selectElements)
        #redRwidgetLabel(topWidgetBox,label='Select the widgets to include in the report.')
        
        self.widgetList = redRtreeWidget(self.topWidgetBox, label=_('Widget List'), displayLabel=False)
        self.widgetList.setHeaderLabels([_('Element'), _('Parameters')])

        self.widgetList.setSelectionMode(QAbstractItemView.NoSelection)
        buttonWidgetBox = redRWidgetBox(self.topWidgetBox,orientation='horizontal')
        
        acceptButton = redRbutton(buttonWidgetBox, _('Expand/Collapse'),callback=self.expandCollapse)
        self.expandState=False
        #acceptButton = redRbutton(buttonWidgetBox, _('Expand'),toggleButton=True)
        # QObject.connect(acceptButton, SIGNAL("clicked()"), self.accept)
        QObject.connect(self.widgetList, SIGNAL(" itemClicked (QTreeWidgetItem *,int)"), 
        self.widgetListItemClicked)
        
        QObject.connect(self.widgetList, SIGNAL(" itemChanged (QTreeWidgetItem *,int)"), 
        self.widgetListStateChange)
        
        self.addPage(self.selectElements)
    
    def expandCollapse(self):
        if self.expandState:
            self.widgetList.collapseAll()
            self.expandState = False
        else:
            self.widgetList.expandAll()
            self.expandState = True
    def widgetListItemClicked(self, item,col):
        #print '@@@@@@@@@@@@', col
        if col > 0:
            return
        #print item.data(col, Qt.DisplayRole).type()
        # if item.checkState(0) == Qt.Checked:
            # item.setCheckState(0,Qt.Unchecked)
        # else:
            # item.setCheckState(0,Qt.Checked)
            
        for x in range(item.childCount()):
            child = item.child(x)
            child.setCheckState(0,item.checkState(0))
            for x in range(child.childCount()):
                child.child(x).setCheckState(0,child.checkState(0))
            
        if item.checkState(0) == Qt.Checked:
            # print 'asdfasdf'
            while item.parent():
                item.parent().setCheckState(0,Qt.Checked)
                item = item.parent()
    def widgetListStateChange(self,item,col):
        try:
            if item.checkState(0) == Qt.Checked:
                item.pointer['includeInReports'] = True
            else:
                item.pointer['includeInReports'] = False
            # print item.pointer
        except:
            redRLog.log(redRLog.REDRCORE, redRLog.ERROR, redRLog.formatException())
            #print 'do nothing'
            pass
        
        # import pprint
        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(self.reportData)
  
    def createTreeWidgetItem(self, parent, elementName, dataPointer):
        
        n  = redRtreeWidgetItem(None, [elementName], flags=Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        n.pointer = dataPointer
        
        if dataPointer['includeInReports']:
            n.setCheckState(0,Qt.Checked)
        else:
            n.setCheckState(0,Qt.Unchecked)
            
        parent.addChild(n)
        
        # print '##############',elementName, parent, dataPointer
        
        # parameterBox = QWidget(None)
        # parameterBox.setLayout(QHBoxLayout())
        # parameterBox.setMinimumWidth(200)
        # parameterBox.layout().setSpacing(9)
        #parameterBox.controlArea.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        # parameterBox.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        if 'numChrLimit' in dataPointer.keys():
            a = lineEdit(None,label=_('Word Limit'), text=unicode(dataPointer['numChrLimit']), width=50,
            textChangedCallBack=lambda: self.lineEditChanged(a.text(),dataPointer,'numChrLimit') )
            a.hb.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            # a.hb.setMaximumWidth(100)
            #a.hb.setMinimumWidth(100)
            self.widgetList.setItemWidget(n, 1, a.controlArea)
        if 'numRowLimit' in dataPointer.keys():
            a = lineEdit(None,label=_('Table Row Limit'),text=unicode(dataPointer['numRowLimit']),width=50,
            textChangedCallBack=lambda: self.lineEditChanged(a.text(),dataPointer,'numRowLimit'))
            a.hb.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            self.widgetList.setItemWidget(n, 1, a.controlArea)
        # x = self.widgetList.itemWidget(n,1)
        # print _('x'), x

        # self.widgetList.setItemWidget(n, 1, parameterBox.controlArea)
        # x = self.widgetList.itemWidget(n,1)
        # print _('x'), x
        # for i in x.children():
            # print 'child:', i

        # for i in n.findChildren(QWidget):
            # print i
        
        
        #return n

    def lineEditChanged(self,newValue,dataPointer,key):
        # print '@@@@@@@@@@@@@@@@@@@@@@@@@@', newValue
        try:
            if key in ['numChrLimit', 'numRowLimit']:
                dataPointer[key] = int(newValue)
        except:
            redRLog.log(redRLog.REDRCORE, redRLog.ERROR, redRLog.formatException())
            pass
        # import pprint
        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(self.reportData)
        
    def updateWidgetList(self):
        #topWidgetBox.layout().addWidget(self.widgetList)
        # self.widgetList = redRtreeWidget(self.topWidgetBox, label=_('Widget List'), displayLabel=False)
        # self.widgetList.setHeaderLabels([_('Element'), _('Parameters')])
        
        #print self.widgetNames.keys()
        self.widgetList.clear()
        # self.widgetList.addItems(self.widgetNames.keys())
        # count = int(self.widgetList.count())
        
        for name,widget in self.reportData.items():
            print _('widget name'), name
            w = redRtreeWidgetItem(self.widgetList, [name], 
            flags=Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            w.pointer = self.reportData[name]
            w.setCheckState(0,Qt.Checked);
            
            notesTreeElement = self.createTreeWidgetItem(w, _('Notes'), widget['notes'])
            
            for container, data in widget['reportData'].items():
                if container =='main':
                    parent = w
                else:
                    parent  = redRtreeWidgetItem(None, [container],
                    flags=Qt.ItemIsUserCheckable | Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    #parent.pointer = self.reportData[name]['reportData'][container]
                    parent.setCheckState(0,Qt.Checked)
                    w.addChild(parent)
                
                for elementName, element in data.items():
                    self.createTreeWidgetItem(parent, elementName, self.reportData[name]['reportData'][container][elementName])
                    
        self.widgetList.setColumnWidth(0,250)
        #self.widgetList.resizeColumnToContents(0)

    def createReportsMenu(self,schemaImage=True):
        qname = QFileDialog.getSaveFileName(self, _("Write Report to File"), 
        redREnviron.directoryNames['documentsDir'] + "/Report-"+unicode(datetime.date.today())+".odt", 
        "Open Office Text (*.odt);; HTML (*.html);; LaTeX (*.tex)")
        if qname.isEmpty(): return
        qname = unicode(qname)
        
        name = unicode(qname) # this is the file name of the Report
        # name = os.path.join(redREnviron.directoryNames['redRDir'],'restr.odt')
        
        if os.path.splitext(name)[1].lower() not in [".odt", ".html", ".tex"]: name = name + '.odt'
        
        fileDir = os.path.split(name)[0]
        try:
            fileDir2 = os.path.join(fileDir, os.path.splitext("Data-"+os.path.split(name)[1])[0])
            fileDir2 = fileDir2.replace('\\', '/')
            fd3 = []
            for p in fileDir2.split('/'):
                if len(p) > 8 and ' ' in p:
                    fd3.append(p.replace(' ', '')[:6]+'~1')
                else:
                    fd3.append(p)
            fileDir2 = '/'.join(fd3)
            if os.path.isdir(fileDir2):
                shutil.rmtree(fileDir2)

            # makes a file to place the temp data into.  
            #This will be deleted once the odt file is made.
            os.mkdir(fileDir2)  
        
        except Exception as inst:
            redRLog.log(redRLog.REDRCORE, redRLog.ERROR,redRLog.formatException())
        
        
        # show the report list and allow the user to select widgets to include in the report.
        ## get the report info for the included widgets.
        # reportData = self.getReportData(fileDir2,name)
        import redRObjects
        done = self.createReport(fileDir2,name,redRObjects.instances(),schemaImage)
        if not done:
            return
        if os.name =='nt':
            #os.startfile
            doneDialog = redRdialog(self.schema,title=_("Report Generated"))
            redRwidgetLabel(doneDialog,label=_('Your report is ready to view.'))
            buttonBox = redRWidgetBox(doneDialog,orientation='horizontal')
            acceptButton = redRbutton(buttonBox,_('View Report'))
            QObject.connect(acceptButton, SIGNAL("clicked()"), doneDialog.accept)
            acceptButton = redRbutton(buttonBox,_('Done'))
            QObject.connect(acceptButton, SIGNAL("clicked()"), doneDialog.reject)
            if doneDialog.exec_() == QDialog.Accepted:
                try:
                    os.startfile(name,'open')
                except:
                    redRLog.log(redRLog.REDRCORE, redRLog.ERROR, redRLog.formatException())
                    mb = QMessageBox(_("Cannot Open File"), 
                    _("Red-R cannot open the reports file. Please open the file manually.\nThis is not a problem with Red-R, it is a problem with your document viewer."), 
                    QMessageBox.Information, 
                    QMessageBox.Ok | QMessageBox.Default, QMessageBox.NoButton, QMessageBox.NoButton,self)
                    mb.exec_()

        else:
            QMessageBox.information(self, _("Red-R Canvas"), _("Your report is ready to view."), 
            QMessageBox.Ok + QMessageBox.Default )          
        
    def createReport(self,fileDir,reportName,widgets,schemaImage):
        
        ## very simply we need to loop through the widgets and get some info 
        ## about them and put that into the report.
        self.reportData = {}
        
        progressBar = QProgressDialog()
        progressBar.setCancelButtonText(QString())
        progressBar.setWindowTitle(_('Gathering Report'))
        progressBar.setLabelText(_('Gathering Report'))
        progressBar.setMaximum(len(widgets))
        progressBar.setValue(0)
        progressBar.show()
        progress= 0
        for widget in widgets:
            progressBar.setLabelText(_('Gathering Report Data from %s') % unicode(widget.windowTitle()))
            self.reportData[unicode(widget.windowTitle())] = self.getReportData(fileDir, widget)
            progress += 1
            progressBar.setValue(progress)

        progressBar.close()

        # import pprint
        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(self.reportData)

        self.updateWidgetList()
        if self.exec_() == QDialog.Rejected:
            print _('deleting data')
            del self.reportData
            import gc
            gc.collect()
            print _('done deleting data')
            return False
        

        reportText = self.buildReportHeader(fileDir,schemaImage)
        
        for name, widgetReport in self.reportData.items():
            if widgetReport['includeInReports']:
                reportText+= self.formatWidgetReport(name,widgetReport)
        
        
        if os.path.splitext(unicode(reportName))[1].lower() in [".odt"]:#, ".html", ".tex"]
            reader = Reader()
            writer = Writer()
            output = publish_string(reportText, reader = reader, writer = writer)
            file = open(reportName, 'wb')
            file.write(output)
            file.close()
            #shutil.rmtree(fileDir)

        elif os.path.splitext(unicode(reportName))[1].lower() in [".tex"]:# , ".tex"]
            output = publish_string(reportText, writer_name='latex')#, writer = writer, reader = reader)
            file = open(reportName, 'w')
            file.write(output)
            file.close()
        elif os.path.splitext(unicode(reportName))[1].lower() in [".html"]:# , ".tex"]
            output = publish_string(reportText, writer_name='html')
            # print output
            # print type(output)
            # print unicode(output)
            file = open(reportName, 'w')
            file.write(output)
            file.close()
            
        return True
    def getReportData(self,fileDir,widget):
        widgetReport = {}
        # print '##############################', widget
        #widgetReport['notes'] = widget.instance.notes.getReportText(fileDir)
        # print widget.instance._widgetInfo.widgetName
        d = widget.getReportText3(fileDir)
        # import pprint
        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(d)
        
        data = {'main':{}}
        for k,v in d.items():
            # print '@@@@@@@@@@@@@',widget.caption, k , v
            if 'container' in v.keys():
                if v['container'] in data.keys():
                    data[v['container']][k] = v
                else:
                    data[v['container']] = {}
                    data[v['container']][k] = v
            else:
                data['main'][k] = v
        
        widgetReport['reportData'] = data
        n = widget.notes.getReportText(fileDir)
        widgetReport['notes'] = n['Notes']
        if n['Notes']['text'] =='': widgetReport['notes']['includeInReports'] = False
        widgetReport['includeInReports'] = widget.includeInReport.isChecked()
        return widgetReport
        
    def formatWidgetReport(self, widgetName, widgetReport):
        # import pprint
        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(widgetReport)
        
        if widgetReport['notes']['text'] == '':
            notes = _('No notes were entered in the widget.')
        else:
            notes = createLitralBlock(widgetReport['notes']['text'][0:widgetReport['notes']['numChrLimit']-1])
        
        
        # import pprint
        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(reportData)
        # raise Exception
        
        tables = {}
        for container,data in  widgetReport['reportData'].items():
            tables[container] = []
            for name,data in data.items():
                # print _('data'),name, data
                if data['includeInReports']:
                    if 'type' not in data.keys():
                        text = data['text']
                    elif data['type'] =='litralBlock':
                        text = createLitralBlock(data['text'][0:data['numChrLimit']-1])
                    elif data['type']=='table':
                        colNames = None
                        tableName = ''
                        if 'colNames' in data:
                            colNames = data['colNames'][0:data['numRowLimit']]
                        if 'tableName' in data:
                            tableName = data['tableName']
                            
                        text = createTable(data['data'][0:data['numRowLimit']], 
                        columnNames=colNames, tableName=tableName)

                    tables[container].append([name, text])
        
        # import pprint
        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(tables)
        
        text = createTable(tables['main'],columnNames = ['Parameter',_('Value')],
        tableName=_('Main Parameters'))
        
        for table,data in tables.items():
            if table == 'main': continue
            text += '\n\n'
            text += createTable(data,columnNames = [_('Parameter'),_('Value')],
            tableName=table)

        
        
        
        tt = """
%s
================================================
""" % widgetName
        if widgetReport['notes']['includeInReports']:
            tt += """
Notes
-----

%s
""" % notes
        tt+="""
Widget Output
-------------

%s

""" %  text

        return tt


    def buildReportHeader(self,fileDir,schemaImage):
       ## first take a picture of the canvas and save as png.

        text = """
===========================================
 Red-R Report
===========================================

:Date: %s

.. contents::
.. sectnum::
""" % datetime.date.today()
        
        if schemaImage:
            import redRObjects
            for v in redRObjects.views():
                image = QImage(1000, 700, QImage.Format_ARGB32_Premultiplied)
                painter = QPainter(image)
                
                
                v.scene().render(painter) #
                painter.end()
                imageFile = os.path.join(fileDir, 'canvas-image%s.png' % str(v.name)).replace('\\', '/')
                if not image.save(imageFile):
                    print _('Error in saving schema')
                    print image
                    print image.width(), 'width'
                text += """
Schema %s
===================================================================================================================================
.. image:: %s
  :scale: 50%% 

""" %  (v.name, imageFile)

        return text;
