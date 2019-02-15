import Config
from Zobjects.States.State import State
from StateManager import StateManager

class Recovery(State):
    ##############################################################    
    def __init__(self):
        super(Recovery, self).__init__()
        self.loggingPrefix = "State.Recovery"
        
        # Normally these details are loaded in from the json file
        # Force them to emulate the loading
        self.id = 0
        self.type = "Zobjects.States.Recovery.Recovery"
        
        self.nameShort = "REC"
        self.nameLong = "Recovery"
        
        self.oldSM = False
        self.newSM = False
        
        self.LogMe("Booted")
        
    ##############################################################    
    def OnEntry(self):
        super(Recovery, self).OnEntry()
        
        self.EnableQuiteMode()
        self.oldSM = StateManager()
        if self.oldSM.LoadStateMachineFromDisk(Config.currentStateMachine) == False:
            self.oldSM = False
            
        
        self.newSM = StateManager()
        if self.newSM.LoadStateMachineFromDisk(Config.newStateMachine) == False:
            self.newSM = False
        self.DisableQuiteMode()
        
        return True
        
    ##############################################################    
    def Process(self):
        # must call the parent process - see comments on State.Process        
        super(Recovery, self).Process()
        
        sm = self.bb.Get("sm")
        timeSec = sm.Get("timeSec")
        
        # if both the new and old are invalid then shit is really broken
        if (self.oldSM == False) and (self.newSM == False):
            return False
        
        # If there is nothing to recover then just punch out and exit recovery mode completely
        if self.oldSM == False:
            self.LogMe("Process: No previous Statemachine found - recovery mode not need")
            sm.Set("recoverOldStateMachine", False)
            return True
            
        
        
        # Pressing the button implies that the user wants to dump the old stateMachine and start fresh
        buttonPressed = self.bb.Get("dm").GetDevice("KeyBoard").ButtonWasPressed("proceed")
        if buttonPressed == True:
            sm.Set("recoverOldStateMachine", False)
            self.LogMe("Process: User pressed the proceed button - recoverOldStateMachine=False")
            return True
        
        # Keeping checking for to see if the timer expires - if so, then recover the old stateMachine        
        thresholdTimeSec = Config.recoveryTimeOutSec + self.startTimeSec
        if timeSec > thresholdTimeSec:
            sm.Set("recoverOldStateMachine", True)
            self.LogMe("Process: Timeout - recoverOldStateMachine=True")            
            return True
        
        # Else - keep on ticking
        return False
        
    ##############################################################     
    def RenderWeb(self):
        
        oldTitle = False
        newTitle = False
        
        # We want to show the titles of the old and new statemachines
        if self.oldSM:
            oldTitle = self.oldSM.Get('name')
            
        if self.newSM:
            newTitle = self.newSM.Get('name')
         
        timeLeftSec = (self.startTimeSec + Config.recoveryTimeOutSec) -  self.bb.Get("sm").Get("timeSec")
        buffer = ""        
        buffer = buffer + "<div class='title'>Recover Mode</div>"
        
        # if both the new and old are invalid then shit is really broken
        if (self.oldSM == False) and (self.newSM == False):
            buffer = buffer + "<div class='proceed'>Can't proceed</div>"
            buffer = buffer + "<div class='proceed'>Old and New are both missing</div>"
            buffer = buffer + "<div class='proceed'>What have you done!</div>"
            return buffer
            
        buffer = buffer + "<div class='proceed'>Time Left: " + str(int(timeLeftSec)) + "</div>"
        buffer = buffer + "<div class='message'>Press PROCEED to dump the OLD run and load the NEW run<br><br>or<br><br>Wait and the OLD run will recover</div>" 
        if oldTitle:
            buffer = buffer + "<div class='proceed'>OLD = " + str(oldTitle) + "</div>"
        if newTitle:
            buffer = buffer + "<div class='proceed'>NEW = " + str(newTitle) + "</div>"
        
        return buffer