from lista_hasttemas import getEstado,getTemas
import time


class Tratamentos:
    def __init__(self,caixa_de_mensagem:object):
        """Inicializa a classe de tratamento de mensagens do servidor caixa de mensagem sera uma window do curses que sera passada para a classe

        Args:
            caixa_de_mensagem (object): windowm ou standard screen do curses que sera passada para a classe modificar aqui dentro
        """
        self.msg_box = caixa_de_mensagem
        self.index_estado = 0



    def GetIndex(self)->int:
         return self.index_estado


    def tratamento_de_mensagem(self,mensagem:str):
        """Função que trata a mensagem recebida do servidor

        Args:
            mensagem (string): mensagem recebida do servidor
        """
        codigo = mensagem.split(':')
        
        if codigo[0] == '200':
            self.tratamento_200(mensagem)



    def tratamento_200(self,mensagem:str):
        estado = getEstado()
        temas = getTemas()
        try:
                mensagem = mensagem.split(':')
                if mensagem[-1] == '0':
                    
                    self.estado_index = 0
                    self.msg_box.clear()
                    self.msg_box.addstr(f'{estado[self.estado_index].upper()}>Você é o {mensagem[1]} jogador a entrar \n Mande um START para começar o jogo\n')   
                    self.msg_box.refresh()
                elif mensagem[-1] == '1':
                    self.estado_index = 1
                    self.msg_box.clear()
                    self.msg_box.addstr(f'{estado[self.estado_index]}>Jogo iniciado a letra é {mensagem[1]} \n Para responder digite o tema mais resposta \n Os temas são: {temas[0]},{temas[1]},{temas[2]},{temas[3]}\n')
                    self.msg_box.refresh()
                elif mensagem[-1] == '2':
                    self.estado_index = 2
                    self.msg_box.addstr(f'{estado[self.estado_index]}>Votação iniciada\n')
                    self.msg_box.addstr(f'{print(mensagem[2])} Essas são as palavras do tema {mensagem[1]}\n')
                    self.msg_box.addstr(f'Vote nas respostas invalidas se houver mais de uma resposta invalida separe por virgula r1,r2,r3\n')
                    self.msg_box.refresh()
                elif mensagem[-1] == '3':
                    self.estado_index = 3
                    self.msg_box.addstr(f'{estado[self.estado_index]}>Quadro de líderes \n')
                    self.msg_box.refresh()
        except Exception as e:
                print(f"Erro ao tratar mensagem 200: {e}")
                self.msg_box.addstr(f'Erro ao tratar mensagem 200: {e}\n')
                self.msg_box.refresh()

    def tratamento_mensagem_com_estado(self,mensagem:str):
    
        if self.estado_index == 0:
            if mensagem == "start":
                return 'start'
            return f'prnt {mensagem}'

        elif self.estado_index == 1:
            if mensagem.split()[-1] not in self.temas and mensagem.split()[0] != 'stop':
                self.msg_box.addstr(f'Tema inválido\n')
                return None
            if mensagem.split()[-1] in self.temas:
                try:
                    self.hashTemas.put(mensagem.split()[-1],mensagem.split()[0])
                    self.msg_box.addstr(f'{mensagem.split()[-1]}: {mensagem.split()[0]}\n')
                    self.msg_box.refresh()
                    return None
                except Exception as e:
                    print(f"Erro ao inserir tema {e}")
                    self.msg_box.addstr(f'Erro ao inserir tema na : {e}\n')
                    self.msg_box.refresh()
                    return None
            if mensagem == "stop":
                self.msg_box.addstr(f'Jogo encerrado\n')
                self.msg_box.refresh()
                for i in range(len(self.temas)):
                    tema_now = self.temas[i]
                    associado = self.hashTemas.get(tema_now.lower())
                    self.send_msg(f'rspt {associado} {tema_now}')
                    time.sleep(0.1)
                return None
        elif self.estado_index == 2:
            if ',' not in mensagem:
                return f'invld {mensagem}'
            mensagem = mensagem.split(',')
            for i in range(len(mensagem)):
                mensagem[i] = mensagem[i].strip()
                self.send_msg(f'invld {mensagem[i]}')
                time.sleep(0.1)
            return None
                
        
        elif self.estado_index == 3:
            return f'prnt {mensagem}'
        

     
    def input_estado(self):
        if self.estado_index == 0:
            return f'Digite aqui > '
        elif self.estado_index == 1:
            return f'Escreva sua resposta > '
        elif self.estado_index == 2:
            return f'Escreva a sua resposta > '
        elif self.estado_index == 3:
            return f'Faz oque tu quiser doidao > '