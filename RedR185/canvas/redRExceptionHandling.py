import sys, traceback,os, re
from datetime import tzinfo, timedelta, datetime
import redRi18n
# def _(a):
    # return a
_ = redRi18n.Coreget_()
def getSafeString( s):
    return unicode(s).replace("<", "&lt;").replace(">", "&gt;")

def formatException(type=None, value=None, tracebackInfo=None, errorMsg = None, plainText=False):
    if not tracebackInfo:
        (type,value, tracebackInfo) =  sys.exc_info()
    
    
    t = datetime.today().isoformat(' ')
    text =  '<br>'*2 + '#'*60 + '<br>'
    if errorMsg:
        text += '<b>' + errorMsg + '</b><br>'
    text += _("Unhandled exception of type %s occured at %s:<br>Traceback:<br>") % ( getSafeString(type.__name__), t)
    list = traceback.extract_tb(tracebackInfo, 10)
    #print list
    space = "&nbsp; "
    totalSpace = space
    #print range(len(list))
    for i in range(len(list)):
        # print list[i]
        (file, line, funct, code) = list[i]
        #print _('code'), code
        
        (dir, filename) = os.path.split(file)
        text += "" + totalSpace + "File: <b>" + filename + "</b>, line %4d" %(line) + " in <b>%s</b><br>" % (getSafeString(funct))
        if code != None:
            if not plainText:
                code = code.replace('<', '&lt;') #convert for html
                code = code.replace('>', '&gt;')
                code = code.replace("\t", "\x5ct") # convert \t to unicode \t
            text += "" + totalSpace + "Code: " + code + "<br>"
        totalSpace += space
    
    lines = traceback.format_exception_only(type, value)
    for line in lines[:-1]:
        text += "" + totalSpace + getSafeString(line) + "<br>"
    text += "<b>" + totalSpace + getSafeString(lines[-1]) + "</b><br>"
    
    text +=  '#'*60 + '<br>'*2
    if plainText:
        text = re.sub('<br>','\n',text)
        text = re.sub('&nbsp;','',text)
        
        text = re.sub("</?[^\W].{0,10}?>", "", text)
        return text
    else:
        return text

