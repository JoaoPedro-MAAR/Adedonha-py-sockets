import socket
import threading
from utilities import separaProtocolo_Aplicacao
from listaSequencial import Lista as l 
from classPlayer import Player
from classTentativa import Tentativa
from Hashtable import HashTable

  
  
TAMANHO_MAXIMO = 10

class Servidor:
    def __init__(self,HOST,PORT):
        self.lista = l(TAMANHO_MAXIMO)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((HOST, PORT))
        self.hashTemas = HashTable()
        self.hashTemas.put('nome',[])
        self.hashTemas.put('animal',[])
        self.hashTemas.put('cidade',[])
        self.hashTemas.put('objeto',[])
        self.estado = ['inicial','jogo','votacao','quadro_lideres']
        self.estado_index = 0
        self.listen_server_to_accept(TAMANHO_MAXIMO)
        
        
        
    
        
        
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
            if jogador:
                self.lista.remover_elemento(jogador)
            conexao_estabelecida.close()
            print(f"Conexão com {addr} encerrada.")


    def read_message(self,conexao):
        return conexao.recv(1024).decode()        


    def message_treatment(self,message: str,conexao, jogador):
        resto_mensagem = separaProtocolo_Aplicacao(message)
        codigo  = resto_mensagem[0]
        print(f'codigo: {codigo}')
        
        codigo_lower = codigo.lower()

        if codigo_lower == "prnt":
            if self.estado[self.estado_index] == 'inicial':
                if jogador:
                    return [self.send_message("ERRO: Você já está registrado", conexao), jogador]
                jogador = self.PRNT(conexao, resto_mensagem[1])
                return ['tentativa de registrar jogador', jogador]
            else:
                return [self.send_message("ERRO: Não é possivel", conexao), jogador]

        elif codigo_lower == "sair":
            return [self.SAIR(conexao, jogador), jogador]

        elif codigo_lower == 'start':
            if self.estado[self.estado_index] == 'inicial':
                return [self.START(conexao, jogador), jogador]
            return [self.send_message("ERRO: Não é possivel", conexao), jogador]

        elif codigo_lower == "rspt":
            self.RSPT(resto_mensagem[1], resto_mensagem[2], conexao, jogador)

            if self.finaliza_partida():
                for i in range(1, len(self.lista) + 1):
                    p = self.lista.elemento(i)
                self.send_message("200 OK: Todos responderam", p.socket)
            return [f'200 OK: Todos responderam', jogador]

        elif codigo_lower == "stop":
            return [self.send_message("RECEBI SEU STOP", conexao), jogador]

        elif codigo_lower == "voto":
            return [self.send_message("RECEBI SEU VOTO", conexao), jogador]

        else:
            return [self.send_message("ERRO: Comando não reconhecido", conexao), jogador]


    def PRNT(self,conexao,username):
        print('entrou em PRNT')

        if self.tratamento_PRNT(username) == username:
            jogador = Player(username,conexao)
            self.lista.append(jogador)
            print(f'Jogador {username} adicionado a lista')
            print(self.lista)
            self.send_message(f'200 OK:{len(self.lista)}:{self.estado_index}',conexao)
            return jogador
        else:
            self.send_message(f'{self.tratamento_PRNT(username)}',conexao)
        
        
        
    def tratamento_PRNT(self,username):
        print('entrou em tratamento_PRNT')
        if len(username) == 0:
            return "ERRO: Nome não pode ser vazio"
        
        if self.existeUsername(username):
            #ainda ta errado continua aceitando o nome repetido
            return "ERRO: Nome já existe"
        return username
        
    
    def existeUsername(self,username):
        if self.lista.existe(username):
            return False
        

        print(self.lista)
        if self.lista.esta_vazia():
            return False
            
        
        for i in range(1,len(self.lista)):
            print(f'username: {self.lista.elemento(i)}')
            if self.lista.elemento(i) == username:
                return True
        return False

        
    def send_message(self, message:str,conexao):
        return conexao.send(message.encode())
    

    def SAIR(self,conexao, jogador):
        self.send_message("200 OK: Desconectando",conexao)
        if jogador:
            self.lista.remover_elemento(jogador)
            print(f'Jogador {jogador} removido da lista')
        conexao.close()
        return "Conexão encerrada"
    

    def START(self,conexao, jogador):
        print('entrou em START')
        letra = 'C'
        for i in range(1,len(self.lista)+1):
            p = self.lista.elemento(i)
            self.send_message(f"200 OK:{letra}:1", p.socket)

        self.estado_index = 1                                                           
        return jogador
    
    def RSPT(self,resposta, tema, conexao, jogador):
        tema = tema.lower()
        resposta = Tentativa(jogador, resposta)
        self.hashTemas[tema].append(resposta)
        jogador.palavras.append(resposta)
        self.send_message("200 OK",conexao)
        #Representa que o Jogador respondeu
        return jogador
    

    def finaliza_partida(self):
        for i in range(1,len(self.lista)+1):
            jogador = self.lista.elemento(i)
            if len(jogador.palavras) < 4:
                return False
        return True