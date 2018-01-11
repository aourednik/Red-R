"""
<name>View Data Table</name>
<tags>View Data</tags>
<icon>datatable.png</icon>
"""

from OWRpy import *
from libraries.base.signalClasses.RDataFrame import RDataFrame as redRRDataFrame
##############################################################################

from libraries.base.qtWidgets.comboBox import comboBox
from libraries.base.qtWidgets.button import button
from libraries.base.qtWidgets.groupBox import groupBox
from libraries.base.qtWidgets.widgetLabel import widgetLabel
from libraries.base.qtWidgets.filterTable import filterTable
from libraries.base.qtWidgets.lineEdit import lineEdit
from libraries.base.qtWidgets.listBox import listBox
from libraries.base.qtWidgets.widgetBox import widgetBox
from libraries.base.qtWidgets.textEdit import textEdit
import redRi18n
_ = redRi18n.get_(package = 'base')
class RDataTable(OWRpy):
    globalSettingsList = ['linkListBox','currentLinks']
    def __init__(self, parent=None, signalManager = None):
        OWRpy.__init__(self, wantGUIDialog = 1)
        
        self.inputs.addInput('id1', _('Input Data Table'), redRRDataFrame, self.dataset) 

        self.data = {}          # dict containing the table infromation
        self.dataParent = None
        self.showMetas = {}     # key: id, value: (True/False, columnList)
        self.showMeta = 1
        self.showAttributeLabels = 1
        self.showDistributions = 1
        self.distColorRgb = (220,220,220, 255)
        self.distColor = QColor(*self.distColorRgb)
        self.locale = QLocale()
        self.currentLinks = {}
        #R modifications
        
        self.currentData = None
        self.dataTableIndex = {}
        self.supressTabClick = False
        self.mylink = ''
        self.link = {}
        #The settings
        self.advancedOptions = widgetBox(self.GUIDialog)
        self.GUIDialog.layout().setAlignment(self.advancedOptions,Qt.AlignTop)
        
        
        self.infoBox = groupBox(self.advancedOptions, label=_("Data Information"))
        self.infoBox.setHidden(True)

        self.rowColCount = widgetLabel(self.infoBox)
        #saveTab = self.tabWidgeta.createTabPage('Save Data')
        saveTab = groupBox(self.advancedOptions,label=_('Save Data'),orientation='horizontal')
        #widgetLabel(saveTab, label=_("Saves the current table to a file."))
        #button(saveTab, label=_("Set File"), callback = self.chooseDirectory)
        #self.fileName = widgetLabel(saveTab, label="")
        self.separator = comboBox(saveTab, label = 'Seperator:', 
        items = [_('Comma'), _('Tab'), _('Space')], orientation = 'horizontal')
        save = button(saveTab, label=_("Save As File"), callback=self.writeFile,
        toolTip = _("Write the table to a text file."))
        saveTab.layout().setAlignment(save,Qt.AlignRight)

        #links:
        linksTab = groupBox(self.advancedOptions, _('Links to Websites'))        
        self.linkListBox = listBox(linksTab,label=_('Links to Websites'), displayLabel=False,includeInReports=False)
        self.linkListBox.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.customLink = lineEdit(linksTab, label = _('Add Link:'), includeInReports=False)
        b = button(linksTab, label = _('Add'), toolTip = _('Adds a link to the link section for interactive data exploration.\nThe link must have a marker for the row information in the form\n{column number}\n\nFor example:http://www.google.com/#q={2}, would do a search Google(TM) for whatever was in column 2 of the row of the cell you clicked.\nYou can test this if you want using the example.'), callback=self.addCustomLink)
        button(linksTab, label = _('Clear Links'), toolTip = _('Clears the links from the links section'), 
        callback = self.clearLinks)
        linksTab.layout().setAlignment(b,Qt.AlignRight)
        widgetLabel(linksTab,label ="""
Creating new links:
http://www.ncbi.nlm.nih.gov/gene/{gene_id}
- Here {gene_id} is a place holder and should be 
  the column name in your table. 
- The value in that column and selected row will 
  replace the place holder. 
          """)
        
        #The table
        self.tableBox = widgetBox(self.controlArea)
        self.tableBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #boxSettings = groupBox(self.advancedOptions, label = _("Settings"))

        self.table = filterTable(self.tableBox,label = _('Data Table'), sortable=True,
        filterable=True,selectionBehavior = QAbstractItemView.SelectItems, callback=self.itemClicked,selectionCallback=self.cellSelection)
        # self.R('data <- data.frame(a=rnorm(1000),b=c("a","b","c","d","e"))')
        # self.table.setRTable('data')
        # self.data = 'data'
        
        self.customSummary = lineEdit(self.advancedOptions, label = _('Custom Summary:'), toolTip = _('Place a custom summary function in here which will be added to the regular summary, use {Col} for the column number.  Ex. mean({Col})'))
        self.summaryLabel = textEdit(self.advancedOptions, label = _('Summary'))
        
    def dataset(self, dataset):
        """Generates a new table and puts it in the table section.  If no table is present the table section remains hidden."""
        if not dataset:
            self.table.clear()
            return
        #print dataset
        self.supressTabClick = True
        #self.table.show()
        self.data = dataset.getData()
        self.dataParent = dataset
            
        if dataset.optionalDataExists('links'):
            linksData = dataset.getOptionalData('links')['data']
            self.linksListBox.update(linksData.keys())
            self.currentLinks.update(linksData)
        
        #self.currentData = dataset.getData()
        dim = dataset.getDims_data()#self.R('dim(' + dataset['data'] + ')')
        self.rowColCount.setText(_('# Row: %(ROWCOUNT)s \n# Columns: %(COLCOUNT)s') %  {'ROWCOUNT':unicode(dim[0]), 'COLCOUNT':unicode(dim[1])})
        self.infoBox.setHidden(False)
        self.table.setRTable(self.data)

        self.supressTabClick = False
    
    
    def cellSelection(self,tmpData):
        # print 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n'
        type = self.R('class('+tmpData+')', wantType = 'Convert', silent = True)
        if type in ['integer', 'complex', 'float', 'numeric']:
            summaryText = _('<strong>Mean</strong>: %(MEAN)s<br/> <strong>Median</strong>: %(MEDIAN)s<br/> <strong>Range</strong>: %(RANGE)s<br/> <strong>Standard Deviation</strong>: %(SD)s<br/> <strong>Count</strong>: %(COUNT)s<br/> <strong>Min</strong>: %(MIN)s<br/> <strong>Max</strong>: %(MAX)s<br/>') % {
                'MEAN':str(self.R('mean(%s)' % tmpData, wantType = 'Convert', silent = True)), 
                'MEDIAN':str(self.R('median(%s)' % tmpData, wantType = 'Convert', silent = True)), 
                'RANGE':str(self.R('range(%s)' % tmpData, wantType = 'Convert', silent = True)), 
                'SD':str(self.R('sd(%s)' % tmpData, wantType = 'Convert', silent = True)), 
                'COUNT':str(self.R('length(%s)' % tmpData, wantType = 'Convert', silent = True)), 
                'MIN':str(self.R('min(%s)'% tmpData, wantType = 'Convert', silent = True)), 
                'MAX':str(self.R('max(%s)' % tmpData, wantType = 'Convert', silent = True))}
        else:
            summaryText = unicode(self.R('summary('+tmpData+')', wantType = 'Convert', silent = True)).replace('\n', '<br/>')        

        self.summaryLabel.setHtml(unicode(summaryText))
        self.working = False
        
    def itemClicked(self, val):
        # print 'item clicked'
        # print self.data
        clickedRow = int(val.row())+1
        clickedCol = int(val.column())+1
        
        for item in self.linkListBox.selectedItems():
            #print item.text()
            #print unicode(self.currentLinks)
            url = self.currentLinks[unicode(item.text())]
            col = url[url.find('{')+1:url.find('}')]
            print 'col', col, type(col)
            if col == 0 or col == 'row': #special cases for looking into rownames
                #cellVal = self.data.getData()['row_names'][val.row()]  
                cellVal = self.R('rownames('+self.data+')['+clickedRow+']')
            else:
                
                #cellVal = self.data.getData()[col][val.row()]  
                cellVal = self.R(self.data+'['+clickedRow+',"'+col+'"]')
            url = url.replace('{'+col+'}', unicode(cellVal))
            #print url
            import webbrowser
            webbrowser.open_new_tab(url)
        return
        ## make the summary of the data.
        type = self.R('class('+self.data+'[,'+str(clickedCol)+'])', wantType = 'Convert', silent = True)
        if type in ['integer', 'complex', 'float', 'numeric']:
            summaryText = _('<strong>Mean</strong>: %(MEAN)s<br/> <strong>Median</strong>: %(MEDIAN)s<br/> <strong>Range</strong>: %(RANGE)s<br/> <strong>Standard Deviation</strong>: %(SD)s<br/> <strong>Count</strong>: %(COUNT)s<br/> <strong>Min</strong>: %(MIN)s<br/> <strong>Max</strong>: %(MAX)s<br/>') % {
                'MEAN':str(self.R('mean(%s[,%s])' % (self.data, clickedCol), wantType = 'Convert', silent = True)), 
                'MEDIAN':str(self.R('median(%s[,%s])' % (self.data, clickedCol), wantType = 'Convert', silent = True)), 
                'RANGE':str(self.R('range(%s[,%s])' % (self.data, clickedCol), wantType = 'Convert', silent = True)), 
                'SD':str(self.R('sd(%s[,%s])' % (self.data, clickedCol), wantType = 'Convert', silent = True)), 
                'COUNT':str(self.R('length(%s[,%s])' % (self.data, clickedCol), wantType = 'Convert', silent = True)), 
                'MIN':str(self.R('min(%s[,%s])' % (self.data, clickedCol), wantType = 'Convert', silent = True)), 
                'MAX':str(self.R('max(%s[,%s])' % (self.data, clickedCol), wantType = 'Convert', silent = True))}
        else:
            summaryText = unicode(self.R('summary('+self.data+'[,'+str(val.column()+1)+'])', wantType = 'Convert', silent = True)).replace('\n', '<br/>')        
        if unicode(self.customSummary.text()) != '':
            summaryText += _('Custom: %s') % unicode(self.R(unicode(self.customSummary.text()).replace('{Col}', '%s[,%s]' % (self.data, val.column()+1)), wantType = 'Convert', silent = True))
        
        self.summaryLabel.setHtml(unicode(summaryText))
        #print summaryText
    
    def clearLinks(self):
        self.linkListBox.clear()
        self.currentLinks = {}
    def addCustomLink(self):
        url = unicode(self.customLink.text())
        self.linkListBox.addItem(url)
        self.currentLinks[url] = url
        self.customLink.clear()
        self.saveGlobalSettings()
        
    def writeFile(self):
        
        if not self.data: 
            self.status.setText('Data does not exist.')
            return
        name = QFileDialog.getSaveFileName(self, _("Save File"), os.path.abspath('/'),
        "Text file (*.csv *.tab *.txt );; All Files (*.*)")
        if name.isEmpty(): return
        name = unicode(name)
        if self.separator.currentId() =='Tab':
            sep  = '\t'
        elif self.separator.currentId() =='Comma':
            sep  = ','
        elif self.separator.currentId() =='Space':
            sep  = ' '
        #use the R function if the parent of the dict is an R object.
        if type(self.data) in [str, unicode]:
            self.R('write.table('+self.data+',file="'+unicode(name)+'", quote = FALSE, sep="'+sep+'")', wantType = 'NoConversion')
        else:  # We write the file ourselves
            if self.dataParent:
                string = ''
                for key in self.dataParent.getData().keys():
                    string += unicode(key)+sep
                string += '\n'
                for i in range(self.dataParent.getItem('length')):
                    for key in self.dataParent.getData().keys():
                        string += self.dataParent.getData()[key][i]+sep
                    string += '\n'
                
                f = open(unicode(name), 'w')
                f.write(string)
                f.close()
            else:
                self.status.setText(_('Can\'t write to a file'))
            
    def changeColor(self):
        color = QColorDialog.getColor(self.distColor, self)
        if color.isValid():
            self.distColorRgb = color.getRgb()
            self.updateColor()

    def updateColor(self):
        self.distColor = QColor(*self.distColorRgb)
        w = self.colButton.width()-8
        h = self.colButton.height()-8
        pixmap = QPixmap(w, h)
        painter = QPainter()
        painter.begin(pixmap)
        painter.fillRect(0,0,w,h, QBrush(self.distColor))
        painter.end()
        self.colButton.setIcon(QIcon(pixmap))


