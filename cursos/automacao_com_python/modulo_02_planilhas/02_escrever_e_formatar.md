# 02 — Criando e formatando planilhas

> **Curso:** Automação com Python  
> **Módulo:** 02 — Planilhas  
> **Tempo estimado:** 1 h 30 min  

---

## 🎯 Objetivos

Ao final desta aula, você será capaz de:

- Criar uma planilha nova com `Workbook()` e acrescentar linhas com `append()`.
- Formatar: **negrito**, **cor de fundo**, **alinhamento**, **bordas** e **largura** das colunas.
- **Congelar** o cabeçalho e repeti-lo na impressão.
- Salvar sem perder nada, e entender o erro de quando a planilha está **aberta no Excel**.

## Pré-requisitos

- [Aula 01](01_ler_planilhas.md): ambiente virtual com openpyxl e planilhas de treino.

---

## Criando uma planilha

```python
from openpyxl import Workbook

livro = Workbook()          # um livro novo já vem com uma aba
aba = livro.active          # a aba ativa (a primeira)
aba.title = "Chamada"       # renomeia a aba
aba.append(["Nº", "Nome"])  # acrescenta uma linha no fim
aba.append([1, "Ana Souza"])
aba["D1"] = "Observação"    # escreve numa célula específica
nova = livro.create_sheet("Resumo")  # cria outra aba
livro.save("teste.xlsx")
```

- `append()` sempre escreve **na próxima linha vazia**: é o jeito mais simples de montar uma tabela.
- `livro.save()` grava o arquivo. Se já existir um arquivo com esse nome, ele é **substituído** (a mesma lição de `shutil.move` do [Módulo 01](../modulo_01_arquivos_e_pastas/03_mover_copiar_com_seguranca.md#os-quatro-comandos)). Por isso, os scripts deste módulo salvam numa pasta **`saida`**, separada dos originais.

## A lista de chamada formatada

O script abaixo lê os nomes da planilha de notas e cria uma **lista de chamada** pronta para imprimir.

```python title="lista_de_chamada.py"
from datetime import date
from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

ORIGEM = Path("treino_planilhas") / "notas_1A.xlsx"
DESTINO = Path("treino_planilhas") / "saida" / "lista_de_chamada_1A.xlsx"

# 1. Ler os nomes da planilha de notas
notas = load_workbook(ORIGEM)["Notas"]
alunos = [(matricula, nome) for matricula, nome, *_ in notas.iter_rows(min_row=2, values_only=True)]

# 2. Criar a planilha nova
livro = Workbook()
aba = livro.active
aba.title = "Chamada"
aba.append(["Nº", "Matrícula", "Nome", "Presença"])
for numero, (matricula, nome) in enumerate(alunos, start=1):
    aba.append([numero, matricula, nome, ""])
aba.append([])
aba.append(["", "", f"Gerada em {date.today():%d/%m/%Y}"])

# 3. Formatar
roxo = PatternFill("solid", start_color="4F35B5")
fina = Side(style="thin", color="BBBBBB")
for celula in aba[1]:
    celula.font = Font(bold=True, color="FFFFFF")
    celula.fill = roxo
    celula.alignment = Alignment(horizontal="center")
for linha in aba.iter_rows(min_row=2, max_row=len(alunos) + 1):
    for celula in linha:
        celula.border = Border(left=fina, right=fina, top=fina, bottom=fina)

for coluna, largura in {"A": 6, "B": 12, "C": 28, "D": 14}.items():
    aba.column_dimensions[coluna].width = largura
aba.freeze_panes = "A2"           # o cabeçalho fica parado ao rolar
aba.print_title_rows = "1:1"      # e se repete em cada página impressa

# 4. Salvar
DESTINO.parent.mkdir(parents=True, exist_ok=True)
livro.save(DESTINO)
print(f"{len(alunos)} alunos -> {DESTINO}")
```

```text
12 alunos -> treino_planilhas\saida\lista_de_chamada_1A.xlsx
```

Abra o arquivo no Excel: cabeçalho roxo com letras brancas, bordas finas, a coluna dos nomes larga e o cabeçalho parado quando você rola a tela.

### As peças da formatação

| Objeto | Para que serve | Exemplo |
|---|---|---|
| `Font` | Letra: negrito, itálico, cor, tamanho | `Font(bold=True, color="FFFFFF", size=12)` |
| `PatternFill` | Cor de fundo da célula | `PatternFill("solid", start_color="4F35B5")` |
| `Alignment` | Alinhamento e quebra de texto | `Alignment(horizontal="center", wrap_text=True)` |
| `Border` + `Side` | Bordas | `Border(bottom=Side(style="thin"))` |
| `column_dimensions["C"].width` | Largura da coluna (em "caracteres") | `28` |
| `number_format` | Como o número aparece | `"0.0"`, `"0%"`, `"dd/mm/yyyy"`, `'"R$" #,##0.00'` |
| `freeze_panes` | Congela linhas/colunas acima e à esquerda da célula | `"A2"` congela a linha 1 |

!!! info "Cores em hexadecimal"
    As cores são códigos de 6 dígitos no formato **RRGGBB** (vermelho, verde, azul), os mesmos do Canva e dos sites: `4F35B5` é o roxo da plataforma, `FFFFFF` é branco, `000000` é preto. Escolha cores com bom **contraste** entre a letra e o fundo.

!!! tip "`aba[1]` é a linha 1 inteira"
    `aba[1]` devolve as células da linha 1; `aba["C"]`, as da coluna C; `aba["A1:D1"]`, um intervalo. Dá para formatar tudo com um `for`.

## "Permission denied": a planilha está aberta

Se o arquivo de destino estiver **aberto no Excel**, o Windows não deixa outro programa gravar nele:

```text
PermissionError: [Errno 13] Permission denied: 'treino_planilhas\\saida\\lista_de_chamada_1A.xlsx'
```

Feche a planilha no Excel e rode de novo. Para dar uma mensagem amigável, use `try`/`except`:

```python
try:
    livro.save(DESTINO)
except PermissionError:
    print("Não consegui salvar: a planilha está aberta no Excel? Feche e rode de novo.")
```

---

## ⚠️ Erros comuns

- **Salvar por cima da planilha original** sem querer. Use a pasta `saida` (ou um nome com a data).
- **`PermissionError`**: a planilha está aberta no Excel.
- **Cor que não aparece**: faltou o `"solid"` no `PatternFill`.
- **`ValueError: Cannot convert [...] to Excel`**: tentou gravar numa célula um valor que o Excel não entende (uma lista, um dicionário). Grave números, textos, datas ou `None`.
- **Formatar antes de existir a linha**: formate **depois** dos `append()`.

---

## Exercícios

### Básico (fixação)

Crie a planilha `treino_planilhas/saida/contatos.xlsx` com o cabeçalho **Nome, E-mail, Telefone** em negrito e três contatos inventados (use e-mails `@example.com`).

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```python
    from pathlib import Path

    from openpyxl import Workbook
    from openpyxl.styles import Font

    livro = Workbook()
    aba = livro.active
    aba.title = "Contatos"
    aba.append(["Nome", "E-mail", "Telefone"])
    aba.append(["Ana Souza", "ana.souza@example.com", "(11) 90000-0001"])
    aba.append(["Bruno Lima", "bruno.lima@example.com", "(11) 90000-0002"])
    aba.append(["Carla Mendes", "carla.mendes@example.com", "(11) 90000-0003"])
    for celula in aba[1]:
        celula.font = Font(bold=True)

    destino = Path("treino_planilhas") / "saida" / "contatos.xlsx"
    destino.parent.mkdir(parents=True, exist_ok=True)
    livro.save(destino)
    ```

    O domínio `example.com` é reservado para exemplos: nenhum e-mail de verdade vai para lá. Telefones ficam como **texto**, para o Excel não "comer" o zero nem os parênteses.

### Intermediário (aplicação)

Gere `treino_planilhas/saida/alerta_faltas.xlsx` só com os alunos da 1A que têm **mais de 10 faltas** (Nome e Faltas), cabeçalho formatado e a coluna dos nomes larga.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```python
    from pathlib import Path

    from openpyxl import Workbook, load_workbook
    from openpyxl.styles import Font, PatternFill

    notas = load_workbook(Path("treino_planilhas") / "notas_1A.xlsx")["Notas"]

    livro = Workbook()
    aba = livro.active
    aba.title = "Alerta de faltas"
    aba.append(["Nome", "Faltas"])
    for matricula, nome, *bimestres, faltas in notas.iter_rows(min_row=2, values_only=True):
        if faltas > 10:
            aba.append([nome, faltas])

    for celula in aba[1]:
        celula.font = Font(bold=True, color="FFFFFF")
        celula.fill = PatternFill("solid", start_color="9C0006")
    aba.column_dimensions["A"].width = 24

    destino = Path("treino_planilhas") / "saida" / "alerta_faltas.xlsx"
    destino.parent.mkdir(parents=True, exist_ok=True)
    livro.save(destino)
    print(f"{aba.max_row - 1} alunos com mais de 10 faltas")
    ```

    Resultado: **3** alunos, Diego (12), Gabriela (25) e Larissa (22). O Bruno tem exatamente 10 faltas e fica de fora, porque "mais de 10" é `> 10` (com `>= 10`, ele entraria).

### Avançado (desafio)

Junte as planilhas da pasta `treino_planilhas/turmas` num **único arquivo com uma aba por turma** (o nome da aba é a turma, lido da aba Info de cada arquivo), copiando a tabela de notas de cada uma.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```python
    from pathlib import Path

    from openpyxl import Workbook, load_workbook
    from openpyxl.styles import Font

    novo = Workbook()
    novo.remove(novo.active)  # tira a aba vazia que vem no livro novo

    for arquivo in sorted((Path("treino_planilhas") / "turmas").glob("notas_*.xlsx")):
        origem = load_workbook(arquivo)
        turma = origem["Info"]["B1"].value
        aba = novo.create_sheet(turma)
        for linha in origem["Notas"].iter_rows(values_only=True):
            aba.append(linha)
        for celula in aba[1]:
            celula.font = Font(bold=True)

    destino = Path("treino_planilhas") / "saida" / "turmas_por_aba.xlsx"
    destino.parent.mkdir(parents=True, exist_ok=True)
    novo.save(destino)
    print(novo.sheetnames)
    ```

    Saída: `['1A', '1B', '1C']`. O `novo.remove(novo.active)` evita que o arquivo fique com uma aba "Sheet" vazia no começo.

---

## 💡 Resumo

- `Workbook()` cria; `append()` acrescenta linhas; `create_sheet()` cria abas; `save()` grava (e **substitui** se existir).
- Formate com `Font`, `PatternFill("solid", ...)`, `Alignment`, `Border`, `width` e `number_format`.
- `freeze_panes = "A2"` congela o cabeçalho; `print_title_rows = "1:1"` repete na impressão.
- `PermissionError` ao salvar = a planilha está aberta no Excel.

## ➡️ Próximo passo

**[03 — Fórmulas, totais e formatação condicional](03_formulas_e_condicional.md)**.
