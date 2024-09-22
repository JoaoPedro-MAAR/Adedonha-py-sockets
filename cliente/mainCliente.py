from sockets_cliente import Jogador

HOST =  'localhost'
PORT = 8081
post = (HOST,PORT)

j1 = Jogador(post)
j1.troca_mensagem_continua()
