 Adedonha-py-sockets

Um projeto que simula virtualmente o jogo de Adedonha, permitindo interações através de comandos.

 Descrição

O **Adedonha-py-sockets** é uma implementação do popular jogo de palavras Adedonha, onde os jogadores podem interagir em um ambiente virtual. O jogo suporta diversos comandos que facilitam a dinâmica de competição e colaboração entre os participantes. Os principais comandos disponíveis são:

- PRNT: Registrar-se no jogo.
- RSPT: Enviar uma resposta.
- INVLD: Invalidar a resposta de outro usuário.
- STOP: Finalizar a rodada, concedendo uma vantagem ao jogador.
- SAIR: Desconectar do jogo.

O jogo possui diferentes estados, incluindo:

- Inicial
- Jogo
- Votação
- Quadro de Líderes

 Uso

Para jogar Adedonha, basta executar o projeto e seguir as instruções na interface de comandos. O sistema pode ser facilmente adaptado para outros jogos de palavras ou jogos em turnos, utilizando os comandos existentes.

### Requisitos

- Python 3.9 ou maior 
- Curses
- time
- threading
 Instalação

1. Clone este repositório:
   ```bash
      https://github.com/JoaoPedro-MAAR/Adedonha-py-sockets

2. Classes 
## Classe Servidor

A classe `Servidor` no arquivo [sockets_servidor.py](https://github.com/JoaoPedro-MAAR/Adedonha-py-sockets/blob/main/servidor/sockets_servidor.py) é responsável por gerenciar a lógica do servidor para o jogo Adedonha. Aqui estão alguns dos principais pontos sobre a classe:

- **Iniciação**: Configura o servidor, define temas e estados do jogo.
- **Conexões**: Aceita novas conexões e cria threads para ouvir mensagens dos clientes.
- **Comandos**: Trata comandos como PRNT (registro), RSPT (resposta), INVLD (invalidar resposta), STOP (finalizar rodada), e SAIR (desconectar).
- **Estados do Jogo**: Implementa a lógica para diferentes estados do jogo, incluindo inicial, jogo, votação e quadro de líderes.
- **Mensagens**: Envia e recebe mensagens dos clientes, tratando as respostas e atualizando o estado do jogo conforme necessário.

Esta classe permite a interação entre os jogadores e mantém o fluxo do jogo de forma organizadação!

Esta classe ainda será modularizada em servidor.py que ficaria a cargo da conexão do jogador, e game.py que ficaria a cargo de 

### Classe Player

A classe `Player` no arquivo [classPlayer.py](https://github.com/JoaoPedro-MAAR/Adedonha-py-sockets/blob/main/servidor/classPlayer.py) representa um jogador no jogo Adedonha. Aqui estão os principais pontos sobre a classe:

- **Atributos**:
  - `name`: Nome do jogador.
  - `socket`: Conexão do socket associada ao jogador.
  - `palavras`: Lista de palavras fornecidas pelo jogador.
  - `pontuacao`: Pontuação atual do jogador.

- **Métodos**:
  - `__init__(self, name: str, socket)`: Inicializa um novo jogador com um nome e uma conexão de socket.
  - `__str__(self)`: Retorna uma string representando o jogador, incluindo seu nome e pontuação.
  - `soma_pontos(self, pontos)`: Adiciona pontos à pontuação do jogador e retorna a pontuação atualizada.
  - `__eq__(self, other)`: Compara dois jogadores com base em seus nomes.

Esta classe encapsula as informações e comportamentos básicos de um jogador no jogo, permitindo o gerenciamento eficiente dos jogadores e suas interações.


### Classe Tentativa

A classe `Tentativa` no arquivo [classTentativa.py](https://github.com/JoaoPedro-MAAR/Adedonha-py-sockets/blob/main/servidor/classTentativa.py) representa uma tentativa de resposta por parte de um jogador no jogo Adedonha. Aqui estão os principais pontos sobre a classe:

- **Atributos**:
  - `nome`: Lista de jogadores que submeteram a mesma palavra.
  - `palavra`: Palavra submetida pelo jogador, armazenada em letras minúsculas.
  - `pontos`: Pontos atribuídos à tentativa.
  - `valid`: Indicador de validade da tentativa (True ou False).

- **Métodos**:
  - `__init__(self, user: object, palavra)`: Inicializa uma nova tentativa com um jogador e uma palavra.
  - `__str__(self)`: Retorna uma string representando a tentativa, incluindo o nome do jogador e a palavra.
  - `setNewPlayers(self, jogador: object)`: Adiciona um novo jogador à lista de jogadores que submeteram a mesma palavra.
  - `uptadePontos(self, pontos)`: Atualiza os pontos atribuídos à tentativa e retorna a nova pontuação.
  - `getPalavra(self)`: Retorna a palavra submetida.
  - `getisValid(self)`: Retorna se a tentativa é válida ou não.
  - `invalidar(self)`: Invalida a tentativa.
  - `submit_points(self)`: Submete os pontos aos jogadores caso a tentativa seja válida.
  - `__eq__(self, value: any) -> bool`: Compara duas tentativas com base na palavra submetida.

Esta classe encapsula as informações e comportamentos básicos de uma tentativa no jogo, permitindo o gerenciamento eficiente das respostas dos jogadores e suas pontuações.


### Classe Jogador

A classe `Jogador` no arquivo [sockets_cliente.py](https://github.com/JoaoPedro-MAAR/Adedonha-py-sockets/blob/main/cliente/sockets_cliente.py) representa um cliente jogador no jogo Adedonha. Aqui estão os principais pontos sobre a classe:

- **Atributos**:
  - `server`: Endereço e porta do servidor.
  - `cliente`: Socket do cliente para conexão com o servidor.
  - `lock`: Lock para operações de thread-safe.
  - `estado`: Lista de estados do jogo.
  - `estado_index`: Índice do estado atual do jogo.
  - `stdscr`: Tela de interface do curses.
  - `temas`: Lista de temas do jogo.
  - `hashTemas`: HashTable para armazenar os temas e respostas.

- **Métodos**:
  - `__init__(self, hostandport: tuple)`: Inicializa um novo jogador com o endereço e porta do servidor.
  - `send_msg(self, mensagem: str)`: Envia uma mensagem para o servidor.
  - `recv_msg(self)`: Recebe mensagens do servidor e as exibe na interface.
  - `tratamento_de_mensagem(self, mensagem: str)`: Trata a mensagem recebida do servidor.
  - `tratamento_200(self, mensagem: str)`: Trata mensagens com código 200 do servidor.
  - `input(self, stdscr)`: Captura a entrada do usuário através da interface curses.
  - `tratamento_mensagem_com_estado(self, mensagem: str)`: Trata a mensagem do usuário de acordo com o estado do jogo.
  - `input_estado(self)`: Retorna uma mensagem de prompt de acordo com o estado do jogo.
  - `start(self)`: Inicia a conexão com o servidor e a interface curses.
  - `listen_continuo(self)`: Escuta continuamente as mensagens do servidor.
  - `troca_msg(self, mensagem: str)`: Envia e recebe uma mensagem do servidor.
  - `troca_mensagem_continua(self)`: Continua a troca de mensagens com o servidor.
  - `valid_prnt(self, mensagem: str) -> bool`: Verifica se o comando prnt está correto.

Esta classe encapsula as informações e comportamentos básicos de um jogador cliente no jogo, permitindo a interação com o servidor e o gerenciamento das respostas e estados do jogo.


Esta classe ainda será modularizada em outras classes exemplo em jogador.py para ser a classe principal , Treatments.py para tratamento das mensagens que chegam do servidor e que saem do input do cliente , alem de outras funções menores






   


