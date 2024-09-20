import socket
import threading

def getlocalhost():
    return socket.gethostname(socket.gethostname())

HOST = getlocalhost()
PORT = 8080




class Servidor:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((HOST, PORT))
        self.socket.listen(10)
        
    
