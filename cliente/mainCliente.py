from sockets_cliente import Jogador

HOST =  '10.0.73.59'
PORT = 8080
post = (HOST,PORT)

j1 = Jogador(post)
j1.start()
