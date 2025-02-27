# 🛰️ Pop (Potstop Online Protocol)

## 📌 Estrutura do Protocolo:
```
method: JOIN | QUIT | START | STOP
data: {}
```

## 📌 Ex:
```
STOP
{"cor": "Azul", "animal": "Arara", "alimento": "Arroz"}
```

## ⚡ Métodos:

> ### 🧩 Erro de requisição:
- **`❌ 0 Bad Request`**: Formato incorreto de requisição.

---

> ### 🛑 STOP
#### 📖 Descrição:
Esse método serve para enviar os dados colocados pelo usuário nas categorias.
É recomendado que os dados sejam enviados no formato de json.
#### 🔍 Exemplo:
```
STOP
{"cor": "Azul", "animal": "Arara", "alimento": "Arroz"}
```
#### 📩 Status:
- ✅ **`10 Stopped`**: O Stop foi realizado com sucesso.
- ❌ **`11 Already Stopped`**: O stop já foi realizado.
- ❌ **`12 Not Started`**: O jogo ainda não começou.

---

> ### 📤 JOIN
#### 📖 Descrição:
Esse método serve para o usuário entrar na sala.
#### 🔍 Exemplo:
```
JOIN
Davi
```
#### 📩 Status:
- ✅ **`20 Joined`**: O usuario entrou na partida com sucesso.
- ❌ **`21 Full Lobby`**: A sala está cheia.
- ❌ **`22 Already Joined`**: Já existe um jogador com esse nome.
- ❌ **`23 Already Started`**: O jogo já começou.
- ❌ **`24 Invalid Name`**: Nome inválido.

---

> ### 📥 QUIT
#### 📖 Descrição:
Esse método serve para o usuários sair da sala.
#### 🔍 Exemplo:
```
QUIT
```
#### 📩 Status:
- ✅ **`30 Left`**: Sucesso ao sair.

---

> ### ✨ START
#### 📖 Descrição:
Esse método serve para iniciar a partida. Apenas o líder consegue iniciá-la.
#### 🔍 Exemplo:
```
START
```
#### 📩 Status:
- ✅ **`40 Started`**: A partida foi iniciada com sucesso.
- ❌ **`41 Unauthorized`**: O usuario não tem permissão para começar a partida.
- ❌ **`42 Already Started`**: A partida já iniciou.
<!-- 
---

> ### 🔄️ RESTART
#### 📖 Descrição:
Esse método serve para recomeçar a partida. Apenas o líder consegue.
#### 🔍 Exemplo:
```
RESTART
```
#### 📩 Status:
- ✅ **`50 Restarted`**: A partida foi iniciada com sucesso.
- ❌ **`51 Unauthorized`**: O usuario não tem permissão para recomeçar a partida (não é o lider).
- ❌ **`52 Game Not Ended`**: A partida não acabou, nem começou.
 -->

<!-- ---

> ### 🪦 END
#### 🛠️ Requisição:
- O usuário envia uma requisição `END` para o servidor.
- Os dados a serem enviados ao servidor estarão em **`data`**.

#### 📩 Resposta:
- ✅ **`50 End`**: Partida encerrada com sucesso.
- ❌ **`54 End Failed`**: Não foi possivel encerrar a partida. -->