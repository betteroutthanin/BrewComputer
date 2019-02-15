import Config
from Zobjects.Devices.Device import Device

class TemperatureProbe(Device):
    ##############################################################    
    def __init__(self):
        super(TemperatureProbe, self).__init__()
        
        self.loggingPrefix = "Device.TemperatureProbe"
        
        self.thinkFreqSec = .25
        self.currentTemperature = 0
        
        if Config.emulationMode == True:
            self.currentTemperature = 25
        
        self.ready = True        
        
        # Start GSS Data
        self.AddGetter("currentTemperature")        
        # End GSS Data
        
        self.LogMe("Booted")
        
    ##############################################################        
    def Process(self):
        if Config.emulationMode == True:
            self.ProcessEmulation()
            return True
        
        # Normal mode
            
    ##############################################################        
    def ProcessEmulation(self):
        elementState = self.bb.Get("dm").GetDevice("HeatingElement").Get("heatingElement")
        if elementState == True:
            self.currentTemperature = self.currentTemperature + 0.2
        else:
            self.currentTemperature = self.currentTemperature - 0.1
            
        if self.currentTemperature < 0:
            self.currentTemperature = 0