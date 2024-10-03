import socket
import threading
import time 
import curses
import multiprocessing
from threading import Thread
from treatments import Tratamentos
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
        self.Tratamento = Tratamentos()
        
        
        
        
       
        
    def send_msg(self,mensagem: str):
        print(mensagem)
        self.cliente.send(mensagem.encode())
    
    
        
        
    def recv_msg(self):
        lasty , lastx = self.stdscr.getmaxyx()
        self.msg_box = curses.newwin(lasty-3,lastx,0,0)
        self.msg_box.clear()
        self.msg_box.scrollok(True)
        self.msg_box.addstr(f'Conectado ao servidor\n Digite "sair" para sair ou se cadastre com seu username\n')
        self.msg_box.refresh()
        time.sleep(5)
        while True:
            msg = self.cliente.recv(1024)
            if not msg:
                break
            self.lock.acquire()
            try:
                new_message,self.estado_index = self.Tratamento.tratamento_de_mensagem(msg.decode(),self.estado_index)
                self.msg_box.clear()
                self.msg_box.addstr(new_message)
                #Captura a mensagem e bota na tela no 0,0(começo da tela)
                self.msg_box.refresh()
                self.input_box.refresh()
            finally:
                self.lock.release()
                                  
        
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
                    self.msg_box.refresh()
                    self.input_box.clear()
                    string_a_ser_adicionada = self.Tratamento.input_estado(self.estado_index)
                    self.input_box.addstr(string_a_ser_adicionada)
                    self.input_box.refresh()
                finally:
                    self.lock.release()
                try:
                    msg = self.input_box.getstr().decode()
                    if msg.lower() == "sair":
                        try:
                            t.interrupt_main()
                            self.send(msg.lower())               
                            self.cliente.close()
                            
                        except: pass
                        break
                    else:
                        msg,épara_o_server = self.Tratamento.tratamento_mensagem_com_estado(msg,self.estado_index)
                        if épara_o_server == True:
                            if msg == None:
                                continue
                            self.send_msg(msg.strip())
                        else:
                            '''
                            Se entrar aqui é porque a mensagem é para ser tratada pelo cliente, épara_o_server pode assumir diversas tipos se passar daqui
                            porem será geralmente uma lista de strings
                            
                            '''
                            if msg == 'rspt':
                                
                                self.Mandar_array_em_forma_de_varias_mensagens(épara_o_server)
                                self.msg_box.addstr("Respostas enviadas")

                            elif msg == 'votos':
                                self.Mandar_array_em_forma_de_varias_mensagens(épara_o_server)
                                    
                            else:
                                self.msg_box.addstr(msg)



                except:pass
        except Exception as e:
            self.stdscr.clear()
            self.stdscr.addstr(0,0,f"Erro na conexão: {e}")
            self.stdscr.refresh()
            print(f"Erro na conexão: {e}")
            self.cliente.close()
            self.stdscr.addstr("Conexão encerrada")
            self.stdscr.refresh()


    def start(self):
        print('start')
        try:
            self.cliente.connect(self.server)
            curses.wrapper(self.input)
        except OSError as e:
            print(f"Erro ao iniciar curses: {e}")
            self.cliente.close()
        
    def Mandar_array_em_forma_de_varias_mensagens(self,lista):
        '''
        Função que recebe uma lista de strings e manda cada uma delas para o servidor, necessario time sleep se não as mensagens são concatenadas
        '''
        for i in range(len(lista)):
            self.send_msg(lista[i])
            time.sleep(0.5)    
    
        
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