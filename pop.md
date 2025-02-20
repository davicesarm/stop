# 🛰️ Pop (Potstop Online Protocol)

## 📌 Estrutura do Protocolo:
```
method: [JOIN | QUIT | START | STOP]
user: [...]
data: [...]
```

## ⚡ Métodos:

> ### 🛑 STOP
#### 🛠️ Requisição:
- Os dados a serem enviados estarão em **`data`**.
- O envio de dados é *opcional* (ex: servidor enviando o stop).
- Dados podem ser retornados na resposta.
#### 📩 Status:
- ✅ **`10 Stopped`**: O Stop foi realizado com sucesso.
- ❌ **`14 Stop Failed`**: Não foi possivel realizar o stop.

---

> ### 📤 JOIN
#### 🛠️ Requisição:
- O usuário envia uma requisição `JOIN` para o servidor.
- *Nenhum dado precisa ser enviado.*
- *Nenhum dado é retornado.*
#### 📩 Status:
- ✅ **`20 Joined`**: O usuario entrou na partida com sucesso.
- ❌ **`21 Full Lobby`**: A sala está cheia.
- ❌ **`22 Room Not Found`**: A sala não foi encontrada.

---

> ### 📥 QUIT
#### 🛠️ Requisição:
- O usuário envia uma requisição `QUIT` para o servidor.
- *Nenhum dado precisa ser enviado.*
- *Nenhum dado é retornado.*
#### 📩 Status:
- ✅ **`30 Left`**: Sucesso ao sair.

---

> ### ✨ START
#### 🛠️ Requisição:
- O usuário envia uma requisição `START` para o servidor.
- *Nenhum dado precisa ser enviado.*
- *Nenhum dado é retornado.*

#### 📩 Status:
- ✅ **`40 Started`**: A partida foi iniciada com sucesso.
- ❌ **`41 Unauthorized`**: O usuario não tem permissão para começar a partida.
- ❌ **`42 Impossible`**: Não foi possível iniciar a partida.

<!-- ---

> ### 🪦 END
#### 🛠️ Requisição:
- O usuário envia uma requisição `END` para o servidor.
- Os dados a serem enviados ao servidor estarão em **`data`**.

#### 📩 Resposta:
- ✅ **`50 End`**: Partida encerrada com sucesso.
- ❌ **`54 End Failed`**: Não foi possivel encerrar a partida. -->