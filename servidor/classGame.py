import socket
import threading
import multiprocessing
from utilities import separaProtocolo_Aplicacao
from listaSequencial import Lista as l 
from classPlayer import Player
from classTentativa import Tentativa
from Hashtable import HashTable
import random
import string
import asyncio


  
  
TAMANHO_MAXIMO = 10

class Game:
    def __init__(self, players):
        self.lista_players = players
        self.hashTemas = HashTable()
        self.hashTemas.put('nome',[])
        self.hashTemas.put('animal',[])
        self.hashTemas.put('cidade',[])
        self.hashTemas.put('objeto',[])
        self.temas = ['nome','animal','cidade','objeto']
        self.estado = ['inicial','jogo','votacao','quadro_lideres']
        self.estado_index = 0
        

    def registrar(self,conexao,username):
        print('entrou em PRNT')

        jogador = Player(username,conexao)
        self.lista_players.append(jogador)
        print(f'Jogador {username} adicionado a lista')
        print(self.lista_players)
        return jogador, self.estado_index
    
    
    def START(self):
        print('entrou em START')
        letra = self.letra_aleatoria()
        self.estado_index = 1                                                           
        return self.estado_index, letra
    
    
    def letra_aleatoria(self):
        return random.choice(string.ascii_uppercase)    


    
    def resposta(self,resposta, tema, conexao, jogador):
        tema = tema.lower()
        resposta = Tentativa(jogador, resposta)
        self.hashTemas[tema].append(resposta)
        jogador.palavras.append(resposta)
        #Representa que o Jogador respondeu
        return self.estado_index
    
    
    def startVotação(self):
        print('entrou em startVotação')
        self.estado_index = 2
        return self.estado_index, self.temas, self.hashTemas
    
    
    def VOTO(self, voto,conexao, jogador):
        tema = voto[0]
        for i in range(1,len(voto)+1):
            self.hashTemas[tema][voto[i]].invalidar()
    
    
    def quadro_lideres(self):
        print('entrou em quadro_lideres')
        self.estado_index = 3
        for j in range(4):
            respostas = self.hashTemas[self.temas[j]]
            for i in range(1,len(self.lista_players)+1):
                self.hashTemas[self.temas[j]][i].submit_points()     
        return self.estado_index
    
    
    def getLideres(self):
        lideres = []
        for i in range(1,len(self.lista_players)+1):
            lideres.append(self.lista_players[i])
        lideres.sort(key=lambda x: x.pontuacao, reverse=True)
        return lideres[:3]
    
    def getEstado(self):
        return self.estado[self.estado_index]
    def getEstadoIndex(self):
        return self.estado_index