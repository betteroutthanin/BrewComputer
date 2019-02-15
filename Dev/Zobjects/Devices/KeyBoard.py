import Config
import os
from Zobjects.Devices.Device import Device

if Config.emulationMode == False:
    from evdev import InputDevice, categorize, ecodes, KeyEvent
    from select import select

class KeyBoard(Device):
    ##############################################################    
    def __init__(self):
        super(KeyBoard, self).__init__()
        self.loggingPrefix = "Device.KeyBoard"
        self.thinkFreqSec = 0.2
                
        # self.dev = InputDevice(Config.KeyPadDevice)

        self.buttonList = {}
                
        if Config.emulationMode == False:
            self.buttonList['pause'] = Button('pause', ecodes.KEY_ENTER)
            self.buttonList['proceed'] = Button('proceed', ecodes.KEY_ENTER)
                                    
        else:
            self.buttonList['pause'] = Button('pause', "")
            self.buttonList['proceed'] = Button('proceed', "")
            
            self.buttonList['pc_incHourST'] = Button('pc_incHourST', "")
            self.buttonList['pc_decHourST'] = Button('pc_decHourST', "")
            self.buttonList['pc_incMinST'] = Button('pc_incMinST', "")
            self.buttonList['pc_decMinST'] = Button('pc_decMinST', "")
            self.buttonList['pc_incLT'] = Button('pc_incLT', "")
            self.buttonList['pc_decLT'] = Button('pc_decLT', "")
            self.buttonList['pc_setConfig'] = Button('pc_setConfig', "")
                        
        self.ClearAllButtons()
        self.ready = True        
        
        self.LogMe("Booted")
    
    def Process(self):
    ##############################################################        
        # self.LogMe("Burp   ")       
        # self.PrintAllButtons() 
        pass
        
    ##############################################################    
    def ButtonWasPressed(self, buttonName):
        # self.LogMe("ButtonWasPressed: Check = " + buttonName)
        wasButtonPressed  = False        
        
        if buttonName in self.buttonList:            
            if self.buttonList[buttonName].pressed:
                wasButtonPressed = True
                # self.buttonList[buttonName].pressed = False
                self.ClearAllButtons()
        else:
                self.LogMe("ButtonWasPressed: Button not found " + buttonName)
                
        return wasButtonPressed
             
    ##############################################################    
    def PressButton(self, buttonName):
        #self.LogMe("PressButton: Name = " + buttonName)
        
        if buttonName in self.buttonList:
            self.buttonList[buttonName].pressed = True
        else:
            pass
            #self.LogMe("PressButton: Button not found " + buttonName)
    
    ##############################################################
    def ClearAllButtons(self):
        for buttonName in self.buttonList:
            buttonObject = self.buttonList[buttonName]
            buttonObject.pressed = False
            
    ##############################################################
    def PrintAllButtons(self):
        buffer = ""
        for buttonName in self.buttonList:
            buttonObject = self.buttonList[buttonName]            
            buffer = buffer + " : " + buttonName + " = " + str(buttonObject.pressed) 
        
        self.LogMe(buffer)
            
class Button():
    def __init__(self, name, keyCode):
        self.name = name
        self.keyCode = keyCode
        self.pressed = False