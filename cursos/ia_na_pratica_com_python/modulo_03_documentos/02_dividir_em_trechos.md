# 02 — Dividir em trechos

> **Curso:** IA na prática com Python  
> **Módulo:** 03 — IA com os seus documentos  
> **Tempo estimado:** 1 h  

---

## 🎯 Objetivos

Ao final desta aula, você será capaz de:

- Explicar por que o documento é dividido em **trechos** antes de ir para a IA.
- Dividir pelas **seções** do documento (títulos numerados), guardando **título** e **página**.
- Juntar as linhas quebradas do PDF e dividir seções grandes demais.

## Pré-requisitos

- [Aula 01](01_ler_documentos.md): `ler_paginas()` e o regulamento de treino.

---

## Por que trechos?

| Mandar o documento inteiro | Mandar só os trechos certos |
|---|---|
| Muitos tokens a cada pergunta (custo e limite) | Poucos tokens |
| A informação certa se perde no meio de muita coisa | A IA foca no que importa |
| Não dá para dizer de onde veio a resposta | Cada trecho tem **título e página**: dá para **citar** |

Um bom trecho é um pedaço que **faz sentido sozinho**. Num regulamento, a unidade natural é a **seção** ("8. Biblioteca"): ela trata de um assunto só.

## O divisor

```python title="trechos.py"
"""Divide o documento em trechos (pedaços com título e página), prontos para busca."""
import re
from dataclasses import dataclass

TITULO = re.compile(r"^\d+\.\s+\S")  # "4. Avaliação", "8. Biblioteca"
TAMANHO_MAXIMO = 900                 # caracteres por trecho


@dataclass
class Trecho:
    id: str
    pagina: int
    titulo: str
    texto: str


def juntar_linhas(texto: str) -> str:
    """O PDF quebra as linhas no meio das frases: junta tudo com espaços."""
    return re.sub(r"\s+", " ", texto).strip()


def dividir(paginas: list[str]) -> list[Trecho]:
    """Um trecho por seção (título numerado). Seção grande demais é dividida em partes."""
    secoes, atual = [], None
    for numero, pagina in enumerate(paginas, start=1):
        for linha in pagina.splitlines():
            if TITULO.match(linha.strip()):
                atual = {"pagina": numero, "titulo": linha.strip(), "linhas": []}
                secoes.append(atual)
            elif atual is not None:
                atual["linhas"].append(linha)
    if not secoes:  # documento sem títulos numerados: um "título" por página
        secoes = [{"pagina": n, "titulo": f"Página {n}", "linhas": p.splitlines()} for n, p in enumerate(paginas, 1)]

    trechos = []
    for secao in secoes:
        texto = juntar_linhas(" ".join(secao["linhas"]))
        partes = [texto[i:i + TAMANHO_MAXIMO] for i in range(0, len(texto), TAMANHO_MAXIMO)] or [""]
        for parte in partes:
            if parte:
                trechos.append(Trecho(f"T{len(trechos) + 1}", secao["pagina"], secao["titulo"], parte))
    return trechos
```

```text
T1 1 1. Horários | As aulas do turno da manhã começam às 7h10 e terminam às 12h
T2 1 2. Atrasos | O aluno que chegar depois do fechamento do portão entra na s
T3 1 3. Frequência | O aluno precisa de pelo menos 75% de presença nas aulas de c
T4 2 4. Avaliação | A média para aprovação é 6,0 em cada disciplina. O aluno com
...
T9 3 9. Laboratório de informática | O laboratório pode ser usado fora do horário de aula com age
```

### Como funciona

1. **Título numerado** (`TITULO`, uma expressão regular) começa uma seção nova, guardando a **página** em que ela começa.
2. As linhas seguintes vão para a seção atual; **`juntar_linhas()`** troca quebras de linha e espaços repetidos por um espaço só.
3. Seção maior que **`TAMANHO_MAXIMO`** (900 caracteres) é cortada em partes, cada uma com o mesmo título. Partes menores ajudam a busca e economizam tokens.
4. Documento **sem** títulos numerados: cada página vira uma seção ("Página 2").
5. Cada trecho ganha um **id** (`T1`, `T2`...): é com ele que a IA vai dizer quais trechos usou.

!!! tip "`@dataclass` para os trechos"
    `Trecho` guarda `id`, `pagina`, `titulo` e `texto` com nomes, como o `Aluno` da [Secretaria automática](../../automacao_com_python/modulo_05_projeto_final/02_pacote_e_dados.md). `trecho.titulo` é mais claro do que `trecho[2]`.

!!! warning "O corte por tamanho é simples"
    Cortar a cada 900 caracteres pode partir uma frase no meio. Para documentos longos de verdade, corte nos **pontos finais** mais próximos do limite (veja o desafio) ou mantenha uma pequena **sobreposição** entre as partes.

---

## ⚠️ Erros comuns

- **Trechos grandes demais** (o documento inteiro): a busca perde o sentido e a IA recebe tokens demais.
- **Trechos pequenos demais** (uma linha): perdem o contexto ("por mais 7 dias" sozinho não diz de quê).
- **Perder a página e o título**: sem eles, não há citação.
- **Esquecer de juntar as linhas** do PDF: palavras partidas atrapalham a busca.

---

## Exercícios

### Básico (fixação)

Mostre o **título** e a **página** de cada trecho do regulamento e o tamanho do maior trecho.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```python
    from pathlib import Path

    from ler_documento import ler_paginas
    from trechos import dividir

    trechos = dividir(ler_paginas(Path("treino_docs") / "regulamento_escola.pdf"))
    for t in trechos:
        print(f"{t.id:4} página {t.pagina}  {t.titulo}")
    maior = max(len(t.texto) for t in trechos)
    print("maior trecho:", maior, "caracteres")
    ```

    São 9 trechos (um por seção); o maior é o da **Biblioteca**, com 244 caracteres, bem abaixo do limite de 900.

### Intermediário (aplicação)

Divida o `faq.txt` da aula 01 (três perguntas numeradas). Quantos trechos saem e em que "página"?

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```python
    from pathlib import Path

    from ler_documento import ler_paginas
    from trechos import dividir

    Path("faq.txt").write_text(
        "1. Onde fica a secretaria?\nNo térreo, ao lado da biblioteca.\n"
        "2. Tem armário para alunos?\nSim, com cadeado próprio.\n"
        "3. Posso trazer lanche?\nSim, e há bebedouros em todos os andares.\n",
        encoding="utf-8",
    )
    trechos = dividir(ler_paginas(Path("faq.txt")))
    print([(t.titulo, t.pagina, t.texto) for t in trechos])
    ```

    3 trechos, todos na página 1, cada um com a pergunta como título e a resposta como texto: o formato perfeito para um tira-dúvidas.

### Avançado (desafio)

Escreva `dividir_em_frases(texto, maximo)`, que corta um texto longo em partes de até `maximo` caracteres **sem partir frases** (corta no último ponto final antes do limite). Teste com uma seção de 3 frases e `maximo=120`.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```python
    import re


    def dividir_em_frases(texto: str, maximo: int) -> list[str]:
        frases = re.split(r"(?<=[.!?])\s+", texto.strip())
        partes, atual = [], ""
        for frase in frases:
            if atual and len(atual) + 1 + len(frase) > maximo:
                partes.append(atual)
                atual = frase
            else:
                atual = f"{atual} {frase}".strip()
        if atual:
            partes.append(atual)
        return partes


    texto = ("O aluno pode pegar até 2 livros por vez, pelo prazo de 7 dias. O empréstimo pode ser renovado uma vez. "
             "Quem atrasar a devolução fica sem novos empréstimos pelo mesmo número de dias do atraso.")
    partes = dividir_em_frases(texto, 120)
    for parte in partes:
        print(len(parte), parte)
    ```

    Saem 2 partes, cada uma terminando num ponto final. Uma frase **sozinha** maior que o limite vira uma parte maior (não é cortada): melhor um trecho um pouco grande do que uma frase sem sentido.

---

## 💡 Resumo

- Trechos economizam tokens, focam a IA e permitem **citar a fonte**.
- Divida pelas **seções** do documento; guarde **id**, **título** e **página**.
- Junte as linhas quebradas; divida seções grandes, de preferência nos pontos finais.

## ➡️ Próximo passo

**[03 — Buscar os trechos certos](03_buscar_trechos.md)**.
