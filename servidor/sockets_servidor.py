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
        jogador = None
        try:
            while True:
                message = self.read_message(conexao_estabelecida)
                if not message:
                    break
                print(f'mensagem clientes: {message}')
                resposta, jogador = self.message_treatment(message, conexao_estabelecida, jogador)
                if resposta == "Conexão encerrada":
                    break
        except Exception as e:
            print(f"Erro na conexão com {addr}: {e}")
        finally:
            conexao_estabelecida.close()
            print(f"Conexão com {addr} encerrada.")


    def read_message(self,conexao):
        return conexao.recv(1024).decode()        


    def message_treatment(self,message: str,conexao, jogador):
        resto_mensagem = separaProtocolo_Aplicacao(message)
        codigo  = resto_mensagem[0]
        
        match codigo.lower():
            case "prnt":
                jogador = self.PRNT(conexao,resto_mensagem[1])
                
                return ['tentativa de registrar jogador', jogador]
            case "sair":
                return [self.SAIR(conexao, jogador), jogador]
            case "rspt":
                return [self.send_message("RECEBI SEU RSPT",conexao), jogador]
            case "stop":
                return [self.send_message("RECEBI SEU STOP",conexao), jogador]
            case "voto":
                return [self.send_message("RECEBI SEU VOTO",conexao), jogador]
            case _:
                return [self.send_message("ERRO: Comando não reconhecido",conexao), jogador]


    def PRNT(self,conexao,username):

        if self.tratamento_PRNT(username) == username:
            jogador = Player(username,conexao)
            self.lista.append(jogador)
            print(f'Jogador {username} adicionado a lista')
            self.send_message(f'200 OK: Você é o {len(self.lista)} jogador a ficar pronto! ',conexao)
            return jogador
        else:
            self.send_message(f'{self.tratamento_PRNT(username)}',conexao)
        
        
        
    def tratamento_PRNT(self,username):
        if len(username) == 0:
            return "ERRO: Nome não pode ser vazio"
        
        if self.existeUsername(username):
            #ainda ta errado continua aceitando o nome repetido
            return "ERRO: Nome já existe"
        return username
        
    
    def existeUsername(self,username):
        for i in range(1,len(self.lista)+1):
            if self.lista.elemento(i).name == username:
                return True
        return False

    def send_message(self, message:str,conexao):
        return conexao.send(message.encode())
    

    def SAIR(self,conexao, jogador):
        self.send_message("200 OK: Desconectando",conexao)
        if jogador:
            self.lista.remover_elemento(jogador)
            print(f'Jogador {jogador.name} removido da lista')
        conexao.close()
        return "Conexão encerrada"