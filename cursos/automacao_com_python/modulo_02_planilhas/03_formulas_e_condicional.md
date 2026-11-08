# 03 — Fórmulas, totais e formatação condicional

> **Curso:** Automação com Python  
> **Módulo:** 02 — Planilhas  
> **Tempo estimado:** 1 h 30 min  

---

## 🎯 Objetivos

Ao final desta aula, você será capaz de:

- Escrever **fórmulas** do Excel pelo Python (`=AVERAGE`, `=SUM`, `=COUNTIF`).
- Entender a diferença entre **fórmula** (o Excel calcula) e **valor** (o Python calcula), e quando usar cada uma.
- Acrescentar uma **linha de totais**.
- Aplicar **formatação condicional**: a célula muda de cor sozinha conforme o valor.

## Pré-requisitos

- [Aula 02](02_escrever_e_formatar.md): criar e formatar planilhas.

---

## Escrevendo fórmulas

Para o openpyxl, uma fórmula é um **texto que começa com `=`**. Ele grava o texto na célula, e o **Excel calcula** quando o arquivo é aberto.

```python title="medias_com_formulas.py"
from pathlib import Path

from openpyxl import load_workbook
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import Font, PatternFill

ORIGEM = Path("treino_planilhas") / "notas_1A.xlsx"
DESTINO = Path("treino_planilhas") / "saida" / "notas_1A_com_medias.xlsx"

livro = load_workbook(ORIGEM)
aba = livro["Notas"]
ultima = aba.max_row  # última linha com alunos

# Coluna H: a média de cada aluno, como FÓRMULA (o Excel calcula ao abrir)
aba["H1"] = "Média"
aba["H1"].font = Font(bold=True)
for linha in range(2, ultima + 1):
    aba[f"H{linha}"] = f"=AVERAGE(C{linha}:F{linha})"
    aba[f"H{linha}"].number_format = "0.0"

# Linha de totais embaixo
aba[f"B{ultima + 2}"] = "Média da turma"
aba[f"B{ultima + 2}"].font = Font(bold=True)
aba[f"H{ultima + 2}"] = f"=AVERAGE(H2:H{ultima})"
aba[f"H{ultima + 2}"].number_format = "0.0"
aba[f"B{ultima + 3}"] = "Alunos abaixo de 6"
aba[f"H{ultima + 3}"] = f'=COUNTIF(H2:H{ultima},"<6")'

# Formatação condicional: média abaixo de 6 fica vermelha
vermelho = PatternFill("solid", start_color="FFC7CE")
aba.conditional_formatting.add(
    f"H2:H{ultima}",
    CellIsRule(operator="lessThan", formula=["6"], fill=vermelho, font=Font(color="9C0006")),
)

DESTINO.parent.mkdir(parents=True, exist_ok=True)
livro.save(DESTINO)
print(f"Salvo: {DESTINO}")
print("H2 contém:", aba["H2"].value)
```

```text
Salvo: treino_planilhas\saida\notas_1A_com_medias.xlsx
H2 contém: =AVERAGE(C2:F2)
```

!!! warning "Fórmulas em inglês e com vírgula"
    No Excel em português você digita `=MÉDIA(C2:F2)` e `=CONT.SE(H2:H13;"<6")`. Mas, **dentro do arquivo**, o Excel guarda tudo em **inglês** e com **vírgula** separando os argumentos: `=AVERAGE(C2:F2)`, `=COUNTIF(H2:H13,"<6")`. O openpyxl escreve direto no arquivo, então use os nomes em inglês. Ao abrir, o Excel em português mostra `MÉDIA` e `CONT.SE` normalmente.

| Em português (Excel) | No arquivo (openpyxl) |
|---|---|
| `=SOMA(A1:A5)` | `=SUM(A1:A5)` |
| `=MÉDIA(A1:A5)` | `=AVERAGE(A1:A5)` |
| `=CONT.SE(A1:A5;">6")` | `=COUNTIF(A1:A5,">6")` |
| `=SE(A1>=6;"Sim";"Não")` | `=IF(A1>=6,"Sim","Não")` |
| `=MÁXIMO(A1:A5)` / `=MÍNIMO(A1:A5)` | `=MAX(A1:A5)` / `=MIN(A1:A5)` |

## Fórmula ou valor?

O openpyxl **não calcula** fórmulas. Se você abrir o arquivo recém-gerado com `data_only=True` (que lê o **resultado** em vez da fórmula), vem `None`:

```python
from openpyxl import load_workbook

aba = load_workbook("treino_planilhas/saida/notas_1A_com_medias.xlsx", data_only=True)["Notas"]
print(aba["H2"].value)   # None: ninguém calculou ainda
```

O resultado só passa a existir depois que alguém abre o arquivo no Excel e **salva**.

| Use **fórmula** quando... | Use **valor** (calcular no Python) quando... |
|---|---|
| A planilha vai ser **editada** por pessoas e o total deve se atualizar sozinho | O **próprio script** precisa do resultado (para decidir a situação, gerar um certificado...) |
| Quem abre quer **ver como** o número foi calculado | As regras são complicadas demais para uma fórmula |
| | Os dados têm problemas que o Python trata antes (aula 04) |

O projeto do módulo ([aula 05](05_projeto_boletim.md)) calcula as médias **no Python**, porque precisa delas para decidir quem foi aprovado.

!!! note "Repare na Elisa e no João Pedro"
    A `=AVERAGE()` **ignora células com texto**: a média da Elisa (que tem `"7,5"` digitado como texto) sai calculada com só três notas. E aceita o **11** do João Pedro sem reclamar. A fórmula não avisa nada. A [aula 04](04_juntar_e_limpar.md) mostra como encontrar e tratar esses problemas antes.

## Formatação condicional

A **formatação condicional** fica gravada na planilha e é aplicada **pelo Excel**: se alguém mudar uma nota depois, a cor muda sozinha.

```python
from openpyxl.formatting.rule import CellIsRule

aba.conditional_formatting.add(
    "H2:H13",                                   # onde
    CellIsRule(operator="lessThan", formula=["6"],  # quando: valor < 6
               fill=PatternFill("solid", start_color="FFC7CE"),
               font=Font(color="9C0006")),      # como fica
)
```

| `operator` | Significa |
|---|---|
| `"lessThan"` / `"greaterThan"` | Menor que / maior que |
| `"lessThanOrEqual"` / `"greaterThanOrEqual"` | Menor ou igual / maior ou igual |
| `"equal"` / `"notEqual"` | Igual / diferente |
| `"between"` | Entre dois valores: `formula=["4", "5.9"]` |

!!! tip "Cores que todo mundo entende"
    Vermelho-claro com letra vermelho-escura (`FFC7CE` / `9C0006`), amarelo (`FFEB9C` / `9C5700`) e verde (`C6EFCE` / `006100`) são as cores-padrão do próprio Excel para "ruim, atenção, bom". Não use **só** a cor para passar a informação (pessoas com daltonismo podem não ver): a coluna "Situação" do projeto escreve também o texto.

---

## ⚠️ Erros comuns

- **Fórmula em português** (`=MÉDIA(...)`): o Excel mostra `#NOME?`. Use o nome em inglês.
- **Ponto e vírgula** nos argumentos dentro do openpyxl: use **vírgula**.
- **Esperar o resultado com `data_only=True`** num arquivo que ninguém abriu no Excel: vem `None`.
- **Intervalo errado** depois de acrescentar linhas: calcule o intervalo com `aba.max_row`, não com número fixo.
- **Formatação condicional com texto no `formula`**: para comparar com texto, use aspas dentro das aspas: `formula=['"Reprovado"']`.

---

## Exercícios

### Básico (fixação)

Na planilha `notas_1A.xlsx`, acrescente a coluna **I — Total de pontos** com a fórmula da **soma** das quatro notas de cada aluno e salve em `saida/notas_1A_total.xlsx`.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```python
    from pathlib import Path

    from openpyxl import load_workbook

    livro = load_workbook(Path("treino_planilhas") / "notas_1A.xlsx")
    aba = livro["Notas"]
    aba["I1"] = "Total de pontos"
    for linha in range(2, aba.max_row + 1):
        aba[f"I{linha}"] = f"=SUM(C{linha}:F{linha})"

    destino = Path("treino_planilhas") / "saida" / "notas_1A_total.xlsx"
    destino.parent.mkdir(parents=True, exist_ok=True)
    livro.save(destino)
    ```

    No Excel em português, a célula I2 vai aparecer como `=SOMA(C2:F2)`.

### Intermediário (aplicação)

Faça o contrário da aula: calcule a média de cada aluno **no Python** (ignorando por enquanto os alunos com nota em texto ou vazia) e grave o **valor** na coluna H. Confira abrindo com `data_only=True`: agora vem o número.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```python
    from pathlib import Path

    from openpyxl import load_workbook

    destino = Path("treino_planilhas") / "saida" / "notas_1A_valores.xlsx"
    livro = load_workbook(Path("treino_planilhas") / "notas_1A.xlsx")
    aba = livro["Notas"]
    aba["H1"] = "Média"
    for linha in range(2, aba.max_row + 1):
        notas = [aba.cell(row=linha, column=c).value for c in range(3, 7)]
        if all(isinstance(n, (int, float)) for n in notas):
            aba[f"H{linha}"] = sum(notas) / len(notas)
            aba[f"H{linha}"].number_format = "0.0"
    destino.parent.mkdir(parents=True, exist_ok=True)
    livro.save(destino)

    conferir = load_workbook(destino, data_only=True)["Notas"]
    print(conferir["H2"].value)   # 8.125
    ```

    O valor gravado é o número completo (`8.125`); o `number_format` só muda **como aparece** (`8,1`). Elisa e Felipe ficam sem média (texto e célula vazia). O João Pedro, com o 11, ainda entra: a aula 04 resolve.

### Avançado (desafio)

Use formatação condicional na coluna **Faltas** (G) para pintar de **amarelo** quem tem **mais de 20 faltas** (frequência abaixo de 75% com 80 aulas) e escreva na célula **G15** uma fórmula que conte quantos são.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```python
    from pathlib import Path

    from openpyxl import load_workbook
    from openpyxl.formatting.rule import CellIsRule
    from openpyxl.styles import Font, PatternFill

    livro = load_workbook(Path("treino_planilhas") / "notas_1A.xlsx")
    aba = livro["Notas"]
    ultima = aba.max_row
    aba.conditional_formatting.add(
        f"G2:G{ultima}",
        CellIsRule(operator="greaterThan", formula=["20"],
                   fill=PatternFill("solid", start_color="FFEB9C"), font=Font(color="9C5700")),
    )
    aba[f"F{ultima + 2}"] = "Acima de 20 faltas:"
    aba[f"G{ultima + 2}"] = f'=COUNTIF(G2:G{ultima},">20")'

    destino = Path("treino_planilhas") / "saida" / "notas_1A_faltas.xlsx"
    destino.parent.mkdir(parents=True, exist_ok=True)
    livro.save(destino)
    ```

    Com 13 linhas na aba (cabeçalho + 12 alunos), a contagem cai em `G15`. Ao abrir no Excel, Gabriela (25) e Larissa (22) ficam amarelas e a fórmula mostra **2**.

---

## 💡 Resumo

- Fórmula = texto que começa com `=`, **em inglês** e com **vírgula**: `=AVERAGE(C2:F2)`.
- O openpyxl **não calcula**: o Excel calcula ao abrir. `data_only=True` só traz o resultado de arquivos salvos pelo Excel.
- **Fórmula** para quem vai editar a planilha; **valor** calculado no Python quando o script precisa do resultado.
- **Formatação condicional** (`CellIsRule`) pinta as células sozinha, mesmo depois de editadas.

## ➡️ Próximo passo

**[04 — Juntar planilhas e limpar dados](04_juntar_e_limpar.md)**: várias turmas num arquivo só, CSV e notas digitadas errado.
