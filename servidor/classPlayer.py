class Player:
    def __init__(self, name: str, socket):
        self.name = name
        self.socket = socket
        self.palavras = []
        self.pontuacao = 0
        
    def __str__(self):
        return f'Nome: {self.name} - Pontuação: {self.pontuacao}'
    
    def soma_pontos(self, pontos):
        self.pontuacao += pontos
        return self.pontuacao
    
    def __eq__(self, other):
        if not isinstance(other, Player):
            return NotImplemented
        print(f'Comparando {self.name} com {other.name} TIPO DE OTHER: {type(other)}')
        return self.name == other.name
    
    
