import Config
from Zobjects.States.State import State
import datetime

class Precondition(State):
    ##############################################################    
    def __init__(self):
        super(Precondition, self).__init__()
        self.loggingPrefix = "State.Precondition"
        
        self.targetStartTS = datetime.datetime.now().timestamp()
        self.leadTimeSec = 60 * 60
        self.stateMessage = ""
        self.setupComplete = False
        
        self.nameShort = "PRC"
        self.nameLong = "Precondition"
        
        # Round the time stamp to create a cleaner look - lock it down to 15 mins segments (or that defined by the config file)
        self.targetStartTS = self.roundTimeStamp(self.targetStartTS, Config.startTimeIncDecMin)
        
        # Start GSS Data       
        self.AddGetterSetterSaver("targetStartTS")
        self.AddGetterSetterSaver("leadTimeSec")
        self.AddGetterSetterSaver("setupComplete")
        # End GSS data
        
        # temp
        self.webSnip_stuff = ""
        
        self.LogMe("Booted")
        
    ##############################################################    
    def Process(self):
        # must call the parent process - see comments on State.Process
        super(Precondition, self).Process()
        
        # we can ignore this is setup is not complete
        if self.setupComplete == False:
            # deal with setup buttons but only if setup is not yet complete
            self.IncHourST()
            self.DecHourST()
            self.IncMinST()
            self.DecMinST()
            self.IncLT()
            self.DecLT()
            self.SetConfig()
            return False
        
        # else, on with the show
        
        currentTS = datetime.datetime.now().timestamp()
        leadTimeStartTS = self.targetStartTS - self.leadTimeSec
        
        cDT = datetime.datetime.now()
        tDT = datetime.datetime.fromtimestamp(self.targetStartTS)
        lDT = datetime.datetime.fromtimestamp(leadTimeStartTS)        
        self.webSnip_stuff = "C=" + str(cDT) + "<br>T=" + str(tDT) + "<br>H=" + str(lDT)
        
        # make sure the element is off when it is not needed
        # todo - is this the best way to handle this
        if currentTS < leadTimeStartTS:
            self.stateMessage = "Waiting for pre-heating to begin"
            if self.bb.Get("dm").IsInSafeMode() == False:
                self.bb.Get("dm").EnableSafeMode()
        else:
            self.stateMessage = "Pre-heating in progress"
            if self.bb.Get("dm").IsInSafeMode() == True:
                self.bb.Get("dm").DisableSafeMode()
                
        self.webSnip_stuff = self.webSnip_stuff + "<br>" + self.stateMessage                 
            
        if currentTS > self.targetStartTS:
            return True
        
        return False
        
    ##############################################################        
    def IncHourST(self):
        if self.bb.Get("dm").GetDevice("KeyBoard").ButtonWasPressed("pc_incHourST"):
            self.targetStartTS = self.targetStartTS + Config.startTimeIncDecHour
        
    ##############################################################        
    def DecHourST(self):
        if self.bb.Get("dm").GetDevice("KeyBoard").ButtonWasPressed("pc_decHourST"):
            self.targetStartTS = self.targetStartTS - Config.startTimeIncDecHour

    ##############################################################        
    def IncMinST(self):
        if self.bb.Get("dm").GetDevice("KeyBoard").ButtonWasPressed("pc_incMinST"):
            self.targetStartTS = self.targetStartTS + Config.startTimeIncDecMin
        
    ##############################################################        
    def DecMinST(self):
        if self.bb.Get("dm").GetDevice("KeyBoard").ButtonWasPressed("pc_decMinST"):
            self.targetStartTS = self.targetStartTS - Config.startTimeIncDecMin
                         
        
    ##############################################################        
    def IncLT(self):
        if self.bb.Get("dm").GetDevice("KeyBoard").ButtonWasPressed("pc_incLT"):
            self.leadTimeSec = self.leadTimeSec + Config.leadTimeIncDec
        
    ##############################################################        
    def DecLT(self):        
        if self.bb.Get("dm").GetDevice("KeyBoard").ButtonWasPressed("pc_decLT"):
            self.leadTimeSec = self.leadTimeSec - Config.leadTimeIncDec
            if self.leadTimeSec < 0:
                self.leadTimeSec = 0
        
    ##############################################################        
    def SetConfig(self):
        if self.bb.Get("dm").GetDevice("KeyBoard").ButtonWasPressed("pc_setConfig"):
            self.setupComplete = True
        
    ##############################################################     
    def RenderWebSetUp(self):
        
        buffer = ""
        buffer = buffer + self.WebSnip_Title()        
        buffer = buffer + "<div class='proceed'>Precondition Setup page<div>"
        buffer = buffer + self.WebSnip_PC_Data() 
        
        if self.setupComplete == False:
            buffer = buffer + "<div class='proceed'>Setup up not yet complete<div>"
        else:
            buffer = buffer + "<div class='proceed'>Setup up complete - not more changes can be made<div>"            

        return buffer
        
    ##############################################################     
    def RenderWeb(self):
        buffer = ""    
        
        if self.setupComplete:
            buffer = buffer + self.WebSnip_Title()        
            buffer = buffer + self.WebSnip_Temperature()
            buffer = buffer + "<div class='message'>" + self.webSnip_stuff + "<div>"       
            buffer = buffer + self.WebSnip_CoreData()                
            buffer = buffer + self.WebSnip_MessageWeb()            
            
        else:
            buffer = buffer + self.WebSnip_Title()
            buffer = buffer + "<div class='proceed'> Setup not complete - please proceed to PreCondition Setup page<div>"
        
        return buffer
        
    ##############################################################    
    def WebSnip_PC_Data(self):        
        
        buffer = """
        <div><table class='temperature'>
            <tr>
                <th>Start Time</th> <th>Lead Time</th>
            </tr>            
            <tr>
                <td>{startTime}</td> <td>{leadTime}</td>
            </tr>
        </table></div>"""
        
        leadTimeSec = int(self.leadTimeSec)
        leadTime = datetime.timedelta(seconds = leadTimeSec)
        
        targetStartDT = datetime.datetime.fromtimestamp(self.targetStartTS)
       
        startTime = '{0:%Y-%m-%d %H:%M:%S}'.format(targetStartDT)
       
        finalOutput = buffer.format(startTime = startTime, leadTime = leadTime)
        return finalOutput
        
        
    def roundTimeStamp(self, timeStamp, roundSecTo = 60):
        tempStamp = int(timeStamp / roundSecTo)
        tempStamp = tempStamp * roundSecTo
        return tempStamp