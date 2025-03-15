- **Título do projeto:** STOP;
- **Autores:** 
    - Davi César de Morais Leite | davi.cesar@academico.ifpb.edu.br;
    - Arthur Felipe Araújo da Silva | arthur.silva.5@academico.ifpb.edu.br;
- **Disciplinas:** 
    - *PIRC* | Leonidas Francisco de Lima Júnior;
    - *Estrutura de Dados* | Alex Sandro da Cunha Rêgo;
- **Descrição do problema:** descrição geral do cenário da aplicação, serviços e funcionalidades que se propõe a contemplar;
- **Arquivos do Projeto:** 
    ```
    stop/
    ├── client/
    │   ├── screens/
    │   │   ├── entry.py
    │   │   ├── game.py
    │   │   ├── ranking.py
    │   │   ├── waiting.py
    │   │   └── __init__.py
    │   ├── app.py
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
    │   ├── server.py
    │   └── __init__.py
    ├── .gitignore
    ├── pop.md
    ├── README.md
    └── requirements.txt
    ```

- **Pré-requisitos para execução:** 
    - Python >= 3.9
    - Pip
- **Protocolo da Aplicação:** documentação de cada uma das mensagens utilizadas no protocolo, indicando os parâmetros enviados e as respostas a serem devolvidas;
- **Instruções para execução:** 
    1. Clone o repositório:
    - `git clone https://github.com/davicesarmorais/stop.git` 
    2. Entre no diretório:
    - `cd stop`
    3. Instale as dependências:
    - `pip install -r requirements.txt`
    4. Rode o servidor:
    - Linux:
        - `python3 servidor.py`
    - Windows:
        - `python servidor.py`
    5. Em outro terminal (no diretorio do projeto), rode *n* clientes:
    - `python cliente.py` ou `python3 cliente.py`
