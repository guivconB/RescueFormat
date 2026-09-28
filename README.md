# RescueFormat 🛡️

RescueFormat é o seu assistente inteligente definitivo para mapear, organizar e salvar o seu PC antes de uma formatação. Ele possui um motor de varredura ultrarrápido feito em Python que vasculha suas pastas ocultas, lê o Registro do Windows e te mostra exatamente o que é Lixo, o que é Ouro e todos os programas que você precisará reinstalar, sob uma interface **SaaS Premium**.

### 🌟 Features Avançadas
- **Monitor de Saúde de Disco (S.M.A.R.T):** Avisa se o seu HD está morrendo fisicamente antes de você tentar formatar em vão.
- **Extrator de Wi-Fi:** Captura e revela todas as senhas de Wi-Fi que seu PC já conectou.
- **Auto-Backup de Drivers:** Exporta todos os drivers nativos da sua placa-mãe via DISM.
- **Geração de Scripts:** Cria automações `.bat` para reinstalar programas (via Winget) e fazer backup das pastas em um clique.

## 🚀 Como Iniciar o Projeto (Método Rápido)

Para não precisar abrir múltiplos terminais, o projeto conta com um script inicializador:
Basta dar **duplo-clique** no arquivo `Iniciar_RescueFormat.bat` localizado na raiz do projeto. Ele abrirá o Motor Python e a Interface React automaticamente.

*(Se preferir fazer manualmente, rode `python -m uvicorn main:app --reload` na pasta `backend` e `npm run dev` na pasta `frontend`).*

---

## 🧠 Como o Ciclo de Vida Funciona (Pré e Pós Formatação)

### 1. Modo Pré-Formatação (O Mapeamento)
Ao abrir a interface no navegador (`http://localhost:5173`), clique em **"Mapear Meu Computador Agora"**. O painel exibirá:
- 🔴 **Lixo Recomendado:** Caches e arquivos temporários.
- 🟢 **Ouro Encontrado (Gems):** Pastas vitais de desenvolvimento (`.vscode`, `antigravity`, etc).
- 🔵 **Arquivos Pesados:** Tudo acima de 100MB no seu PC.
- 💻 **Programas Instalados:** Tudo o que consta no Registro do Windows.

Após revisar, role até o final e clique em **"Gerar Scripts de Auto-Backup"**. 
Isto criará uma pasta chamada **`Arquivos_de_Backup_Gerados`** na raiz do projeto contendo:
- `Format_Master_Plan.json` (A memória do sistema)
- `Instalar_Tudo.bat` (Para o PC novo baixar as coisas)
- `Realizar_Backup.bat` (Caminhão de mudança)

⚠️ **Muito importante:** Copie a pasta `Arquivos_de_Backup_Gerados` e este projeto inteiro para o seu HD Externo/Pen Drive!

### 2. Modo Pós-Formatação (A Restauração / Guia de Sobrevivência)
Você formatou o PC e ele está limpinho!
Abra este projeto de dentro do seu HD Externo, inicie o `Iniciar_RescueFormat.bat` novamente e clique em **"Carregar Plano Salvo (Pós-Formatação)"**.

A interface vai entrar no "Modo Recuperação", agindo como seu **Guia de Sobrevivência**. Ela lerá o JSON salvo e te mostrará:
* A chave original do seu Windows.
* Suas senhas antigas de Wi-Fi.
* Textos de tutoriais nativos ensinando onde colar cada pasta oculta no Windows novo (ex: usando `%appdata%`).
* Botões para buscar rapidamente tutoriais extras no Google/YouTube.
