from Base import Base
from Property import Property

class DeviceManager(Base, Property):
    ##############################################################    
    def __init__(self):
        Base.__init__(self)
        Property.__init__(self)
        self.loggingPrefix = "DeviceManager"
                
        self.devices = {}
        self.inSafeMode = True      # Some device should just force to be off in safe mode
        self.timeSec = 0.0
        
        # Start GSS Data
        self.AddGetterSetter("timeSec")
        # End GSS data   
        
        self.EnableSafeMode()       # Call this so we get a log message
        self.LogMe("Booted")
        
    ##############################################################    
    def Tick(self, deltaTimeSec):
        # Loop and tick all the devices  
        # self.LogMe("Tick")

        self.timeSec = self.timeSec + deltaTimeSec       
              
        for deviceName, deviceObject in self.devices.items():
                deviceObject.Tick()
     
    ##############################################################    
    def LoadDevice(self, deviceName):
        fullDeviceName = "Zobjects.Devices." + deviceName + "." + deviceName
        
        # self.LogMe("LoadDevice: do this " + str(fullDeviceName))       
        
        deviceObject = self.MillNewZobject(fullDeviceName)        
        
        if deviceObject == False:
            self.LogMe("LoadDevice: Failed to load device " + str(fullDeviceName))
            return False
            
        # all good - add it to the list
        self.devices[deviceName] = deviceObject
    
    ##############################################################    
    def IsInSafeMode(self):
        return self.inSafeMode

    ##############################################################
    def SetSafeMode(self, safeModeState):        
        self.inSafeMode = safeModeState
        self.LogMe("Safe Set = " + str(self.inSafeMode))

    ##############################################################        
    def EnableSafeMode(self):
        self.LogMe("Safe Mode Enabled")
        self.inSafeMode = True

    ##############################################################
    def DisableSafeMode(self):
        self.LogMe("Safe Mode Disabled")
        self.inSafeMode = False               
        
    ##############################################################    
    def ResetAllDevices(self):
        for deviceName in self.devices:
            device = self.devices[deviceName]
            device.Reset()
        
    ##############################################################    
    def RemoveAllDevices(self):
        for deviceName in self.devices:
            self.RemoveDevice(deviceName)
        
    ##############################################################    
    def RemoveDevice(self, deviceName):
        if deviceName in self.devices:
            deviceObject = self.devices[deviceName]
            deviceObject.ShutDown()
            self.devices[deviceName] = False
            del deviceObject            
        return False
    
    ##############################################################        
    def GetDevice(self, deviceName):
        if deviceName in self.devices:
            return self.devices[deviceName]
        return False                        
        
    
