class Tentativa:
    def __init__ (self,user:str,palavra):
        self.nome = [user]
        self.palavra = palavra.lower()
        self.votos = 0
        self.pontos = 10
        self.valid = True
        
        
    def __str__(self):
        return f'{self.palavra}'

    def __repr__(self) -> str:
        return f'{self.palavra}'
    
    def Engenharia_reversa(self,str)-> bool:
        if str == self.__repr__():
            return True


    def setNewPlayers(self,jogador: object):
        self.nome.append(jogador)
        self.uptadePontos(5) 
        
    def uptadePontos(self,pontos):
        self.pontos = pontos
        return self.pontos    
    
    def getPalavra(self):
        return self.palavra
    
    def getisValid(self):
        return self.valid
    
    def invalidar(self):
       
            self.valid = False
    
    def submit_points(self, qtdePlayers):
        self.invalidar(qtdePlayers)
        if self.getisValid():
            for i in range(0,len(self.nome)):
                self.nome[i].soma_pontos(self.pontos)
    
    def __eq__(self, value:any) -> bool:
        if value.getPalavra() == self.getPalavra():
            return True
        return False


    def __str__(self):
        return f'{self.palavra}'
    



