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
O método `STOP` é utilizado para enviar os dados preenchidos pelo usuário nas categorias do jogo.
Os dados devem ser enviados no formato JSON.
#### 🔍 Exemplo:
```
STOP
{"cor": "Azul", "animal": "Arara", "alimento": "Arroz"}
```
#### 📩 Status:
- ✅ **`10 Stopped`**: O Stop foi realizado com sucesso.
- ❌ **`11 Not Started`**: O jogo ainda não começou.

---

> ### 📤 JOIN
#### 📖 Descrição:
O método `JOIN` permite que um usuário entre na sala do jogo.
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
O método `QUIT` permite que um usuário saia da sala.
#### 🔍 Exemplo:
```
QUIT
```
#### 📩 Status:
- ✅ **`30 Left`**: Sucesso ao sair.
- ❌ **`31 Player Not Found`**: Usuário não encontrado.
---

> ### ✨ START
#### 📖 Descrição:
O método `START` é utilizado para iniciar a partida. Apenas o líder pode iniciar o jogo.
#### 🔍 Exemplo:
```
START
```
#### 📩 Status:
- ✅ **`40 Started`**: A partida foi iniciada com sucesso.
- ❌ **`41 Unauthorized`**: O usuario não tem permissão para começar a partida.
- ❌ **`42 Already Started`**: A partida já iniciou.
