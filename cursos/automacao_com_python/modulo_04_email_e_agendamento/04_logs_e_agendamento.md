# 04 — Logs, erros e agendamento

> **Curso:** Automação com Python  
> **Módulo:** 04 — E-mail, agendamento e boas práticas  
> **Tempo estimado:** 1 h 30 min  

---

## 🎯 Objetivos

Ao final desta aula, você será capaz de:

- Registrar o que o script fez num **arquivo de log**, com data, hora e nível (INFO, WARNING, ERROR).
- Tratar erros de um jeito que **não esconde** o problema: log com a explicação e **código de saída** diferente de zero.
- Criar um **`.bat`** que roda o script com o Python do ambiente virtual.
- **Agendar** o script no **Agendador de Tarefas do Windows** (pela tela ou com o comando `schtasks`).

## Pré-requisitos

- [Aula 03](03_env_e_configuracao.md): configuração no `.env`.

---

## Por que log?

Quando o script roda **sozinho** (às 8h de segunda-feira, com ninguém olhando), o `print()` não serve: não há tela. O **log** é o diário do script: o que fez, quando, o que deu errado. Na segunda à tarde, você abre o arquivo e sabe se os lembretes saíram.

```python title="tarefa_com_log.py"
import logging
import sys
from pathlib import Path

logging.basicConfig(
    filename="tarefa.log",
    encoding="utf-8",
    level=logging.INFO,
    format="%(asctime)s %(levelname)-7s %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S",
)
log = logging.getLogger("tarefa")


def main() -> int:
    log.info("Começou")
    pasta = Path("treino_emails")
    try:
        itens = list(pasta.iterdir())
    except FileNotFoundError:
        log.exception("A pasta %s não existe", pasta)
        return 1
    log.info("A pasta tem %d itens", len(itens))
    if not (pasta / "pendencias.xlsx").exists():
        log.warning("Não achei a planilha de pendências")
    log.info("Terminou")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

O `tarefa.log` depois de duas execuções (na segunda, a pasta `treino_emails` não existia):

```text
08/11/2026 17:49:02 INFO    Começou
08/11/2026 17:49:02 INFO    A pasta tem 3 itens
08/11/2026 17:49:02 INFO    Terminou
08/11/2026 17:49:03 INFO    Começou
08/11/2026 17:49:03 ERROR   A pasta treino_emails não existe
Traceback (most recent call last):
  ...
FileNotFoundError: [WinError 3] O sistema não pode encontrar o caminho especificado: 'treino_emails'
```

| Nível | Quando usar | Exemplo |
|---|---|---|
| `log.debug()` | Detalhes para investigar problemas (normalmente desligado) | "linha 7 lida: ..." |
| `log.info()` | O que aconteceu normalmente | "3 e-mails enviados" |
| `log.warning()` | Algo estranho, mas o script continuou | "aluno sem e-mail" |
| `log.error()` | Algo falhou | "não consegui conectar" |
| `log.exception()` | Como `error`, mas grava também o **traceback** (use dentro do `except`) | |

!!! tip "Use `%s` no log, não f-string"
    `log.info("A pasta tem %d itens", len(itens))` só monta o texto se a mensagem for mesmo gravada (economiza quando o nível está desligado). Funciona igual a f-string para quem lê.

### Código de saída

`sys.exit(main())` termina o programa com o número que o `main()` devolveu: **0** quer dizer "deu certo"; qualquer outro número, "deu errado". O Agendador de Tarefas mostra esse número na coluna **Resultado da Última Execução**: `0x0` é sucesso, `0x1` é o erro do script. É um jeito de ver de longe se algo falhou, sem abrir o log.

## O `.bat`: um atalho para o agendador

O Agendador de Tarefas não sabe ativar ambientes virtuais. A solução é um arquivo `.bat` na pasta do projeto que chama **direto** o Python do `.venv`:

```bat title="rodar_lembrete.bat"
@echo off
rem Roda o lembrete semanal com o Python do ambiente virtual desta pasta
cd /d "%~dp0"
set PYTHONUTF8=1
".venv\Scripts\python.exe" lembrete_semanal.py --enviar
```

- **`cd /d "%~dp0"`** entra na pasta onde o `.bat` está (`%~dp0`), seja qual for a pasta de onde ele foi chamado. Sem isso, o script procuraria o `.env` e as planilhas no lugar errado.
- **`".venv\Scripts\python.exe"`** é o Python do ambiente virtual, com as bibliotecas instaladas.
- **`set PYTHONUTF8=1`** faz os acentos saírem certos se você rodar o `.bat` num terminal.

Teste com **duplo clique** no `.bat` (ou rodando no terminal) **antes** de agendar. Ele foi testado assim neste curso: chamado de outra pasta, rodou com o Python do ambiente virtual e gravou no log.

## Agendando no Windows

### Pela tela

1. Menu Iniciar ➔ **Agendador de Tarefas**.
2. **Criar Tarefa Básica...** ➔ nome: `Lembrete semanal` ➔ **Avançar**.
3. **Disparador:** *Semanalmente* ➔ segunda-feira, 08:00.
4. **Ação:** *Iniciar um programa* ➔ **Programa/script:** escolha o `rodar_lembrete.bat` ➔ **Iniciar em:** a pasta do projeto (por exemplo, `C:\Automacao`).
5. Concluir. Depois, nas **propriedades** da tarefa, aba **Configurações**, marque **"Executar a tarefa o mais cedo possível após uma inicialização agendada ter sido perdida"**: se o computador estiver desligado na segunda às 8h, ele roda quando for ligado.

### Pelo terminal (`schtasks`)

O mesmo, num comando só (num terminal normal, sem precisar ser administrador):

```powershell
schtasks /Create /TN "Lembrete semanal" /TR "C:\Automacao\rodar_lembrete.bat" /SC WEEKLY /D MON /ST 08:00
```

| Comando | Faz |
|---|---|
| `schtasks /Query /TN "Lembrete semanal"` | Mostra a tarefa e a próxima execução |
| `schtasks /Run /TN "Lembrete semanal"` | Roda **agora** (bom para testar) |
| `schtasks /Change /TN "Lembrete semanal" /DISABLE` | Pausa (e `/ENABLE` volta) |
| `schtasks /Delete /TN "Lembrete semanal" /F` | Apaga a tarefa |

!!! warning "Agendar = automação sem ninguém olhando"
    Só agende o que já rodou várias vezes **manualmente**, com o resultado conferido. E combine com quem vai receber: um lembrete semanal que ninguém pediu vira *spam*. Por padrão, a tarefa só roda quando o seu usuário está conectado no computador; para rodar com o computador bloqueado ou sem ninguém conectado, há opções nas propriedades da tarefa (que pedem a senha do Windows).

!!! note "Para o professor"
    Os comandos `schtasks` e o passo a passo da tela foram escritos conforme a documentação do Windows, mas **não foram executados** na preparação desta aula, para não criar tarefas no computador usado. Vale fazer uma demonstração na sala com um script inofensivo (por exemplo, o `tarefa_com_log.py`).

---

## ⚠️ Erros comuns

- **Tarefa roda, mas "não faz nada"**: faltou o `cd /d "%~dp0"` (ou o *Iniciar em*), e o script procurou os arquivos na pasta `C:\Windows\System32`.
- **`ModuleNotFoundError` só quando agendado**: o `.bat` chamou o `python` "solto", e não o do `.venv`.
- **Resultado `0x1` no agendador**: o script terminou com erro; abra o log.
- **Log crescendo para sempre**: para scripts que rodam muito, use `logging.handlers.RotatingFileHandler` (veja o exercício intermediário).
- **`except Exception: pass`**: esconde o erro. No mínimo, `log.exception(...)`.

---

## Exercícios

### Básico (fixação)

Acrescente ao `tarefa_com_log.py` um `log.warning` quando a pasta tiver **mais de 2 itens** ("pasta cheia"). Rode e confira no `tarefa.log`.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```python
    import logging
    import sys
    from pathlib import Path

    logging.basicConfig(filename="tarefa.log", encoding="utf-8", level=logging.INFO,
                        format="%(asctime)s %(levelname)-7s %(message)s", datefmt="%d/%m/%Y %H:%M:%S")
    log = logging.getLogger("tarefa")


    def main() -> int:
        itens = list(Path("treino_emails").iterdir())
        log.info("A pasta tem %d itens", len(itens))
        if len(itens) > 2:
            log.warning("Pasta cheia: %d itens", len(itens))
        return 0


    if __name__ == "__main__":
        sys.exit(main())
    ```

    Depois das aulas 01 a 03, a pasta de treino tem 3 itens (a planilha, o anexo e a pasta `saida`), então aparece a linha `WARNING Pasta cheia: 3 itens`. Numa pasta de treino recém-criada, são só 2, e o aviso não aparece.

### Intermediário (aplicação)

Troque o arquivo de log simples por um **log com rotação**: no máximo **100 KB** por arquivo e **3** arquivos antigos guardados (`tarefa.log.1`, `.2`, `.3`).

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```python
    import logging
    from logging.handlers import RotatingFileHandler

    rotacao = RotatingFileHandler("tarefa.log", maxBytes=100_000, backupCount=3, encoding="utf-8")
    rotacao.setFormatter(logging.Formatter("%(asctime)s %(levelname)-7s %(message)s", datefmt="%d/%m/%Y %H:%M:%S"))

    log = logging.getLogger("tarefa_rotacao")
    log.setLevel(logging.INFO)
    log.addHandler(rotacao)

    for i in range(3):
        log.info("Execução de teste %d", i + 1)
    ```

    Quando o `tarefa.log` passa de 100 KB, ele vira `tarefa.log.1` e um novo começa; o mais antigo (`.3`) é descartado. Assim o log nunca ocupa mais que uns 400 KB.

### Avançado (desafio)

Escreva o `resumo_do_log.py`, que lê o `treino_emails/logs/lembrete.log` do projeto ([aula 05](05_projeto_lembrete.md)) e mostra quantas linhas de cada nível (INFO, WARNING, ERROR) aparecem **hoje**.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```python
    from collections import Counter
    from datetime import date
    from pathlib import Path

    hoje = f"{date.today():%d/%m/%Y}"
    niveis = Counter()
    caminho = Path("treino_emails") / "logs" / "lembrete.log"
    for linha in caminho.read_text(encoding="utf-8").splitlines():
        partes = linha.split()
        if len(partes) >= 3 and partes[0] == hoje:
            niveis[partes[2]] += 1

    for nivel in ("INFO", "WARNING", "ERROR"):
        print(f"{nivel:8} {niveis[nivel]}")
    ```

    Cada linha começa com `data hora NÍVEL`, então `split()` separa e `partes[2]` é o nível. Linhas de traceback (que não começam com a data) são ignoradas. Um "resumo do log" assim pode até ir num e-mail para você no fim do dia.

---

## 💡 Resumo

- **Log** = diário do script: `logging` com data, hora e nível; `log.exception()` dentro do `except`.
- `sys.exit(main())`: **0** é sucesso; outro número é erro, visível no Agendador.
- **`.bat`** com `cd /d "%~dp0"` e o Python do `.venv`; teste com duplo clique antes de agendar.
- **Agendador de Tarefas** (tela ou `schtasks /Create ... /SC WEEKLY /D MON /ST 08:00`), com "executar o mais cedo possível" se o PC estava desligado.

## ➡️ Próximo passo

**[05 — Projeto do módulo: lembrete semanal](05_projeto_lembrete.md)**.
