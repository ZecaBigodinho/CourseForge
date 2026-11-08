# 03 — Senhas no `.env` e configuração

> **Curso:** Automação com Python  
> **Módulo:** 04 — E-mail, agendamento e boas práticas  
> **Tempo estimado:** 1 h  

---

## 🎯 Objetivos

Ao final desta aula, você será capaz de:

- Explicar por que **senha no código** é um problema sério.
- Guardar a configuração num arquivo **`.env`** e ler com o **python-dotenv**.
- Criar o **`.env.example`** (o modelo sem segredos) e proteger o `.env` com o **`.gitignore`**.
- **Validar** a configuração no começo do script, com mensagens claras.
- Trocar do servidor de teste para o servidor real **sem mudar uma linha de código**.

## Pré-requisitos

- [Aula 02](02_servidor_de_teste.md): envio pelo servidor de teste.

---

## Por que não escrever a senha no código

```python
servidor.login("professor@gmail.com", "minha senha 123")   # ⛔ nunca
```

- O script vai ser **copiado**: para um colega, para o GitHub, para um pendrive, para o computador da escola. A senha vai junto.
- O código aparece na **tela** durante a aula, em prints, em vídeos.
- Para trocar a senha, é preciso mexer no código (e lembrar de todos os lugares).

A solução é separar **código** (que pode ser compartilhado) de **configuração secreta** (que fica só no seu computador). É a mesma ideia do `.env` do [curso de Python](../../python_para_desktop/modulo_05_git_github/03_vscode_e_github_desktop.md#passo-1-antes-de-tudo-o-gitignore).

## O arquivo `.env`

O `.env` é um arquivo de texto na pasta do projeto, com uma configuração por linha (`NOME=valor`). O projeto traz um **modelo**, o `.env.example`, que **pode** ser compartilhado porque não tem segredo nenhum:

```ini title=".env.example"
# Copie este arquivo para .env e preencha. O .env NUNCA vai para o Git nem para colegas.

# Servidor de teste (aula 02): nada sai do seu computador
SMTP_SERVIDOR=localhost
SMTP_PORTA=8025
SMTP_SEGURANCA=nenhuma
SMTP_USUARIO=
SMTP_SENHA=
EMAIL_REMETENTE=professor@example.com

# Gmail de verdade (só com autorização e depois de testar bastante):
# SMTP_SERVIDOR=smtp.gmail.com
# SMTP_PORTA=587
# SMTP_SEGURANCA=starttls
# SMTP_USUARIO=seu.email@gmail.com
# SMTP_SENHA=senha de app de 16 letras (não é a senha da conta)
# EMAIL_REMETENTE=seu.email@gmail.com
```

Para usar: **copie** o `.env.example` com o nome `.env` e preencha. Para o servidor de teste, nem precisa mudar nada.

```powershell
copy .env.example .env
```

!!! danger "O `.env` nunca vai para o Git, nem para colegas"
    Crie (ou complete) o arquivo **`.gitignore`** na pasta do curso com estas linhas:

    ```text
    .env
    .venv/
    treino*/
    ```

    Assim o Git ignora o `.env`, o ambiente virtual e as pastas de treino. Publicou um `.env` com senha sem querer? **Troque a senha (ou revogue a senha de app) na hora**: apagar o arquivo depois não resolve, porque o histórico guarda.

## Lendo a configuração

```python title="configuracao.py"
"""Lê a configuração de e-mail do arquivo .env (nunca do código)."""
import os
import smtplib
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass
class ConfigEmail:
    servidor: str
    porta: int
    seguranca: str  # "nenhuma" (servidor de teste), "starttls" ou "ssl"
    usuario: str
    senha: str
    remetente: str


def carregar_config() -> ConfigEmail:
    load_dotenv()  # lê o .env da pasta atual e coloca os valores nas variáveis de ambiente
    config = ConfigEmail(
        servidor=os.getenv("SMTP_SERVIDOR", "localhost"),
        porta=int(os.getenv("SMTP_PORTA", "8025")),
        seguranca=os.getenv("SMTP_SEGURANCA", "nenhuma").lower(),
        usuario=os.getenv("SMTP_USUARIO", ""),
        senha=os.getenv("SMTP_SENHA", ""),
        remetente=os.getenv("EMAIL_REMETENTE", "professor@example.com"),
    )
    if config.seguranca not in {"nenhuma", "starttls", "ssl"}:
        raise ValueError(f"SMTP_SEGURANCA inválido: {config.seguranca!r} (use nenhuma, starttls ou ssl)")
    if config.seguranca != "nenhuma" and not (config.usuario and config.senha):
        raise ValueError("Para um servidor de verdade, preencha SMTP_USUARIO e SMTP_SENHA no .env")
    return config


def conectar(config: ConfigEmail) -> smtplib.SMTP:
    """Abre a conexão com o servidor de e-mail, com a segurança e o login configurados."""
    if config.seguranca == "ssl":
        servidor = smtplib.SMTP_SSL(config.servidor, config.porta, timeout=30)
    else:
        servidor = smtplib.SMTP(config.servidor, config.porta, timeout=30)
        if config.seguranca == "starttls":
            servidor.starttls()
    if config.usuario:
        servidor.login(config.usuario, config.senha)
    return servidor


if __name__ == "__main__":
    config = carregar_config()
    senha = "(vazia)" if not config.senha else "*" * 8
    print(f"Servidor: {config.servidor}:{config.porta} ({config.seguranca})")
    print(f"Usuário: {config.usuario or '(nenhum)'} | Senha: {senha} | Remetente: {config.remetente}")
```

```text
> python configuracao.py
Servidor: localhost:8025 (nenhuma)
Usuário: (nenhum) | Senha: (vazia) | Remetente: professor@example.com
```

### O que o código faz

- **`load_dotenv()`** lê o `.env` e coloca cada linha como **variável de ambiente**. **`os.getenv("NOME", "padrão")`** lê a variável, com um valor padrão se ela não existir. Sem `.env` nenhum, o script cai nos padrões do **servidor de teste**: o jeito mais seguro de "dar errado".
- **`@dataclass`** cria uma classe só para **guardar dados** (`config.servidor`, `config.porta`...), sem precisar escrever o `__init__`. É mais claro do que um dicionário com chaves digitadas à mão.
- **Validação no começo:** um valor estranho em `SMTP_SEGURANCA` ou um servidor real sem usuário e senha param o script **antes** de tentar enviar, com uma mensagem que diz o que corrigir:

    ```text
    ValueError: Para um servidor de verdade, preencha SMTP_USUARIO e SMTP_SENHA no .env
    ```

- **`conectar()`** abre a conexão do jeito certo para cada caso: sem criptografia (teste), **STARTTLS** (porta 587) ou **SSL** (porta 465), e faz o login se houver usuário.
- **A senha nunca é mostrada:** a conferência imprime `********`.

!!! tip "Trocar de servidor = trocar o `.env`"
    O script do projeto usa `carregar_config()` e `conectar()`. Para passar do servidor de teste para o Gmail, você muda **só o `.env`**: o código é o mesmo que foi testado. É por isso que vale a pena testar tudo no servidor local primeiro.

---

## ⚠️ Erros comuns

- **`ModuleNotFoundError: No module named 'dotenv'`**: o pacote se instala como `python-dotenv` e se importa como `dotenv`.
- **O `.env` "não funciona"**: ele precisa estar na **pasta onde o terminal está** quando o script roda (ou passe o caminho: `load_dotenv("C:/Automacao/.env")`).
- **Arquivo salvo como `.env.txt`**: no Explorador do Windows, a extensão escondida engana. Crie o arquivo pelo VS Code.
- **Aspas e espaços**: `SMTP_SENHA = "abc"` funciona, mas é mais seguro escrever `SMTP_SENHA=abc`, sem espaços em volta do `=`.
- **`.env` no Git**: confira o `.gitignore` **antes** do primeiro commit.

---

## Exercícios

### Básico (fixação)

Copie o `.env.example` para `.env`, mude o `EMAIL_REMETENTE` para `secretaria@example.com` e rode o `configuracao.py`. O que mudou na saída?

<!-- gabarito -->
??? success "Gabarito — Básico"
    No `.env`, a linha fica:

    ```ini
    EMAIL_REMETENTE=secretaria@example.com
    ```

    A última linha da saída passa a mostrar `Remetente: secretaria@example.com`. Nenhuma linha de código mudou: só a configuração.

    Para conferir pelo próprio Python:

    ```python
    from configuracao import carregar_config

    print(carregar_config().remetente)
    ```

### Intermediário (aplicação)

Com `SMTP_PORTA=oito mil` no `.env`, o `carregar_config()` quebra com um erro difícil de entender (`ValueError: invalid literal for int()...`). Escreva a função `ler_porta()` que devolve a porta como número ou levanta um `ValueError` com a mensagem **"SMTP_PORTA precisa ser um número, por exemplo 8025"**.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```python
    import os


    def ler_porta() -> int:
        texto = os.getenv("SMTP_PORTA", "8025").strip()
        if not texto.isdigit():
            raise ValueError(f"SMTP_PORTA precisa ser um número, por exemplo 8025 (está: {texto!r})")
        return int(texto)


    os.environ["SMTP_PORTA"] = "oito mil"
    try:
        ler_porta()
    except ValueError as erro:
        mensagem = str(erro)
        print(mensagem)
    ```

    `isdigit()` confere se o texto só tem dígitos. A mensagem diz **o que** está errado, **onde** e **como** consertar, e mostra o valor encontrado. No `configuracao.py`, troque o `int(os.getenv(...))` por `ler_porta()`.

### Avançado (desafio)

Escreva um script `conferir_env.py` que compara o `.env` com o `.env.example` e avisa quais **variáveis do modelo estão faltando** no `.env` (sem nunca mostrar os valores do `.env`).

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```python
    from pathlib import Path

    from dotenv import dotenv_values

    modelo = dotenv_values(".env.example")
    atual = dotenv_values(".env") if Path(".env").exists() else {}

    faltando = sorted(set(modelo) - set(atual))
    if faltando:
        print("Faltam no .env:", ", ".join(faltando))
    else:
        print("O .env tem todas as variáveis do modelo.")
    ```

    `dotenv_values()` lê o arquivo para um **dicionário**, sem mexer nas variáveis de ambiente. A diferença de conjuntos (`set(modelo) - set(atual)`) dá os nomes que estão no modelo e não no `.env`. O script só mostra **nomes**, nunca valores: seguro para rodar com a tela projetada.

---

## 💡 Resumo

- **Código** pode ser compartilhado; **segredos** ficam no **`.env`**, que nunca vai para o Git (`.gitignore`).
- O **`.env.example`** é o modelo sem segredos; copie para `.env` e preencha.
- `load_dotenv()` + `os.getenv("NOME", "padrão")`; padrões apontando para o **servidor de teste**.
- **Valide** a configuração no começo, com mensagens que dizem como consertar. Nunca mostre a senha.

## ➡️ Próximo passo

**[04 — Logs, erros e agendamento](04_logs_e_agendamento.md)**: o script que roda sozinho toda segunda-feira e conta o que fez.
