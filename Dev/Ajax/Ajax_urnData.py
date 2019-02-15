import Config
from Ajax.Ajax import Ajax
from BlackBoard import BlackBoard
import time

class Ajax_urnData(Ajax):
    ##############################################################
    def __init__(self):
        super(Ajax_urnData, self).__init__()
        self.loggingPrefix = "Ajax_urnData"
        
    def Process(self, requestHandler):                
        bb = BlackBoard.Instance()
        
        stateObjectID = self.bb.Get("sm").Get("currentStateID")        
        stateObject = self.bb.Get("sm").GetState(stateObjectID)

        if stateObject == False:
            return
            
        contents = stateObject.RenderWeb()
        requestHandler.SendSimplePage(contents)  
        
        '''    
        # route based on state
        if stateObject.Get("type") == "Zobjects.States.Recovery.Recovery":
            self.ProcessRecover(requestHandler)
        else:
            self.ProcessNormal(requestHandler)
        '''
            
'''
    ##############################################################
    def ProcessRecover(self, requestHandler):
        bb = BlackBoard.Instance()                
        stateObjectID = self.bb.Get("sm").Get("currentStateID")        
        stateObject = self.bb.Get("sm").GetState(stateObjectID)
        if stateObject == False:
            return                       
            
        startSec = stateObject.Get("startTimeSec")
        currentTimeSec = self.bb.Get("sm").Get("timeSec")
        timeLeftSec = (startSec + Config.recoveryTimeOutSec) -  currentTimeSec

        message = ""
        message = message + "Recover Mode<br>"
        message = message + "Time Left: " + str(int(timeLeftSec)) + "<br>"                
        
        requestHandler.SendSimplePage(message)            
               
               
    ##############################################################               
    def ProcessNormal(self, requestHandler):
        bb = BlackBoard.Instance()                
        stateObjectID = self.bb.Get("sm").Get("currentStateID")        
        stateObject = self.bb.Get("sm").GetState(stateObjectID)
        if stateObject == False:
            return                       
        
        currentTemp = bb.Get("dm").GetDevice("TemperatureProbe").Get("currentTemperature")
        targetTemp = targetTemp = self.bb.Get("sm").Get("targetTemperature")
        elementState = bb.Get("dm").GetDevice("HeatingElement").Get("heatingElement")
        safeMode = bb.Get("dm").IsInSafeMode()      
        webMessage = stateObject.Get("messageWeb")
        stateID = self.bb.Get("sm").Get("currentStateID")
        stateRenderData = stateObject.RenderWeb()
        smPausedStatus = self.bb.Get("sm").Get("paused")
        timeInStateSec = self.bb.Get("sm").Get("timeSec") - stateObject.Get("startTimeSec")
        timeInStateMessage = time.strftime('%H:%M:%S', time.gmtime(timeInStateSec))
        
        message = ""
        message = message + stateObject.loggingPrefix +" ( " + str(stateID) + " )<br>"
        message = message + "Current Temp = " + str(round(currentTemp, 2)) + "<br>"
        message = message + "Target Temp = " + str(round(targetTemp, 2)) + "<br>"
        message = message + "Element State = " + str(elementState) + "<br>"
        message = message + "Safe Mode = " + str(safeMode) + "<br>"
        message = message + "Paused= " + str(smPausedStatus) + "<br>"
        message = message + "timeInStateSec= " + timeInStateMessage + "<br>"
        message = message +  webMessage + "<br>"        
        message = message +  stateRenderData + "<br>"
        requestHandler.SendSimplePage(message)
 '''