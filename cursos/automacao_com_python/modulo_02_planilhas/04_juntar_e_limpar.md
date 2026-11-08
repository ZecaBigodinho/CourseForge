# 04 — Juntar planilhas e limpar dados

> **Curso:** Automação com Python  
> **Módulo:** 02 — Planilhas  
> **Tempo estimado:** 1 h 30 min  

---

## 🎯 Objetivos

Ao final desta aula, você será capaz de:

- **Juntar** várias planilhas iguais (uma por turma) numa só.
- Gravar e ler **CSV** que abre certo no Excel em português.
- **Limpar** dados digitados errado: número como texto, célula vazia, valor fora do intervalo.
- Listar os **problemas** encontrados em vez de esconder ou "chutar" um valor.

## Pré-requisitos

- [Aulas 01 a 03](01_ler_planilhas.md) deste módulo.

---

## Juntando as planilhas das turmas

Cada turma tem a sua planilha, com o mesmo formato, na pasta `treino_planilhas/turmas`. O script junta todas numa planilha só e numa versão **CSV**, acrescentando a coluna **Turma** (lida da aba Info de cada arquivo).

```python title="juntar_turmas.py"
import csv
from pathlib import Path

from openpyxl import Workbook, load_workbook

PASTA = Path("treino_planilhas") / "turmas"
SAIDA = Path("treino_planilhas") / "saida"

linhas = []
for arquivo in sorted(PASTA.glob("notas_*.xlsx")):
    livro = load_workbook(arquivo, read_only=True)
    turma = livro["Info"]["B1"].value
    dados = livro["Notas"].iter_rows(values_only=True)
    cabecalho = next(dados)
    for linha in dados:
        if any(v is not None for v in linha):
            linhas.append([turma, *linha])
    livro.close()
    print(f"{arquivo.name}: turma {turma}")

# Planilha consolidada
consolidado = Workbook()
aba = consolidado.active
aba.title = "Todas as turmas"
aba.append(["Turma", *cabecalho])
for linha in linhas:
    aba.append(linha)
SAIDA.mkdir(parents=True, exist_ok=True)
consolidado.save(SAIDA / "todas_as_turmas.xlsx")

# A mesma tabela em CSV (abre no Excel em português)
with open(SAIDA / "todas_as_turmas.csv", "w", newline="", encoding="utf-8-sig") as arq:
    escritor = csv.writer(arq, delimiter=";")
    escritor.writerow(["Turma", *cabecalho])
    for linha in linhas:
        escritor.writerow([str(v).replace(".", ",") if isinstance(v, float) else v for v in linha])

print(f"{len(linhas)} alunos juntados em {SAIDA}")
```

```text
notas_1A.xlsx: turma 1A
notas_1B.xlsx: turma 1B
notas_1C.xlsx: turma 1C
8 alunos juntados em treino_planilhas\saida
```

E o começo do CSV:

```text
Turma;Matrícula;Nome;1º bim;2º bim;3º bim;4º bim;Faltas
1A;2026001;Ana Souza;8,5;7;9;8;4
1A;2026002;Bruno Lima;5;6,5;4,5;6;10
```

!!! info "CSV para o Excel em português"
    Três detalhes fazem o CSV abrir direto, com colunas separadas e acentos certos: **`;`** como separador (no Brasil, a vírgula é o separador decimal), **`utf-8-sig`** (a marca que diz ao Excel "isto é UTF-8") e números decimais com **vírgula** (`8,5`). O `livro.close()` fecha o arquivo aberto em `read_only`.

## Dados sujos

Planilhas preenchidas por pessoas têm erros. Na `notas_1A.xlsx` de treino, de propósito:

| Aluno | Valor | Problema |
|---|---|---|
| Elisa Prado | `"7,5"` | Número digitado como **texto** (célula formatada como texto, ou colado de outro lugar) |
| Felipe Torres | (vazia) | Nota **não lançada** |
| João Pedro Melo | `11` | Fora do intervalo de **0 a 10** |

Um script que ignora isso calcula médias **erradas sem avisar** (como a `=AVERAGE` da [aula 03](03_formulas_e_condicional.md#formula-ou-valor)). Um script que "chuta" um valor (trocar o 11 por 10, o vazio por 0) toma uma **decisão que não é dele**. O certo: **converter** o que dá para converter com segurança e **listar** o resto para uma pessoa resolver.

## `converter_nota()`: tratar sem esconder

```python title="converter_nota.py"
def converter_nota(valor) -> tuple[float | None, str]:
    """Transforma o valor da célula em nota. Devolve (nota, problema); problema vazio = tudo certo."""
    if valor is None or str(valor).strip() == "":
        return None, "nota não lançada"
    if isinstance(valor, str):
        try:
            valor = float(valor.strip().replace(",", "."))
        except ValueError:
            return None, f"valor inválido: {valor!r}"
    if not 0 <= valor <= 10:
        return None, f"fora de 0 a 10: {valor}"
    return float(valor), ""


for teste in [8.5, 7, "7,5", " 6.0 ", None, "", "dez", 11, -1]:
    print(f"{teste!r:8} -> {converter_nota(teste)}")
```

```text
8.5      -> (8.5, '')
7        -> (7.0, '')
'7,5'    -> (7.5, '')
' 6.0 '  -> (6.0, '')
None     -> (None, 'nota não lançada')
''       -> (None, 'nota não lançada')
'dez'    -> (None, "valor inválido: 'dez'")
11       -> (None, 'fora de 0 a 10: 11')
-1       -> (None, 'fora de 0 a 10: -1')
```

- A função **sempre** devolve duas coisas: a nota (ou `None`) e a descrição do problema (ou `""`). Quem chama decide o que fazer com cada caso.
- `"7,5"` é convertido com segurança: trocar a vírgula por ponto não muda o significado.
- `try`/`except ValueError` pega textos que não são número (`"dez"`, `"F"`).
- A lista de testes no fim mostra **todos os casos** de uma vez. Sempre teste uma função de limpeza com os valores estranhos, não só com os bons.

!!! tip "Escreva os testes antes de usar a função"
    A linha `for teste in [...]` é um teste rápido. Se um dia você mudar a função, rode de novo e veja se tudo continua igual. É assim que os gabaritos deste curso são conferidos automaticamente.

---

## ⚠️ Erros comuns

- **CSV com vírgula** como separador: no Excel em português, tudo cai numa coluna só.
- **CSV sem `-sig`**: os acentos aparecem como `Ã©`.
- **`float("7,5")`**: dá `ValueError`. Troque a vírgula por ponto antes.
- **Trocar valores problemáticos por um "padrão"** (0, 10, a média) sem avisar ninguém.
- **Juntar planilhas com colunas em ordem diferente**: confira se o cabeçalho de todas é igual antes de juntar (veja o desafio).

---

## Exercícios

### Básico (fixação)

Usando a `converter_nota()`, mostre **todas as notas com problema** da `notas_1A.xlsx`, no formato `Felipe Torres, 4º bim: nota não lançada`.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```python
    from pathlib import Path

    from openpyxl import load_workbook


    def converter_nota(valor) -> tuple[float | None, str]:
        if valor is None or str(valor).strip() == "":
            return None, "nota não lançada"
        if isinstance(valor, str):
            try:
                valor = float(valor.strip().replace(",", "."))
            except ValueError:
                return None, f"valor inválido: {valor!r}"
        if not 0 <= valor <= 10:
            return None, f"fora de 0 a 10: {valor}"
        return float(valor), ""


    aba = load_workbook(Path("treino_planilhas") / "notas_1A.xlsx")["Notas"]
    problemas = []
    for matricula, nome, *bimestres, faltas in aba.iter_rows(min_row=2, values_only=True):
        for bim, valor in enumerate(bimestres, start=1):
            nota, problema = converter_nota(valor)
            if problema:
                problemas.append(problema)
                print(f"{nome}, {bim}º bim: {problema}")
    ```

    Aparecem dois: o 4º bimestre do Felipe (não lançada) e o do João Pedro (fora de 0 a 10: 11). O `"7,5"` da Elisa **não** é problema: foi convertido.

### Intermediário (aplicação)

Leia de volta o `saida/todas_as_turmas.csv` com o módulo `csv` e calcule a **média do 1º bimestre** de todos os alunos juntos. Atenção: no CSV, as notas são **texto** com vírgula.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```python
    import csv
    from pathlib import Path

    caminho = Path("treino_planilhas") / "saida" / "todas_as_turmas.csv"
    with open(caminho, newline="", encoding="utf-8-sig") as arq:
        linhas = list(csv.DictReader(arq, delimiter=";"))

    notas = [float(linha["1º bim"].replace(",", ".")) for linha in linhas]
    media = sum(notas) / len(notas)
    print(f"{len(notas)} alunos, média do 1º bimestre: {media:.2f}")
    ```

    Ler com `utf-8-sig` faz a "marca" do começo do arquivo sumir; sem ela, a primeira coluna viria com o nome `﻿Turma`. Resultado: 8 alunos, média **7,31** (o `print` mostra `7.31`, com ponto: para mostrar com vírgula, use `f"{media:.2f}".replace(".", ",")`).

### Avançado (desafio)

Antes de juntar, o script deveria conferir se **todas** as planilhas têm o **mesmo cabeçalho**. Escreva a função `cabecalhos_iguais(arquivos)` que devolve `True` se todos forem iguais e, se não forem, mostra qual arquivo é diferente.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```python
    from pathlib import Path

    from openpyxl import load_workbook


    def cabecalho(arquivo: Path) -> tuple:
        livro = load_workbook(arquivo, read_only=True)
        primeira = next(livro["Notas"].iter_rows(max_row=1, values_only=True))
        livro.close()
        return primeira


    def cabecalhos_iguais(arquivos: list[Path]) -> bool:
        referencia = cabecalho(arquivos[0])
        iguais = True
        for arquivo in arquivos[1:]:
            atual = cabecalho(arquivo)
            if atual != referencia:
                print(f"{arquivo.name} é diferente: {atual}")
                iguais = False
        return iguais


    arquivos = sorted((Path("treino_planilhas") / "turmas").glob("notas_*.xlsx"))
    print(cabecalhos_iguais(arquivos))
    ```

    Nas planilhas de treino, todas são iguais: `True`. Use a função no começo do `juntar_turmas.py` e **pare** (sem juntar nada) se ela devolver `False`.

---

## 💡 Resumo

- Junte planilhas iguais com um `for` em `glob("notas_*.xlsx")`, acrescentando de onde veio cada linha.
- CSV para o Excel em português: **`;`**, **`utf-8-sig`** e decimais com **vírgula**.
- Dados sujos: **converta** o que é seguro (`"7,5"`), **liste** o resto (vazio, fora do intervalo, inválido). Nunca "chute" valores.
- Teste funções de limpeza com os valores **estranhos**.

## ➡️ Próximo passo

**[05 — Projeto do módulo: boletim da turma](05_projeto_boletim.md)**.
