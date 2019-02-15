from Zobjects.States.State import State

class StartPage(State):
    ##############################################################    
    def __init__(self):
        super(StartPage, self).__init__()
        self.loggingPrefix = "State.StartPage"
        
        self.nameShort = "STP"
        self.nameLong = "Start Page"
        
        self.LogMe("Booted")
        
    ##############################################################    
    def Process(self):
        # must call the parent process - see comments on State.Process
        super(StartPage, self).Process()
        
        return self.bb.Get("dm").GetDevice("KeyBoard").ButtonWasPressed("proceed")
        
    ##############################################################     
    def RenderWeb(self):
        buffer = ""
        buffer = buffer + self.WebSnip_Title()        
        buffer = buffer + self.WebSnip_MessageWeb()
        buffer = buffer + self.WebSnip_Proceed()
        
        return buffer