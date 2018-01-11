###############Define global data###############
import orngSignalManager

globalData = {}
def _(a):
    return a
def setGlobalData(creatorWidget, name, data, description = None):
    if type(creatorWidget) in [str]:
        widgetID = 'none'
    elif hasattr(creatorWidget, 'widgetID'):
        widgetID = creatorWidget.widgetID
        
    if widgetID not in globalData.keys():
        globalData[widgetID] = {}
    
    globalData[widgetID][name] = {
    'creator': widgetID, 
    'data':data,
    'description':description
    }

def getGlobalData(widget,name):
    parents = orngSignalManager.globalSignalManager.getParents(widget)
    parentIDs = [w.widgetID for w in parents]
    data = []
    for key,value in globalData.items():
        if key in parentIDs and  name in value.keys(): 
            data.append(value[name])
    return data
    
def globalDataExists(widget,name):
    parents = orngSignalManager.globalSignalManager.getParents(widget)
    parentIDs = [w.widgetID for w in parents]
    for key,value in globalData.items():
        if key in parentIDs and  name in value.keys(): 
            return True
    
    return False
    
def removeGlobalData(creatorWidget,name):
    if creatorWidget.widgetID in globalData.keys() and name in globalData[creatorWidget.widgetID].keys():
        del value[name]
