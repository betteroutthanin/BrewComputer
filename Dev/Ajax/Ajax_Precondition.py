import Config
from Ajax.Ajax import Ajax
from BlackBoard import BlackBoard
import time
import Zobjects.States.Precondition

class Ajax_Precondition(Ajax):
    ##############################################################
    def __init__(self):
        super(Ajax_Precondition, self).__init__()
        self.loggingPrefix = "Ajax_Precondition"
        
    def Process(self, requestHandler):                
        bb = BlackBoard.Instance()
        
        stateObjectID = self.bb.Get("sm").Get("currentStateID")        
        stateObject = self.bb.Get("sm").GetState(stateObjectID)

        if stateObject == False:
            return
                        
        # Make sure we are in the correct state type
        if isinstance(stateObject, Zobjects.States.Precondition.Precondition) == False:
            requestHandler.SendSimplePage("Must be in PreCondition mode to view this page")
            return
            
        contents = stateObject.RenderWebSetUp()
        
        requestHandler.SendSimplePage(contents)