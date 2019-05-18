import socketserver
import EIJ
import json
#Code Taken from https://docs.python.org/3.4/library/socketserver.html
class SocketListener(socketserver.BaseRequestHandler):
    """
    Listner for the Socket 9999
    """
    def handle(self):
        #Pull the request body
        data = self.request[0].strip()
        #Which socket we are listening on and will respond on
        socket = self.request[1]
        ev = EIJ.evalStories(data)
        
        #Respond
        socket.sendto(bytes(ev,"utf-8"), self.client_address)
        
if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    #Initialize the server on port 9999 and keep it going forever
    server = socketserver.UDPServer((HOST, PORT), SocketListener)
    server.serve_forever()
