import SocketServer
import os
import time
import json
import thread

from Request import Request

FILE_HEADER_200 = "HTTP/1.1 200 OK\n"
FILE_HEADER_404 = "HTTP/1.1 404 Not Found\n"
INDEX_FILE = "info.html"
WWW_FOLDER = "www"

mimeTypes = {
    "html" : "text/html",
    "css" : "text/css",
    "js" : "application/javascript",
    "jpg" : "image/jpeg",
    "png" : "image/png",
    "svg" : "image/svg+xml",
    "ico" : "image/x-icon",
    "json" : "application/json"
}

regFields = {
    "name" : str,
    "age" : int,
    "bloodtype" : str,
    "homeaddr" : str,
    "lat" : float,
    "long" : float,
    "checkinmissed" : int,
    "specneeds" : str,
    "other" : str,
    "id" : str,
    "notsafe": str
}

jsonFile = {
    # "people": {
    #     "id20" : {
    #         "name": "Alec",
		  #  "age":16,
		  #  "bloodtype":"A",
		  #  "homeaddr":"cool place",
		  #  "lat":52.370216,
		  #  "long":4.895168,
		  #  "timestamp":10000,
		  #  "specneeds":"none",
		  #  "other":"none",
		  #  "notsafe":"false"
    #     },
    #     "id69" : {
		  #  "name": "Emily",
		  #  "age":12,
		  #  "bloodtype":"A",
		  #  "homeaddr":"lame address",
		  #  "lat":40.730610,
		  #  "long":-73.935242,
		  #  "timestamp":1000000,
		  #  "specneeds":"short af",
		  #  "other":"allergic to milk",
		  #  "notsafe":"true"
    #     },
    #     "id21" : {
    #         "name": "Bob",
		  #  "age":16,
		  #  "bloodtype":"A",
		  #  "homeaddr":"house",
		  #  "lat":37.5326,
		  #  "long":127.024612,
		  #  "timestamp":100000,
		  #  "specneeds":"none",
		  #  "other":"none",
		  #  "notsafe":"true"
    #     }
    # }
}

curId = 70
GROUND_SHAKING_OH_NO = False
    
class ConnHandler(SocketServer.BaseRequestHandler):
    def handleWebRequest(self):
        global GROUND_SHAKING_OH_NO
        
        file = self.robj.path
        
        if file == "/shitgroundisshakingbruh":
            GROUND_SHAKING_OH_NO = not GROUND_SHAKING_OH_NO
            return
        
        if file == "/404.html":
            usedHeader = FILE_HEADER_404
        else:
            usedHeader = FILE_HEADER_200
            
        if file == "/":
            file += INDEX_FILE
            
        try:
            contentType = "Content-Type: %s\n\n" % (mimeTypes[file.split(".")[-1]])
        except Exception as e:
            print "Exception", e
            return
        
        finalHead = usedHeader + contentType
        
        if file.endswith("people.json"):
            print "sending spectial json"
            resp = finalHead.encode("utf-8") + json.dumps(jsonFile)
            self.request.sendall(resp)
            return
        
        file = WWW_FOLDER + file
        
        try:
            fHandle = open(file, "rb")
            respData = fHandle.read()
            fHandle.close()
        except Exception as e:
            self.robj.path = "/404.html"
            self.handleWebRequest()
            return
        
        resp = finalHead.encode("utf-8") + respData
        self.request.sendall(resp)
        
    def handlePost(self):
        global curId
        
        rd = self.robj.requestDict
        
        print rd
        
        if "lpoll" in rd.keys():
            self.request.sendall(FILE_HEADER_200 + ("Content-Type: text/plain\n\n%s" % (GROUND_SHAKING_OH_NO)))
            return
            
        rd["timestamp"] = time.time()
        print rd["timestamp"]
        
        idstr = rd.pop("id", None)
        if idstr is None:
            if rd.pop("act", None) != "REG":
                return
            idstr = "id%d" % (curId)
            curId += 1
            self.request.sendall(FILE_HEADER_200 + "Content-Type: text/plain\n\n" + idstr)
            jsonFile["people"][idstr] = rd
        else:
            for key in rd.keys():
                jsonFile["people"][idstr][key] = rd[key]
    
    def handle(self):
        self.robj = Request(raw = self.request.recv(1024).strip(), tag = "natdis-")
        
        if self.robj.method == "GET":
            self.handleWebRequest()
        elif self.robj.method == "POST":
            # print "{}: {}".format(self.client_address, self.robj.raw)
            self.handlePost()
            
server = SocketServer.TCPServer(("0.0.0.0", 8080), ConnHandler)
server.serve_forever()