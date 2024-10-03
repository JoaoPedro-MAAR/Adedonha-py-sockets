import multiprocessing
import random
import socket
import string
import threading
import time

from classGame import Game
from classPlayer import Player
from classTentativa import Tentativa
from Hashtable import HashTable
from listaSequencial import Lista as l
from utilities import separaProtocolo_Aplicacao

TAMANHO_MAXIMO = 10

class Servidor:
    def __init__(self,HOST,PORT):
        self.lista = l(TAMANHO_MAXIMO)
        self.lock = multiprocessing.Lock()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((HOST, PORT))
        self.game = Game(self.lista)
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
                self.lock.acquire()
                resposta, jogador = self.message_treatment(message, conexao_estabelecida, jogador)
                if resposta == "Conexão encerrada":
                    break
                if resposta == 2:
                    threading.Thread(target=self.startVotacao).start()
                self.lock.release()
        
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
            if self.game.getEstado() == 'inicial':
                if jogador:
                    return [self.send_message(f"402:{self.game.getEstadoIndex()}", conexao), jogador]
                jogador = self.PRNT(conexao, resto_mensagem[1])
                return ['tentativa de registrar jogador', jogador]
            else:
                return [self.send_message(f"407:{self.game.getEstadoIndex()}", conexao), jogador]

        elif codigo_lower == "sair":
            return [self.SAIR(conexao, jogador), jogador]

        elif codigo_lower == 'start':
            if self.game.getEstado() == 'inicial':
                return [self.START(conexao, jogador), jogador]
            return [self.send_message("ERRO: Não é possivel", conexao), jogador]

        elif codigo_lower == "rspt":
            self.RSPT(resto_mensagem[1], resto_mensagem[2], conexao, jogador)

            if self.finaliza_partida():
                self.send_broadcast(f"200:{self.game.getEstadoIndex()}")
                return [2, jogador]
            return [f'200: Resposta registrada', jogador]

        elif codigo_lower == "stop":
            return [self.send_message("RECEBI SEU STOP", conexao), jogador]

        elif codigo_lower == "invld":
            return [self.handleInvalid(resto_mensagem,conexao,jogador), jogador]

        else:
            return [self.send_message("400", conexao), jogador]


    def PRNT(self,conexao,username):
        print('entrou em PRNT')

        tratado = self.tratamento_PRNT(username)

        if tratado == username:
            jogador, estado = self.game.registrar(conexao,username)
            self.send_message(f'200:{len(self.lista)}:{estado}',conexao)
            return jogador
        else:
            self.send_message(f'{tratado}:{self.game.getEstadoIndex}',conexao)
        
        
        
    def tratamento_PRNT(self,username):
        print('entrou em tratamento_PRNT')
        if len(username) == 0:
            return "400"
        
        if self.existeUsername(username):
            #ainda ta errado continua aceitando o nome repetido
            return "402"
        return username
        
    
    def existeUsername(self,username):
        for i in range(1,len(self.lista)+1):
            if self.lista.elemento(i).name == username:
                return True
        

        print(self.lista)
        if self.lista.esta_vazia():
            return False
            
        
        for i in range(1,len(self.lista)):
            print(f'username: {self.lista.elemento(i)}')
            if self.lista.elemento(i) == username:
                return True
        return False

        
    def send_message(self, message:str,conexao):
        print(message)
        return conexao.send(message.encode())


    def send_broadcast(self, message:str):
        for i in range(1,len(self.lista)+1):
            p = self.lista.elemento(i)
            self.send_message(message, p.socket)


    def SAIR(self,conexao, jogador):
        self.send_message("200:Desconectando",conexao)
        if jogador:
            self.lista.remover_elemento(jogador)
            print(f'Jogador {jogador} removido da lista')
        conexao.close()
        return "Conexão encerrada"
    

    def START(self,conexao, jogador):
        print('entrou em START')
        estado, letra = self.game.START()
        
        self.send_broadcast(f"200:{letra}:{estado}")
                                                          
        return jogador
    
    
    
    
    def RSPT(self,resposta, tema, conexao, jogador):
        estado = self.game.resposta(resposta, tema, conexao, jogador)
        self.send_message(f"200:{estado}",conexao)
        #Representa que o Jogador respondeu
        return jogador
    

    def finaliza_partida(self):
        for i in range(1,len(self.lista)+1):
            jogador = self.lista.elemento(i)
            if len(jogador.palavras) < 4:
                return False
        return True
    
    def startVotacao(self):
        estado, temas, hashTemas = self.game.startVotação()
        str_respostas = ''
        for j in range(4):
            respostas = hashTemas[temas[j]]
            str_respostas = self.ArrayObjectsToString(respostas)
            print(str_respostas)
            self.send_broadcast(f"200:{temas[j]}:{str_respostas}:{estado}")
            time.sleep(30)
            
          
        estado = self.game.quadro_lideres()
        self.send_broadcast(f"200:{estado}")
        time.sleep(1)
        lideres = self.game.getLideres()
        self.send_broadcast(f"200:{lideres}")
        time.sleep(5)
        self.end()
        return

    
    def ArrayObjectsToString(self,array)->str:
        """
        Função que transforma um array de objetos em uma string
        """
 
        return ' '.join(repr(obj) for obj in array)


    
    def handleInvalid(self, voto,conexao, jogador):
        estado = self.game.VOTO(voto,conexao, jogador)
        self.send_message(f"200:{estado}",conexao)

    
    def end(self):
        self.server.close()
        print("Servidor encerrado")
        
    
    
                
