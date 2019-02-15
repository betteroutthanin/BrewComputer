from Zobjects.Devices.Device import Device

class Dummy(Device):
    ##############################################################    
    def __init__(self):
        super(Dummy, self).__init__()
        self.loggingPrefix = "Device.Dummy"
        
        self.thinkFreqSec = .25
        
        self.ready = True        
        
        self.LogMe("Booted")
        
    ##############################################################        
    def Process(self):
        # self.LogMe("Burp   ")
        pass