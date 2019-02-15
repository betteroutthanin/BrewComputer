import Config
from BlackBoard import BlackBoard
from Zobjects.Devices.Device import Device
from Base import Base

import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from http.cookies import SimpleCookie
from urllib.parse import urlparse, parse_qs


class WebServer(Device):
    ##############################################################    
    def __init__(self):
        super(WebServer, self).__init__()
        self.loggingPrefix = "Device.WebServer"
        
        self.thinkFreqSec = 2.0        
        self.ready = True        
        self.wst = WebServerThread().start()
        
        self.LogMe("Booted")
  
    ##############################################################        
    def Process(self):
        pass

##############################################################        
class WebServerThread(threading.Thread, Base):
    def run (self):
        # __init__ replacement
        self.loggingPrefix = "WebServerThread"
        self.LogMe("Booting webserver thread")
        
        server_address = ('127.0.0.1', 8081)
        httpd = HTTPServer(server_address, WebSereverRequestHandler)        
        httpd.serve_forever()

##############################################################            
class WebSereverRequestHandler(BaseHTTPRequestHandler, Base): 
    # not ideal, but it will work
    authTokens = []

    ##############################################################
    def log_message(self, format, *args):
        # you must be quite - now!
        return
        
    ##############################################################
    def ProcessPage(self):
        # self.LogMe("Processing page")
        # Make sure there is a page to server
        finalPath = self.pathData.path        
        if self.pathData.path.lower().endswith(("/")):
            finalPath = self.pathData.path + "index.html"

        filePath =  Config.webSitePath + finalPath
        #self.LogMe("*** " + filePath)        
        
        message = self.FileGetContents(filePath);    
        
        if message == False:
            self.LogMe("page not found")
            return
        
        self.SendSimplePage(message)
        
    ##############################################################
    def ProcessImage(self):
        # self.LogMe("Processing image")
        filePath =  Config.webSitePath + self.pathData.path
        # self.LogMe("*** " + filePath)     
        
        imageContents = self.FileGetContentsBinMode(filePath)
        if imageContents == False:
            return
        
        self.send_response(200)        
        self.send_header('Content-type:', ' image/png')
        self.end_headers()        
        self.wfile.write(imageContents)
        
    ##############################################################    
    def ProcessCSS(self):
        # self.LogMe("Processing CSS")
        filePath =  Config.webSitePath + self.pathData.path
        
        contents = self.FileGetContents(filePath)        
        if contents == False:
            return
        
        self.send_response(200)        
        self.send_header('Content-type','text/css')
        self.end_headers()        
        self.wfile.write(contents.encode("utf-8"))
        
    ##############################################################        
    def ProcessAuth(self):
        # Check to see if the Auth code matches the stored one
        securityCode = BlackBoard.Instance().Get("securityCode")        
        passedCode = self.pathData.path.replace(".authme", "")
        passedCode = passedCode.replace("/", "")
        
        self.LogMe("Passed Code = " + passedCode)
        self.LogMe("securityCode = " + securityCode)        
        
        # Assume failure
        authToken = "NotAllowed"
        message = "Authorization Failed"
        
        # For the Win?        
        if (securityCode == passedCode):        
            authToken = self.id_generator()        
            self.authTokens.append(authToken)
            message = "Welcome - You have been authorized - Token = " +   authToken
            self.LogMe(authToken)
        
        self.send_response(200)        
        self.send_header('Content-type','text/html')        
        self.send_header('Set-Cookie', 'authToken=' + authToken)
        self.end_headers()
        self.wfile.write(message.encode("utf-8"))
    
    ##############################################################        
    def ProcessAccessDenied(self):
        #self.LogMe("Processing AccessDenied")
        message = "You are not authorized"
        self.send_response(200)
        
        self.send_header('Content-type','text/html')
        self.send_header('Set-Cookie', 'authToken=NotAllowed')
        self.end_headers()
        self.wfile.write(message.encode("utf-8"))
        
    ##############################################################
    def ProcessView(self):
        # call view based on outcome        
        finalPath = self.pathData.path.replace(".view", "")
        finalPath =finalPath.replace("/", "")        
        
        viewObjectName = "Views." + finalPath + "." + finalPath        
        viewObject = self.MillNewZobject(viewObjectName)        
        if viewObject == False:
            self.LogMe("Files to create view " + viewObjectName)
            return
        
        # ok you lazy shit - do some work    
        viewObject.RenderView(self)
        
        # todo - de we need to delete the milled object
        
    ##############################################################
    def ProcessAjax(self):
        finalPath = self.pathData.path.replace(".pax", "")
        finalPath =finalPath.replace("/", "")
           
        ajaxObjectName = "Ajax." + finalPath + "." + finalPath
        ajaxObject = self.MillNewZobject(ajaxObjectName)        
        if ajaxObject == False:
            self.LogMe("Filed to create ajax " + ajaxObjectName)
            return
        
        # ok you lazy shit - do some work    
        ajaxObject.ProcessAjax(self)        
            
    ##############################################################        
    def SendSimplePage(self, message):
        self.send_response(200)        
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write(message.encode("utf-8"))
    
    ##############################################################
    def do_GET(self):
        self.loggingPrefix = "WebSereverRequestHandler"
        
        # Convert the URL to something more useful
        self.pathData = urlparse(self.path)
        self.queryData = parse_qs(self.pathData.query)
        
        # Debug fun time
        #self.LogMe(self.server.server_name)                
        #self.LogMe(self.path)        
        #self.LogMe(self.pathData)
        #self.LogMe(self.queryData)
        
        # what sort of request are they making
        # /favicon.ico
        if self.pathData.path == "/favicon.ico":
            # do nothing
            # todo - work out a better way of handling this
            return
            
        # do this before we do the auth test
        if self.pathData.path.lower().endswith("authme"):
            self.ProcessAuth()
            return
        
        # Do the auth testing - assume it will not work
        self.authed = False
        authToken = False        
        
        # Auth Tokens are stored in cookies
        cookies = SimpleCookie()
        cookieString = self.headers.get('Cookie')        
        if cookieString != None:
            cookies.load(cookieString)        
            if "authToken" in cookies.keys():
                authToken = cookies['authToken'].value                
            if authToken in self.authTokens:
                self.authed  = True
        if self.authed == False:
            self.ProcessAccessDenied()
            return
        
        # At this point we are authed
        # image calls         
        if self.pathData.path.lower().endswith(('.png')):
            self.ProcessImage()
            return

        # ajax calls            
        if self.pathData.path.lower().endswith(('.pax')):
            self.ProcessAjax()
            return
        
        # View calls
        if self.pathData.path.lower().endswith(('.view')):
            self.ProcessView()
            return
            
        # CSS calls
        if self.pathData.path.lower().endswith(('.css')):
            self.ProcessCSS()
            return
            
        # Finally - normal processing
        self.ProcessPage()
        return