import socket


class Jogador:
    def __init__(self,hostandport: tuple):
        self.cliente = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.cliente.connect((hostandport))
        
       
        
    def send_msg(self,mensagem: str):
        self.cliente.send(mensagem.encode())
        
    def recv_msg(self):
        print(self.cliente.recv(1024).decode())
        
    def troca_msg(self,mensagem:str):
            self.send_msg(mensagem)
            self.recv_msg()
            
    def troca_mensagem_continua(self):
        while True:
            mensagem = input("Digite a mensagem: ")
            self.troca_msg(mensagem)
            
    