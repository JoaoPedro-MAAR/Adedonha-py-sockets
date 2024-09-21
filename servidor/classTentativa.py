class Tentativa:
    def __init__ (self,user:object,palavra):
        self.nome = [user]
        self.palavra = palavra
        self.pontos = 0
    def __str__(self):
        return f'{self.nome} : {self.palavra}'

    def setNewPlayers(self,nome: object):
        self.nome = [self.nome,nome]
        
    def uptadePontos(self,pontos):
        self.pontos = pontos
        return self.pontos    
    
    def getPalavra(self):
        return self.palavra