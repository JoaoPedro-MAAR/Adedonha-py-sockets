from sockets_cliente import Jogador

HOST = 'localhost'
PORT = 8082
address = (HOST, PORT)

j1 = Jogador(address)
j1.start()