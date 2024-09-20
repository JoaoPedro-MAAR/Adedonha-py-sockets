import socket
import threading

def getlocalhost():
    return socket.gethostname(socket.gethostname())

HOST = getlocalhost()
PORT = 8080

def separaProtocolo_Aplicacao(msg:str): 
    return []
    


class Servidor:
    def __init__(self):
        self.sever = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((HOST, PORT))
        self.listen_server(10)
        
    def listen_server (self,n:10 ):
        self.sever.listen(n)
        while True:
            conexao_estabelecida , addr = self.sever.accept()
            print(f"Conectado {addr}")
            t = threading.Thread(target=self.listen_server, args=(conexao_estabelecida, addr))