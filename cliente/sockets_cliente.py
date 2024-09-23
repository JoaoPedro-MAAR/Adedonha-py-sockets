import socket
import threading


class Jogador:
    def __init__(self,hostandport: tuple):
        self.cliente = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.cliente.connect((hostandport))
        
       
        
    def send_msg(self,mensagem: str):
        self.cliente.send(mensagem.encode())
        
        
    def recv_msg(self):
        print(self.cliente.recv(1024).decode())

    def listen_continuo(self):
        while True:
            self.recv_msg()

    def troca_msg(self,mensagem:str):
            self.send_msg(mensagem)
            self.recv_msg()
            
    def troca_mensagem_continua(self):
        try:
            while True:
                mensagem = input("Digite a mensagem: ")
                self.troca_msg(mensagem)
                if mensagem == "sair":
                    self.cliente.close()
                    print("Conexão encerrada")
                    break
                elif mensagem.split()[0] == "prnt":
                    t = threading.Thread(target=self.listen_continuo, args=())
                    t.start()
        except Exception as e:
            print(f"Erro na conexão: {e}")
            self.cliente.close()
            print("Conexão encerrada")
            
    