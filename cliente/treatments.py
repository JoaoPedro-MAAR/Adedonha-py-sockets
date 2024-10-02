from lista_hasttemas import getEstado,getTemas



class TratamentosFROMServer:
    def __init__(self,caixa_de_mensagem:object):
        """Inicializa a classe de tratamento de mensagens do servidor caixa de mensagem sera uma window do curses que sera passada para a classe

        Args:
            caixa_de_mensagem (object): windowm ou standard screen do curses que sera passada para a classe modificar aqui dentro
        """
        self.msg_box = caixa_de_mensagem

    def tratamento_200(self,mensagem:str):
        estado = getEstado()
        temas = getTemas()
        try:
                mensagem = mensagem.split(':')
                if mensagem[-1] == '0':
                    
                    estado_index = 0
                    self.msg_box.clear()
                    self.msg_box.addstr(f'{estado[estado_index].upper()}>Você é o {mensagem[1]} jogador a entrar \n Mande um START para começar o jogo\n')   
                    self.msg_box.refresh()
                elif mensagem[-1] == '1':
                    estado_index = 1
                    self.msg_box.clear()
                    self.msg_box.addstr(f'{estado[estado_index]}>Jogo iniciado a letra é {mensagem[1]} \n Para responder digite o tema mais resposta \n Os temas são: {temas[0]},{temas[1]},{temas[2]},{temas[3]}\n')
                    self.msg_box.refresh()
                elif mensagem[-1] == '2':
                    estado_index = 2
                    self.msg_box.addstr(f'{estado[estado_index]}>Votação iniciada\n')
                    self.msg_box.addstr(f'{print(mensagem[2])} Essas são as palavras do tema {mensagem[1]}\n')
                    self.msg_box.addstr(f'Vote nas respostas invalidas se houver mais de uma resposta invalida separe por virgula r1,r2,r3\n')
                    self.msg_box.refresh()
                elif mensagem[-1] == '3':
                    estado_index = 3
                    self.msg_box.addstr(f'{estado[estado_index]}>Quadro de líderes \n')
                    self.msg_box.refresh()
        except Exception as e:
                print(f"Erro ao tratar mensagem 200: {e}")
                self.msg_box.addstr(f'Erro ao tratar mensagem 200: {e}\n')
                self.msg_box.refresh()