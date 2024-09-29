import numpy as np

class ListaError(Exception):
    def __init__(self, msg:str):
        super().__init__(msg)

class Lista:
    '''
    Classe que implementa a estrutura de dados Lista usando a 
    técnica sequencial
    '''
    def __init__(self, tamanho:int = 10):
        self.__array = np.full(tamanho,None)
        self.__ultimo = -1

    def __len__(self)->int:
        return self.__ultimo + 1

    def esta_vazia(self):
        return self.__ultimo == -1

    def esta_cheia(self):
        return self.__ultimo + 1 == len(self.__array)
    
    def elemento(self, posicao:int)->any:
        '''
        Método que recebe a posição de um elemento da pilha que deseja
        consultar. Retorna a carga armazenada na posição específica.
        A posicao retornada é em direição da base para o topo
        '''
        try:
            assert  0 < posicao <= self.__ultimo + 1
            return self.__array[posicao-1]
        except AssertionError:
            raise ListaError(f'Posicao invalida. A lista no momento possui {len(self)} elementos.')

    def busca(self, chave:any)->int:
        '''
        Método que recebe uma chave de busca e retorna a posição em
        que a carga foi encontrada na pilha
        '''
        for i in range(len(self)):
            if chave == self.__array[i]:
                return i + 1
        raise ListaError(f"Chave {chave} não encontrada")

    def inserir(self, posicao:int, carga:any):
        if self.esta_cheia():
            raise ListaError('Lista está cheia')
        assert  0 < posicao <= self.__ultimo + 2
        # assert 0 < posicao <= len(self)+1,"Posicao invalida para insercao"

        for i in range(self.__ultimo + 1, posicao-1, -1):
            self.__array[i] = self.__array[i-1]
        
        self.__array[posicao-1] = carga
        self.__ultimo += 1

    def append(self, carga:any):
        self.inserir(len(self)+1, carga)
        # if self.esta_cheia():
        #     raise ListaError('Lista está cheia')
        # self.__array[self.__ultimo + 1] = carga
        # self.__ultimo += 1


    def remover(self, posicao:int)->any:
        if self.esta_vazia():
            raise ListaError('Lista está vazia')
        
        try:
            assert posicao > 0 and posicao <= len(self),f'Posicao invalida para remocao. Informe um numero de 1 a {self.__len__()}'

            carga = self.__array[posicao-1]
            # Iniciando o deslocamento à esquerda dos elementos
            for i in range(posicao, self.__ultimo + 1):
                self.__dado[i-1] = self.__dado[i]

            self.__ultimo -= 1
            return carga
        except AssertionError as ae:
            raise ListaError(ae)
        
    def esvaziar(self):
        while not self.esta_vazia():
            self.remover(len(self))
    
    def existe(self, chave:any)->bool:
        '''
        Método que recebe uma chave de busca e retorna True se a chave
        for encontrada na pilha e False caso contrário
        '''
        if self.esta_vazia():
            return False
        try:
            self.busca(chave)
            return True
        except ListaError:
            return False

        

    def __str__(self)->str:
        s = 'lista->[ '
        for i in range(len(self)):
            s += f'{self.__array[i]}, '
        s = s.strip(', ')
        s += ' ]'
        return s