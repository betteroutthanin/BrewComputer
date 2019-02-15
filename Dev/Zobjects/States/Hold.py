from Zobjects.States.State import State

class Hold(State):
    ##############################################################    
    def __init__(self):
        super(Hold, self).__init__()
        self.loggingPrefix = "State.Hold"
        self.LogMe("Booted")
        
        self.holdTimeSec = 0
        
        self.nameShort = "HLD"
        self.nameLong = "Hold"
        
        # Start GSS Data
        self.AddGetterSetterSaver("holdTimeSec")
         # End GSS data
        
    ##############################################################    
    def Process(self):
        # must call the parent process - see comments on State.Process
        super(Hold, self).Process()
        
        # have we expired out time        
        thresholdTimeSec = self.holdTimeSec + self.startTimeSec
        timeSec = self.bb.Get("sm").Get("timeSec")
        
        if timeSec > thresholdTimeSec:
            return True
        
        return False        
        
    ##############################################################    
    def RenderWeb(self):
        buffer = ""
        buffer = buffer + self.WebSnip_Title()
        buffer = buffer + self.WebSnip_Temperature()
        buffer = buffer + self.WebSnip_CoreData()
        buffer = buffer + self.WebSnip_MessageWeb()
        
        return buffer    