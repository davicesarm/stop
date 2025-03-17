# 🎮 Projeto: STOP

## 👥 Autores
- **Davi César de Morais Leite** 📧 *davi.cesar@academico.ifpb.edu.br*
- **Arthur Felipe Araújo da Silva** 📧 *arthur.silva.5@academico.ifpb.edu.br*

## 📚 Disciplinas
- **🖥️ PIRC**  
  *Professor: Leonidas Francisco de Lima Júnior*
- **📊 Estrutura de Dados**  
  *Professor: Alex Sandro da Cunha Rêgo*

## 📝 Descrição do Problema
Este projeto implementa o jogo **STOP** (*também conhecido como Adedonha*) em um ambiente de terminal. A aplicação é desenvolvida em **Python**, utilizando uma arquitetura **cliente-servidor** onde a comunicação entre os jogadores é feita usando **sockets**, garantindo um sistema de rede eficiente e responsivo.  

## 🛠️ Tecnologias Utilizadas
- 🐍 **Python**: Linguagem principal para a lógica do jogo e comunicação entre os clientes.
- 🔗 **Sockets**: Protocolo de comunicação para conectar múltiplos jogadores em uma mesma partida.
- 🎨 **Textual**: Biblioteca utilizada para criar uma interface de terminal interativa e estilizada.

## 🎯 Funcionalidades
- 🕹️ **Modo Multiplayer**: Permite que os jogadores se conectem ao servidor e participem de partidas em tempo real.
- 🔤 **Rodadas Dinâmicas**: O jogo gera letras aleatórias e desafia os jogadores a preencher categorias dentro do tempo estipulado.
- 💻 **Interface no Terminal**: A utilização da biblioteca *Textual* proporciona uma experiência visual agradável e interativa.
- 🌐 **Comunicação via Rede**: O servidor gerencia as conexões dos jogadores e sincroniza as respostas e pontuações.

## 🎯 Objetivo do Projeto
Este projeto tem como objetivo **aplicar conceitos de redes e comunicação via sockets**, ao mesmo tempo que proporciona uma experiência divertida com uma interface no terminal. Também serve como um estudo prático de **desenvolvimento de jogos e sistemas distribuídos**.

## 📂 Estrutura dos Arquivos do Projeto

```plaintext
stop/
├── client/
│   ├── screens/
│   │   ├── entry.py
│   │   ├── game.py
│   │   ├── ranking.py
│   │   ├── waiting.py
│   │   └── __init__.py
│   ├── app.py <- Aplicação cliente principal
│   ├── client.py
│   ├── potstop.tcss
│   └── __init__.py
├── server/
│   ├── data_structures/
│   │   ├── hashtable.py
│   │   ├── queue.py
│   │   └── __init__.py
│   ├── pots.py
│   ├── potstop.py
│   ├── server.py <- Aplicacação servidor principal
│   └── __init__.py
├── .gitignore
├── pop.md
├── README.md
└── requirements.txt
```

## ⚙️ Pré-Requisitos para Execução
- ✅ **Python**: Versão 3.11 ou superior. **(Importante!)**
- ✅ **Pip**: Gerenciador de pacotes para instalar as dependências.

## 🔗 Protocolo da Aplicação
[📜 Documentação do Protocolo (clique aqui!)](pop.md)

## 🚀 Instruções para Execução

1. **Clone o repositório:**  
   ```bash
   git clone https://github.com/davicesarm/stop.git
   ```
2. **Entre no diretório do projeto:**  
   ```bash
   cd stop
   ```
3. **Instale as dependências:**  
   ```bash
   pip install -r requirements.txt
   ```
4. **Rode o servidor:**  
   - **🐧 Linux:**  
     ```bash
     python3 server/server.py
     ```
   - **🖥️ Windows:**  
     ```bash
     python .\server\server.py
     ```
5. **Em outro terminal (dentro do diretório do projeto), rode *n* clientes:**  
   ```bash
   python -m client.app
   ```
   ou, dependendo do sistema operacional:  
   ```bash
   python3 -m client.app
   ```
