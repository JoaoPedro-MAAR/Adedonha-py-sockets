class Tentativa:
    def __init__ (self,user:object,palavra):
        self.nome = [user]
        self.palavra = palavra.lower()
        self.pontos = 0
        self.valid = True
    def __str__(self):
        return f'{self.nome} : {self.palavra}'

    def setNewPlayers(self,jogador: object):
        self.nome.append(jogador) 
        
    def uptadePontos(self,pontos):
        self.pontos = pontos
        return self.pontos    
    
    def getPalavra(self):
        return self.palavra
    
    def getisValid(self):
        return self.valid
    
    def invalidar(self):
        self.valid = False
    
    def submit_points(self):
        if self.getisValid():
            for i in range(0,len(self.nome)):
                self.nome[i].soma_pontos(self.pontos)
    
    def __eq__(self, value:any) -> bool:
        if value.getPalavra() == self.getPalavra():
            return True
        return False


    def __str__(self):
        return f'{self.palavra}'
    
