# RescueFormat 🛡️

RescueFormat é o seu assistente inteligente definitivo para mapear, organizar e salvar o seu PC antes de uma formatação. Ele possui um motor de varredura ultrarrápido feito em Python que vasculha suas pastas ocultas, lê o Registro do Windows e te mostra exatamente o que é Lixo, o que é Ouro e todos os programas que você precisará reinstalar.

## 🚀 Tecnologias Utilizadas
- **Backend:** Python, FastAPI, Uvicorn (Motor de varredura com `os.scandir` e `winreg`)
- **Frontend:** React, Vite, Lucide-React, CSS Customizado (Premium Dark UI)

## 📦 Como Instalar e Rodar o Projeto

Você precisará abrir dois terminais simultaneamente: um para o servidor Python e outro para a interface em React.

### Passo 1: Iniciando o Backend (Motor Python)
1. Abra um terminal na raiz do projeto e entre na pasta `backend`:
   ```bash
   cd backend
   ```
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Inicie o servidor da API (nós usamos o `python -m` para evitar erros de variável de ambiente do uvicorn):
   ```bash
   python -m uvicorn main:app --reload
   ```
   *A API ficará rodando na porta `http://localhost:8000`.*

### Passo 2: Iniciando o Frontend (Interface React)
1. Abra um NOVO terminal na raiz do projeto e entre na pasta `frontend`:
   ```bash
   cd frontend
   ```
2. Instale os pacotes do Node.js:
   ```bash
   npm install
   ```
3. Inicie o painel visual:
   ```bash
   npm run dev
   ```
   *Acesse a interface no seu navegador pelo link: **http://localhost:5173***

---

## 🧠 Como o Ciclo de Vida Funciona (Pré e Pós Formatação)

### 1. Modo Pré-Formatação (O Mapeamento)
Ao abrir a interface no navegador, clique em **"Mapear Meu Computador Agora"**. O painel dividirá sua máquina em quatro colunas:
- 🔴 **Lixo Recomendado:** Caches e arquivos temporários.
- 🟢 **Ouro Encontrado (Gems):** Suas pastas essenciais de usuário e diretórios escondidos vitais (ex: `.vscode`, `.android`, `antigravity`).
- 🔵 **Arquivos Pesados:** Tudo acima de 100MB no seu PC.
- 💻 **Programas para Reinstalar:** A lista definitiva lida direto do Registro do Windows.

Após revisar, role até o final da página e clique em **Salvar "Format_Master_Plan.json"**. 
⚠️ **Muito importante:** Copie este projeto inteiro e o arquivo `.json` gerado para o seu HD Externo/Pen Drive junto com seus arquivos de backup!

### 2. Modo Pós-Formatação (A Restauração)
Você formatou o PC e ele está limpinho!
Abra este projeto de dentro do seu HD Externo, inicie os servidores novamente e clique no botão escuro **"Simular Modo Pós-Formatação"**.

A interface vai entrar no "Modo Recuperação", agindo como seu **Guia de Sobrevivência**. Em vez de escanear o PC, ela vai ler o plano que você salvou e te mostrar:
* Textos nativos informando onde colar cada configuração sensível.
* Botões rápidos para pesquisar tutoriais de instalação no Google ou YouTube para cada software que você tinha antes.
