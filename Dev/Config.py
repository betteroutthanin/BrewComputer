# Test
frameworkFPS = float(30)
saveFrameCounter = frameworkFPS * 2.0     # every 2 seconds

recoveryTimeOutSec = 20.0
stateSaveFrequencySec = 5.0

securityFilePath = "../Data/Current/security.file"

currentStateMachine = "../Data/Current/statemachine.json"
newStateMachine = "../Data/OrderUp/statemachine.json"

#statemachine.json
#statemachine_WFI.json
#statemachine_RTT.json

leadTimeIncDec = 60 * 15
startTimeIncDecMin = 60 * 15
startTimeIncDecHour = 60 * 60 

# softedge for temp control
softEdge = 0.0

emulationMode = True

# Web Site related goodies
webSitePath = "../Data/WebSite"
