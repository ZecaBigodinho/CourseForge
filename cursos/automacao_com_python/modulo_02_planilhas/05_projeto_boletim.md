# 05 — Projeto do módulo: boletim da turma

> **Curso:** Automação com Python  
> **Módulo:** 02 — Planilhas  
> **Tempo estimado:** 2 h  

---

## 🎯 Objetivos

Ao final desta aula, você terá um script que:

- Lê a planilha de notas da turma, **limpa** os dados e lista os **problemas**.
- Calcula **média**, **frequência** e **situação** de cada aluno, com as regras da escola.
- Gera um **boletim em Excel** com três abas: **Boletim** (formatado e colorido), **Resumo** e **Problemas**.
- **Arredonda** as médias do jeito certo (e você vai entender por que o `round()` não serve).

## Pré-requisitos

- Aulas [01](01_ler_planilhas.md) a [04](04_juntar_e_limpar.md) deste módulo.
- As planilhas de treino originais (apague a `treino_planilhas` e rode o `criar_planilhas_treino.py`, se precisar).

---

## As regras

| Regra | Valor no script |
|---|---|
| Média = média simples dos 4 bimestres, com **1 casa decimal** | `arredondar()` |
| **Aprovado:** média ≥ 6,0 e frequência ≥ 75% | `MEDIA_APROVACAO = 6.0`, `FREQUENCIA_MINIMA = 0.75` |
| **Recuperação:** média entre 4,0 e 5,9 (com frequência ≥ 75%) | `MEDIA_RECUPERACAO = 4.0` |
| **Reprovado:** média abaixo de 4,0 **ou** frequência abaixo de 75% | |
| **Pendente:** alguma nota com problema (não lançada, inválida ou fora de 0 a 10) | |

!!! info "As regras da sua escola podem ser outras"
    Por isso elas ficam em **constantes** no começo do script. Mudou a regra? Muda o número, não o código.

## O arredondamento: um bug que o teste achou

A primeira versão do boletim usava `round(media, 1)`. Conferindo as médias à mão, apareceu a diferença:

```text
>>> round(4.25, 1), round(7.25, 1)
(4.2, 7.2)
```

Na escola, **4,25 vira 4,3**. O Python deu 4,2 por dois motivos: o `round()` usa o "arredondamento do banqueiro" (empates vão para o número **par**: `round(2.5)` dá `2`) e, além disso, `4.25` guardado como número de ponto flutuante é, na verdade, um pouquinho diferente de 4,25. No boletim da turma de treino, isso mudava a média de **quatro** alunos (Diego, Elisa, Gabriela e Heitor).

A solução é o módulo `decimal`, que trabalha com o número **exatamente como escrito** e deixa escolher a regra de arredondamento:

```python
from decimal import ROUND_HALF_UP, Decimal


def arredondar(valor: float) -> float:
    return float(Decimal(str(valor)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))


print(arredondar(4.25), arredondar(7.25), arredondar(8.125))   # 4.3 7.3 8.1
```

- `str(valor)` transforma o número em texto (`"4.25"`) antes de virar `Decimal`, para não carregar o "pouquinho diferente".
- `quantize(Decimal("0.1"))` fixa **uma** casa decimal; `ROUND_HALF_UP` arredonda o 5 **para cima**, como na escola.

!!! warning "Dinheiro e notas: nada de `round()` para decidir"
    Sempre que um arredondamento **decide** alguma coisa (aprovação, valor a pagar, troco), use `Decimal` com a regra explícita. O curso de [Java](../../java/modulo_03_colecoes_e_arquivos/index.md) mostra o mesmo problema com o `BigDecimal`.

## O script

```python title="boletim.py"
"""Boletim da turma: lê a planilha de notas, calcula médias e situação e gera um Excel formatado."""
from collections import Counter
from datetime import date
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import Alignment, Font, PatternFill

ORIGEM = Path("treino_planilhas") / "notas_1A.xlsx"
SAIDA = Path("treino_planilhas") / "saida"
MEDIA_APROVACAO = 6.0
MEDIA_RECUPERACAO = 4.0
FREQUENCIA_MINIMA = 0.75  # 75% de presença

CORES = {"Aprovado": "C6EFCE", "Recuperação": "FFEB9C", "Reprovado": "FFC7CE", "Pendente": "D9D9D9"}


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


def arredondar(valor: float) -> float:
    """Arredonda para 1 casa do jeito da escola: 4,25 vira 4,3 (o round() do Python daria 4,2)."""
    return float(Decimal(str(valor)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))


def situacao(media: float | None, frequencia: float) -> str:
    if media is None:
        return "Pendente"
    if frequencia < FREQUENCIA_MINIMA:
        return "Reprovado"  # por falta, mesmo com nota boa
    if media >= MEDIA_APROVACAO:
        return "Aprovado"
    if media >= MEDIA_RECUPERACAO:
        return "Recuperação"
    return "Reprovado"


def ler_turma(caminho: Path) -> tuple[str, int, list[dict], list[list]]:
    livro = load_workbook(caminho, read_only=True)
    info = {chave: valor for chave, valor in livro["Info"].iter_rows(values_only=True)}
    alunos, problemas = [], []
    linhas = livro["Notas"].iter_rows(min_row=2, values_only=True)
    for numero, (matricula, nome, *bimestres, faltas) in enumerate(linhas, start=2):
        if matricula is None:
            continue
        notas = []
        for bim, valor in enumerate(bimestres, start=1):
            nota, problema = converter_nota(valor)
            notas.append(nota)
            if problema:
                problemas.append([numero, nome, f"{bim}º bim", problema])
        alunos.append({"matricula": matricula, "nome": nome, "notas": notas, "faltas": faltas or 0})
    livro.close()
    return info["Turma"], info["Aulas dadas"], alunos, problemas


def calcular(alunos: list[dict], aulas: int) -> None:
    for aluno in alunos:
        notas = aluno["notas"]
        aluno["media"] = None if None in notas else arredondar(sum(notas) / len(notas))
        aluno["frequencia"] = (aulas - aluno["faltas"]) / aulas
        aluno["situacao"] = situacao(aluno["media"], aluno["frequencia"])


def gerar(turma: str, alunos: list[dict], problemas: list[list]) -> Path:
    livro = Workbook()
    aba = livro.active
    aba.title = "Boletim"
    aba.append(["Matrícula", "Nome", "1º bim", "2º bim", "3º bim", "4º bim", "Média", "Frequência", "Situação"])
    for a in alunos:
        aba.append([a["matricula"], a["nome"], *a["notas"], a["media"], a["frequencia"], a["situacao"]])

    for celula in aba[1]:
        celula.font = Font(bold=True, color="FFFFFF")
        celula.fill = PatternFill("solid", start_color="4F35B5")
        celula.alignment = Alignment(horizontal="center")
    for linha in aba.iter_rows(min_row=2):
        for celula in linha[2:7]:
            celula.number_format = "0.0"
        linha[7].number_format = "0%"
        cor = CORES[linha[8].value]
        linha[8].fill = PatternFill("solid", start_color=cor)
    ultima = aba.max_row
    aba.conditional_formatting.add(
        f"C2:G{ultima}", CellIsRule(operator="lessThan", formula=["6"], font=Font(color="9C0006", bold=True)))
    for coluna, largura in zip("ABCDEFGHI", [12, 24, 8, 8, 8, 8, 8, 12, 14]):
        aba.column_dimensions[coluna].width = largura
    aba.freeze_panes = "C2"

    resumo = livro.create_sheet("Resumo")
    resumo.append(["Turma", turma])
    resumo.append(["Gerado em", f"{date.today():%d/%m/%Y}"])
    resumo.append([])
    resumo.append(["Situação", "Alunos"])
    for nome, quantidade in Counter(a["situacao"] for a in alunos).most_common():
        resumo.append([nome, quantidade])
    medias = [a["media"] for a in alunos if a["media"] is not None]
    resumo.append([])
    resumo.append(["Média da turma", arredondar(sum(medias) / len(medias)) if medias else "-"])
    resumo.column_dimensions["A"].width = 18

    aba_problemas = livro.create_sheet("Problemas")
    aba_problemas.append(["Linha", "Aluno", "Onde", "Problema"])
    for problema in problemas:
        aba_problemas.append(problema)
    aba_problemas.column_dimensions["B"].width = 24
    aba_problemas.column_dimensions["D"].width = 28

    SAIDA.mkdir(parents=True, exist_ok=True)
    destino = SAIDA / f"boletim_{turma}_{date.today():%Y-%m-%d}.xlsx"
    livro.save(destino)
    return destino


def main() -> None:
    turma, aulas, alunos, problemas = ler_turma(ORIGEM)
    calcular(alunos, aulas)
    for a in alunos:
        media = "-" if a["media"] is None else f"{a['media']:.1f}"
        print(f"{a['nome']:18} média {media:>4}  frequência {a['frequencia']:4.0%}  {a['situacao']}")
    if problemas:
        print(f"\n⚠ {len(problemas)} problema(s) na planilha: veja a aba 'Problemas'.")
        for linha, nome, onde, problema in problemas:
            print(f"  linha {linha}, {nome}, {onde}: {problema}")
    try:
        destino = gerar(turma, alunos, problemas)
    except PermissionError:
        print("\nNão consegui salvar: o boletim está aberto no Excel? Feche e rode de novo.")
        return
    print(f"\nBoletim salvo em: {destino}")


if __name__ == "__main__":
    main()
```

### Como ele está organizado

| Função | Faz | Lê/escreve arquivo? |
|---|---|---|
| `converter_nota()` | Limpa uma nota ([aula 04](04_juntar_e_limpar.md#converter_nota-tratar-sem-esconder)) | Não |
| `arredondar()` | Arredonda como a escola | Não |
| `situacao()` | Aplica as regras | Não |
| `ler_turma()` | Lê a planilha e junta os problemas | Lê |
| `calcular()` | Média, frequência e situação de cada aluno | Não |
| `gerar()` | Monta e salva o boletim | Escreve |
| `main()` | Chama tudo na ordem e mostra o resumo no terminal | |

Separar **ler**, **calcular** e **gravar** em funções diferentes facilita testar (as funções do meio não precisam de arquivo nenhum) e reaproveitar (o Módulo 05 vai usar `ler_turma()` e `calcular()` na Secretaria automática).

## Rodando

```text
> python boletim.py
Ana Souza          média  8.1  frequência  95%  Aprovado
Bruno Lima         média  5.5  frequência  88%  Recuperação
Carla Mendes       média  9.5  frequência 100%  Aprovado
Diego Rocha        média  4.3  frequência  85%  Recuperação
Elisa Prado        média  7.3  frequência  98%  Aprovado
Felipe Torres      média    -  frequência  92%  Pendente
Gabriela Nunes     média  3.3  frequência  69%  Reprovado
Heitor Alves       média  8.3  frequência  99%  Aprovado
Isabela Costa      média  6.1  frequência  90%  Aprovado
João Pedro Melo    média    -  frequência  96%  Pendente
Larissa Freitas    média  5.5  frequência  72%  Reprovado
Mateus Ribeiro     média  7.8  frequência  94%  Aprovado

⚠ 2 problema(s) na planilha: veja a aba 'Problemas'.
  linha 7, Felipe Torres, 4º bim: nota não lançada
  linha 11, João Pedro Melo, 4º bim: fora de 0 a 10: 11

Boletim salvo em: treino_planilhas\saida\boletim_1A_2026-11-08.xlsx
```

Repare:

- A **Elisa** tem média normal: o `"7,5"` foi convertido com segurança.
- A **Larissa** tem média 5,5 (seria recuperação), mas está **reprovada por falta** (72% de frequência).
- **Felipe** e **João Pedro** ficam **Pendentes**, com a linha da planilha para a secretaria corrigir. O script não inventou nota nenhuma.

No Excel, a aba **Resumo** mostra: 6 aprovados, 2 em recuperação, 2 pendentes, 2 reprovados e a média da turma (**6,6**, calculada só com quem tem média).

---

## ⚠️ Erros comuns

- **Usar `round()`** para a média que decide a situação.
- **Esquecer a frequência** e aprovar quem tem nota boa mas faltou demais.
- **Dar nota zero** para a nota não lançada: o aluno seria reprovado por um erro da planilha.
- **Rodar com o boletim aberto no Excel**: o script avisa (`PermissionError`) e não grava.
- **Mudar as regras no meio do código** em vez de nas constantes.

---

## Exercícios

### Básico (fixação)

A escola mudou a média de aprovação para **7,0** e a de recuperação para **5,0**. Mude o script e diga quais alunos da 1A mudam de situação.

<!-- gabarito -->
??? success "Gabarito — Básico"
    Basta mudar as constantes do começo do `boletim.py`:

    ```python
    MEDIA_APROVACAO = 7.0
    MEDIA_RECUPERACAO = 5.0
    FREQUENCIA_MINIMA = 0.75  # 75% de presença
    ```

    Mudam: **Isabela** (6,1) passa de Aprovada para **Recuperação**; **Diego** (4,3) passa de Recuperação para **Reprovado**. Os outros continuam iguais (Elisa, com 7,3, segue aprovada).

### Intermediário (aplicação)

Escreva um script separado que leia o **boletim gerado** (a aba Boletim) e mostre as **3 maiores médias** da turma, como um "quadro de honra".

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```python
    from pathlib import Path

    from openpyxl import load_workbook

    boletim = sorted((Path("treino_planilhas") / "saida").glob("boletim_1A_*.xlsx"))[-1]
    aba = load_workbook(boletim)["Boletim"]

    alunos = [(nome, media) for _, nome, *_, media, _, _ in aba.iter_rows(min_row=2, values_only=True)
              if media is not None]
    podio = sorted(alunos, key=lambda par: par[1], reverse=True)[:3]
    for posicao, (nome, media) in enumerate(podio, start=1):
        print(f"{posicao}º {nome} ({media:.1f})")
    ```

    Resultado: 1º Carla Mendes (9,5), 2º Heitor Alves (8,3), 3º Ana Souza (8,1). O `*_` no meio "pula" as quatro notas: da linha, só interessam o nome (2ª coluna) e a média (7ª).

### Avançado (desafio)

Gere um boletim para **cada** planilha da pasta `treino_planilhas/turmas`, **reaproveitando** as funções do `boletim.py` com `import` (sem copiar o código).

<!-- gabarito -->
??? success "Gabarito — Avançado"
    Salve como `boletins_de_todas.py`, na mesma pasta do `boletim.py`:

    ```python
    from pathlib import Path

    from boletim import calcular, gerar, ler_turma

    for arquivo in sorted((Path("treino_planilhas") / "turmas").glob("notas_*.xlsx")):
        turma, aulas, alunos, problemas = ler_turma(arquivo)
        calcular(alunos, aulas)
        destino = gerar(turma, alunos, problemas)
        print(f"{turma}: {len(alunos)} alunos, {len(problemas)} problema(s) -> {destino.name}")
    ```

    O `import` funciona porque o `boletim.py` está na mesma pasta, e o `main()` dele **não** roda ao importar, graças ao `if __name__ == "__main__":` ([Módulo 01](../modulo_01_arquivos_e_pastas/01_o_que_vale_automatizar.md#a-pasta-de-treino)). Saem três boletins: `boletim_1A_...`, `boletim_1B_...` e `boletim_1C_...`.

---

## 💡 Resumo

- **Ler** ➔ **limpar** ➔ **calcular** ➔ **gerar**, cada parte numa função.
- Regras da escola em **constantes**; problemas da planilha listados numa aba, nunca "chutados".
- **`Decimal` com `ROUND_HALF_UP`** para arredondar como a escola; o `round()` do Python arredonda empates para o par.
- Funções bem separadas podem ser **importadas** por outros scripts.

## ➡️ Próximo passo

**[Módulo 03 — Documentos e PDFs](../modulo_03_documentos_e_pdfs/index.md)**: preencher modelos do Word, gerar PDFs e fazer os certificados da turma a partir da planilha.
