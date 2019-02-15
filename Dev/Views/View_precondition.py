import Config
from Views.View import View

class View_precondition(View):
    ##############################################################
    def __init__(self):
        super(View_precondition, self).__init__()
        self.loggingPrefix = "View_precondition"
        
    def Render(self, requestHandler):
        self.LogMe("RenderView")
        
        message = ""
        message = message + self.FileGetContents(Config.webSitePath + "/PageParts/html_header.html")        
        message = message + self.FileGetContents(Config.webSitePath + "/PageParts/PreconditionSetUp.html")
        message = message + self.FileGetContents(Config.webSitePath + "/PageParts/html_footer.html")

        requestHandler.SendSimplePage(message)