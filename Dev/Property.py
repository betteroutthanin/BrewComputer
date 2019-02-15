import Config
from BlackBoard import BlackBoard

class Property(object):
    ##############################################################    
    def __init__(self):
        self.getList = []
        self.setList = []
        self.saveList = []        
        
    ##############################################################    
    def Get(self, varName):
        if varName in self.getList:
            return getattr(self, varName)
        
        return False
        
    ##############################################################    
    def Set(self, varName, value):
        if varName in self.setList:
            setattr(self, varName, value)
        
    ##############################################################    
    def AddSaver(self, varName):
        if varName not in self.saveList:
            self.saveList.append(varName)
            #print "Saver added " + varName
        
    ##############################################################    
    def AddSetter(self, varName):
        if varName not in self.setList:
            self.setList.append(varName)
            #print "Setter added " + varName
        
    ##############################################################
    def AddGetter(self, varName):
        if varName not in self.getList:
            self.getList.append(varName)
            #print "Getter added " + varName
        
    ##############################################################
    def AddGetterSetter(self, varName):
        self.AddSetter(varName)
        self.AddGetter(varName)
        
    ##############################################################
    def AddGetterSetterSaver(self, varName):
        self.AddSetter(varName)
        self.AddGetter(varName)        
        self.AddSaver(varName)

    ##############################################################
    def SaveListToJson(self):
        jsonData = {}                
        for valueName in self.saveList:
            jsonData[valueName] = getattr(self, valueName)
            
        return jsonData
    