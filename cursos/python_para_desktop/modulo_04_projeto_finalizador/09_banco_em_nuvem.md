# 09 — Banco em Nuvem com Neon

## 🎯 Objetivo

Neste capítulo, o Sistema Escolar deixa de guardar os dados num arquivo do seu computador e passa a usar um **banco de dados PostgreSQL na nuvem**, o **Neon**. Qualquer computador com o programa e a senha certa enxerga os mesmos alunos.

Ao final, você terá:

- Um projeto no **Neon** com o banco do Sistema Escolar
- A **connection string** guardada num arquivo `.env`, fora do código e fora do Git
- O módulo `database/conexao.py` conectando ao Neon com o driver **psycopg**
- O módulo `database/operacoes.py` falando **PostgreSQL** (as diferenças para o SQLite)
- Um script que **leva os alunos do `escola.db` para a nuvem**
- Um indicador 🟢 **Online** / 🔴 **Offline** e um botão **🔄 Recarregar** na tela de cadastro
- Mensagens claras quando não há internet, em vez de um erro gigante no terminal

## 📍 Contextualização

No Capítulo 08, você concluiu o CRUD: o sistema cadastra, lista, edita, exclui e busca alunos, tudo no SQLite (`escola.db`). Funciona — mas os dados moram **dentro de um arquivo, num único computador**.

E se a secretaria tiver dois computadores? E se a coordenação quiser consultar de outra sala? E se o computador estragar?

A resposta profissional é um **banco em nuvem**: um servidor de banco de dados que fica ligado na internet, e o programa conversa com ele pela rede. Vamos usar o **Neon**, um serviço de **PostgreSQL** — o mesmo tipo de banco que empresas usam em produção — com plano gratuito.

E aqui a arquitetura do Capítulo 02 mostra o seu valor: **só a pasta `database/` muda**. As telas (`views/`) e os controllers (`controllers/`) continuam exatamente iguais, porque nunca souberam qual banco estava por trás.

```mermaid
flowchart LR
    V["🖥️ views/<br/>cadastro.py"] --> C["🧠 controllers/<br/>aluno.py"]
    C --> D["🗄️ database/<br/>conexao.py + operacoes.py"]
    D -- "antes (Cap. 07–08)" --> S[("💾 escola.db<br/>SQLite no seu PC")]
    D -- "agora (Cap. 09)" --> N[("☁️ Neon<br/>PostgreSQL na nuvem")]
```

**Progresso do Sistema:**

```text
✅ Capítulo 01 — Introdução e Planejamento
✅ Capítulo 02 — Arquitetura do Sistema
✅ Capítulo 03 — Tela de Login
✅ Capítulo 04 — Menu Principal
✅ Capítulo 05 — Múltiplas Janelas
✅ Capítulo 06 — Cadastro de Alunos
✅ Capítulo 07 — SQLite
✅ Capítulo 08 — CRUD Completo
🔨 Banco em Nuvem (Neon) ← VOCÊ ESTÁ AQUI
⬜ Integração e Testes
⬜ Refatoração e Entrega
```

!!! warning "A troca tem um preço: sem internet, sem banco"
    Com o SQLite, o sistema funcionava até no meio do mato. Com o banco na nuvem, **cada operação passa pela internet**. Em troca, os dados ficam num só lugar, com cópia de segurança, e acessíveis de qualquer computador. Neste capítulo você vai tratar a falta de conexão com mensagens claras — e, no Desafio, pensar em como juntar os dois mundos.

## ✅ Resultado Esperado

A tela de cadastro continua igual, com uma faixa nova embaixo da busca:

```text
┌──────────────────────────────────────────────────────┐
│  Cadastro de Alunos                              _ □ X│
│                                                      │
│  ┌─ Dados do Aluno ────────────────────────────────┐ │
│  │  ...                                            │ │
│  └─────────────────────────────────────────────────┘ │
│  ┌─ Busca ─────────────────────────────────────────┐ │
│  │  ...                                            │ │
│  └─────────────────────────────────────────────────┘ │
│  ☁️ Neon: 🟢 Online                 [🔄 Recarregar]  │
│  ┌─ Alunos Cadastrados (12) ───────────────────────┐ │
│  │  ...                                            │ │
│  └─────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────┘
```

<figure markdown="span">
  ![Tela Cadastro de Alunos do Sistema Escolar com a faixa Neon Online em verde, o botão Recarregar e a lista com os cinco alunos migrados do SQLite](assets/09_app_online.webp){ loading=lazy }
  <figcaption>O Sistema Escolar de verdade, conectado ao Neon: (1) o indicador <strong>Online</strong> · (2) o botão <strong>Recarregar</strong> · (3) os alunos vêm da nuvem.</figcaption>
</figure>

- Tudo o que você cadastrar vai direto para o Neon. Abra o sistema em **outro computador** com o mesmo `.env` e os alunos estão lá.
- Sem internet: o sistema avisa com uma mensagem amigável em vez de travar ou mostrar um traceback.

Arquivos criados ou modificados:

| Arquivo | Ação |
|---|---|
| `.env` | Novo — a connection string do Neon (**NÃO** vai para o Git) |
| `.env.exemplo` | Novo — modelo do `.env`, sem a senha (esse vai para o Git) |
| `.gitignore` | Novo ou modificado — ignora `.env` e `escola.db` |
| `database/conexao.py` | Reescrito — conecta ao Neon em vez do SQLite |
| `database/operacoes.py` | Modificado — SQL no jeito do PostgreSQL |
| `migrar_para_nuvem.py` | Novo — copia os alunos do `escola.db` para o Neon (roda uma vez) |
| `main.py` | Modificado — avisa se não conseguir conectar ao abrir |
| `views/cadastro.py` | Modificado — indicador de status, botão Recarregar e erros de rede |
| `controllers/aluno.py` | **Não muda** |

!!! tip "Antes de começar: guarde uma cópia"
    Você vai reescrever o `database/conexao.py`. Se usa Git (Módulo 05), faça um commit agora. Se não, copie a pasta do projeto inteira para `sistema_escolar_sqlite`. Assim dá para voltar se algo der errado.

## 💻 Implementação Guiada

### Passo 1 — SQLite × PostgreSQL: o que muda

O SQL que você aprendeu continua valendo: `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `WHERE`, `ORDER BY`. Mudam alguns detalhes — e eles aparecem no código deste capítulo:

| Assunto | SQLite (Cap. 07–08) | PostgreSQL / Neon (Cap. 09) |
|---|---|---|
| Onde fica | Um arquivo (`escola.db`) | Um servidor na internet |
| Biblioteca Python | `sqlite3` (já vem com o Python) | `psycopg` (instalar com `pip`) |
| Como conectar | Caminho do arquivo | **Connection string** com usuário e senha |
| Marcador dos valores | `?` | `%s` |
| Id automático | `INTEGER PRIMARY KEY AUTOINCREMENT` | `INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY` |
| Pegar o id criado | `cursor.lastrowid` | `INSERT ... RETURNING id` |
| Busca sem diferenciar maiúsculas | `LIKE` já ignora (para letras sem acento) | `LIKE` **diferencia** — use `ILIKE` |
| Quem acessa | Quem tem o arquivo | Quem tem a connection string |

!!! danger "Nunca monte SQL juntando texto"
    O `%s` do psycopg **não** é o `%` de formatação de texto do Python. Escreva `conn.execute("... WHERE id = %s", (id_aluno,))` e deixe o psycopg encaixar o valor com segurança. Nunca faça `f"... WHERE nome = '{nome}'"`: um nome como `x'; DROP TABLE alunos; --` apagaria a tabela. Esse ataque se chama **SQL injection**.

### Passo 2 — Criando o banco no Neon

Escolha o seu caminho:

=== "Caminho A — tenho 18 anos ou mais"

    O Neon (hoje parte da empresa Databricks) **não é direcionado a menores de 18 anos**. Se você tem 18 ou mais, crie a sua conta gratuita — o plano gratuito **não pede cartão de crédito**.

    1. Acesse **neon.com** e clique em **Sign up**. Dá para entrar com a conta do GitHub ou do Google, ou com e-mail.
    2. Clique em **New project** e preencha:
        - **Project name:** `sistema-escolar`
        - **Region:** **AWS South America East 1 (São Paulo)** — a mais perto do Brasil, então as respostas chegam mais rápido
        - Deixe **Postgres database** ligado e clique em **Create project**.

        ![Janela Create project do Neon com o nome sistema-escolar, a região AWS South America East 1 (São Paulo) e o quadro do plano gratuito com 1 GB storage](assets/09_neon_criar_projeto.webp){ loading=lazy }

        *(1) Nome do projeto · (2) região São Paulo · (3) o que o plano gratuito inclui: 1 GB de armazenamento e o banco que “dorme” quando ninguém usa · (4) Create project.*

    3. O projeto abre no painel. À esquerda ficam o botão **Connect** e, mais abaixo, **Tables**, **SQL Editor** e **Roles**, que você vai usar neste capítulo.

        ![Painel do projeto sistema-escolar no Neon, com o botão Connect e os itens Tables, SQL Editor e Roles do menu em destaque](assets/09_neon_painel.webp){ loading=lazy }

        *(1) Connect · (2) Tables: ver os dados · (3) SQL Editor: rodar comandos SQL · (4) Roles: usuários e senhas do banco.*

    4. Clique em **Connect**. Na janela **Connect to your branch**, deixe o banco `neondb` e o usuário (*Role*) que vierem marcados e clique em **Copy snippet**: ele copia a connection string **com a senha**. Na tela, a senha aparece escondida (`****`); **Show password** mostra a senha — evite clicar nele com alguém olhando a sua tela.

        ![Janela Connect to your branch com a connection string, a senha escondida por asteriscos e o endereço do servidor coberto, e os botões Copy snippet, Show password, Reset password e a chave Connection pooling](assets/09_neon_connect.webp){ loading=lazy }

        *(1) A connection string (o endereço do servidor foi coberto nesta imagem) · (2) Copy snippet: copia tudo, com a senha · (3) Show password · (4) Reset password: troca a senha · (5) Connection pooling: deixe ligado.*

    A connection string tem este formato:

    ```text
    postgresql://usuario:SENHA@ep-nome-123456.sa-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
    ```

    !!! note "O console do Neon é em inglês"
        Os nomes dos botões estão em inglês e podem mudar um pouco com o tempo. Procure pelo sentido: *criar projeto*, *conectar*, *copiar*.

=== "Caminho B — tenho menos de 18 anos"

    Você **não** cria conta no Neon. O professor cria o banco e entrega a sua equipe a **connection string** por um canal privado (nunca no grupo da turma).

    1. Receba a connection string do professor.
    2. Siga normalmente a partir do **Passo 3**: o resto do capítulo é igual para todos.

    Quando fizer 18 anos, você pode criar a sua conta e trocar só a connection string no `.env` — o código não muda.

!!! important "Nota para o Professor"
    Para o Caminho B, crie a conta com o **seu** e-mail. O plano gratuito permite **até 100 projetos** (cada um com 1 GB e 100 horas de computação por mês): um projeto por equipe deixa os dados de cada equipe separados e o limite de um não atrapalha o outro. Entregue a connection string a cada equipe em particular. No fim do semestre, troque a senha de cada projeto (**Connect ➔ Reset password**, ou em **Roles**) ou apague os projetos.

Entenda as partes da connection string:

```text
postgresql://usuario:SENHA@ep-nome-123456.sa-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
└─ tipo ───┘ └─ quem ─┘└ ─ ┘ └──────────── onde (servidor) ────────────┘ └banco┘ └──────── segurança ────────┘
                       senha
```

- **usuário e senha**: quem pode entrar. Com eles, qualquer pessoa lê, altera e apaga o banco inteiro.
- **servidor (host)**: o endereço do seu banco na internet.
- **banco**: `neondb`, o banco padrão do projeto.
- **`sslmode=require`**: a conversa entre o seu programa e o Neon vai **criptografada**.

!!! tip "O banco “dorme” quando ninguém usa"
    No plano gratuito, o Neon desliga a computação depois de **5 minutos parado** e liga de novo na próxima conexão. Por isso, a primeira operação depois de um tempo pode demorar um pouquinho mais. É normal.

### Passo 3 — Instalando o psycopg e guardando a senha no `.env`

Instale as bibliotecas (no terminal do VS Code, com o ambiente virtual ativo, se você usa um):

```bash
pip install "psycopg[binary]" python-dotenv
```

- **`psycopg`** (versão 3): o driver que deixa o Python conversar com PostgreSQL. É o que o próprio Neon recomenda para projetos novos. O `[binary]` instala a versão pronta, sem precisar compilar nada.
- **`python-dotenv`**: lê o arquivo `.env` e coloca os valores nas variáveis de ambiente.

Crie o arquivo **`.env`** na raiz do projeto (`sistema_escolar/.env`) e cole a sua connection string:

```text
# ===== BANCO EM NUVEM (NEON) =====
# ATENÇÃO: este arquivo NÃO vai para o Git nem para o grupo da turma.
DATABASE_URL=postgresql://usuario:SENHA@ep-nome-123456.sa-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
```

Crie também o **`.env.exemplo`**, um modelo **sem** a senha, que pode ir para o Git e mostra aos colegas o que preencher:

```text
# Copie este arquivo para .env e cole a connection string do Neon.
DATABASE_URL=postgresql://usuario:senha@servidor/neondb?sslmode=require&channel_binding=require
```

E crie (ou complete) o **`.gitignore`** na raiz:

```text
# Segredos
.env

# Banco local antigo (Cap. 07–08)
escola.db

# Arquivos gerados pelo Python
__pycache__/
*.pyc
```

```mermaid
flowchart LR
    E["🔑 .env<br/>DATABASE_URL com a senha"] -->|"lido pelo python-dotenv<br/>quando o programa abre"| P["🐍 database/conexao.py"]
    E -. "bloqueado pelo .gitignore" .-x G["🌐 GitHub"]
    X["📄 .env.exemplo<br/>sem a senha"] --> G
    P -->|"conexão criptografada"| N[("☁️ Neon")]
```

!!! danger "Erro crítico: senha no código ou no GitHub"
    **Nunca** cole a connection string dentro de um arquivo `.py` e **nunca** faça commit do `.env`. Robôs varrem o GitHub o tempo todo atrás de senhas de banco. Se a sua vazar, troque a senha **na hora** no console do Neon (**Connect ➔ Reset password**) e atualize o `.env` com a connection string nova.

### Passo 4 — Reescrevendo `database/conexao.py`

Substitua todo o conteúdo de `database/conexao.py`:

```python
# ======================================================================
# conexao.py — Gerenciador de Conexão com o Neon (PostgreSQL)
# ======================================================================
# Eu sou o responsável por conectar ao banco na nuvem e garantir
# que as tabelas existam antes de qualquer operação.
# A senha NÃO fica aqui: eu leio a DATABASE_URL do arquivo .env.
# ======================================================================

import os
from pathlib import Path

import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

# ---------- CARREGAMENTO DO .env ----------
# Eu procuro o .env na raiz do projeto (a pasta acima de database/).
load_dotenv(Path(__file__).parent.parent / ".env")


def _url_do_banco():
    """
    Eu devolvo a connection string guardada no .env.

    Se ela não existir, eu aviso com uma mensagem clara
    em vez de deixar o erro aparecer lá na frente.
    """
    url = os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError(
            "DATABASE_URL não encontrada. Crie o arquivo .env na raiz "
            "do projeto com a connection string do Neon."
        )
    return url


def conectar():
    """
    Eu abro e retorno uma conexão com o Neon.

    Use sempre com 'with conectar() as conn:'. Ao sair do with,
    o psycopg confirma as alterações (commit) e fecha a conexão.
    Se der erro dentro do with, ele desfaz tudo (rollback).

    row_factory=dict_row faz cada linha vir como dicionário,
    igual ao sqlite3.Row dos capítulos anteriores: aluno["nome"].
    """
    return psycopg.connect(
        _url_do_banco(),
        row_factory=dict_row,
        connect_timeout=10,  # desisto depois de 10 s sem resposta
    )


def inicializar_banco():
    """
    Eu crio as tabelas do sistema, caso ainda não existam.

    Chamada uma vez, quando o programa abre (no main.py).
    """
    with conectar() as conn:
        # ---------- TABELA DE ALUNOS ----------
        # GENERATED ALWAYS AS IDENTITY é o jeito do PostgreSQL de
        # numerar os registros sozinho (no SQLite era AUTOINCREMENT).
        conn.execute("""
            CREATE TABLE IF NOT EXISTS alunos (
                id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                nome TEXT NOT NULL,
                idade INTEGER NOT NULL,
                turma TEXT NOT NULL
            )
        """)


def verificar_conexao():
    """
    Eu testo se o Neon está respondendo.

    Retorno True se conseguir conectar, False se não houver
    internet, se a senha estiver errada ou se faltar o .env.
    """
    try:
        with psycopg.connect(_url_do_banco(), connect_timeout=5) as conn:
            conn.execute("SELECT 1")
        return True
    except (psycopg.Error, RuntimeError):
        return False
```

!!! note "Conceito Importante: `with` no psycopg"
    No `sqlite3`, o `with` confirmava as alterações, mas **não fechava** a conexão. No `psycopg`, o `with conectar() as conn:` faz as duas coisas: confirma (*commit*) quando tudo dá certo — ou desfaz (*rollback*) se acontecer um erro — e fecha a conexão no fim. Por isso não precisamos mais chamar `conn.commit()`.

### Passo 5 — Adaptando `database/operacoes.py`

As funções têm **os mesmos nomes e os mesmos parâmetros** do Capítulo 08 — por isso o controller não muda. Por dentro, o SQL ganha o sotaque do PostgreSQL. Substitua o conteúdo de `database/operacoes.py`:

```python
# ======================================================================
# operacoes.py — Operações CRUD no Neon (PostgreSQL)
# ======================================================================
# Eu centralizo todas as queries SQL do sistema.
# O controller me chama — eu converso com o banco.
# Diferenças para o SQLite: %s no lugar de ?, RETURNING id
# no lugar de lastrowid, e ILIKE para buscar sem ligar
# para maiúsculas e minúsculas.
# ======================================================================

from database.conexao import conectar


def inserir_aluno(nome, idade, turma):
    """
    Eu insiro um novo aluno e retorno o id gerado pelo banco.
    """
    with conectar() as conn:
        linha = conn.execute("""
            INSERT INTO alunos (nome, idade, turma)
            VALUES (%s, %s, %s)
            RETURNING id
        """, (nome, idade, turma)).fetchone()
        return linha["id"]


def listar_alunos(filtro_nome=None):
    """
    Eu busco os alunos em ordem alfabética, com filtro opcional.

    Retorno uma lista de dicionários com id, nome, idade e turma.
    """
    with conectar() as conn:
        if filtro_nome:
            # ILIKE: "ana" encontra "Ana" e "ANA".
            cursor = conn.execute("""
                SELECT id, nome, idade, turma FROM alunos
                WHERE nome ILIKE %s
                ORDER BY nome
            """, (f"{filtro_nome}%",))
        else:
            cursor = conn.execute(
                "SELECT id, nome, idade, turma FROM alunos ORDER BY nome"
            )
        return cursor.fetchall()


def atualizar_aluno(id_aluno, nome, idade, turma):
    """
    Eu atualizo os dados de um aluno existente.
    """
    with conectar() as conn:
        conn.execute("""
            UPDATE alunos
            SET nome = %s, idade = %s, turma = %s
            WHERE id = %s
        """, (nome, idade, turma, id_aluno))


def excluir_aluno(id_aluno):
    """
    Eu removo um aluno do banco.
    """
    with conectar() as conn:
        conn.execute("DELETE FROM alunos WHERE id = %s", (id_aluno,))


def contar_alunos(filtro_nome=None):
    """
    Eu retorno quantos alunos existem (com o mesmo filtro da listagem).
    """
    with conectar() as conn:
        if filtro_nome:
            linha = conn.execute(
                "SELECT COUNT(*) AS total FROM alunos WHERE nome ILIKE %s",
                (f"{filtro_nome}%",)
            ).fetchone()
        else:
            linha = conn.execute(
                "SELECT COUNT(*) AS total FROM alunos"
            ).fetchone()
        return linha["total"]
```

O caminho de um clique em **Salvar**, do botão até a nuvem e de volta:

```mermaid
sequenceDiagram
    actor U as 👤 Secretaria
    participant V as views/cadastro.py
    participant C as controllers/aluno.py
    participant O as database/operacoes.py
    participant N as ☁️ Neon
    U->>V: clica em 💾 Salvar
    V->>C: salvar_aluno("Ana", 15, "1A")
    C->>O: inserir_aluno("Ana", 15, "1A")
    O->>N: INSERT ... VALUES (%s, %s, %s) RETURNING id
    N-->>O: id = 13
    O-->>C: 13
    C-->>V: {"id": 13, "nome": "Ana", ...}
    V-->>U: "Aluno 'Ana' cadastrado!"
```

!!! tip "Dica Profissional"
    Repare: `controllers/aluno.py` e `views/cadastro.py` **não sabem** que o banco mudou. Essa é a recompensa por separar as responsabilidades no Capítulo 02. Em empresas, trocar de banco sem mexer nas telas é exatamente o que essa organização permite.

### Passo 6 — Levando os alunos do `escola.db` para o Neon

Os alunos que você cadastrou nos Capítulos 07 e 08 estão no `escola.db`. Vamos copiá-los para a nuvem **uma única vez**. Crie o arquivo `migrar_para_nuvem.py` na raiz do projeto (ao lado do `main.py`):

```python
# ======================================================================
# migrar_para_nuvem.py — Copia os alunos do SQLite para o Neon
# ======================================================================
# Eu rodo UMA vez: leio o escola.db (Cap. 07–08) e envio os alunos
# para a tabela no Neon. Se a tabela na nuvem já tiver alunos,
# eu paro, para não duplicar ninguém.
# Uso: python migrar_para_nuvem.py
# ======================================================================

import sqlite3
from pathlib import Path

from database.conexao import conectar, inicializar_banco

CAMINHO_SQLITE = Path(__file__).parent / "escola.db"


def migrar():
    if not CAMINHO_SQLITE.exists():
        print("Não encontrei o escola.db. Nada para migrar.")
        return

    # 1. Leio os alunos do banco local.
    local = sqlite3.connect(CAMINHO_SQLITE)
    alunos = local.execute("SELECT nome, idade, turma FROM alunos").fetchall()
    local.close()
    print(f"Encontrei {len(alunos)} aluno(s) no escola.db.")

    # 2. Garanto que a tabela exista no Neon.
    inicializar_banco()

    with conectar() as conn:
        # 3. Não migro duas vezes.
        total = conn.execute(
            "SELECT COUNT(*) AS total FROM alunos"
        ).fetchone()["total"]
        if total > 0:
            print(f"O Neon já tem {total} aluno(s). Migração cancelada.")
            return

        # 4. Envio todos de uma vez. Os ids são criados pelo Neon.
        with conn.cursor() as cursor:
            cursor.executemany(
                "INSERT INTO alunos (nome, idade, turma) VALUES (%s, %s, %s)",
                alunos
            )

    print(f"Pronto: {len(alunos)} aluno(s) copiados para o Neon.")


if __name__ == "__main__":
    migrar()
```

Rode no terminal, na pasta do projeto:

```bash
python migrar_para_nuvem.py
```

Saída esperada (com os seus números):

```text
Encontrei 5 aluno(s) no escola.db.
Pronto: 5 aluno(s) copiados para o Neon.
```

Rodou de novo sem querer? Ele responde `O Neon já tem 5 aluno(s). Migração cancelada.` e não duplica nada.

!!! note "E os ids?"
    No Neon, os alunos ganham ids novos (1, 2, 3...), na ordem em que foram enviados. O sistema não depende do número em si — ele só usa o id para saber qual linha editar ou excluir. E o banco **não reaproveita** números: se o aluno 6 for excluído, o próximo cadastrado recebe o 7, e o 6 fica vago para sempre.

    ![Página Tables do Neon com a tabela alunos selecionada e os ids 1, 2, 3, 4, 5, 7 e 8, sem o 6](assets/09_neon_tables.webp){ loading=lazy }

    *(1) Em **Tables**, a tabela `alunos` aparece com os dados · (2) do 5 o id pula para o 7: o 6 foi de um aluno excluído.*

### Passo 7 — Avisando no `main.py` quando não há conexão

Antes, `inicializar_banco()` sempre funcionava, porque o arquivo estava no seu computador. Agora ele depende da internet e do `.env`. Abra o `main.py` e troque a chamada do Capítulo 07 por esta versão:

```python
# ===== SUBSTITUA a chamada inicializar_banco() do Cap. 07 por: =====
from tkinter import messagebox
from database.conexao import inicializar_banco

# Eu preparo o banco na nuvem. Sem conexão, eu aviso e encerro,
# em vez de abrir um sistema que não consegue salvar nada.
try:
    inicializar_banco()
except Exception as erro:
    # O detalhe técnico vai para o terminal, para quem programa.
    print(f"Erro ao conectar ao banco: {erro}")
    # A janela mostra só o que o usuário precisa saber.
    messagebox.showerror(
        "❌ Sem conexão com o banco",
        "Não consegui conectar ao banco na nuvem (Neon).\n\n"
        "Confira a internet e o arquivo .env e abra o sistema de novo."
    )
    janela.destroy()
    raise SystemExit(1)
```

<figure markdown="span">
  ![Mensagem Sem conexão com o banco: Não consegui conectar ao banco na nuvem (Neon). Confira a internet e o arquivo .env e abra o sistema de novo.](assets/09_app_abertura_sem_conexao.webp){ loading=lazy }
  <figcaption>O que aparece ao abrir o sistema sem conexão: uma frase clara, sem detalhes técnicos.</figcaption>
</figure>

!!! tip "Mensagem para o usuário, detalhe para o programador"
    A mensagem de erro do psycopg pode ter **várias linhas** técnicas (endereços, portas, tentativas). Na tela, isso só assusta quem usa o sistema. Por isso ela vai para o **terminal** com `print`, e a janela mostra uma frase que o usuário entende e sabe o que fazer.

!!! note "Por que `except Exception` aqui"
    Na abertura podem acontecer erros diferentes: sem internet (`psycopg.OperationalError`), senha errada (também `OperationalError`) ou `.env` faltando (`RuntimeError`, que nós mesmos criamos no `conexao.py`). Todos levam à mesma resposta — avisar e fechar —, então um `except Exception` é suficiente neste ponto.

### Passo 8 — Status, Recarregar e erros de rede na tela de cadastro

Agora a tela de cadastro mostra se o Neon está respondendo e ganha um botão para recarregar a lista — útil quando **outro computador** cadastrou alunos.

No topo de `views/cadastro.py`, adicione os imports:

```python
# ===== ADICIONE ESTES IMPORTS no topo de views/cadastro.py =====
import psycopg
from database.conexao import verificar_conexao
```

Logo depois do `frame_busca.pack(...)` e **antes** do `frame_lista`, crie a faixa de status:

```python
    # ---------- FAIXA DE STATUS DA NUVEM ----------
    frame_status = tk.Frame(janela, bg="#f5f6fa")
    frame_status.pack(fill=tk.X, padx=20, pady=(5, 0))

    # Eu mostro se o Neon está respondendo.
    lbl_status = tk.Label(
        frame_status,
        text="☁️ Neon: ⏳ verificando...",
        font=("Arial", 10, "bold"),
        bg="#f5f6fa",
        fg="#555555"
    )
    lbl_status.pack(side=tk.LEFT)

    # Eu recarrego a lista direto da nuvem.
    btn_recarregar = tk.Button(
        frame_status,
        text="🔄 Recarregar",
        font=("Arial", 10, "bold"),
        bg="#3498db",
        fg="white",
        activebackground="#2980b9",
        activeforeground="white",
        width=14,
        bd=0,
        cursor="hand2",
        command=lambda: ao_clicar_recarregar()
    )
    btn_recarregar.pack(side=tk.RIGHT)
```

Dentro de `abrir_janela_cadastro`, junto das outras funções, adicione:

```python
    # ===== STATUS DA NUVEM =====

    def verificar_status():
        """Eu testo a conexão e pinto o indicador."""
        if verificar_conexao():
            lbl_status.config(text="☁️ Neon: 🟢 Online", fg="#27ae60")
            return True
        lbl_status.config(text="☁️ Neon: 🔴 Offline", fg="#e74c3c")
        return False

    def avisar_sem_conexao():
        """Eu explico o problema de rede sem assustar o usuário."""
        verificar_status()
        messagebox.showerror(
            "❌ Sem conexão",
            "Não consegui falar com o banco na nuvem.\n"
            "Confira a internet e tente de novo."
        )

    def ao_clicar_recarregar():
        """Eu busco a lista de novo no Neon."""
        try:
            atualizar_tabela()
            verificar_status()
        except psycopg.OperationalError:
            avisar_sem_conexao()
```

E proteja as operações que conversam com o banco. Veja como fica o `ao_clicar_salvar`:

```python
    def ao_clicar_salvar():
        """Eu insiro um novo aluno no banco."""
        nome = entry_nome.get().strip()
        idade_str = entry_idade.get().strip()
        turma = combo_turma.get().strip()
        valido, idade = validar_campos(nome, idade_str, turma)
        if not valido:
            return
        try:
            salvar_aluno(nome, idade, turma)
        except psycopg.OperationalError:
            # Os campos continuam preenchidos: dá para tentar de novo.
            avisar_sem_conexao()
            return
        messagebox.showinfo("Sucesso", f"Aluno '{nome}' cadastrado!")
        limpar_campos()
        atualizar_tabela()
```

Por fim, no **carregamento inicial** (o final de `abrir_janela_cadastro`), troque o `atualizar_tabela()` por:

```python
    # ===== CARREGAMENTO INICIAL =====
    if verificar_status():
        atualizar_tabela()
```

!!! tip "A janela “congela” uns segundos sem internet"
    Sem conexão, `verificar_conexao()` espera até **5 segundos** (o `connect_timeout`) antes de desistir, e nesse tempo a janela não responde. É o comportamento esperado neste capítulo. Programas profissionais fazem essa espera em segundo plano, com `threading` — fica como ideia para depois do curso.

!!! note "Por que `psycopg.OperationalError`"
    É o erro que o psycopg lança quando a **conexão** falha: sem internet, servidor fora do ar, tempo esgotado. Erros de SQL (uma coluna com nome errado, por exemplo) são de outro tipo e **devem** aparecer enquanto você programa, para serem corrigidos — por isso não capturamos todos os erros aqui.

### Passo 9 — Testando

1. Rode `python main.py`, faça login e abra o **Cadastro de Alunos**.
2. O indicador deve mostrar **☁️ Neon: 🟢 Online**, e a tabela, os alunos migrados.
3. Cadastre um aluno novo. Ele aparece na tabela.
4. Abra o console do Neon ➔ **SQL Editor** e rode:

    ```sql
    SELECT * FROM alunos ORDER BY id;
    ```

    O aluno que você acabou de cadastrar está lá — gravado na nuvem.

    ![SQL Editor do Neon com a consulta SELECT * FROM alunos ORDER BY id, o botão Run e o resultado com seis alunos, o último sendo Fábio Nunes, cadastrado pelo app](assets/09_neon_sql_select.webp){ loading=lazy }

    *(1) A consulta · (2) Run · (3) o aluno cadastrado pelo app minutos antes.*

5. Ainda no SQL Editor, cadastre um aluno “por fora”:

    ```sql
    INSERT INTO alunos (nome, idade, turma) VALUES ('Bruna Teixeira', 15, '1A');
    ```

    ![SQL Editor com o comando INSERT da aluna Bruna Teixeira e a mensagem Statement executed successfully](assets/09_neon_sql_insert.webp){ loading=lazy }

    Volte ao sistema e clique em **🔄 Recarregar**: a Bruna aparece. Foi isso que um segundo computador faria.

    ![Tela Cadastro de Alunos depois do Recarregar, com Bruna Teixeira na lista e o total de 7 alunos](assets/09_app_recarregar.webp){ loading=lazy }

    *(1) Recarregar · (2) a Bruna, inserida pelo SQL Editor, já aparece no sistema.*

6. **Teste sem internet:** desligue o Wi-Fi (ou tire o cabo) e clique em **Salvar** com um aluno preenchido. Deve aparecer a mensagem **Sem conexão** — e os campos continuam preenchidos. Ligue a internet, clique em **Recarregar** e salve de novo.

    ![À esquerda, a tela de cadastro com o indicador Neon Offline em vermelho e o formulário ainda preenchido com Gabriela Alves; à direita, a mensagem Sem conexão: Não consegui falar com o banco na nuvem. Confira a internet e tente de novo.](assets/09_app_sem_conexao.webp){ loading=lazy }

    *(1) A mensagem amigável · (2) o indicador fica vermelho · (3) os dados digitados continuam lá para tentar de novo.*

7. Feche o sistema, desligue a internet e abra de novo: deve aparecer a mensagem do `main.py` e o sistema fecha sem traceback.

## 📝 Exercício

**Tempo estimado:** 20–25 minutos

**Tarefa:** O Passo 8 protegeu só o `ao_clicar_salvar`. Proteja também `ao_clicar_editar`, `ao_clicar_excluir` e `ao_clicar_buscar`, para que **nenhuma** falta de internet gere traceback. (O `ao_selecionar` não precisa: ele só lê a linha clicada na tabela da tela, sem consultar o banco.) Depois, faça o teste 6 com cada botão.

??? hint "Dica"
    O padrão é sempre o mesmo: envolva **só a linha que conversa com o banco** num `try/except psycopg.OperationalError`, chame `avisar_sem_conexao()` e use `return` para não seguir em frente (não mostrar “Sucesso”, não limpar os campos).

??? success "Solução resumida"
    ```python
    def ao_clicar_editar():
        """Eu atualizo o aluno selecionado no banco."""
        global id_selecionado
        if id_selecionado is None:
            messagebox.showwarning("Aviso", "Selecione um aluno para editar.")
            return
        nome = entry_nome.get().strip()
        idade_str = entry_idade.get().strip()
        turma = combo_turma.get().strip()
        valido, idade = validar_campos(nome, idade_str, turma)
        if not valido:
            return
        try:
            editar_aluno(id_selecionado, nome, idade, turma)
        except psycopg.OperationalError:
            avisar_sem_conexao()
            return
        messagebox.showinfo("Sucesso", f"Aluno '{nome}' atualizado!")
        limpar_campos()
        atualizar_tabela()

    def ao_clicar_excluir():
        """Eu removo o aluno selecionado após confirmação."""
        global id_selecionado
        if id_selecionado is None:
            messagebox.showwarning("Aviso", "Selecione um aluno para excluir.")
            return
        nome = entry_nome.get().strip()
        resposta = messagebox.askyesno(
            "Confirmar Exclusão",
            f"Tem certeza que deseja excluir o aluno '{nome}'?\n\nEsta ação não pode ser desfeita."
        )
        if not resposta:
            return
        try:
            remover_aluno(id_selecionado)
        except psycopg.OperationalError:
            avisar_sem_conexao()
            return
        messagebox.showinfo("Excluído", f"Aluno '{nome}' removido do sistema.")
        limpar_campos()
        atualizar_tabela()

    def ao_clicar_buscar():
        """Eu filtro a tabela pelo texto digitado na busca."""
        termo = entry_busca.get().strip()
        try:
            atualizar_tabela(filtro_nome=termo if termo else None)
        except psycopg.OperationalError:
            avisar_sem_conexao()
    ```

    **Confira:** sem internet, cada botão mostra a mensagem *Sem conexão* e o indicador fica 🔴. Com a internet de volta, **Recarregar** deixa tudo 🟢.

## 🏆 Missão da Equipe

**Tempo estimado:** 40–50 minutos

**Tarefa:** Levem o sistema da equipe para o Neon.

**Entregável:** o sistema da equipe com:

- Banco no Neon — conta própria (18+) ou connection string entregue pelo professor
- `.env` com a `DATABASE_URL` (fora do Git) e `.env.exemplo` (no Git)
- `database/conexao.py` e `database/operacoes.py` no jeito do PostgreSQL, para a entidade do projeto
- Os registros do SQLite migrados com um `migrar_para_nuvem.py` adaptado
- Indicador 🟢/🔴, botão Recarregar e mensagens de erro de rede

**Checklist da Missão:**

- [ ] Projeto no Neon criado (ou connection string recebida do professor)
- [ ] `.env` com `DATABASE_URL`; `.env.exemplo` sem a senha
- [ ] `.gitignore` com `.env` e o arquivo `.db`
- [ ] `psycopg` e `python-dotenv` instalados
- [ ] Tabela da entidade criada com `GENERATED ALWAYS AS IDENTITY`
- [ ] Todas as operações usam `%s` (nenhum SQL montado com f-string)
- [ ] Migração feita uma vez, sem duplicar
- [ ] Registro novo aparece no **SQL Editor** do Neon
- [ ] Registro inserido pelo SQL Editor aparece no sistema depois de **Recarregar**
- [ ] Sem internet: mensagem amigável, nenhum traceback
- [ ] O professor viu o sistema funcionando

!!! important "Nota para o Professor"
    Peça a cada equipe: (1) cadastrar um registro pelo sistema e mostrá-lo no **SQL Editor**; (2) inserir um registro pelo SQL Editor e mostrá-lo no sistema com **Recarregar**; (3) abrir o `.gitignore` e o `git status`, para provar que o `.env` não vai para o Git; (4) desligar a internet e clicar em **Salvar**. Se der, rode o sistema da equipe em **dois computadores** ao mesmo tempo: é a demonstração mais convincente do banco em nuvem.

## ⚡ Desafio

**Vá além:** anote **quando** cada aluno foi cadastrado.

1. No SQL Editor do Neon, acrescente uma coluna com a data e a hora do cadastro, preenchida sozinha pelo banco:

    ```sql
    ALTER TABLE alunos
    ADD COLUMN cadastrado_em TIMESTAMPTZ NOT NULL DEFAULT now();
    ```

2. Em `operacoes.py`, inclua `cadastrado_em` no `SELECT` de `listar_alunos`.
3. Em `views/cadastro.py`, mostre uma coluna **Cadastrado em** no Treeview, no formato `dd/mm/aaaa hh:mm`.

??? success "Solução resumida"
    No `listar_alunos`, troque `SELECT id, nome, idade, turma` por `SELECT id, nome, idade, turma, cadastrado_em` (nos dois `SELECT`). No Treeview:

    ```python
    colunas = ("nome", "idade", "turma", "cadastrado")
    tree = ttk.Treeview(frame_lista, columns=colunas, show="headings", height=10)
    tree.heading("cadastrado", text="Cadastrado em")
    tree.column("cadastrado", width=140, anchor="center")
    ```

    E no `atualizar_tabela`:

    ```python
    for aluno in listar_alunos(filtro_nome):
        data = aluno["cadastrado_em"].astimezone().strftime("%d/%m/%Y %H:%M")
        tree.insert(
            "", tk.END,
            iid=aluno["id"],
            values=(aluno["nome"], aluno["idade"], aluno["turma"], data)
        )
    ```

    O psycopg entrega `cadastrado_em` como um `datetime` do Python. O `.astimezone()` converte para o fuso do seu computador. Os alunos migrados mostram a hora em que a coluna foi criada.

**Para pensar (sem código):** com o banco só na nuvem, a secretaria fica parada quando a internet cai. Como você juntaria os dois mundos — gravar no SQLite quando estiver sem rede e enviar para o Neon quando a conexão voltar? Que problemas apareceriam se dois computadores editassem o mesmo aluno enquanto estavam desconectados? (Esse é um problema real, chamado **conflito de sincronização**.)

## ⚠️ Erros Comuns

!!! danger "`RuntimeError: DATABASE_URL não encontrada`"
    **Causa:** o `.env` não existe, está em outra pasta ou a variável tem outro nome.

    **Solução:** o `.env` fica na **raiz** do projeto, ao lado do `main.py` — não dentro de `database/`. Confira se a linha começa exatamente com `DATABASE_URL=` e se o arquivo não ficou salvo como `.env.txt` (no Windows, ative *Exibir ➔ Extensões de nomes de arquivos*).

!!! danger "`psycopg.OperationalError: ... password authentication failed`"
    **Causa:** a senha na connection string está errada ou foi trocada no console.

    **Solução:** copie a connection string **de novo** na janela **Connect** do Neon e cole no `.env`, sem espaços e sem aspas sobrando.

!!! warning "`psycopg.OperationalError: ... timeout expired` ou `could not translate host name`"
    **Causa:** sem internet, ou a rede da escola bloqueia a porta do PostgreSQL (5432).

    **Solução:** teste outra rede (o roteador do celular, por exemplo). Se só a rede da escola falha, peça ao professor para verificar o bloqueio com a equipe de TI.

!!! warning "`psycopg.errors.SyntaxError: ... at or near \"?\"`"
    **Causa:** sobrou um `?` do SQLite numa consulta.

    **Solução:** no psycopg, o marcador é `%s`. Procure por `?` em `operacoes.py` (`Ctrl + F`) e troque todos.

!!! warning "A busca por “ana” não encontra “Ana”"
    **Causa:** no PostgreSQL, `LIKE` diferencia maiúsculas de minúsculas.

    **Solução:** use `ILIKE`, como em `listar_alunos` e `contar_alunos`.

!!! warning "`ModuleNotFoundError: No module named 'psycopg'`"
    **Causa:** a biblioteca foi instalada em outro Python, ou o nome está errado.

    **Solução:** rode `pip install "psycopg[binary]"` no **mesmo** terminal em que você executa o `main.py` (com o ambiente virtual ativo). Atenção: `psycopg2` é a versão antiga, com outro nome de módulo.

!!! warning "A primeira operação demora alguns segundos"
    **Causa:** o banco estava “dormindo” (5 minutos sem uso, no plano gratuito).

    **Solução:** nenhuma — é o funcionamento normal. As operações seguintes são rápidas.

## 💡 Boas Práticas

**1. Segredo mora no `.env`**

A connection string é a chave do banco inteiro. Ela fica no `.env`, que está no `.gitignore`. No Git vai apenas o `.env.exemplo`. Em empresas, os servidores injetam essas variáveis sem arquivo nenhum — a ideia é a mesma.

**2. Sempre `%s`, nunca f-string no SQL**

Deixar o psycopg encaixar os valores protege contra **SQL injection** e evita erros com nomes que têm apóstrofo, como *D'Ávila*.

**3. Trate o erro de rede onde o usuário está**

Erro de conexão é esperado num sistema em nuvem. Mostre uma mensagem clara na tela e mantenha os dados digitados para o usuário tentar de novo.

**4. Uma camada só conhece o banco**

Toda a troca de SQLite por PostgreSQL ficou em `database/`. Se um dia o sistema mudar para outro banco, as telas e os controllers continuam intactos.

**5. Migração com trava**

Scripts que mexem em dados devem ser seguros para rodar duas vezes. O `migrar_para_nuvem.py` confere se a nuvem já tem alunos antes de enviar.

## ☑️ Checklist

Antes de prosseguir para o próximo capítulo, confirme:

- [ ] Banco criado no Neon (Caminho A) ou connection string recebida do professor (Caminho B)
- [ ] `psycopg` e `python-dotenv` instalados
- [ ] `.env` na raiz com `DATABASE_URL`; `.env.exemplo` sem a senha
- [ ] `.gitignore` com `.env` e `escola.db`
- [ ] `database/conexao.py` reescrito para o Neon, com `verificar_conexao()`
- [ ] `database/operacoes.py` com `%s`, `RETURNING id` e `ILIKE`
- [ ] Alunos do `escola.db` migrados uma única vez
- [ ] `main.py` avisa e fecha se não houver conexão
- [ ] Indicador 🟢/🔴 e botão 🔄 Recarregar funcionando
- [ ] Teste sem internet feito: mensagens amigáveis, nenhum traceback
- [ ] Aluno cadastrado no sistema aparece no SQL Editor (e vice-versa)
- [ ] Minha equipe concluiu a Missão da Equipe

## ➡️ Próximo Capítulo

No **Capítulo 10 — Integração**, você fará a revisão completa do sistema. Todas as peças estão construídas: login, menu, navegação, cadastro, CRUD e o banco em nuvem. Agora é hora de:

- Revisar o fluxo completo (Login → Menu → Cadastro → dados no Neon)
- Corrigir arestas (botão X, mensagens de erro, centralização)
- Testar o sistema como um todo — com e sem internet
- Preparar o projeto final para apresentação

O sistema está quase pronto. A reta final chegou! 🏁
