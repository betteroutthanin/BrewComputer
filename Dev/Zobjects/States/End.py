from Zobjects.States.State import State

class End(State):
    ##############################################################    
    def __init__(self):
        super(End, self).__init__()
        self.loggingPrefix = "State.End"
        
        self.nameShort = "END"
        self.nameLong = "End"
        
        self.type = "Zobjects.States.End.End"
        self.messageWeb = "The run is now complete\nEnjoy the clean up :)"
        self.messageLCD = ""
        
        self.LogMe("Booted")

    def OnEntry(self):
        super(End, self).OnEntry()
        self.bb.Get("dm").EnableSafeMode()        
        
    ##############################################################    
    def Process(self):
        # must call the parent process - see comments on State.Process
        super(End, self).Process()
        
        # Force the heater off by setting the target temp to something really low      
        targetTemp = self.bb.Get("sm").Set("targetTemperature", 0)  
        
        # Never end
        return False
        
    ##############################################################    
    def RenderWeb(self):
        buffer = ""
        buffer = buffer + self.WebSnip_Title()
        buffer = buffer + self.WebSnip_Temperature()
        buffer = buffer + self.WebSnip_CoreData()
        buffer = buffer + self.WebSnip_MessageWeb()
        
        return buffer            