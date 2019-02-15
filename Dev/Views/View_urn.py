import Config
from Views.View import View

class View_urn(View):
    ##############################################################
    def __init__(self):
        super(View_urn, self).__init__()
        self.loggingPrefix = "View_urn"
        
    def Render(self, requestHandler):
        self.LogMe("RenderView")
        
        message = ""
        message = message + self.FileGetContents(Config.webSitePath + "/PageParts/html_header.html")        
        message = message + self.FileGetContents(Config.webSitePath + "/PageParts/UrnView.html")
        message = message + self.FileGetContents(Config.webSitePath + "/PageParts/VirtualKeyPad.html")
        message = message + self.FileGetContents(Config.webSitePath + "/PageParts/html_footer.html")

        requestHandler.SendSimplePage(message)