# ATENCAO! AINDA SERÁ IMPLEMENTADA A CLASSE LISTA ENCADEADA


class ListaError(Exception):
    def __init__(self, msg:str):
        super().__init__(msg)


class No:
    def __init__(self, carga:any):
        self.carga = carga
        self.proximo = None
    
    def __str__(self):
        return f'{self.carga}'


class Lista:
    '''
    Classe que implementa a estrutura de dados Lista usando a 
    técnica simplesmente encadeada
    '''
    def __init__(self):
        self.__head = None
        self.__tamanho = 0

    def __len__(self)->int:
        return self.__tamanho

    def esta_vazia(self):
        return self.__head == None
    
    def elemento(self, posicao:int)->any:
        '''
        Método que recebe a posição de um elemento da pilha que deseja
        consultar. Retorna a carga armazenada na posição específica.
        A posicao retornada é em direição da base para o topo
        '''
        try:
            assert  0 < posicao <= len(self)
            cursor = self.__head
            for _ in range(posicao-1):
                cursor = cursor.proximo
            return cursor.carga
        except AssertionError:
            raise ListaError(f'Posicao invalida. A lista no momento possui {len(self)} elementos.')

    def busca(self, chave:any)->int:
        '''
        Método que recebe uma chave de busca e retorna a posição em
        que a carga foi encontrada na pilha
        '''
        cursor = self.__head
        contador = 1
        while(cursor != None):
            if cursor.carga == chave:
                return contador
            cursor = cursor.proximo
            contador +=1
        raise ListaError(f"Chave {chave} não encontrada")
    
    
    def existe(self, chave:any)->bool:
        '''
        Método que recebe uma chave de busca e retorna True se a chave
        for encontrada na pilha e False caso contrário
        '''
        try:
            self.busca(chave)
            return True
        except ListaError:
            return False

    def inserir(self, posicao:int, carga:any):
        try:
            assert 0 < posicao <= len(self)+1, f'Posicao invalida. Lista contém {self.__tamanho} elementos' 

            # CONDICAO 1: insercao se a lista estiver vazia
            if (self.esta_vazia()):
                if ( posicao != 1):
                    raise ListaError(f'A lista esta vazia. A posicao correta para insercao é 1.')

                self.__head = No(carga)
                self.__tamanho += 1
                return
            
            # CONDICAO 2: insercao na primeira posicao em uma lista nao vazia
            if ( posicao == 1):
                novo = No(carga)
                novo.proximo = self.__head
                self.__head = novo
                self.__tamanho += 1
                return

            # CONDICAO 3: insercao apos a primeira posicao em lista nao vazia
            cursor = self.__head
            contador = 1
            while ( contador < posicao-1):
                cursor = cursor.proximo
                contador += 1

            novo = No(carga)
            novo.proximo = cursor.proximo
            cursor.proximo = novo
            self.__tamanho += 1

        except AssertionError:
            raise ListaError(f'A posicao não pode ser um número negativo ou 0 (zero)')


    def append(self, carga:any):
        self.inserir(len(self)+1, carga)

        

    def remover(self, posicao:int)->any:
        try:
            if( self.esta_vazia() ):
                raise ListaError(f'Não é possível remover de uma lista vazia')
            
            assert 0 < posicao <= len(self), f'Posicao invalida. Lista contém {self.__tamanho} elementos'

            cursor = self.__head
            contador = 1

            while( contador <= posicao-1 ) :
                anterior = cursor
                cursor = cursor.proximo
                contador+=1

            carga = cursor.carga

            if( posicao == 1):
                self.__head = cursor.proximo
            else:
                anterior.proximo = cursor.proximo

            self.__tamanho -= 1
            return carga
        
        except TypeError:
            raise ListaException(f'A posição deve ser um número inteiro')            
        except AssertionError:
            raise ListaException(f'A posicao não pode ser um número negativo')
        
    def esvaziar(self):
        while not self.esta_vazia():
            self.remover(1)

    def __str__(self)->str:
        s = 'lista->[ '

        cursor = self.__head
        while( cursor != None):
            s += f'{cursor.carga}, '
            cursor = cursor.proximo

        s = s.strip(', ')
        s += ' ]'
        return s
    
     