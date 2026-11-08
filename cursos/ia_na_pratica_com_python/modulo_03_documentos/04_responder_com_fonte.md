# 04 — Responder só com base no documento

> **Curso:** IA na prática com Python  
> **Módulo:** 03 — IA com os seus documentos  
> **Tempo estimado:** 1 h 30 min  

---

## 🎯 Objetivos

Ao final desta aula, você será capaz de:

- Montar o pedido com os **trechos numerados** e a pergunta.
- Fazer a IA responder **só** com os trechos e dizer **"não encontrei"** quando eles não respondem.
- Exigir que a IA diga **quais trechos usou**, e conferir com código.
- Mostrar a **fonte** (título e página) junto com a resposta.

## Pré-requisitos

- [Aula 03](03_buscar_trechos.md): a busca.

---

## O pedido

A IA recebe os trechos que a busca achou, cada um com o seu **id**, a página e o título, e depois a pergunta:

```text
Trechos do regulamento:
[T8] (página 3, 8. Biblioteca) O aluno pode pegar até 2 livros por vez, pelo prazo de 7 dias. ...

Pergunta: Quantos livros posso pegar na biblioteca?
```

E responde em **JSON**, com três campos: `encontrou` (sim ou não), `resposta` e `trechos` (os ids que usou).

```python title="responder.py"
"""Responde a uma pergunta usando SÓ os trechos do documento, e diz de onde tirou a resposta."""
import json
import re

from buscar import buscar

INSTRUCOES = (
    "Você responde dúvidas de alunos sobre o regulamento da escola. Use SOMENTE os trechos fornecidos. "
    "Se a resposta não estiver nos trechos, marque encontrou=false e não invente. "
    "Responda em português do Brasil, em até 3 frases simples. Em 'trechos', liste os ids usados (ex.: T8)."
)
ESQUEMA = {
    "type": "object",
    "properties": {
        "encontrou": {"type": "boolean"},
        "resposta": {"type": "string"},
        "trechos": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["encontrou", "resposta", "trechos"],
}
NAO_ENCONTREI = "Não encontrei essa informação no regulamento. Procure a secretaria."
PONTOS_PARA_IA = 2.0   # trechos com menos pontos nem vão para a IA
PONTOS_SEM_IA = 3.0    # sem IA para julgar, a regra precisa ser mais exigente


def montar_entrada(pergunta: str, achados: list) -> str:
    blocos = [f"[{t.id}] (página {t.pagina}, {t.titulo}) {t.texto}" for _, t in achados]
    return "Trechos do regulamento:\n" + "\n".join(blocos) + f"\n\nPergunta: {pergunta}"


def citar(trechos_usados: list) -> str:
    return "; ".join(f"{t.titulo}, página {t.pagina}" for t in trechos_usados)


def responder(cliente, modelo: str, pergunta: str, trechos: list) -> dict:
    """{'resposta', 'fonte', 'encontrou'}. A IA só vê os trechos que a busca achou."""
    achados = [par for par in buscar(pergunta, trechos) if par[0] >= PONTOS_PARA_IA]
    if not achados:  # nem chama a IA: economiza e não dá chance de inventar
        return {"encontrou": False, "resposta": NAO_ENCONTREI, "fonte": ""}
    resposta = cliente.interactions.create(
        model=modelo,
        input=montar_entrada(pergunta, achados),
        system_instruction=INSTRUCOES,
        generation_config={"thinking_level": "low"},
        response_format={"type": "text", "mime_type": "application/json", "schema": ESQUEMA},
    )
    try:
        dados = json.loads(resposta.output_text)
    except json.JSONDecodeError:
        return {"encontrou": False, "resposta": NAO_ENCONTREI, "fonte": "(resposta da IA em formato inválido)"}
    por_id = {t.id: t for _, t in achados}
    usados = [por_id[i] for i in dados.get("trechos", []) if i in por_id]  # ignora ids inventados
    if not dados.get("encontrou") or not usados:
        return {"encontrou": False, "resposta": NAO_ENCONTREI, "fonte": ""}
    return {"encontrou": True, "resposta": dados["resposta"].strip(), "fonte": citar(usados)}


def responder_simulado(pergunta: str, trechos: list) -> dict:
    """Sem IA: devolve as primeiras frases do trecho mais relevante, com a fonte."""
    achados = [par for par in buscar(pergunta, trechos) if par[0] >= PONTOS_SEM_IA]
    if not achados:
        return {"encontrou": False, "resposta": NAO_ENCONTREI, "fonte": ""}
    melhor = achados[0][1]
    frases = re.split(r"(?<=[.!?])\s+", melhor.texto)
    return {"encontrou": True, "resposta": " ".join(frases[:2]), "fonte": citar([melhor])}
```

### As quatro proteções contra respostas inventadas

| Proteção | Onde | O que evita |
|---|---|---|
| **Só os trechos achados vão para a IA** | `montar_entrada()` | A IA "completar" com o que acha que sabe |
| **Sem trecho com pontos suficientes, nem chama a IA** | `PONTOS_PARA_IA` | Gastar tokens e dar chance de inventar |
| **"encontrou=false" se não estiver nos trechos** | instruções + esquema | Resposta plausível sobre o que o documento não diz |
| **Ids conferidos pelo código** | `usados = [...] if i in por_id` | A IA citar um trecho que não recebeu (`T99`) |

Se a IA disser que encontrou mas não citar nenhum trecho **válido**, o programa responde "Não encontrei": **sem fonte, sem resposta**.

```text
>>> responder(ClienteFalso('{"encontrou": true, "resposta": "Até 2 livros, por 7 dias.", "trechos": ["T8", "T99"]}'), ...)
{'encontrou': True, 'resposta': 'Até 2 livros, por 7 dias.', 'fonte': '8. Biblioteca, página 3'}
```

O `T99` (inventado) é **ignorado**; a fonte mostra só o trecho que existe.

### Dois limites de pontos

- **`PONTOS_PARA_IA = 2.0`**: trechos com uma única palavra rara em comum já vão para a IA, porque **ela lê e decide**. Assim, "Perdi a **prova**, o que faço?" chega no trecho da Segunda chamada, e "Tem **cantina** na escola?" chega no do Uniforme, mas a IA responde `encontrou=false`.
- **`PONTOS_SEM_IA = 3.0`**: sem IA para julgar, a regra precisa ser mais exigente. O custo: no modo simulado, "Perdi a prova" fica sem resposta (só uma palavra em comum). É a troca clássica entre **responder errado** e **deixar de responder**; num regulamento, deixar de responder (e mandar para a secretaria) é o erro menos grave.

---

## ⚠️ Erros comuns

- **Mandar o documento inteiro** e confiar que a IA "vai achar": mais tokens e mais chance de misturar informações.
- **Instruções sem a saída "não sei"**: a IA tende a responder algo, mesmo sem base.
- **Mostrar a resposta sem a fonte**: o aluno não tem como conferir.
- **Não conferir os ids citados**: uma fonte inventada parece verdadeira.

---

## Exercícios

### Básico (fixação)

Use o `responder_simulado()` com três perguntas: uma sobre a **biblioteca**, uma sobre o **laboratório** e uma sobre **estacionamento**. Mostre resposta e fonte.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```python
    from pathlib import Path

    from ler_documento import ler_paginas
    from responder import responder_simulado
    from trechos import dividir

    trechos = dividir(ler_paginas(Path("treino_docs") / "regulamento_escola.pdf"))
    perguntas = ["Quantos livros posso pegar na biblioteca?",
                 "Posso usar o laboratório de informática fora do horário?",
                 "Onde fica o estacionamento?"]
    resultados = [responder_simulado(p, trechos) for p in perguntas]
    for r in resultados:
        print(r["resposta"], "|", r["fonte"] or "(sem fonte)")
    ```

    Biblioteca e laboratório são respondidos com a fonte; estacionamento recebe "Não encontrei essa informação no regulamento. Procure a secretaria."

### Intermediário (aplicação)

Com o `ClienteFalso`, teste o `responder()` em três situações: a IA cita um trecho válido; a IA diz `encontrou=true` mas cita só `T99`; a IA devolve um texto que não é JSON.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```python
    import json
    from pathlib import Path

    from cliente_falso import ClienteFalso
    from ler_documento import ler_paginas
    from responder import responder
    from trechos import dividir

    trechos = dividir(ler_paginas(Path("treino_docs") / "regulamento_escola.pdf"))
    pergunta = "Quantos livros posso pegar na biblioteca?"
    respostas = [
        json.dumps({"encontrou": True, "resposta": "Até 2 livros.", "trechos": ["T8"]}),
        json.dumps({"encontrou": True, "resposta": "Até 5 livros.", "trechos": ["T99"]}),
        "Você pode pegar até 2 livros.",
    ]
    resultados = [responder(ClienteFalso(r), "gemini-3.8-flash", pergunta, trechos) for r in respostas]
    for r in resultados:
        print(r)
    ```

    Só o primeiro é aceito, com a fonte "8. Biblioteca, página 3". O segundo (fonte inventada) e o terceiro (fora do formato) viram "Não encontrei". Melhor dizer "não sei" do que mostrar "até 5 livros" sem base.

### Avançado (desafio)

Prove que, para uma pergunta **fora** do documento, a IA **nem é chamada**: conte os pedidos do `ClienteFalso` para "Qual é a senha do Wi-Fi?".

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```python
    from pathlib import Path

    from cliente_falso import ClienteFalso
    from ler_documento import ler_paginas
    from responder import responder
    from trechos import dividir

    trechos = dividir(ler_paginas(Path("treino_docs") / "regulamento_escola.pdf"))
    falso = ClienteFalso("não deveria ser usado")
    resultado = responder(falso, "gemini-3.8-flash", "Qual é a senha do Wi-Fi?", trechos)
    print(resultado["encontrou"], len(falso.pedidos))
    ```

    `False 0`: nenhuma palavra da pergunta está no regulamento, então a busca não acha nada e o programa responde "Não encontrei" **sem gastar** nenhum token. Perguntas fora do assunto custam zero.

---

## 💡 Resumo

- A IA recebe **só** os trechos achados, com **id**, página e título, e responde em JSON (`encontrou`, `resposta`, `trechos`).
- O código **confere** os ids: fonte inventada = "não encontrei".
- Sem trechos suficientes, **nem chama** a IA. Com IA, limite de pontos mais baixo; sem IA, mais alto.
- Toda resposta vem com a **fonte**.

## ➡️ Próximo passo

**[05 — Projeto do módulo: tira-dúvidas do regulamento](05_projeto_tira_duvidas.md)**.
