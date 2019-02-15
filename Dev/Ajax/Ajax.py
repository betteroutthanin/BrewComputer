from Base import Base
from BlackBoard import BlackBoard

class Ajax(Base):
    ##############################################################
    def __init__(self):        
        super(Ajax, self).__init__()
        self.loggingPrefix = "Ajax"        
        
    def ProcessAjax(self, requestHandler):
        sm = BlackBoard.Instance().Get("sm")
        if sm == False:
            return
        
        # need to make sure that the main system is still running
        smActive = sm.HasStates()
        if smActive == False:
            return
            
        self.Process(requestHandler)