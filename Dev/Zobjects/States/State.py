import HeatTypes
from Zobjects.Zobject import Zobject
from BlackBoard import BlackBoard
import datetime

class State(Zobject):
    ##############################################################    
    def __init__(self):
        super(State, self).__init__()                
        self.loggingPrefix = "State"        
        
        self.startTimeSec = 0.0
        self.targetTemperature = 0.0
        self.heatType = HeatTypes.off                 
        self.messageWeb = "Web Message Missing"
        self.messageLCD = "LCD Message Missing"
        
        self.nameShort = "SNA"
        self.nameLong = "State Name"
        
        # Start GSS Data
        self.AddGetterSetterSaver("startTimeSec")
        self.AddGetterSetterSaver("targetTemperature")
        self.AddGetterSetterSaver("heatType")
        self.AddGetterSetterSaver("messageWeb")
        self.AddGetterSetterSaver("messageLCD")
        self.AddGetterSetter("nameShort")
        self.AddGetterSetter("nameLong")
        # End GSS data
        
        # self.LogMe("Booted")

    ##############################################################    
    def Process(self):
        # Nothing here yet
        
        return True
        
    ##############################################################    
    def OnEntry(self):
        self.startTimeSec = self.bb.Get("sm").Get("timeSec")
        self.bb.Get("sm").Set("targetTemperature", self.targetTemperature)
        self.bb.Get("sm").Set("heatType", self.heatType)
        
        self.LogMe("OnEntry: State ID = " + str(self.id) + " :startTimeSec = " + str(round(self.startTimeSec, 2)))
        
        return True
        
    ##############################################################    
    def OnExit(self):
        self.LogMe("OnExit: State ID = " + str(self.id))        
        
        return True       
        
    ##############################################################    
    def RenderWeb(self):
        buffer = "RenderWeb"
        return buffer
        
    ##############################################################    
    def RenderLCD(self):
        buffer = "RenderLCD"
        return buffer
        

    ##############################################################    
    def WebSnip_Title(self):
        title = self.bb.Get("sm").Get("name")
        
        buffer = """
        <div class='title'>
        {title}
        </div>        
        """    
       
        finalOutput = buffer.format(title = title)
        return finalOutput
        
    ##############################################################    
    def WebSnip_StateMachineData(self):
        buffer = ""
        return buffer
        
    ##############################################################    
    def WebSnip_Proceed(self):
        buffer = """
        <div class='proceed'>
            Press PROCEED to continue        
        </div>        
        """        
        return buffer

    ##############################################################    
    def WebSnip_MessageWeb(self):        
        message = self.messageWeb.replace('\n', '<br>')
        
        buffer = """
        <div class='message'>
            {message}        
        </div>        
        """        
        finalOutput = buffer.format(message = message)
        return finalOutput
        
    ##############################################################    
    def WebSnip_CoreData(self):
        buffer = """        
        <div class='coredata'>{stateDetails}</div>       
        <div><table class='coredata'>
            <tr>
                <th>Time</th> <th>Heater</th> <th>Misc</th>
            </tr>            
            <tr>
                <td>                
                    <table class='coredata'>
                        <tr>
                            <td>Total</td><td>{timeTotal}</td>
                        </tr>
                        <tr>
                            <td>In State</td><td>{timeState}</td>
                        </tr>
                        <tr>
                            <td>Left</td><td>{timeLeft}</td>
                        </tr>
                    </table>
                </td>
                <td>
                     <table class='coredata'>
                        <tr>
                            <td>State</td><td>{heaterState}</td>
                        </tr>
                        <tr>
                            <td>Type</td><td>{heaterType}</td>
                        </tr>
                    </table>
                </td>
                <td>
                     <table class='coredata'>
                        <tr>
                            <td>P Errors</td><td>{pErrors}</td>                            
                        </tr>
                        <tr>
                            <td>Safe Mode</td><td>{safeMode}</td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table></div>"""

        # State Details
        stateDetails =self.Get("nameLong")

        # Total time        
        totalTimeSec = int(self.bb.Get("sm").Get("timeSec"))
        timeTotal = datetime.timedelta(seconds = totalTimeSec)
        
        # Time in State
        stateStartTimeSec = int(self.Get("startTimeSec"))        
        timeState = datetime.timedelta(seconds = totalTimeSec - stateStartTimeSec)
        
        # Time left is a little more complex
        holdTimeSec =  int(self.Get("holdTimeSec"))        
        if holdTimeSec != False:
            thresholdTimeSec = holdTimeSec + stateStartTimeSec
            timeLeftSec = thresholdTimeSec - totalTimeSec       
            timeLeft = datetime.timedelta(seconds = timeLeftSec)
        else:
            timeLeft = "NA"
        
        # Heating Element stuff
        elementState = self.bb.Get("dm").GetDevice("HeatingElement").Get("heatingElement")
        heaterState = "Off"
        if elementState:
            heaterState = "On"
        
        heaterType = self.bb.Get("sm").Get("heatType")
        pErrors = "16"
        
        # Save Mode
        safeModeStatus = self.bb.Get("dm").IsInSafeMode()
        safeMode = "Off"
        if safeModeStatus:
            safeMode = "On"
        
        buffer = buffer.format(stateDetails = stateDetails, timeTotal = timeTotal, timeState = timeState, timeLeft = timeLeft, heaterState = heaterState, heaterType = heaterType, pErrors = pErrors, safeMode = safeMode)
        
        return buffer        

    ##############################################################    
    def WebSnip_Temperature(self):
        bb = BlackBoard.Instance()
        
        buffer = """
        <div><table class='temperature'>
            <tr>
                <th>Target Temp</th> <th>Current Temp</th>
            </tr>            
            <tr>
                <td>{targetTemp}</td> <td>{currentTemp}</td>
            </tr>
        </table></div>"""
        
        targetTemp = self.bb.Get("sm").Get("targetTemperature")
        targetTemp = round(targetTemp, 2)
        targetTemp = str(targetTemp) + "c"
        
        currentTemp = bb.Get("dm").GetDevice("TemperatureProbe").Get("currentTemperature")
        currentTemp = round(currentTemp, 2)
        currentTemp = str(currentTemp) + "c"
        
        buffer = buffer.format(targetTemp = targetTemp, currentTemp = currentTemp)
        
        return buffer    