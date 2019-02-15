import Config
import HeatTypes
import os.path
import json
from Base import Base
from Property import Property
from BlackBoard import BlackBoard

class StateManager(Base, Property):
    ##############################################################
    def __init__(self):
        #super(StateManager, self).__init__()

        Base.__init__(self)
        Property.__init__(self)        
        
        self.loggingPrefix = "StateManager"

        #### reset these        
        self.states = {}            # Dict of states
        
        self.currentStateID = -2        # todo - explain this
        self.lastStateID = -2           # todo - explain this
        self.timeSec = 0.0
        self.timeNextSaveSec = 0.0      # time threshold for when we will save the state
        self.recoveryCounter = 0        
        
        self.name = ""        
        self.targetTemperature = 0.0
        self.heatType = HeatTypes.off        
        
        self.paused = False
        self.saveMode = False       # defines if the state machines needs to back itself up
        ##### End reset

        self.recoverOldStateMachine = True
        
        # Start GSS Data
        self.AddGetterSetterSaver("name")
        self.AddGetterSetterSaver("currentStateID")
        self.AddGetterSetterSaver("lastStateID")
        self.AddGetterSetterSaver("timeSec")
        self.AddGetterSetterSaver("targetTemperature")
        self.AddGetterSetterSaver("heatType")
        self.AddGetterSetterSaver("recoveryCounter")        
        
        self.AddGetterSetter("recoverOldStateMachine")
        self.AddGetter("paused")
        # End GSS data       
        
        self.bb = BlackBoard.Instance()        
        
        self.LogMe("Booted")

    ##############################################################
    def Reset(self):
        self.LogMe("Reset: Reseting state machine data")
        self.states = {}
        self.currentStateID = -2
        self.lastStateID = -2
        self.timeSec = 0.0
        self.timeNextSaveSec = 0.0
        self.name = ""
        self.targetTemperature = 0.0
        self.heatType = HeatTypes.off
        self.paused = False
        self.saveMode = False

    ##############################################################
    def BootRecoveryMode(self):
        self.LogMe("BootRecoveryMode:")
        
        self.Reset()
        recoveryState = self.MillNewZobject("Zobjects.States.Recovery.Recovery")
        self.AddState(recoveryState)
        self.name = "Recovery Mode"
        
        # self.LogMe("BootRecoveryMode: Name = " + str(self.name))
        
        return True
        
    ##############################################################
    def BootNormalMode(self):
        self.LogMe("BootNormalMode:")
    
        self.Reset()
        
        loaded = False
        stateMachineName = ""

        if self.recoverOldStateMachine == True:
            stateMachineName = Config.currentStateMachine
            self.LogMe("BootNormalMode: Recovering old run > " + stateMachineName)
        else:
            stateMachineName = Config.newStateMachine
            self.LogMe("BootNormalMode: Starting new run > " + stateMachineName)

        loaded = self.LoadStateMachineFromDisk(stateMachineName)
        
        # Need to ensure that the end state is the last state, but only do this if it a new boot and not on an recovery
        if self.recoverOldStateMachine == False:
            tempEndStateObject = self.MillNewZobject("Zobjects.States.End.End")
            tempEndStateObject.Set("id", len(self.states))
            self.AddState(tempEndStateObject)
            self.LogMe("Just popping and end state on . . . . . just incase the json file doesn't already have one")
        
        # need to ensure that the state machine will save itself from this point on
        self.saveMode = True
        
        # This will keep track if there has been a heap of reboots
        self.recoveryCounter = self.recoveryCounter + 1
        
        # self.LogMe("BootNormalMode: Name = " + str(self.name))

        return loaded

    ##############################################################
    def Tick(self, deltaTimeSec):
        # self.LogMe("Tick")        
        
        # Time walking time
        # Punch out if we are paused
        self.UpdatePausedState()
        if self.paused:
            return True
        
        # Time is passed to the stateMachine as delta time.  Make sure the timeSec is updates
        # as early as possible to ensure that sub-systems have the most correct time    
        self.timeSec = self.timeSec + deltaTimeSec
    
        # Take a snap shot of the system if needed.  This is key to recovery
        self.DoWeNeedToSave()

        # need to make sure we are using a valid state
        if self.currentStateID < 0:
            self.currentStateID = 0
            self.LogMe("First State set to " + str(self.currentStateID))

        # Get the state object
        curentStateObject = self.GetState(self.currentStateID)
        # Note - normally we would validate this object right after we get it, but we do this
        # lower down to ensure that we can call exit on the last state

        # Did we transition - yes
        if self.currentStateID != self.lastStateID:
            self.LogMe("Tick -> state change detect -> " + str(self.lastStateID) + " to -> " + str(self.currentStateID))

            # call the OnExit on the last state if we need to
            if self.lastStateID >= 0:
                lastStateObject = self.GetState(self.lastStateID)
                # todo - add some error handling here
                lastStateObject.OnExit()

            # Call this here to ensure that the last state has a chance to call it's OnExit function
            if curentStateObject is False:                
                return False

            # call the OnEntry to the new state
            curentStateObject.OnEntry()

        # new is old - needed to ensure we can transition properly
        self.lastStateID = self.currentStateID

        # Process the current state and check if we can move on
        stateComplete = curentStateObject.Process()
        if stateComplete == True:
            self.currentStateID = self.currentStateID + 1

        return True
    
     ##############################################################
    def UpdatePausedState(self):              
        if self.bb.Get("dm").GetDevice("KeyBoard").ButtonWasPressed("pause")   :            
                self.paused = not self.paused
                self.bb.Get("dm").SetSafeMode(self.paused)
        
    ##############################################################
    def DoWeNeedToSave(self):
        # Only save if we are in saveMode
        if self.saveMode == False:
            return
    
        # Saving is based on timer
        if self.timeSec > self.timeNextSaveSec:
            self.timeNextSaveSec = self.timeSec + Config.stateSaveFrequencySec
            self.SaveStateMachineToDisk()
        
    ##############################################################
    def GetState(self, stateID):
        if stateID in self.states:
            return self.states[stateID]

        self.LogMe("GetState: Failed to find state ID -> " + str(stateID))
        return False
        
    ##############################################################
    def HasStates(self):
        if len(self.states) == 0:
            return False
            
        return True

    ##############################################################
    def AddState(self, stateObject):
        # ensure that the state object has a valid id and type
        # todo - use the get method for ID
        if (stateObject.id < 0):
            self.LogMe("AddState: stateObject ID is invalid -> " + str(stateObject.id))
            return False

        if (stateObject.type == ""):
            self.LogMe("AddState: stateObject type is invalid-> " + str(stateObject.type))
            return False

        # ok all good lets add the state
        self.states[stateObject.id] = stateObject

        self.LogMe("State Object added -> " + str(stateObject.type) + " as id -> " + str(stateObject.id))
        return True

    ##############################################################
    def LoadStateMachineFromDisk(self, nameOfStateMachineToLoad):
        # Make sure the file exists
        if os.path.exists(nameOfStateMachineToLoad) == False:
            self.LogMe("LoadStateMachineFromDisk:  StateMachine json file missing -> " + str(nameOfStateMachineToLoad))
            return False            
        
        jsonData = json.loads(self.FileGetContents(nameOfStateMachineToLoad))

        #  Need to ensure that the json file contains the states section
        if "states" not in jsonData:
            self.LogMe("LoadStateMachineFromDisk:  StateMachine json file missing 'states'")
            return False
            
        if "data" not in jsonData:
            self.LogMe("LoadStateMachineFromDisk:  StateMachine json file missing 'data'")
            return False

        # Loop and load all the states
        states = jsonData["states"]
        for stateData in states:
            # create the new state object
            tempStateObject = self.MillNewZobject(stateData["type"])
            
            #todo - add error handling if object can't be milled

            # fill the state object with love
            for key, value in stateData.items():
                setattr(tempStateObject, key, value)

            # Push the new state object onto the state machine
            self.AddState(tempStateObject)

        ###### The other state machine variables needed to make this happen               
        stameMachineData = jsonData["data"]
        for key, value in stameMachineData.items():
            setattr(self, key, value)            
        
        return True

    ##############################################################
    def SaveStateMachineToDisk(self):
        jsonData = {}

        # State Machine data
        jsonData["data"] = self.SaveListToJson()
        
        # The States
        jsonData["states"] = []
        for stateKey, stateObject in self.states.items():
            jsonData["states"].append(stateObject.SaveListToJson())

        self.FilePutContents(Config.currentStateMachine, json.dumps(jsonData, indent=4, sort_keys=False))
                
        # self.LogMe("SaveStateMachineToDisk: State machine saved")
        
