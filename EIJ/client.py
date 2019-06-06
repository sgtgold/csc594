import socket
import sys
import Data
import json
#From https://jfine-python-classes.readthedocs.io/en/latest/dict_from_class.html
def dict_from_class(cls):
    return dict(
        (key, value)
        for (key, value) in cls.__dict__.items()
        )

#Code Taken from https://docs.python.org/3.4/library/socketserver.html
HOST, PORT = "localhost", 9999

# SOCK_DGRAM is the socket type to use for UDP sockets
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# As you can see, there is no connect() call; UDP has no connections.
# Instead, data is directly sent to the recipient via sendto().
data = Data.loadStories()
#Here I am choosing the story to send to the EIJ to be evaluated

for i in range(0,len(data)):
    print('Choice ',i,':',data[i].what)
x = ''
while x != 'q':
    x = input('\nType the ID of a story to evaluate (or q to quit):')
    if x!= 'q':
        file1 = open("AISocketLog.txt","a+") 
        file1.writelines('Client Sent: '+ data[int(x)].what+'\n') 
        file1.close() #to change file access modes 
        #Send the byte array of the story to the server which is connected to EIJ
        #And we have to convert our class Story to a dictionary so it can convert to JSON
        sock.sendto(json.dumps(dict_from_class(data[int(x)])).encode("utf-8"), (HOST, PORT))
        #Get a response
        received = str(sock.recv(1024),"utf-8")
        print('\n'+received)
        file1 = open("AISocketLog.txt","a+") 
        file1.writelines('Server Sent Back: '+received+'\n') 
        file1.close() #to change file access modes 