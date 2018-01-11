"""
<name>Dummy</name>
<tags>R</tags>
<icon>dummy.png</icon>
"""
from OWRpy import * 
import redRGUI
from libraries.base.qtWidgets.groupBox import groupBox
from libraries.base.qtWidgets.widgetLabel import widgetLabel
import redRi18n
_ = redRi18n.get_(package = 'base')
class dummy(OWRpy): 
    settingsList = []
    def __init__(self, parent=None, signalManager=None, forceInSignals = None, forceOutSignals = None):
        OWRpy.__init__(self)
        print unicode(forceInSignals) +' and ' + unicode(forceOutSignals) + ' appending to dummy'
        if forceInSignals: 
            import signals
            for (a, b) in [signal for signal in forceInSignals]:
                print 'Appending ' + unicode(a) + ' in dummy to the '+unicode(b)+' signal'
                self.inputs.addInput((a, a, b, None))
        if forceOutSignals:
            import signals
            for (a, b) in [signal for signal in  forceOutSignals]:
                print 'Appending ' +unicode(a)+' in dummy using the '+unicode(b)+' signal'
                self.outputs.addOutput((a, a, b))
        print self.inputs
        print self.outputs
            
        box = groupBox(self.controlArea, label=_("Info"))
        self.infoa = widgetLabel(box, _("A widget failed to load this was put in it's place."))
        self.infob = widgetLabel(box, _("The variables that were saved with this widget are %s .\n You can use R Executor to retrieve these variables and incorporate them into your schema.") % str(self.linksOut))
        
    