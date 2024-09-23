class Tentativa:
    def __init__ (self,user:object,palavra, tema):
        self.nome = [user]
        self.palavra = palavra
        self.tema = tema
        self.pontos = 0
    def __str__(self):
        return f'{self.nome} : {self.palavra}'

    def setNewPlayers(self,jogador: object):
        self.nome.append(jogador) 
        
    def uptadePontos(self,pontos):
        self.pontos = pontos
        return self.pontos    
    
    def getPalavra(self):
        return self.palavra