# 01. Instalando e Configurando o VS Code do Zero

> **Curso:** Python para Desktop  
> **Módulo:** 00 — Configuração do VS Code & Ambiente Python  
> **Nível:** Iniciante / Passo a Passo  
> **Tempo estimado:** 25 min  

---

## 🎯 Objetivos de Aprendizagem

Ao final deste capítulo, você será capaz de:

- Baixar e instalar o **Python 3.14** (ou qualquer versão da 3.11 à 3.15) e o **VS Code** no seu computador.
- Garantir que o comando `python` funcione no terminal.
- Instalar as **extensões profissionais** recomendadas para Python no VS Code.
- Dominar os **atalhos de teclado indispensáveis** do dia a dia.
- Configurar o VS Code para formatar e salvar seu código automaticamente.

---

## 📥 Passo 1: Instalando o Python no Computador

Antes do VS Code, seu computador precisa aprender a entender a linguagem Python.

!!! info "Qual versão instalar?"
    Use o **Python 3.14** — é estável e todas as bibliotecas do curso já funcionam nele. Qualquer versão da **3.11 à 3.15** serve; evite a 3.10 ou anteriores, que já não recebem atualizações de segurança.

=== "🪟 Windows"
    Desde o Python 3.14, o jeito recomendado no Windows é o **Python Install Manager** — um pequeno programa que instala e atualiza o Python pelo terminal.

    1. Acesse [python.org/downloads](https://www.python.org/downloads/) e baixe o **Python install manager** (ou instale **Python Install Manager** pela Microsoft Store).
    2. Execute o instalador e conclua a instalação.
    3. Abra o **PowerShell** e instale o Python 3.14:
       ```powershell
       py install 3.14
       ```
       Na primeira vez, o programa faz algumas perguntas de configuração — pode aceitar as opções sugeridas.
    4. Confira se deu certo:
       ```powershell
       py list
       python --version
       ```
       O segundo comando deve mostrar `Python 3.14.x`.

    ??? note "Computador do laboratório com o instalador antigo?"
        O instalador tradicional (`python-3.14.x-amd64.exe`) ainda existe para as versões 3.14 e 3.15. Se usá-lo, marque `[X] Add python.exe to PATH` na **primeira tela** antes de clicar em **Install Now**.

=== "🐧 Linux (Ubuntu/Debian)"
    Abra o terminal e execute:
    ```bash
    sudo apt update
    sudo apt install python3 python3-pip python3-venv -y
    ```

=== "🍎 macOS"
    Baixe o instalador no site oficial ou via Homebrew:
    ```bash
    brew install python
    ```

!!! danger "O terminal diz que `python` não foi encontrado?"
    - **Com o Install Manager:** abra *Configurações → Aplicativos → Configurações avançadas de aplicativos → Aliases de execução de aplicativo* e deixe ligado o **Python (default)**. Depois rode `py install --refresh` e abra um terminal novo.
    - **Com o instalador antigo:** você não marcou `Add python.exe to PATH`. Execute o instalador de novo, escolha `Modify` e marque a opção.
    - Em qualquer caso, **feche e abra o VS Code** depois de instalar — ele só enxerga o Python novo ao reiniciar.

---

## 💻 Passo 2: Instalando o VS Code

1. Acesse [code.visualstudio.com](https://code.visualstudio.com/) e baixe o instalador para seu sistema operacional.
2. Durante a instalação no Windows, recomendamos marcar as opções:
   - `[X] Criar um atalho na Área de Trabalho`
   - `[X] Adicionar "Abrir com Código" ao menu de contexto de arquivos`
   - `[X] Adicionar "Abrir com Código" ao menu de contexto de diretórios`

---

## 🧩 Passo 3: Extensões Indispensáveis para Python

Abra o VS Code, clique no ícone de **Extensões** na barra lateral esquerda (ou pressione `Ctrl + Shift + X`) e pesquise pelas seguintes extensões:

<div class="grid cards" markdown>

-   :material-language-python: **1. Python (Microsoft)**
    ---
    **Id:** `ms-python.python`  
    Suporte oficial para execução, depuração (debug), autocompletar e linting.

-   :material-lightning-bolt: **2. Pylance (Microsoft)**
    ---
    **Id:** `ms-python.vscode-pylance`  
    Fornece autocompletar ultra-rápido, verificação de tipos e sugestões inteligentes de código.

-   :material-format-paint: **3. Material Icon Theme**
    ---
    **Id:** `PKief.material-icon-theme`  
    Adiciona ícones visuais bonitos e coloridos para cada tipo de arquivo e pasta no seu explorador.

-   :material-circle-slice-8: **4. Error Lens**
    ---
    **Id:** `usernamehw.errorlens`  
    Destaca erros e avisos de sintaxe diretamente na linha do código sem precisar passar o mouse por cima.

-   :material-format-align-left: **5. Python Indent**
    ---
    **Id:** `KevinRose.vsc-python-indent`  
    Ajusta a indentação automática de blocos `if`, `for`, `def` exatamente como o Python exige.

-   :material-auto-fix: **6. Black Formatter (Microsoft)**
    ---
    **Id:** `ms-python.black-formatter`  
    Arruma espaços, aspas e quebras de linha do seu código ao salvar. A extensão Python não traz formatador próprio — sem esta, o "formatar ao salvar" não faz nada.

</div>

---

## ⚙️ Passo 4: Configuração Automática do VS Code (`settings.json`)

Para que seu VS Code formate o código automaticamente ao salvar, pressione `Ctrl + Shift + P`, digite **Preferences: Open User Settings (JSON)** e adicione estas configurações:

```json
{
    "workbench.iconTheme": "material-icon-theme",
    "editor.fontSize": 15,
    "editor.fontFamily": "'JetBrains Mono', 'Fira Code', Consolas, monospace",
    "editor.fontLigatures": true,
    "editor.formatOnSave": true,
    "editor.tabSize": 4,
    "editor.insertSpaces": true,
    "python.analysis.typeCheckingMode": "basic",
    "files.autoSave": "afterDelay",
    "[python]": {
        "editor.defaultFormatter": "ms-python.black-formatter"
    }
}
```

!!! tip "Formatar ao salvar só funciona com um formatador"
    A linha `"[python]"` diz ao VS Code para usar o **Black Formatter** (extensão 6) nos arquivos `.py`. Se ao salvar aparecer "Não há formatador instalado", confira se a extensão está instalada.

---

## ⌨️ Atalhos de Teclado Mágicos do VS Code

| Atalho (Windows/Linux) | Função |
|------------------------|--------|
| `Ctrl + Shift + P` | **Paleta de Comandos** (Busca qualquer comando do VS Code) |
| `Ctrl + ~` (ou `Ctrl + '`) | **Abrir / Fechar Terminal Integrado** |
| `Ctrl + F5` | Executar o arquivo Python atual sem depurador |
| `F5` | Iniciar Depuração (Debug) com pontos de interrupção (breakpoints) |
| `Alt + Shift + F` | Formatar o código atual |
| `Ctrl + B` | Ocultar / Mostrar a barra lateral esquerda |
| `Ctrl + /` | Comentar / Descomentar a linha selecionada |
| `Alt + Seta Cima/Baixo` | Mover a linha atual para cima ou para baixo |

---

## 🧪 Teste Prático: Seu Primeiro Script no VS Code

1. No VS Code, clique em **File ➔ Open Folder** e selecione uma pasta vazia.
2. Crie um arquivo chamado `teste.py`.
3. Digite o seguinte código:

```python
import sys

print("🎉 Parabéns! Seu ambiente Python está funcionando no VS Code!")
print(f"Versão do Python: {sys.version}")
```

4. Pressione `Ctrl + F5` (ou clique no botão de **Play** no canto superior direito).
5. O resultado aparecerá no **Terminal Integrado** na parte inferior!

---

## Exercícios

### Básico (fixação)

1. Crie uma pasta chamada `curso_python` e abra-a no VS Code (**File ➔ Open Folder**).
2. Crie o arquivo `ola.py` com uma linha que mostre `Olá, <seu nome>! Estou pronto para programar.`
3. Execute de **duas formas**: com `Ctrl + F5` e digitando `python ola.py` no terminal integrado (`Ctrl + '`). As duas devem mostrar a mesma mensagem.

<!-- gabarito -->
??? success "Gabarito — Básico"
    Uma solução possível — compare com a sua. Outras formas também podem estar certas.

    ```python
    # ola.py
    print("Olá, Ana! Estou pronto para programar.")

    # Para executar pelo terminal integrado (Ctrl + '), na pasta curso_python:
    #     python ola.py
    # Se aparecer "python não foi encontrado", volte à caixa vermelha do Passo 1.
    ```


### Intermediário (aplicação)

Teste a formatação automática. Crie o arquivo `bagunca.py` com o código abaixo **exatamente assim**, bagunçado:

```python
x=10;y  =  20
print( "soma:",x+y )
nomes=['ana','bia'  ,'caio']
print(len( nomes ))
```

Salve com `Ctrl + S`. O Black deve reorganizar o arquivo sozinho. Compare o antes e o depois: o que mudou nos espaços, nas aspas e no `;`? Rode o arquivo para confirmar que o resultado continua o mesmo.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    Uma solução possível — compare com a sua. Outras formas também podem estar certas.

    ```python
    # bagunca.py — depois de salvar com o Black Formatter ativo
    x = 10
    y = 20
    print("soma:", x + y)
    nomes = ["ana", "bia", "caio"]
    print(len(nomes))

    # O que mudou:
    # - o ";" virou duas linhas: cada instrução na sua linha;
    # - um espaço de cada lado do "=" e do "+", e depois de cada vírgula;
    # - nenhum espaço logo depois de "(" ou antes de ")";
    # - aspas simples viraram duplas (padrão do Black).
    # A saída continua igual: "soma: 30" e "3". Formatar muda a aparência, não o comportamento.
    ```


### Avançado (desafio)

Transforme o script do **Teste Prático** em um `diagnostico.py` que mostre:

- a versão do Python e se ela é **3.11 ou mais nova** (as versões que o curso usa);
- o caminho do executável do Python em uso (`sys.executable`) — é assim que você descobre *qual* Python o VS Code está usando;
- o sistema operacional (`platform.system()` e `platform.release()`).

Dica: você ainda vai aprender `if` no Módulo 01 — se travar, abra o gabarito, copie, rode e observe o resultado.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    Uma solução possível — compare com a sua. Outras formas também podem estar certas.

    ```python
    # diagnostico.py
    import platform
    import sys

    versao = sys.version_info
    print(f"Python {versao.major}.{versao.minor}.{versao.micro}")

    if versao >= (3, 11):
        print("✅ Versão compatível com o curso (3.11 ou mais nova).")
    else:
        print("⚠️ Versão antiga: instale o Python 3.14 (Passo 1).")

    print(f"Executável em uso: {sys.executable}")
    print(f"Sistema: {platform.system()} {platform.release()}")
    ```

