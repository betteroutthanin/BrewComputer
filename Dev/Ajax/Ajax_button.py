import Config
from Ajax.Ajax import Ajax
from BlackBoard import BlackBoard

class Ajax_button(Ajax):
    ##############################################################
    def __init__(self):
        super(Ajax_button, self).__init__()
        self.loggingPrefix = "Ajax_button"
        
    def Process(self, requestHandler):                
        # was a button presses
        bb = BlackBoard.Instance()
        buttonName = False
        if "ButtonName" in requestHandler.queryData:
            buttonName = requestHandler.queryData['ButtonName'][0]
            bb.Get("dm").GetDevice("KeyBoard").PressButton(buttonName)
            self.LogMe("Button was pressed + " + buttonName)        
        
        message = " "       
        requestHandler.SendSimplePage(message)