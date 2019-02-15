from Zobjects.States.State import State

class WaitForInput(State):
    ##############################################################    
    def __init__(self):
        super(WaitForInput, self).__init__()
        self.loggingPrefix = "State.WaitForInput"
        
        self.nameShort = "WFI"
        self.nameLong = "Wait for input"
        
        self.LogMe("Booted")
        
    ##############################################################    
    def Process(self):
        # must call the parent process - see comments on State.Process
        super(WaitForInput, self).Process()
        
        return self.bb.Get("dm").GetDevice("KeyBoard").ButtonWasPressed("proceed")
        
        
        
    ##############################################################    
    def RenderWeb(self):
        buffer = ""
        buffer = buffer + self.WebSnip_Title()
        buffer = buffer + self.WebSnip_Temperature()
        buffer = buffer + self.WebSnip_CoreData()
        buffer = buffer + self.WebSnip_MessageWeb()
        buffer = buffer + self.WebSnip_Proceed()      
        
        return buffer
