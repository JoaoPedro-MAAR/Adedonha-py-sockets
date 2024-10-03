import numpy as np


class HashTable(object):
    '''
    Implementação de uma tabela hash com tratamento de colisão por 
    sondagem linear (linear probing) e redimensionamento automático 
    da tabela hash quando o fator de carga máximo é atingido.

    A tabela hash armazena em cada bucket uma tupla com o par
    chave/valor.
    O código funciona com qualquer tipo de chave e valor.

    Dependência: instalação do numpy
    
    Autor: Prof. Alex Sandro da Cunha Rêgo
    Última modificação: 03/09/2024
    '''

    def __init__(self, size = 500):
        '''
        Construtor da classe HashTable, sem argumentos.
        Inicializa a tabela hash com 500 posições, fator de carga 
        máximo de 70%.
        Utiliza tratamento de colisão por sondagem linear (linear probing).
        '''
        self.__load_factor = 0.70  # fator de carga máximo 70%
        self.__length = 0          # quantidade de buckets ocupados
        self.__table = np.full(size, None) # tabela hash usando um array numpy

    def __hash(self, key:any)->int:
        '''
        Calcula o hash da chave, utilizando o método de resto da divisão
        (Hash modular)
        Argumentos
        ----------
        key (any): chave de mapeamento
        Retorno
        -------
        int: índice (bucket) mapeado para a tabela hash
        '''
        return hash(key) % len(self.__table)

    def __rehash(self, bucket:any)->int:
        '''
        Realiza o rehashing do bucket em colisão utilizando o cálculo por sondagem linear.
        Argumentos
        ----------
        bucket (int): índice do bucket em colisão
        Retorno
        -------
        int: índice do próximo bucket
        '''
        return (bucket + 1) % len(self.__table)

    def __search(self, key:any):
        '''
        Retorna o bucket correspondente a uma determinada chave na tabela hash.
        Argumentos:
            key(any): chave a ser pesquisada
        Retorna:
            bucket(int): índice da chave na tabela hash
        Raise
            KeyError: se a chave não for encontrada na tabela hash
        '''
        bucket = self.__hash(key)
        if self.__table[bucket] is None:
            raise KeyError(f'Key {key} not found')
        if self.__table[bucket][0] != key:
            original_bucket = bucket
            while self.__table[bucket][0] != key:
                bucket = self.__rehash(bucket)
                if self.__table[bucket] is None:
                    raise KeyError(f'Key {key} not found')
                if bucket == original_bucket:
                    raise KeyError(f'Key {key} not found')
        return bucket

    def put(self, key:any, value:any):
        '''
        Insere uma entrada chave/valor na tabela hash.
        Se a chave já existir, o valor associado à chave será substituído.
        Argumentos
        ----------
        key (any): chave de mapeamento
        value (any): valor associado à chave
        '''
        slot = self.__hash(key) # calcula o hash modular da chave
        
        while self.__table[slot] not in [None,'X'] and \
              self.__table[slot][0] != key:
            slot = self.__rehash(slot)

        if self.__table[slot] in [None,'X']:
            self.__length += 1

        tuple = (key, value)
        self.__table[slot] = tuple
        # Teste do fator de carga
        if (self.__length / float(len(self.__table))) >= self.__load_factor:
            self.__resize()

    def __setitem__(self, key:any, value:any):
        self.put(key, value)

    def get(self, key:any)->any:
        '''
        Retorna o valor associado à chave
        Argumentos
        ----------
        key (any): chave de busca
        Retorno
        -------
        any: valor associado à chave (de qualquer tipo)
        Raise
        -----
        KeyError: se a chave não for encontrada na tabela hash
        '''
        index = self.__search(key)
        return self.__table[index][1]

    def __getitem__(self, key:any)->any:
        '''
        Retorna o valor associado à chave
        Argumentos
        ----------
        key (any): chave de busca
        Retorno
        -------
        any: valor associado à chave (de qualquer tipo)
        '''
        return self.get(key)
    
    def remove(self, key:any)->any:
        '''
        Elimina a entrada da tabela hash correspondente à chave de busca
        Argumentos:
            key(any): chave a ser removida
        Retorna:
            data(any): valor associado à chave removida
        Observação:
            A chave é substituída por 'X' para indicar que o bucket está livre
            e impedir a busca infinita, ou seja, quando um slot dentro de 
            um agrupamento é removido e os slots seguintes não são alcançados.
        '''
        bucket = self.__search(key)
        data = None
        if bucket is not None:
            data = self.__table[bucket][1] 
            self.__table[bucket] = 'X'
            self.__length -= 1
            return data
        raise KeyError(f'chave {key} nao encontrada')

    def __delitem__(self, key):
        self.remove(key)

    def __contains__(self, key:any)->bool:
        '''
        Método que verifica se uma chave está na tabela de dispersão.
        Acionado em situações de uso do operador "in": "if chave in hashTable".
        Argumentos:
            key(Any): chave do elemento a ser buscado.
        Retorna:
            bool: True se a chave estiver na tabela de dispersão e False caso contrário.
        '''
        try:
            self.__search(key)
            return True
        except KeyError:
            return False

    def items(self)->list[tuple]:
        '''
        Método que retorna um list com todos os pares chave/valor da tabela de dispersão.
        Retorna:
            list(tuple): lista de tuplas com todos os pares chave/valor 
        '''
        return [tuple for tuple in self.__table if tuple not in [None,'X']]

    def keys(self)->list:
        '''
        Retorna uma lista com todas as chaves da tabela hash
        '''
        return [tuple[0] for tuple in self.__table if (tuple is not None and tuple != 'X')]

    def values(self)->list:
        '''
        Retorna uma lista com todos os valores da tabela hash
        '''
        return [tuple[1] for tuple in self.__table if tuple is not None]
 
    def __len__(self)->int:
        '''
        Retorna a quantidade de elementos na tabela hash
        '''
        return self.__length
    def __resize(self):
        '''
        Redimensiona a tabela hash para o dobro do seu tamanho.
        Uma nova tabela é criada e os elementos da tabela antiga são 
        inseridos na nova tabela. Haverá todo o transporte de dados,
        novo rehashing e novo tratamento de colisão.
        '''
        new_size = len(self.__table) * 2 # dobra o tamanho da tabela
        old_table = self.__table
        self.__table = [None] * new_size
        self.__length = 0
        for tuple in old_table:
            if tuple is not None:
                self[tuple[0]] = tuple[1]

    def showHashTable(self):
        entrada = -1
        print('+--+')
        for item in self.__table:
            entrada += 1
            print(f'|{entrada:2d}| = ', end='') 
            print(f' {item}')
        print('+--+')
    
    def __str__(self):
        '''
        Método que retorna uma string com o conteúdo da tabela de dispersão.        
        Retorno:
            str: string no formato: {chave1:valor1, chave2:valor2, ...}
        '''
        str = '{'
        for i,key in enumerate(self.__table):
            if key == None or key == 'X':
                continue
            str += f'{self.__table[i][0]}:{self.__table[i][1]}, '
        str = str.rstrip(', ')
        str += '}'
        return str