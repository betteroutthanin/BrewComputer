import Config
from BlackBoard import BlackBoard

import string
import random
import os.path

class Base(object):
    lastLogPrefix = ""
    quiteMode = False

    ##############################################################    
    def __init__(self):
        self.loggingPrefix = "Base"
        self.bb = BlackBoard.Instance()
        # self.LogMe("Base Created")
        
    ##############################################################
    def Here(self, message):        
        self.LogMe("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        self.LogMe("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        self.LogMe(message)
        self.LogMe("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        self.LogMe("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        while True:
            pass                

    ##############################################################
    def LogMe(self, message):    
        prefix = ""
        
        if Base.quiteMode:
            return
        
        if (Base.lastLogPrefix == self.loggingPrefix):
            prefix =  " " * len(self.loggingPrefix)
        else:
            prefix = self.loggingPrefix
    
        Base.lastLogPrefix = self.loggingPrefix
        print("- " + prefix + ":" + str(message))
        
    ##############################################################
    def EnableQuiteMode(self):
        Base.quiteMode = True
        
    ##############################################################
    def DisableQuiteMode(self):
        Base.quiteMode = False
        
    ##############################################################
    def id_generator(self, size=20, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    ##############################################################
    def FileGetContents(self, path):
        if os.path.isfile(path): 
            file = open(path,'r')
            buffer = file.read()
            file.close()
            return buffer
            
        else:
            return False
            
    ##############################################################
    def FileGetContentsBinMode(self, path):
        if os.path.isfile(path): 
            file = open(path,'rb')
            buffer = file.read()
            file.close()
            return buffer
            
        else:
            return False

    ##############################################################
    def FilePutContents(self, path, buffer):
        file = open(path,'w')
        file.write(buffer)
        file.close()
        
     ##############################################################
    def MillNewZobject(self, zobjectType):
        # self.LogMe("Attempting to Mill new object for -> " + zobjectType)
        m = self.GetClass(zobjectType)
        object = m()
        return object
        
     ##############################################################
    def GetClass(self, name):
        parts = name.split('.')
        module = ".".join(parts[:-1])
        m = __import__( module )
        for comp in parts[1:]:
            m = getattr(m, comp)
        return m