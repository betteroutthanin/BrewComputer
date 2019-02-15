import Config
from Base import Base
from Property import Property

class Zobject(Base, Property):
    ##############################################################    
    def __init__(self):
        Base.__init__(self)
        Property.__init__(self)       
        
        self.loggingPrefix = "Zobject"
        
        self.id = -2
        self.type = False
        self.save = True
        
        # Start GSS Data     
        self.AddGetterSetterSaver("id")
        self.AddGetterSetterSaver("type")        
        # End GSS data
        
        # self.LogMe("Booted")