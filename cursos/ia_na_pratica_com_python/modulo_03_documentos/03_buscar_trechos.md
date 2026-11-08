# 03 — Buscar os trechos certos

> **Curso:** IA na prática com Python  
> **Módulo:** 03 — IA com os seus documentos  
> **Tempo estimado:** 1 h 30 min  

---

## 🎯 Objetivos

Ao final desta aula, você será capaz de:

- Buscar os trechos mais relevantes para uma pergunta, **sem IA**, contando palavras em comum.
- Dar mais valor às palavras **raras** no documento.
- Reconhecer os dois limites da busca por palavras: **sinônimos** e **coincidências**.

## Pré-requisitos

- [Aula 02](02_dividir_em_trechos.md): os trechos do regulamento.

---

## A ideia

Para "Quantos livros posso pegar na biblioteca?", o trecho certo é o que tem **livros** e **biblioteca**. A busca:

1. **Limpa** a pergunta e cada trecho: minúsculas, sem acentos, sem palavras vazias ("quantos", "posso", "na"), plural simples cortado (`livros` ➔ `livro`).
2. Para cada trecho, **soma pontos** pelas palavras da pergunta que ele tem.
3. Palavras **raras** valem mais: "biblioteca" aparece em 1 trecho e vale muito; "aluno" aparece em vários e vale pouco.
4. Devolve os **3** trechos com mais pontos.

```python title="buscar.py"
"""Busca os trechos mais parecidos com a pergunta, contando palavras em comum (sem IA)."""
import math
import re
import unicodedata
from collections import Counter

VAZIAS = set("""a o as os um uma de da do das dos em na no nas nos por para pra com sem e ou que se
qual quais quando como onde quanto quantos posso pode podem meu minha ser ter tem é são foi ao à
eu voce você isso esse essa este esta mais menos""".split())


def palavras(texto: str) -> list[str]:
    """Minúsculas, sem acento, sem palavras vazias e com o plural simples cortado (livros -> livro)."""
    sem_acento = unicodedata.normalize("NFKD", texto.lower()).encode("ascii", "ignore").decode()
    resultado = []
    for p in re.findall(r"[a-z0-9]+", sem_acento):
        if p in VAZIAS or len(p) < 2:
            continue
        if len(p) > 4 and p.endswith("s"):
            p = p[:-1]
        resultado.append(p)
    return resultado


def buscar(pergunta: str, trechos: list, quantos: int = 3) -> list[tuple[float, object]]:
    """[(pontos, trecho)] dos mais relevantes. Palavras raras no documento valem mais."""
    documentos = [Counter(palavras(t.titulo + " " + t.texto)) for t in trechos]
    em_quantos = Counter(p for doc in documentos for p in doc)
    total = len(trechos)
    termos = set(palavras(pergunta))
    resultado = []
    for trecho, doc in zip(trechos, documentos):
        pontos = sum(math.log(1 + total / em_quantos[p]) for p in termos if p in doc)
        if pontos > 0:
            resultado.append((round(pontos, 2), trecho))
    resultado.sort(key=lambda par: par[0], reverse=True)
    return resultado[:quantos]
```

O peso de cada palavra é `log(1 + total / em_quantos)`: com 9 trechos, uma palavra que está em **1** só vale `log(10) ≈ 2,3`; uma que está em **9** vale `log(2) ≈ 0,7`. É uma versão simplificada de técnicas clássicas de busca (TF-IDF, BM25).

## Testando

```text
Quantos livros posso pegar na biblioteca? -> [(6.91, 'T8', '8. Biblioteca')]
Perdi a prova, o que faço?                -> [(2.3, 'T5', '5. Segunda chamada')]
Posso usar o celular na aula?             -> [(3.33, 'T6', '6. Celular'), (2.3, 'T7', '7. Uniforme'), (1.03, 'T1', '1. Horários')]
A que horas fecha o portão?               -> [(4.01, 'T1', '1. Horários'), (2.3, 'T5', '5. Segunda chamada'), (1.7, 'T2', '2. Atrasos')]
Qual a nota para passar de ano?           -> []
Tem cantina na escola?                    -> [(2.3, 'T7', '7. Uniforme')]
```

### Os dois limites

**1. Sinônimos (falso negativo).** "Qual a **nota** para **passar** de ano?" não acha **nada**: o regulamento diz "**média** para **aprovação**". Nenhuma palavra em comum. A busca por palavras não sabe que "passar" e "ser aprovado" são a mesma ideia.

**2. Coincidências (falso positivo).** "Tem **cantina** na **escola**?" acha o trecho do **uniforme**, só porque ele tem a palavra "escola" ("camiseta da escola"). O regulamento não fala de cantina.

!!! info "Como resolver"
    - **Falso positivo:** a próxima etapa ([aula 04](04_responder_com_fonte.md)) manda os trechos para a IA, que **lê** e diz "não encontrei" quando eles não respondem. E um **limite mínimo de pontos** descarta coincidências fracas.
    - **Falso negativo:** um pequeno dicionário de **sinônimos** do assunto resolve o comum (veja o desafio da [aula 05](05_projeto_tira_duvidas.md)). A solução mais completa são os ***embeddings***, que comparam o **significado** dos textos em vez das palavras: um assunto para quem quiser ir além do curso.

---

## ⚠️ Erros comuns

- **Não tirar as palavras vazias**: "o", "de", "que" combinam com todos os trechos.
- **Dar o mesmo peso a todas as palavras**: "aluno" (em todo lugar) passa a valer tanto quanto "biblioteca".
- **Confiar no primeiro resultado sempre**: às vezes ele é uma coincidência. Use um limite de pontos e deixe a IA conferir.
- **Esquecer os acentos**: "horário" e "horario" precisam ser a mesma palavra.

---

## Exercícios

### Básico (fixação)

Mostre as palavras que a `palavras()` tira de "Quantos livros posso pegar na Biblioteca?" e de "O aluno pode pegar até 2 livros por vez".

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```python
    from buscar import palavras

    pergunta = palavras("Quantos livros posso pegar na Biblioteca?")
    trecho = palavras("O aluno pode pegar até 2 livros por vez")
    print(pergunta)
    print(trecho)
    print("em comum:", sorted(set(pergunta) & set(trecho)))
    ```

    Pergunta: `['livro', 'pegar', 'biblioteca']`. Trecho: `['aluno', 'pegar', 'ate', 'livro', 'vez']` (o `2` some por ter só 1 caractere). Em comum: `livro` e `pegar`.

### Intermediário (aplicação)

Para a pergunta "Posso usar o celular na aula?", mostre os pontos dos 3 trechos e explique por que o **Uniforme** aparece em segundo.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```python
    from pathlib import Path

    from buscar import buscar, palavras
    from ler_documento import ler_paginas
    from trechos import dividir

    trechos = dividir(ler_paginas(Path("treino_docs") / "regulamento_escola.pdf"))
    achados = buscar("Posso usar o celular na aula?", trechos)
    for pontos, trecho in achados:
        comuns = sorted(set(palavras("Posso usar o celular na aula?")) & set(palavras(trecho.titulo + " " + trecho.texto)))
        print(pontos, trecho.titulo, comuns)
    ```

    O **Celular** tem `celular` e `aula` (o texto diz "uso", e não "usar"). O **Uniforme** tem só `usar` ("deve usar tênis"), que aparece em poucos trechos e por isso vale bastante. É uma coincidência: o limite de pontos e a IA ([aula 04](04_responder_com_fonte.md)) cuidam disso.

### Avançado (desafio)

Teste a busca com 5 perguntas **suas** sobre o regulamento, escritas do jeito que um aluno escreveria (com gírias e erros). Quantas encontram a seção certa em primeiro lugar?

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```python
    from pathlib import Path

    from buscar import buscar
    from ler_documento import ler_paginas
    from trechos import dividir

    trechos = dividir(ler_paginas(Path("treino_docs") / "regulamento_escola.pdf"))
    perguntas = {
        "posso ficar com o livro mais tempo?": "8. Biblioteca",
        "q horas abre a escola de manha": "1. Horários",
        "dá pra mexer no cel na aula?": "6. Celular",
        "tenho q ir de camiseta da escola?": "7. Uniforme",
        "quanto preciso tirar pra passar": "4. Avaliação",
    }
    acertos = 0
    for pergunta, esperado in perguntas.items():
        achados = buscar(pergunta, trechos)
        primeiro = achados[0][1].titulo if achados else "(nada)"
        acertos += primeiro == esperado
        print(f"{primeiro == esperado!s:5} {pergunta} -> {primeiro}")
    print(f"{acertos} de {len(perguntas)}")
    ```

    "q", "cel", "manha" e "tirar pra passar" mostram o limite das palavras: abreviações e sinônimos não batem. Por isso o tira-dúvidas da [aula 05](05_projeto_tira_duvidas.md) tem uma **avaliação** com perguntas de teste: medir antes de confiar.

---

## 💡 Resumo

- Busca por palavras: limpar, contar palavras em comum, valorizar as **raras**, pegar os 3 melhores.
- Limites: **sinônimos** (não acha) e **coincidências** (acha errado).
- Limite de pontos + IA conferindo + sinônimos do assunto resolvem a maior parte; *embeddings* são o próximo passo.

## ➡️ Próximo passo

**[04 — Responder só com base no documento](04_responder_com_fonte.md)**.
