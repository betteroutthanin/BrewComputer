import Config
import HeatTypes
from Zobjects.Devices.Device import Device

class HeatingElement(Device):
    ##############################################################    
    def __init__(self):
        super(HeatingElement, self).__init__()        
        self.loggingPrefix = "Device.HeatingElement"
        
        self.thinkFreqSec = 0.25
        self.ready = True
        
        self.heatingElement = False
        
        # Element control settings
        self.autoFullModeDelta = 10.0    # Use Full Mode until we are this far from target temp
        self.autoMaxDutyMS = 4000
        self.autoLowDutyMS = 1000
        self.autoHighDutyMS = 3000
        self.autoNextThingSec = 0.0        
        
        # Start GSS Data
        self.AddGetter("heatingElement")        
        # End GSS Data
        
        self.LogMe("Booted")
                
    ##############################################################        
    def Process(self):
        # Exit early and turn off the element if we are in safe mode         
        if self.bb.Get("dm").IsInSafeMode():                        
            self.ElementOff()            
            return
            
        # Todo - exit and off if there is no temp probe
        
        # Todo - exit and off if the SM is paused           
            
        # Exit early and turn off the element if the heatType is Off
        if self.bb.Get("sm").Get("heatType") == HeatTypes.off:
            self.ElementOff()
            return
            
        # Final fail safe - Just in-case there is some really bad logic later in processing paths
        targetTemp = self.bb.Get("sm").Get("targetTemperature")
        currentTemp = self.bb.Get("dm").GetDevice("TemperatureProbe").Get("currentTemperature")
        if (currentTemp + Config.softEdge) > targetTemp:
            self.ElementOff()
            return 
            
        if self.bb.Get("sm").Get("heatType") == HeatTypes.full:
            self.ProcessHeatFull()        
            
        if self.bb.Get("sm").Get("heatType") == HeatTypes.auto:
            self.ProcessHeatAuto()            
   
    ##############################################################        
    def ProcessHeatFull(self):
        self.ElementOn()
        
     ##############################################################        
    def ProcessHeatAuto(self):
        targetTemp = self.bb.Get("sm").Get("targetTemperature")
        currentTemp = self.bb.Get("dm").GetDevice("TemperatureProbe").Get("currentTemperature")

        # Use full heat mode until we get with autoFullModeDelta of target temp
        if currentTemp < (targetTemp - self.autoFullModeDelta):
            self.ProcessHeatFull()
            return
            
        # is AutoMode ready to think - use dm instead of sm - this is due to the fact that the sm time can be paused
        # this will result in the elment being left of        
        timeSec = self.bb.Get("dm").Get("timeSec")
        
        if timeSec > self.autoNextThingSec:
            if self.heatingElement == True:
                self.ElementOff()
            else:
                self.ElementOn()
                
            self.autoNextThingSec = timeSec + ((self.autoMaxDutyMS / 1000 )/ 2)            
            
    ##############################################################        
    def ElementOn(self):
        self.heatingElement = True        
        
    ##############################################################        
    def ElementOff(self):
        self.heatingElement = False
                