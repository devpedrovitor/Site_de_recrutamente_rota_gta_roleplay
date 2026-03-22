# 🎮 RotaGTA — Sistema de Recrutamento RP

Sistema web de recrutamento de players para servidor de roleplay, com formulário em duas etapas, armazenamento no MongoDB e envio automático de embed no Discord via bot.

---

## 📋 Funcionalidades

- Formulário em duas etapas (dados pessoais + questões táticas)
- Armazenamento das candidaturas no MongoDB Atlas
- Envio automático de embed no canal do Discord ao finalizar o formulário
- Reações ✅ ❌ para aprovação/recusa pelo staff
- Bot e servidor web rodando juntos no mesmo processo

---

## 🗂️ Estrutura do Projeto

```
rotagta/
├── modules/
│   └── mongodb_conncetion.py    # Handler de conexão com MongoDB
├── static/
│   └── logo_rota.jpg            # Logo do servidor
├── template/
│   ├── index.html               # Landing page
│   ├── formulario.html          # Etapa 1 — dados pessoais
│   └── tatico.html              # Etapa 2 — questões táticas
├── .env                         # Variáveis de ambiente (não sobe pro Git)
├── .gitignore
├── bot.py                       # Bot do Discord e função de embed
├── main.py                      # Flask + inicialização do bot
├── README.md
└── requirements.txt
```

---

## ⚙️ Fluxo do Sistema

```
Candidato preenche /formulario
        ↓ insert_one() — salva dados pessoais
    session['id'] salvo
        ↓
Candidato preenche /tatico
        ↓ update_one() — adiciona questões táticas
Documento completo buscado do MongoDB
        ↓
Bot envia embed no canal do Discord
        ↓
Staff reage com ✅ ou ❌
```

---

## 🚀 Como Rodar

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/rotagta.git
cd rotagta
```

### 2. Crie e ative o ambiente virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o `.env`

Crie um arquivo `.env` na raiz do projeto:

```env
TOKEN_DISCORD=seu_token_aqui
MONGO_URI=mongodb+srv://usuario:senha@cluster.mongodb.net/
```

### 5. Rode o projeto

```bash
python main.py
```

Você verá no terminal:

```
🌐 Flask iniciando na porta 5000...
🤖 Bot do Discord iniciando...
✅ Bot online como SeuBot#1234
```

Acesse em: `http://localhost:5000`

### 6. Acessar na rede local (celular, outro PC)

```bash
# Windows — descubra seu IP
ipconfig
```

Acesse pelo IP: `http://SEU_IP:5000`

---

## 🗃️ Variáveis de Ambiente

| Variável | Descrição |
|---|---|
| `TOKEN_DISCORD` | Token do bot do Discord |
| `MONGO_URI` | URI de conexão com o MongoDB Atlas |

---

## 🗄️ Estrutura do Documento no MongoDB

Cada candidatura é salva com a seguinte estrutura:

```json
{
  "_id": "ObjectId(...)",
  "name": "PlayerX",
  "age": "22",
  "nick": "PlayerX_GTA",
  "discord": "playerx#1234",
  "server_id": "123456",
  "exp": "3 anos em servidores RP",
  "hist": "Sem histórico de ban",
  "rdm": "Não",
  "vdm": "Não",
  "pg": "Não",
  "meta": "Não",
  "car_jacking": "Sim, com RP",
  "surf": "Não",
  "disp": "Noite e fins de semana",
  "q1": "Resposta da questão 1",
  "q2": "Resposta da questão 2",
  "q3": "Resposta da questão 3",
  "q4": "Resposta da questão 4",
  "q5": "Resposta da questão 5",
  "q6": "Resposta da questão 6",
  "status": "pendente"
}
```

---

## 🤖 Embed no Discord

Ao finalizar o formulário, o bot envia automaticamente uma embed no canal configurado com todos os dados do candidato e adiciona as reações ✅ e ❌ para o staff votar.

Para configurar o canal, altere o `CANAL_ID` no `bot.py`:

```python
CANAL_ID = 1485285844292997152  # ID do canal do Discord
```

---

## 📦 Dependências

```
flask
discord.py
pymongo
python-dotenv
dnspython
```

Gere o arquivo com:

```bash
pip freeze > requirements.txt
```

---
