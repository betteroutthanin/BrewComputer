from Zobjects.Zobject import Zobject

class Device(Zobject):
    ##############################################################    
    def __init__(self):
        super(Device, self).__init__()
        self.loggingPrefix = "Device"
        
        self.nextThinkSec = 0.0                # New Nextthink threshold
        self.thinkFreqSec = 1.0                # A nice fat base line
        
        self.ready = False        
        
        # self.LogMe("Booted")

    ##############################################################        
    def Process(self):
        self.LogMe("Burp")
        
    ##############################################################        
    def Reset(self):
        self.nextThinkSec = 0.0                  
            
    ##############################################################    
    def Tick(self):
        readyToProcess = self.ReadyToThink()
        
        if readyToProcess == True:
            # Ready to think, call the main process function
            self.Process()
            return True
            
        # not ready to think
        return False
            
    ##############################################################
    def ReadyToThink(self):
        currentSec = self.bb.Get("dm").Get("timeSec")
        
        if (currentSec > self.nextThinkSec):
            # Reset the next think
            self.nextThinkSec = currentSec + self.thinkFreqSec
            return True
        else:
            return False
    
    ##############################################################        
    def ShutDown(self):
        pass