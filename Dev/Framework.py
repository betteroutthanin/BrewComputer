import Config
import time
import datetime
from Base import Base

from DeviceManager import DeviceManager
from StateManager import StateManager

class Framework(Base):
    ##############################################################
    def __init__(self):
        super(Framework, self).__init__()
        self.loggingPrefix = "Framework"
        
        self.Boot()
        
        self.LogMe("Booted")

    ##############################################################
    def Boot(self):
        self.dm = self.bb.Set("dm", DeviceManager())
        self.sm = self.bb.Set("sm", StateManager())
        
        # Load the security code
        securityCode = self.FileGetContents(Config.securityFilePath)
        if (securityCode == "") or (securityCode == False):
            securityCode = "ABCD"                     
        self.bb.Set("securityCode", securityCode)
        self.LogMe("securityCode = " + str(securityCode))        
        
        # device time
        self.BootDevices()
        
        # Recovery Mode
        # Force dm into Safe Mode
        self.dm.EnableSafeMode()
        smBooted = self.sm.BootRecoveryMode()
        if smBooted == False:
            self.LogMe("Boot: Failed to create StateMachine in 'Recovery' mode")
            return False
        self.Loop()
                
        self.LogMe("--------- The Gap Between recovery and normal mode ---------")
        
        # Normal Mode
        # dm can now turn of Safe Mode
        self.dm.DisableSafeMode()
        smBooted = self.sm.BootNormalMode()
        if smBooted == False:
            self.LogMe("Boot: Failed to create StateMachine in 'Normal' mode")
            return False
        self.Loop()
        
        # All Done - lets shutdown the devices
        self.dm.RemoveAllDevices()
        
    ##############################################################
    def BootDevices(self):
        self.dm.LoadDevice("Dummy")
        self.dm.LoadDevice("KeyBoard")
        self.dm.LoadDevice("TemperatureProbe")
        self.dm.LoadDevice("HeatingElement")
        self.dm.LoadDevice("WebServer")

    ##############################################################
    def Loop(self):
        frameWorkLoop = True
        
        oldTimeSec = time.time()

        self.LogMe("Entering FrameWork Main Loop")
        self.LogMe("===================================================")

        while frameWorkLoop:
            # self.LogMe(".")
            startTimeSec = time.time()
            
            # Do the magic - bust out if the statemachine is done
            deltaTimeSec = startTimeSec - oldTimeSec
            frameWorkLoop = self.sm.Tick(deltaTimeSec)
            oldTimeSec = startTimeSec
            
            # self.LogMe("Times start=" + str(startTimeSec) + " old=" + str(oldTimeSec) + " delta=" + str(deltaTimeSec))            
            
            # Device time
            self.dm.Tick(deltaTimeSec)
            
            ######### Time management
            endTimeSec = time.time()
            timeDiffSec = endTimeSec - startTimeSec             
            sleepTimeSec = (1.0 / Config.frameworkFPS) - timeDiffSec

            # Ensure that the sleep call is not called with a negative number
            if (sleepTimeSec < 0):
                self.LogMe("State Loop took too long -> " + str(timeDiffSec) + ", TargetTime = " + str(1.0 / Config.frameworkFPS))
                sleepTimeSec = 0.0

            time.sleep(sleepTimeSec)            

        # End While
        self.LogMe("Loop: Ended")
        return False


