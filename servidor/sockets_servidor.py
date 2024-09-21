import socket
import threading
from utilities import separaProtocolo_Aplicacao
from listaEncadeada import Lista as l 
from classPlayer import Player
from classTentativa import Tentativa


  
  


class Servidor:
    def __init__(self,HOST,PORT):
        self.lista = l()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((HOST, PORT))
        self.listen_server_to_accept(10)
        
       
        
    def listen_server_to_accept(self, n: int = 10):
        self.server.listen(n)
        while True:
            conexao_estabelecida, addr = self.server.accept()
            print(f"Conectado {addr}")
            t = threading.Thread(target=self.listen_server, args=(conexao_estabelecida, addr))
            t.start()

    def listen_server(self, conexao_estabelecida, addr):
        try:
            while True:
                message = self.read_message(conexao_estabelecida)
                if not message:
                    break
                print(f'mensagem clientes: {message}')
                self.message_treatment(message, conexao_estabelecida)
        except Exception as e:
            print(f"Erro na conexão com {addr}: {e}")
        finally:
            conexao_estabelecida.close()
            print(f"Conexão com {addr} encerrada.")
            
    def read_message(self,conexao):
        return conexao.recv(1024).decode()        
            
    def message_treatment(self,message: str,conexao):
        codigo  = separaProtocolo_Aplicacao(message)[0]
        resto_mensagem = separaProtocolo_Aplicacao(message)[1]
        print(codigo)
        match codigo.lower():
            case "prnt":
                #Precisa de um tratamento para verificar se o nome já existe, e se foi passado um nome 
                
                return self.PRNT(conexao,resto_mensagem)
            case "sair":
                return self.send_message("RECEBI SEU SAIR",conexao)
            case "rspt":
                return self.send_message("RECEBI SEU RSPT",conexao)
            case "stop":
                return self.send_message("RECEBI SEU STOP",conexao)
            case "voto":
                return self.send_message("RECEBI SEU VOTO",conexao)
            
    def PRNT(self,conexao,username):

        if self.tratamento_PRNT(username) == username:
            self.lista.append(Player(username))
            print(f'Jogador {username} adicionado a lista')
            self.send_message(f'200 OK',conexao)
            self.send_message(f'\nRegistrado você é o {len(self.lista)} jogador a ficar pronto! ',conexao)
        else:
            self.send_message(f'{self.tratamento_PRNT(username)}',conexao)
        
        
        
    def tratamento_PRNT(self,username):
        if len(username) == 0:
            return "ERRO: Nome não pode ser vazio"
        
        if self.lista.existe(username):
            #ainda ta errado continua aceitando o nome repetido
            return "ERRO: Nome já existe"
        return username
        
    
    
    def send_message(self, message:str,conexao):
        return conexao.send(message.encode())