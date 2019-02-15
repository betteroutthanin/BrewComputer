from Base import Base
from BlackBoard import BlackBoard

class View(Base):
    ##############################################################
    def __init__(self):        
        super(View, self).__init__()
        self.loggingPrefix = "View"        
        
    def RenderView(self, requestHandler):
        sm = BlackBoard.Instance().Get("sm")
        if sm == False:
            return
        
        # need to make sure that the main system is still running
        smActive = sm.HasStates()
        if smActive == False:
            return
        
        self.Render(requestHandler)
        
        