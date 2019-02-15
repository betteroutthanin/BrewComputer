from Zobjects.States.State import State

class Dummy(State):
    ##############################################################    
    def __init__(self):
        super(Dummy, self).__init__()                
        self.loggingPrefix = "State.Dummy"
        
        self.nameShort = "DUM"
        self.nameLong = "Dummy"
        
        self.LogMe("Booted")
        
    ##############################################################    
    def Process(self):
        # must call the parent process - see comments on State.Process
        super(Dummy, self).Process()
        return True
        
        