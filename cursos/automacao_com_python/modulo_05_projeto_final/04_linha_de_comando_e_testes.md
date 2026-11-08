# 04 — Linha de comando e testes

> **Curso:** Automação com Python  
> **Módulo:** 05 — Projeto final  
> **Tempo estimado:** 2 h  

---

## 🎯 Objetivos

Ao final desta aula, você terá:

- O `cli.py`, com **comandos**, **argumentos** e **opções** feitos com o `argparse` (e uma ajuda automática com `--help`).
- A Secretaria rodando de ponta a ponta: `python -m secretaria tudo ...`.
- **Testes automáticos** com o **pytest**, que conferem as regras e o resultado final em segundos.

## Pré-requisitos

- [Aula 03](03_documentos_e_emails.md): `documentos.py` e `emails.py`.

---

## A linha de comando: `cli.py`

```python title="secretaria/cli.py"
"""Secretaria automática: a linha de comando que junta tudo.

    python -m secretaria boletim     treino_secretaria/turma_1A.xlsx
    python -m secretaria certificados treino_secretaria/turma_1A.xlsx
    python -m secretaria emails      treino_secretaria/turma_1A.xlsx [--enviar]
    python -m secretaria tudo        treino_secretaria/turma_1A.xlsx [--enviar]
"""
import argparse
import csv
import logging
import sys
from datetime import date
from pathlib import Path

from . import documentos, emails
from .dados import ler_turma

log = logging.getLogger("secretaria")


def configurar_log(pasta: Path) -> None:
    if log.handlers:
        return
    formato = logging.Formatter("%(asctime)s %(levelname)-7s %(message)s", datefmt="%d/%m/%Y %H:%M:%S")
    for destino in (logging.FileHandler(pasta / "secretaria.log", encoding="utf-8"),
                    logging.StreamHandler(sys.stdout)):
        destino.setFormatter(formato)
        log.addHandler(destino)
    log.setLevel(logging.INFO)


def criar_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="secretaria", description="Secretaria automática da turma.")
    parser.add_argument("comando", choices=["boletim", "certificados", "emails", "tudo"],
                        help="o que fazer")
    parser.add_argument("planilha", type=Path, help="planilha da turma (.xlsx)")
    parser.add_argument("--saida", type=Path, default=Path("saida"),
                        help="pasta de saída (padrão: saida); dentro dela, uma pasta com a data de hoje")
    parser.add_argument("--enviar", action="store_true",
                        help="envia os e-mails de verdade (sem isto, só salva rascunhos .eml)")
    return parser


def main(argumentos: list[str] | None = None) -> int:
    args = criar_parser().parse_args(argumentos)
    if not args.planilha.exists():
        print(f"Planilha não encontrada: {args.planilha}")
        return 2
    pasta = args.saida / f"{date.today():%Y-%m-%d}"
    pasta.mkdir(parents=True, exist_ok=True)
    configurar_log(pasta)
    log.info("Início: %s %s%s", args.comando, args.planilha.name, " (ENVIO)" if args.enviar else "")

    try:
        info, alunos = ler_turma(args.planilha)
    except Exception as erro:
        log.error("Não consegui ler a planilha: %s", erro)
        return 1
    for aluno in alunos:
        for problema in aluno.problemas:
            log.warning("%s: %s", aluno.nome, problema)

    falhas = 0
    certificados = {}
    if args.comando in ("boletim", "tudo"):
        log.info("Boletim: %s", documentos.gerar_boletim(info, alunos, pasta).name)
    if args.comando in ("certificados", "emails", "tudo"):
        emitidos = documentos.gerar_certificados(info, alunos, pasta)
        certificados = {aluno.matricula: arquivo for aluno, arquivo, _ in emitidos}
        with open(pasta / "certificados.csv", "w", newline="", encoding="utf-8-sig") as arq:
            escritor = csv.writer(arq, delimiter=";")
            escritor.writerow(["Matrícula", "Nome", "Média", "Código", "Arquivo"])
            for aluno, arquivo, codigo in emitidos:
                escritor.writerow([aluno.matricula, aluno.nome, aluno.media, codigo, arquivo.name])
        log.info("Certificados: %d emitidos", len(emitidos))
    if args.comando in ("emails", "tudo"):
        config = emails.configuracao_smtp()
        mensagens = [(a, emails.montar(a, info, config["remetente"], certificados.get(a.matricula)))
                     for a in alunos if a.email_valido]
        falhas = emails.processar(mensagens, pasta, args.enviar, config)
        log.info("E-mails: %d %s, %d falha(s)", len(mensagens) - falhas,
                 "enviados" if args.enviar else "em rascunho", falhas)

    log.info("Fim. Arquivos em: %s", pasta)
    return 1 if falhas else 0
```

### O `argparse`

| Linha | Cria |
|---|---|
| `add_argument("comando", choices=[...])` | Um argumento **obrigatório**, que só aceita os valores da lista |
| `add_argument("planilha", type=Path)` | Outro obrigatório, já convertido em `Path` |
| `add_argument("--saida", type=Path, default=Path("saida"))` | Uma **opção** com valor padrão |
| `add_argument("--enviar", action="store_true")` | Uma **chave liga/desliga**: `True` só se for digitada |

E de graça vem a **ajuda**:

```text
> python -m secretaria --help
usage: secretaria [-h] [--saida SAIDA] [--enviar]
                  {boletim,certificados,emails,tudo} planilha

Secretaria automática da turma.

positional arguments:
  {boletim,certificados,emails,tudo}
                        o que fazer
  planilha              planilha da turma (.xlsx)

options:
  -h, --help            show this help message and exit
  --saida SAIDA         pasta de saída (padrão: saida); dentro dela, uma pasta
                        com a data de hoje
  --enviar              envia os e-mails de verdade (sem isto, só salva
                        rascunhos .eml)
```

Um comando errado (`python -m secretaria boletins ...`) é recusado com uma mensagem que mostra as opções válidas, sem nem chegar no seu código.

!!! tip "`main(argumentos=None)`"
    O `parse_args(argumentos)` lê o que foi digitado no terminal quando `argumentos` é `None`. Mas dá para chamar `main(["boletim", "planilha.xlsx"])` de dentro do Python: é assim que os **testes** usam a linha de comando, sem abrir terminal nenhum.

## Rodando tudo

```text
> python -m secretaria tudo treino_secretaria/turma_1A.xlsx
08/11/2026 18:16:50 INFO    Início: tudo turma_1A.xlsx
08/11/2026 18:16:50 WARNING Diego Rocha: e-mail inválido: vazio
08/11/2026 18:16:50 WARNING Felipe Torres: 4º bim: nota não lançada
08/11/2026 18:16:50 WARNING Heitor Alves: e-mail inválido: heitor.alves@example
08/11/2026 18:16:50 INFO    Boletim: boletim_1A.xlsx
08/11/2026 18:16:50 INFO    Certificados: 4 emitidos
08/11/2026 18:16:50 INFO    Rascunho: ana.souza@example.com
...
08/11/2026 18:16:50 INFO    E-mails: 6 em rascunho, 0 falha(s)
08/11/2026 18:16:50 INFO    Fim. Arquivos em: saida\2026-11-08
```

Na pasta `saida\2026-11-08`: `boletim_1A.xlsx`, quatro `certificado_*.pdf`, o `certificados.csv` com os códigos, a pasta `rascunhos` com 6 e-mails e o `secretaria.log`.

Para enviar pelo **servidor de teste** ([Módulo 04](../modulo_04_email_e_agendamento/02_servidor_de_teste.md#ligando-o-servidor-de-teste)), com ele ligado no outro terminal:

```powershell
python -m secretaria emails treino_secretaria/turma_1A.xlsx --enviar
```

## Testes com pytest

Até aqui, você conferiu os resultados **olhando**. Num projeto deste tamanho, cada mudança pode quebrar algo em outro lugar. **Testes automáticos** conferem tudo de novo, sozinhos, em segundos. O **pytest** é a ferramenta mais usada para isso:

```powershell
python -m pip install pytest==8.4.2
```

```python title="testes/test_secretaria.py"
"""Testes da Secretaria automática. Rode com: python -m pytest testes"""
import csv
from pathlib import Path

import pytest
from openpyxl import load_workbook

import criar_treino_secretaria
from secretaria.cli import main
from secretaria.dados import arredondar, calcular_situacao, converter_nota, ler_turma


@pytest.mark.parametrize("valor, esperado", [
    (8.5, (8.5, "")),
    ("7,5", (7.5, "")),
    (None, (None, "nota não lançada")),
    (11, (None, "fora de 0 a 10: 11")),
])
def test_converter_nota(valor, esperado):
    assert converter_nota(valor) == esperado


def test_arredondar_como_a_escola():
    assert arredondar(4.25) == 4.3
    assert arredondar(8.125) == 8.1


@pytest.mark.parametrize("media, frequencia, situacao", [
    (8.0, 0.95, "Aprovado"),
    (6.0, 0.75, "Aprovado"),       # exatamente no limite
    (5.5, 0.90, "Recuperação"),
    (9.0, 0.70, "Reprovado"),      # nota boa, mas faltou demais
    (None, 1.00, "Pendente"),
])
def test_situacao(media, frequencia, situacao):
    assert calcular_situacao(media, frequencia) == situacao


@pytest.fixture
def planilha(tmp_path, monkeypatch):
    """Cria a planilha de treino numa pasta temporária e trabalha dentro dela."""
    monkeypatch.chdir(tmp_path)
    criar_treino_secretaria.main()
    return tmp_path / "treino_secretaria" / "turma_1A.xlsx"


def test_ler_turma(planilha):
    info, alunos = ler_turma(planilha)
    assert info["Turma"] == "1A" and len(alunos) == 8
    elisa = next(a for a in alunos if a.nome == "Elisa Prado")
    assert elisa.media == 7.3 and elisa.situacao == "Aprovado"
    diego = next(a for a in alunos if a.nome == "Diego Rocha")
    assert not diego.email_valido


def test_tudo_em_simulacao(planilha, tmp_path):
    assert main(["tudo", str(planilha), "--saida", str(tmp_path / "saida")]) == 0
    pasta = next((tmp_path / "saida").iterdir())
    boletim = load_workbook(pasta / "boletim_1A.xlsx")
    assert boletim.sheetnames == ["Boletim", "Resumo", "Problemas"]
    with open(pasta / "certificados.csv", encoding="utf-8-sig") as arq:
        emitidos = list(csv.DictReader(arq, delimiter=";"))
    assert [e["Nome"] for e in emitidos] == ["Ana Souza", "Carla Mendes", "Elisa Prado", "Heitor Alves"]
    assert len(list((pasta / "rascunhos").iterdir())) == 6   # sem os 2 e-mails inválidos


def test_planilha_que_nao_existe(tmp_path):
    assert main(["boletim", str(tmp_path / "nao_existe.xlsx")]) == 2
```

```text
> python -m pytest testes -q
.............                                                            [100%]
13 passed in 2.44s
```

### Como o pytest funciona

- Ele procura arquivos `test_*.py` e roda cada função que começa com **`test_`**.
- Dentro do teste, **`assert condição`**: se for falsa, o teste **falha** e o pytest mostra os valores que não bateram.
- **`@pytest.mark.parametrize`** roda o mesmo teste com vários valores: os 4 casos de `converter_nota` e os 5 de `calcular_situacao` viram 9 testes.
- Uma **fixture** (`@pytest.fixture`) prepara o que o teste precisa. Os parâmetros `tmp_path` (uma pasta temporária nova para cada teste) e `monkeypatch` (para mudar a pasta de trabalho só durante o teste) vêm prontos do pytest. A fixture `planilha` usa os dois para criar a planilha de treino num lugar descartável.

!!! info "Rode com `python -m pytest`"
    Com `python -m`, a pasta atual entra na lista de lugares onde o Python procura módulos, e o teste encontra o pacote `secretaria` e o `criar_treino_secretaria.py`. Rodando só `pytest`, pode aparecer `ModuleNotFoundError: No module named 'secretaria'`.

!!! tip "Quando rodar os testes"
    **Sempre que mudar alguma coisa** no projeto, e antes de usar a Secretaria com a planilha de verdade. Um teste que passa não prova que está tudo certo, mas um teste que falha avisa **antes** de o erro chegar no boletim de um aluno. Os gabaritos deste curso são conferidos assim, a cada mudança no site.

---

## ⚠️ Erros comuns

- **`error: argument comando: invalid choice`**: o comando foi digitado errado (o `argparse` mostra os válidos).
- **`error: the following arguments are required: planilha`**: faltou o caminho da planilha.
- **`--enviar` sem o servidor de teste ligado**: o log registra "Não consegui conectar" e o código de saída é 1.
- **`ModuleNotFoundError` nos testes**: rode `python -m pytest` a partir da pasta do projeto.
- **Teste que depende de arquivos de outro teste**: cada teste deve criar o que precisa (as fixtures existem para isso).

---

## Exercícios

### Básico (fixação)

Acrescente ao `argparse` a opção **`--silencioso`** (liga/desliga). Teste o `criar_parser()` com e sem ela.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```python
    from secretaria.cli import criar_parser

    parser = criar_parser()
    parser.add_argument("--silencioso", action="store_true", help="não mostra o log na tela")

    com = parser.parse_args(["boletim", "turma.xlsx", "--silencioso"])
    sem = parser.parse_args(["boletim", "turma.xlsx"])
    print(com.silencioso, sem.silencioso)
    ```

    Saída: `True False`. No `cli.py`, a linha entra dentro de `criar_parser()`; depois, o `configurar_log()` pode deixar de acrescentar o `StreamHandler` (a tela) quando `args.silencioso` for `True`. O arquivo de log continua sendo gravado.

### Intermediário (aplicação)

Escreva um **teste** novo para o arquivo de testes: a turma de treino deve ter **exatamente** 4 aprovados, e o **Heitor** deve estar entre eles mesmo com o e-mail inválido.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```python
    from pathlib import Path

    import criar_treino_secretaria
    from secretaria.dados import ler_turma


    def test_aprovados(tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        criar_treino_secretaria.main()
        info, alunos = ler_turma(Path("treino_secretaria") / "turma_1A.xlsx")
        aprovados = [a.nome for a in alunos if a.situacao == "Aprovado"]
        assert len(aprovados) == 4
        assert "Heitor Alves" in aprovados   # e-mail errado não muda a situação
    ```

    O teste documenta uma regra importante: **problema de e-mail não reprova ninguém**. Se um dia alguém misturar as duas coisas no código, o teste avisa.

### Avançado (desafio)

Escreva um teste que **envia** os e-mails para um servidor de teste criado **dentro** do próprio teste (com o `Controller` do `aiosmtpd`) e confere que chegaram **6** e-mails, e que o da Ana tem um **PDF** anexado.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```python
    import email
    from email import policy

    from aiosmtpd.controller import Controller

    import criar_treino_secretaria
    from secretaria import emails
    from secretaria.cli import main


    class Caixa:
        def __init__(self):
            self.mensagens = []

        async def handle_DATA(self, server, session, envelope):
            self.mensagens.append(email.message_from_bytes(envelope.content, policy=policy.default))
            return "250 OK"


    def test_envio(tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        monkeypatch.setenv("SMTP_PORTA", "8026")
        monkeypatch.setattr(emails, "PAUSA_ENTRE_ENVIOS", 0)
        criar_treino_secretaria.main()
        caixa = Caixa()
        servidor = Controller(caixa, hostname="localhost", port=8026)
        servidor.start()
        try:
            assert main(["emails", "treino_secretaria/turma_1A.xlsx", "--enviar"]) == 0
        finally:
            servidor.stop()
        assert len(caixa.mensagens) == 6
        da_ana = next(m for m in caixa.mensagens if "ana.souza" in m["To"])
        assert [a.get_content_type() for a in da_ana.iter_attachments()] == ["application/pdf"]
    ```

    O `Controller` liga um servidor SMTP de verdade, numa porta própria, só durante o teste; o `finally` garante que ele é desligado mesmo se o teste falhar. `monkeypatch.setenv` e `monkeypatch.setattr` mudam a porta e a pausa **só** durante o teste.

---

## 💡 Resumo

- **`argparse`**: argumentos obrigatórios, `choices`, opções com padrão, `store_true` e `--help` automático.
- **`python -m secretaria tudo planilha.xlsx`** gera tudo numa pasta com a data; `--enviar` só quando for a hora.
- **pytest**: funções `test_*`, `assert`, `parametrize` e fixtures (`tmp_path`, `monkeypatch`). Rode `python -m pytest` a cada mudança.

## ➡️ Próximo passo

**[05 — Demonstração, entrega e certificado](05_entrega_e_certificado.md)**.
