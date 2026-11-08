# 01 — Instalando o openpyxl e lendo planilhas

> **Curso:** Automação com Python  
> **Módulo:** 02 — Planilhas  
> **Tempo estimado:** 1 h 30 min  

---

## 🎯 Objetivos

Ao final desta aula, você será capaz de:

- Criar um **ambiente virtual** e instalar o **openpyxl**.
- Criar as **planilhas de treino** do módulo.
- Abrir um arquivo `.xlsx`, escolher a **aba** e ler **células**.
- Percorrer as linhas com `iter_rows()` e transformar a tabela numa **lista de dicionários**.

## Pré-requisitos

- [Módulo 01](../modulo_01_arquivos_e_pastas/index.md): `pathlib`, regras de segurança e pasta de treino.

!!! info "Não precisa ter o Excel instalado"
    O `openpyxl` lê e escreve arquivos `.xlsx` sozinho. Para **ver** o resultado, use o Excel, o LibreOffice Calc (gratuito) ou abra no Google Planilhas.

---

## O ambiente virtual e o openpyxl

O `openpyxl` não vem com o Python: é uma **biblioteca** que se instala com o `pip`. Para não misturar bibliotecas de projetos diferentes, ela vai num **ambiente virtual** (a pasta `.venv`), dentro da pasta do curso.

No terminal do VS Code, dentro de `C:\Automacao`:

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install openpyxl==3.1.5
```

- O segundo comando **ativa** o ambiente: o terminal passa a mostrar `(.venv)` no começo da linha.
- No VS Code, escolha o Python do ambiente: `Ctrl+Shift+P` ➔ **Python: Select Interpreter** ➔ o que tem `.venv`. Assim o botão ▶ também usa o ambiente.
- O `==3.1.5` fixa a versão testada neste curso.

!!! warning "\"A execução de scripts foi desabilitada neste sistema\""
    Se o `activate` der esse erro no PowerShell, rode uma vez `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` e confirme com `S`. Isso libera scripts locais só para o seu usuário. O [curso de Python](../../python_para_desktop/modulo_06_vscode_config/index.md) explica ambientes virtuais com mais detalhes.

!!! tip "Toda vez que abrir um terminal novo"
    Ative o ambiente de novo (`.venv\Scripts\activate`). Se esquecer, o Python reclama: `ModuleNotFoundError: No module named 'openpyxl'`.

## As planilhas de treino

Como no Módulo 01, vamos praticar em arquivos **de mentira**. Este script cria a pasta `treino_planilhas` com a planilha de notas da turma **1A** (12 alunos inventados, 4 bimestres e faltas) e, na subpasta `turmas`, planilhas menores das turmas 1A, 1B e 1C.

```python title="criar_planilhas_treino.py"
"""Cria as planilhas de treino do Módulo 02 (dados inventados)."""
from pathlib import Path

from openpyxl import Workbook

TREINO = Path("treino_planilhas")

CABECALHO = ["Matrícula", "Nome", "1º bim", "2º bim", "3º bim", "4º bim", "Faltas"]

# A turma do projeto. Alguns valores têm problemas de propósito (aula 04 e projeto).
TURMA_1A = [
    [2026001, "Ana Souza", 8.5, 7.0, 9.0, 8.0, 4],
    [2026002, "Bruno Lima", 5.0, 6.5, 4.5, 6.0, 10],
    [2026003, "Carla Mendes", 9.5, 9.0, 10.0, 9.5, 0],
    [2026004, "Diego Rocha", 4.0, 3.5, 5.0, 4.5, 12],
    [2026005, "Elisa Prado", 7.0, "7,5", 6.5, 8.0, 2],      # nota digitada como texto
    [2026006, "Felipe Torres", 6.0, 5.5, 6.0, None, 6],     # nota ainda não lançada
    [2026007, "Gabriela Nunes", 3.0, 4.0, 2.5, 3.5, 25],
    [2026008, "Heitor Alves", 8.0, 8.5, 7.5, 9.0, 1],
    [2026009, "Isabela Costa", 6.5, 6.0, 5.5, 6.5, 8],
    [2026010, "João Pedro Melo", 10.0, 9.5, 9.0, 11.0, 3],  # nota fora de 0 a 10
    [2026011, "Larissa Freitas", 5.5, 5.0, 6.0, 5.5, 22],
    [2026012, "Mateus Ribeiro", 7.5, 8.0, 8.5, 7.0, 5],
]

OUTRAS_TURMAS = {
    "1B": [
        [2026101, "Natália Gomes", 7.0, 8.0, 7.5, 8.5, 3],
        [2026102, "Otávio Dias", 5.0, 4.5, 6.0, 5.5, 9],
        [2026103, "Paula Martins", 9.0, 9.5, 8.5, 9.0, 0],
    ],
    "1C": [
        [2026201, "Rafael Pinto", 6.0, 6.5, 7.0, 6.0, 7],
        [2026202, "Sofia Barros", 8.5, 9.0, 9.5, 10.0, 1],
    ],
}


def salvar_turma(caminho: Path, turma: str, linhas: list[list]) -> None:
    livro = Workbook()
    aba = livro.active
    aba.title = "Notas"
    aba.append(CABECALHO)
    for linha in linhas:
        aba.append(linha)
    info = livro.create_sheet("Info")
    info.append(["Turma", turma])
    info.append(["Aulas dadas", 80])
    caminho.parent.mkdir(parents=True, exist_ok=True)
    livro.save(caminho)


def main() -> None:
    if TREINO.exists():
        print(f"A pasta '{TREINO}' já existe. Apague-a se quiser começar do zero.")
        return
    salvar_turma(TREINO / "notas_1A.xlsx", "1A", TURMA_1A)
    for turma, linhas in OUTRAS_TURMAS.items():
        salvar_turma(TREINO / "turmas" / f"notas_{turma}.xlsx", turma, linhas)
    salvar_turma(TREINO / "turmas" / "notas_1A.xlsx", "1A", TURMA_1A[:3])
    print(f"Planilhas de treino criadas em: {TREINO.resolve()}")


if __name__ == "__main__":
    main()
```

Rode com `python criar_planilhas_treino.py` e abra a `notas_1A.xlsx` no Excel. Ela tem duas abas: **Notas** e **Info** (turma e aulas dadas).

!!! note "Dados com problemas de propósito"
    Três alunos têm dados "sujos", como em planilhas reais: uma nota digitada como **texto** (`"7,5"`), uma nota **não lançada** (célula vazia) e uma nota **11**. Por enquanto, só repare neles; a [aula 04](04_juntar_e_limpar.md) ensina a tratar.

## Abrindo e lendo células

```python title="ler_notas.py"
from pathlib import Path

from openpyxl import load_workbook

livro = load_workbook(Path("treino_planilhas") / "notas_1A.xlsx")
print(livro.sheetnames)

aba = livro["Notas"]
print(f"{aba.max_row} linhas, {aba.max_column} colunas")
print("A1 =", aba["A1"].value, "| B2 =", aba["B2"].value, "| C2 =", aba.cell(row=2, column=3).value)

for linha in aba.iter_rows(min_row=2, max_row=4, values_only=True):
    print(linha)
```

```text
['Notas', 'Info']
13 linhas, 7 colunas
A1 = Matrícula | B2 = Ana Souza | C2 = 8.5
(2026001, 'Ana Souza', 8.5, 7, 9, 8, 4)
(2026002, 'Bruno Lima', 5, 6.5, 4.5, 6, 10)
(2026003, 'Carla Mendes', 9.5, 9, 10, 9.5, 0)
```

| Comando | O que faz |
|---|---|
| `load_workbook(caminho)` | Abre o arquivo (o "livro") |
| `livro.sheetnames` | Nomes das abas |
| `livro["Notas"]` | Uma aba pelo nome |
| `aba["B2"].value` / `aba.cell(row=2, column=2).value` | O valor de uma célula, pela letra ou pelos números |
| `aba.max_row`, `aba.max_column` | Última linha e última coluna usadas |
| `aba.iter_rows(min_row=2, values_only=True)` | As linhas, como tuplas de **valores**, a partir da linha 2 (pulando o cabeçalho) |

!!! info "Por que `7` e não `7.0`?"
    O Excel guarda `7,0` como o número `7`, e o openpyxl devolve um `int`. Para contas, não faz diferença (`7 + 0.5` dá `7.5`). Célula vazia vem como `None`.

## Tabela ➔ lista de dicionários

Acessar `linha[5]` é difícil de ler. É melhor transformar cada linha num **dicionário** com os nomes do cabeçalho:

```python title="ler_como_dicionarios.py"
from pathlib import Path

from openpyxl import load_workbook


def ler_tabela(caminho: Path, aba: str) -> list[dict]:
    """Lê uma aba com cabeçalho na linha 1 e devolve uma lista de dicionários."""
    planilha = load_workbook(caminho, read_only=True)[aba]
    linhas = planilha.iter_rows(values_only=True)
    cabecalho = next(linhas)
    return [dict(zip(cabecalho, linha)) for linha in linhas if any(v is not None for v in linha)]


alunos = ler_tabela(Path("treino_planilhas") / "notas_1A.xlsx", "Notas")
print(len(alunos), "alunos")
print(alunos[0])
for aluno in alunos:
    if aluno["Faltas"] > 10:
        print(f"{aluno['Nome']}: {aluno['Faltas']} faltas")
```

```text
12 alunos
{'Matrícula': 2026001, 'Nome': 'Ana Souza', '1º bim': 8.5, '2º bim': 7, '3º bim': 9, '4º bim': 8, 'Faltas': 4}
Diego Rocha: 12 faltas
Gabriela Nunes: 25 faltas
Larissa Freitas: 22 faltas
```

- `next(linhas)` pega a **primeira** linha (o cabeçalho) e avança.
- `dict(zip(cabecalho, linha))` junta cada nome de coluna com o valor da mesma posição.
- `if any(v is not None for v in linha)` pula linhas totalmente vazias.
- `read_only=True` abre mais rápido e gasta menos memória (bom para planilhas grandes); nesse modo, só dá para **ler**.

---

## ⚠️ Erros comuns

- **`ModuleNotFoundError: No module named 'openpyxl'`**: o ambiente virtual não está ativado (ou o VS Code está usando outro Python).
- **`KeyError: 'Worksheet Notas does not exist.'`**: o nome da aba está diferente (maiúsculas, acento, espaço). Confira com `livro.sheetnames`.
- **`InvalidFileException`**: o arquivo não é `.xlsx` (é `.xls` antigo ou `.csv`). Abra no Excel e salve como `.xlsx`, ou leia o CSV com o módulo `csv` ([aula 04](04_juntar_e_limpar.md)).
- **Contar o cabeçalho como aluno**: use `min_row=2` ou o `next()`.

---

## Exercícios

### Básico (fixação)

Mostre o **nome** e as **faltas** de todos os alunos da `notas_1A.xlsx`, no formato `Ana Souza: 4 faltas`.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```python
    from pathlib import Path

    from openpyxl import load_workbook

    aba = load_workbook(Path("treino_planilhas") / "notas_1A.xlsx")["Notas"]
    for matricula, nome, *notas, faltas in aba.iter_rows(min_row=2, values_only=True):
        print(f"{nome}: {faltas} faltas")
    ```

    O `*notas` "recolhe" as quatro notas do meio numa lista: assim dá para pegar só o primeiro, o segundo e o último valor da linha.

### Intermediário (aplicação)

Descubra o aluno com **mais faltas** da turma 1A e mostre o nome e o número de faltas.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```python
    from pathlib import Path

    from openpyxl import load_workbook

    aba = load_workbook(Path("treino_planilhas") / "notas_1A.xlsx")["Notas"]
    linhas = list(aba.iter_rows(min_row=2, values_only=True))
    mais_faltas = max(linhas, key=lambda linha: linha[6])
    print(f"Mais faltas: {mais_faltas[1]} ({mais_faltas[6]})")
    ```

    `max(..., key=...)` escolhe a linha com o maior valor na coluna 6 (Faltas, contando do zero). Resultado: `Gabriela Nunes (25)`.

### Avançado (desafio)

Leia também a aba **Info** (aulas dadas) e mostre a **frequência** de cada aluno em porcentagem. Destaque com `⚠` quem ficou **abaixo de 75%**.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```python
    from pathlib import Path

    from openpyxl import load_workbook

    livro = load_workbook(Path("treino_planilhas") / "notas_1A.xlsx")
    aulas = livro["Info"]["B2"].value

    abaixo = []
    for matricula, nome, *notas, faltas in livro["Notas"].iter_rows(min_row=2, values_only=True):
        frequencia = (aulas - faltas) / aulas
        alerta = " ⚠" if frequencia < 0.75 else ""
        print(f"{nome:18} {frequencia:5.0%}{alerta}")
        if alerta:
            abaixo.append(nome)
    ```

    Com 80 aulas, 75% de presença permite até 20 faltas. Ficam abaixo: **Gabriela Nunes** (69%) e **Larissa Freitas** (72%). O `:5.0%` mostra o número como porcentagem, sem casas decimais.

---

## 💡 Resumo

- Instale o **openpyxl** num **ambiente virtual** (`python -m venv .venv`, `activate`, `pip install openpyxl==3.1.5`).
- `load_workbook()` abre; `livro["Aba"]` escolhe a aba; `aba["B2"].value` lê uma célula.
- `iter_rows(min_row=2, values_only=True)` percorre as linhas; `dict(zip(cabecalho, linha))` vira dicionário.
- Célula vazia é `None`; `7,0` vem como `7`.

## ➡️ Próximo passo

**[02 — Criando e formatando planilhas](02_escrever_e_formatar.md)**: cabeçalho colorido, larguras, bordas e o cabeçalho que não some ao rolar.
