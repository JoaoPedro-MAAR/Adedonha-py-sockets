import socket
import threading
import time 
import curses
import multiprocessing
from threading import Thread
from treatments import TratamentosFROMServer
from Hashtable import HashTable

#Ainda sera modularizado em classes, as classes serão separadas em arquivos diferentes e importadas aqui


class Jogador:
    def __init__(self,hostandport: tuple):
        self.server = hostandport
        self.cliente = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.lock = multiprocessing.Lock()
        self.estado = ['inicial','jogo','votacao','quadro_lideres']
        self.estado_index = 0
        self.stdscr = None
        self.temas = ['nome','animal','cidade','objeto']
        self.hashTemas = HashTable()
        
        
        
        
       
        
    def send_msg(self,mensagem: str):
        self.cliente.send(mensagem.encode())
    
    
        
        
    def recv_msg(self):
        lasty , lastx = self.stdscr.getmaxyx()
        self.msg_box = curses.newwin(lasty-3,lastx,0,0)
        self.msg_box.clear()
        self.msg_box.scrollok(True)
        self.msg_box.addstr(f'Conectado ao servidor\n Digite "sair" para sair ou se cadastre com seu username\n')
        self.msg_box.refresh()
        while True:
            msg = self.cliente.recv(1024)
            if not msg:
                break
            self.lock.acquire()
            try:
                self.tratamento_de_mensagem(msg.decode())
                
                #Captura a mensagem e bota na tela no 0,0(começo da tela)
                self.msg_box.refresh()
                self.input_box.refresh()
            finally:
                self.lock.release()
                
    def tratamento_de_mensagem(self,mensagem:str):
        """Função que trata a mensagem recebida do servidor

        Args:
            mensagem (string): mensagem recebida do servidor
        """
        codigo = mensagem.split(' ')
        
        if codigo[0] == '200':
            self.tratamento_200(mensagem)
            
    
                    
    def tratamento_200(self,mensagem:str):
        try:
            mensagem = mensagem.split(':')
            if mensagem[-1] == '0':
                self.estado_index = 0
                self.msg_box.clear()
                self.msg_box.addstr(f'{self.estado[self.estado_index].upper()}>Você é o {mensagem[1]} jogador a entrar \n Mande um START para começar o jogo\n')   
                self.msg_box.refresh()
            elif mensagem[-1] == '1':
                self.estado_index = 1
                self.msg_box.clear()
                self.msg_box.addstr(f'{self.estado[self.estado_index]}>Jogo iniciado a letra é {mensagem[1]} \n Para responder digite o tema mais resposta \n Os temas são: {self.temas[0]},{self.temas[1]},{self.temas[2]},{self.temas[3]}\n')
                self.msg_box.refresh()
            elif mensagem[-1] == '2':
                self.estado_index = 2
                self.msg_box.addstr(f'{self.estado[self.estado_index]}>Votação iniciada\n')
                self.msg_box.addstr(f'{print(mensagem[2])} Essas são as palavras do tema {mensagem[1]}\n')
                self.msg_box.addstr(f'Vote nas respostas invalidas se houver mais de uma resposta invalida separe por virgula r1,r2,r3\n')
                self.msg_box.refresh()
            elif mensagem[-1] == '3':
                self.estado_index = 3
                self.msg_box.addstr(f'{self.estado[self.estado_index]}>Quadro de líderes \n')
                self.msg_box.refresh()
        except Exception as e:
            print(f"Erro ao tratar mensagem 200: {e}")
            self.msg_box.addstr(f'Erro ao tratar mensagem 200: {e}\n')
            self.msg_box.refresh()                        
        
    def input(self, stdscr):
        self.stdscr = stdscr
        self.stdscr.clear()
        curses.echo()
        lasty , lastx = self.stdscr.getmaxyx()
        self.input_box = curses.newwin(2,lastx, lasty-2,0)
        t = Thread(target=self.recv_msg).start()
        try:
            while True:
                self.lock.acquire()
                try:
                    self.input_box.clear()
                    self.input_box.addstr(self.input_estado())
                    self.input_box.refresh()
                finally:
                    self.lock.release()
                try:
                    msg = self.input_box.getstr().decode()
                    if msg.lower() == "sair":
                        try:
                            t.interrupt_main()               
                            self.cliente.close()
                            
                        except: pass
                        break
                    else:
                        msg = self.tratamento_mensagem_com_estado(msg)
                        if msg == None:
                            continue
                        self.send_msg(msg)
                except:pass
        except Exception as e:
            self.stdscr.clear()
            self.stdscr.addstr(0,0,f"Erro na conexão: {e}")
            self.stdscr.refresh()
            print(f"Erro na conexão: {e}")
            self.cliente.close()
            self.stdscr.addstr("Conexão encerrada")
            self.stdscr.refresh()
    
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
            return f'Digite aqui>'
        elif self.estado_index == 1:
            return f'Escreva sua resposta>'
        elif self.estado_index == 2:
            return f'Escreva a sua resposta>'
        elif self.estado_index == 3:
            return f'Faz oque tu quiser doidao>'
    
    def start(self):
        print('start')
        try:
            self.cliente.connect(self.server)
            curses.wrapper(self.input)
        except OSError as e:
            print(f"Erro ao iniciar curses: {e}")
            self.cliente.close()
        
        
        
        
    def listen_continuo(self):
        while True:
            self.recv_msg()

    def troca_msg(self,mensagem:str):
            self.send_msg(mensagem)
            self.recv_msg()
            
    def troca_mensagem_continua(self):
        try:
            while True:
                mensagem = input("Digite a mensagem: ")
                self.troca_msg(mensagem)
                if mensagem == "sair":
                    self.cliente.close()
                    print("Conexão encerrada")
                    break
                elif mensagem.split()[0] == "prnt":
                    if not self.valid_prnt(mensagem):
                        continue
                    #t = threading.Thread(target=self.listen_continuo, args=())
                    #t.start()
        except Exception as e:
            print(f"Erro na conexão: {e}")
            self.cliente.close()
            print("Conexão encerrada")
            
    def valid_prnt(self,mensagem:str )-> bool:
        """comando para verificar se o comando prnt está correto 

        Args:
            mensagem (string): string que contém o comando prnt que o usuario digitou

        Returns:
            boolean : True se o comando estiver correto, False caso contrário
        """
        if len(mensagem.split()) != 2:
            print("Comando inválido")
            return False
        return True