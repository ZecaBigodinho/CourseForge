# 04 — Regras ou IA?

> **Curso:** IA na prática com Python  
> **Módulo:** 02 — Tarefas úteis  
> **Tempo estimado:** 1 h  

---

## 🎯 Objetivos

Ao final desta aula, você será capaz de:

- Reconhecer tarefas em que **não** se deve usar IA.
- Comparar **regras** e **IA** em custo, velocidade, previsibilidade e flexibilidade.
- Montar um classificador **híbrido**: regras para o óbvio, IA só para o duvidoso.

## Pré-requisitos

- Aulas [01](01_classificar_mensagens.md) a [03](03_reescrever_com_tom.md) deste módulo.

---

## Quando **não** usar IA

| Tarefa | Use | Por quê |
|---|---|---|
| Somar o total de um pedido, calcular média | **Código** | A IA pode errar contas; o Python não erra |
| Conferir se um CPF ou e-mail tem formato válido | **Código** (regra) | Há regras exatas; a IA "acha" |
| Ordenar, filtrar, contar | **Código** | Mais rápido, de graça e sempre igual |
| Decidir algo sobre **uma pessoa** (aprovar, reprovar, contratar) | **Pessoa** | Decisão com consequência exige responsabilidade e explicação |
| Informação que precisa estar **atualizada** (preço de hoje, horário de ônibus) | **Fonte oficial** | O modelo não sabe o que mudou depois do treino |
| Entender texto livre, variado, com erros de digitação | **IA** | É onde regras falham |
| Reescrever, resumir, classificar por **sentido** | **IA** | Idem |

!!! tip "Pergunta-teste"
    *"Dá para escrever a regra num `if` e ela vale sempre?"* Se sim, use código. A IA entra quando a regra seria uma lista sem fim de exceções.

## Regras × IA

| | Regras (código) | IA |
|---|---|---|
| Custo | Zero | Tokens (cota ou dinheiro) |
| Velocidade | Instantânea | Segundos por pedido |
| Previsível | Sempre a mesma resposta | Pode variar |
| Frases novas | Quebra | Lida bem |
| Explicação | Dá para ler a regra | Difícil saber "por quê" |

## O melhor dos dois: híbrido

```python title="regras_ou_ia.py"
"""Classificador híbrido: regras simples primeiro; a IA só para o que as regras não resolvem."""
from classificar import PALAVRAS, classificar, sem_acento


def pelas_regras(mensagem: str) -> str | None:
    """Categoria quando EXATAMENTE uma regra combina; None quando nenhuma ou mais de uma (caso duvidoso)."""
    texto = sem_acento(mensagem)
    achadas = [c for c, palavras in PALAVRAS.items() if any(sem_acento(p) in texto for p in palavras)]
    return achadas[0] if len(achadas) == 1 else None


def classificar_hibrido(mensagens: list[str], cliente, modelo: str) -> tuple[list[str], int]:
    """Devolve (categorias, quantas chamadas à IA foram feitas)."""
    categorias, chamadas = [], 0
    for mensagem in mensagens:
        categoria = pelas_regras(mensagem)
        if categoria is None:
            categoria = classificar(cliente, modelo, mensagem)
            chamadas += 1
        categorias.append(categoria)
    return categorias, chamadas
```

A ideia: as regras resolvem o que é **óbvio** (só uma categoria combina); a IA só é chamada quando **nenhuma** ou **mais de uma** regra combina.

Nas 10 mensagens de treino:

```text
>>> [pelas_regras(m) for m in mensagens]
['pedido', 'dúvida', 'reclamação', 'elogio', None, 'dúvida', 'dúvida', None, 'pedido', None]
```

- A **5** ("Preciso de 50 coxinhas ... dá?") combina com **pedido** e **dúvida**: duvidosa.
- A **8** ("veio sem recheio, quero meu dinheiro de volta") combina com **reclamação** e **pedido**: duvidosa.
- A **10** ("kkkkk") não combina com nada.

Resultado: **3 chamadas** à IA em vez de 10. Numa padaria com 300 mensagens por semana, a economia de cota e de tempo é grande, e as decisões fáceis ficam **previsíveis**.

---

## ⚠️ Erros comuns

- **IA para tudo** "porque é mais moderno": mais lento, mais caro e menos previsível.
- **Regras para tudo**: cada frase nova vira mais um `if`, até ninguém entender o código.
- **IA fazendo contas** que vão para documento oficial.
- **IA decidindo sobre pessoas** sem revisão humana.

---

## Exercícios

### Básico (fixação)

Para cada tarefa, responda **código**, **IA** ou **pessoa**: (a) calcular o troco; (b) separar e-mails de clientes por assunto; (c) decidir quem ganha uma bolsa de estudos; (d) conferir se uma data está no formato dd/mm/aaaa; (e) resumir as reclamações da semana.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```python
    respostas = {
        "calcular o troco": "código",
        "separar e-mails por assunto": "IA",
        "decidir quem ganha uma bolsa": "pessoa",
        "conferir o formato da data": "código",
        "resumir as reclamações da semana": "IA",
    }
    for tarefa, quem in respostas.items():
        print(f"{tarefa:34} -> {quem}")
    ```

    A bolsa é decisão sobre **pessoas**: a IA pode, no máximo, ajudar a organizar documentos, e a decisão (com critérios claros e explicáveis) é de uma comissão.

### Intermediário (aplicação)

Rode o `classificar_hibrido()` com as mensagens de treino e o `ClienteFalso` respondendo `"outro"`. Quantas chamadas foram feitas? Quais mensagens foram para a IA?

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```python
    import csv

    from cliente_falso import ClienteFalso
    from regras_ou_ia import classificar_hibrido

    with open("mensagens_exemplo.csv", encoding="utf-8") as arq:
        mensagens = [linha["mensagem"] for linha in csv.DictReader(arq, delimiter=";")]
    falso = ClienteFalso("outro")
    categorias, chamadas = classificar_hibrido(mensagens, falso, "gemini-3.8-flash")
    foram_para_ia = [p["input"][:30] for p in falso.pedidos]
    print(chamadas, foram_para_ia)
    ```

    **3** chamadas: as mensagens 5, 8 e 10. O `falso.pedidos` mostra exatamente o que foi mandado, e é assim que se confere a economia sem gastar nada.

### Avançado (desafio)

Escreva a função `total_pedido(itens)` que calcula o total de um pedido com **código** (nunca com IA), a partir de uma tabela de preços inventada. Itens fora da tabela devem aparecer numa lista de "sem preço", em vez de serem ignorados.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```python
    from decimal import Decimal

    PRECOS = {"bolo de fubá": Decimal("28.00"), "coxinha": Decimal("6.50"), "torta de frango": Decimal("45.00")}


    def total_pedido(itens: list[tuple[str, int]]) -> tuple[Decimal, list[str]]:
        total, sem_preco = Decimal("0"), []
        for produto, quantidade in itens:
            if produto in PRECOS:
                total += PRECOS[produto] * quantidade
            else:
                sem_preco.append(produto)
        return total, sem_preco


    total, sem_preco = total_pedido([("bolo de fubá", 2), ("coxinha", 50), ("pão de mel", 3)])
    print(total, sem_preco)
    ```

    Total `381.00` e `['pão de mel']`. Dinheiro em **`Decimal`** (sem erros de arredondamento, como no [Automação com Python](../../automacao_com_python/modulo_02_planilhas/05_projeto_boletim.md#o-arredondamento-um-bug-que-o-teste-achou)), e o item desconhecido **aparece**: um programa que some com itens é pior do que um que avisa.

---

## 💡 Resumo

- **Código** para contas, formatos e regras exatas; **pessoa** para decisões sobre gente; **IA** para texto variado.
- Regras: grátis, rápidas, previsíveis e frágeis. IA: flexível, com custo e variação.
- **Híbrido**: regras no óbvio, IA no duvidoso. Nas mensagens de treino, 3 chamadas em vez de 10.

## ➡️ Próximo passo

**[05 — Projeto do módulo: triagem de mensagens](05_projeto_triagem.md)**.
