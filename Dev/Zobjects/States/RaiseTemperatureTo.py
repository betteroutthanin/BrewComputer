from Zobjects.States.State import State

class RaiseTemperatureTo(State):
    ##############################################################    
    def __init__(self):
        super(RaiseTemperatureTo, self).__init__()
        self.loggingPrefix = "State.RaiseTemperatureTo"
        
        self.nameShort = "RTT"
        self.nameLong = "Raise temperature to"
        
        self.LogMe("Booted")
        
    ##############################################################    
    def Process(self):        
        # must call the parent process - see comments on State.Process
        super(RaiseTemperatureTo, self).Process()
        
        # threshold time - yah
        targetTemp = self.bb.Get("sm").Get("targetTemperature")
        currentTemp = self.bb.Get("dm").GetDevice("TemperatureProbe").Get("currentTemperature")
        
        # self.LogMe("T = " + str(round(targetTemp, 2)) + " : C = " + str(round(currentTemp, 2)))
        
        if currentTemp > targetTemp:
            return True
            
        # not there yet
        return False
        
    ##############################################################    
    def RenderWeb(self):
        buffer = ""
        buffer = buffer + self.WebSnip_Title()
        buffer = buffer + self.WebSnip_Temperature()
        buffer = buffer + self.WebSnip_CoreData()
        buffer = buffer + self.WebSnip_MessageWeb()
        
        return buffer    