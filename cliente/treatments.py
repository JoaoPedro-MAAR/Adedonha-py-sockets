from lista_hasttemas import getEstado,getTemas
from Hashtable import HashTable


class Tratamentos:
    def __init__(self):
        """Inicializa a classe de tratamento de mensagens do servidor caixa de mensagem sera uma window do curses que sera passada para a classe

        Args:
            caixa_de_mensagem (object): windowm ou standard screen do curses que sera passada para a classe modificar aqui dentro
        """
        self.estado = getEstado()
        self.temas = getTemas()
        self.hashTemas = HashTable()

    def tratamento_de_mensagem(self,mensagem:str,estado):
        """Função que trata a mensagem recebida do servidor

        Args:
            mensagem (string): mensagem recebida do servidor
        """
        codigo = mensagem.split(':')
        
        if codigo[0] == '200':
            return self.tratamento_200(mensagem,estado)
        elif codigo[0].isdigit() and 400 <= int(codigo[0]) < 408:
            return self.tratamento_4xx(mensagem,estado)
        

                
    def tratamento_200(self,mensagem:str,estado_index:int):
        try:
            mensagem = mensagem.split(':')
            if mensagem[-1] == '0':
                estado_index = 0
                
                
                return f'{self.estado[estado_index].upper()}>Você é o {mensagem[1]} jogador a entrar \n Mande um START para começar o jogo \n', estado_index  
                
            elif mensagem[-1] == '1':
                estado_index = 1
                
                return f'{self.estado[estado_index]}>Jogo iniciado a letra é {mensagem[1]} \n Para responder digite o tema mais resposta \n Os temas são: {self.temas[0]},{self.temas[1]},{self.temas[2]},{self.temas[3]}\n', estado_index
                
            elif mensagem[-1] == '2':
                estado_index = 2
                temas = mensagem[1]
                respostasArray = mensagem[2]
                respostasString = self.ArrayToString(respostasArray)
                return f'{self.estado[estado_index]}>Votação iniciada\n {print(respostasString)} Essas são as palavras do tema :  {temas}\n Vote nas respostas invalidas se houver mais de uma resposta invalida separe por virgula r1,r2,r3\n',estado_index

            elif mensagem[-1] == '3':
                estado_index = 3
                return f'{self.estado[estado_index]}>Quadro de líderes \n', estado_index



        except Exception as e:
            return f'Erro ao tratar mensagem 200: {e}\n', estado_index
            
    def tratamento_4xx(self,mensagem:str,estado_index:int):
        dict_400 = {
            '400':'Mensagem inválida',
            '401':'Jogador não encontrado',
            '402':'Jogador já cadastrado',
            '403':'Requisição negada',
            '404':'tema não encontrado',
            '406': 'Partida não pode ser iniciada',
            '407': 'Patida em andamento'    
            }
        try:
            mensagem = mensagem.split(':')
            valor = dict_400[mensagem[-1]]
            return f'Erro {valor}\n',estado_index
        except KeyError as e:
            return f'Erro desconhecido 4xx\n',estado_index
            
            
                        

    def tratamento_mensagem_com_estado(self,mensagem:str,estado):
        '''
        Um tratamento de mensagens que recebe uma mensagem e um estado e retorna uma mensagem e um booleano
        Se o booleano for True a mensagem é para ser enviada para o servidor imediatamente
        Se o booleano for False a mensagem é para ser tratada pelo cliente
        e depois pode ser enviada para o servidor
        
        '''
    
        
        if estado == 0:
            if mensagem == "start":
                return 'start',True
            return f'prnt {mensagem}',True

        elif estado == 1:
            if mensagem.split()[-1] not in self.temas and mensagem.split()[0] != 'stop':
                return f'Tema inválido\n',False
                
            if mensagem.split()[-1] in self.temas:
                try:
                    self.hashTemas.put(mensagem.split()[-1],mensagem.split()[0])
                    return f'{mensagem.split()[-1]}:{mensagem.split()[0]}\n', False
                    
                except Exception as e:
                    print(f"Erro ao inserir tema {e}"),
                    return f'Erro ao inserir tema na : {e}\n' , False

            if mensagem == "stop":
                return self.STOP()




        elif estado == 2:
            if ',' in mensagem:
                array_de_mensagem = mensagem.strip().split(',')
                for i in range(len(array_de_mensagem)):
                    internal_text = array_de_mensagem[i].strip()
                    new_internal_text = 'invld ' + internal_text
                    array_de_mensagem[i] = new_internal_text




                return 'votos',array_de_mensagem
            return f'invld {mensagem}',True
               
            
    
        elif estado == 3:
            return f'prnt {mensagem}'

    def input_estado(self,estado):
        if estado == 0:
            return f'Digite aqui > '
        elif estado == 1:
            return f'Escreva sua resposta>'
        elif estado == 2:
            return f'Escreva a sua resposta>'
        elif estado== 3:
            return f'Faz oque tu quiser doidao>'



    def STOP(self):
        """
        Funçao que mandara um array para o sockets_cliente.py com todas as respostas dos temas desse respectivo jogador
        """
        lista_dos_rspt = []
        for i in range(len(self.temas)):
            tema_now = self.temas[i]            
            associado = self.hashTemas.get(tema_now.lower())
            lista_dos_rspt.append(f'rspt {associado} {tema_now} ')
        return 'rspt',lista_dos_rspt



    def ArrayToString(self,array)->str:
        """
        Função que transforma um array em uma string
        """
        string = ''
        for i in range(len(array)):
            string += f'{array[i]} '
        return string