import socket
import threading


class Jogador:
    def __init__(self,hostandport: tuple):
        self.cliente = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.cliente.connect(hostandport)
        
       
        
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
                    if not self.valid_prnt(mensagem):
                        continue
                    #t = threading.Thread(target=self.listen_continuo, args=())
                    #t.start()
        except Exception as e:
            print(f"Erro na conexão: {e}")
            self.cliente.close()
            print("Conexão encerrada")
            
    def valid_prnt(self,mensagem:str )-> bool:
        """comando para verificar se o comando prnt está correto 

        Args:
            mensagem (string): string que contém o comando prnt que o usuario digitou

        Returns:
            boolean : True se o comando estiver correto, False caso contrário
        """
        if len(mensagem.split()) != 2:
            print("Comando inválido")
            return False
        return True