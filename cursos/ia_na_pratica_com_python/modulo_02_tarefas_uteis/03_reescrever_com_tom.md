# 03 — Reescrever com tom definido

> **Curso:** IA na prática com Python  
> **Módulo:** 02 — Tarefas úteis  
> **Tempo estimado:** 1 h  

---

## 🎯 Objetivos

Ao final desta aula, você será capaz de:

- Usar a IA para **reescrever** um rascunho apressado numa resposta educada, no **tom** escolhido.
- Escrever instruções que **proíbem** acrescentar informações (preços, prazos, promessas).
- **Conferir** a resposta com código antes de mandar para o cliente.
- Manter uma **pessoa no controle**: a IA sugere, o atendente decide.

## Pré-requisitos

- [Aula 02](02_extrair_json.md): extrair dados e validar.

---

## A tarefa

O atendente escreve rápido, no meio do movimento: *"vamos trocar o sonho, é só passar no balcão"*. A IA transforma isso numa resposta educada, sem mudar o que foi decidido.

```python title="reescrever.py"
"""Transforma o rascunho apressado do atendente numa resposta educada, no tom escolhido."""
import re

TONS = {
    "cordial": "educado e acolhedor, sem exageros",
    "formal": "formal e respeitoso, sem gírias nem emojis",
    "descontraído": "simpático e próximo, com no máximo 1 emoji",
}
INSTRUCOES = (
    "Você reescreve respostas de atendentes de uma padaria para os clientes. Mantenha TODAS as "
    "informações do rascunho e não acrescente promessas, preços, prazos nem descontos que não estejam nele. "
    "Tom: {tom}. Máximo de 3 frases. Responda só com a mensagem pronta."
)
LIMITE_CARACTERES = 400
PRECO = re.compile(r"R\$\s*\d+|\d+([.,]\d{2})?\s*reais|desconto|\d+\s*%", re.IGNORECASE)


def conferir(texto: str, rascunho: str) -> list[str]:
    """Problemas da resposta (lista vazia = pode enviar). O código confere o que as instruções pedem."""
    problemas = []
    if not texto.strip():
        problemas.append("resposta vazia")
    if len(texto) > LIMITE_CARACTERES:
        problemas.append(f"longa demais ({len(texto)} caracteres)")
    if PRECO.search(texto) and not PRECO.search(rascunho):
        problemas.append("apareceu preço ou desconto que não estava no rascunho")
    return problemas


def reescrever(cliente, modelo: str, mensagem_cliente: str, rascunho: str, tom: str = "cordial") -> tuple[str, list[str]]:
    resposta = cliente.interactions.create(
        model=modelo,
        input=f"Mensagem do cliente: {mensagem_cliente}\nRascunho do atendente: {rascunho}",
        system_instruction=INSTRUCOES.format(tom=TONS[tom]),
        generation_config={"thinking_level": "low"},
    )
    texto = resposta.output_text.strip()
    return texto, conferir(texto, rascunho)


def reescrever_simulado(mensagem_cliente: str, rascunho: str, tom: str = "cordial") -> tuple[str, list[str]]:
    """Sem IA: só põe uma saudação e um fecho em volta do rascunho."""
    abertura = {"cordial": "Olá!", "formal": "Prezado(a) cliente,", "descontraído": "Oi! 😊"}[tom]
    texto = f"{abertura} {rascunho.strip().rstrip('.').capitalize()}. Obrigado pelo contato!"
    return texto, conferir(texto, rascunho)
```

### O risco desta tarefa: a IA "ajudar demais"

Ao reescrever, um modelo pode **acrescentar** coisas que parecem gentis, mas que o atendente **não** decidiu: "e você ganha 10% de desconto na próxima compra!", "entregamos ainda hoje!". Para a padaria, isso vira um **compromisso** com o cliente.

Por isso, duas camadas:

1. **Instruções:** "Mantenha TODAS as informações do rascunho e não acrescente promessas, preços, prazos nem descontos."
2. **Código:** a `conferir()` procura preços, porcentagens e a palavra "desconto" que **não** estavam no rascunho, e limita o tamanho.

```text
>>> reescrever(ClienteFalso("Olá! Pedimos desculpas, trocamos o sonho com 10% de desconto."), "m", "...", "vamos trocar o sonho")
('Olá! Pedimos desculpas, trocamos o sonho com 10% de desconto.', ['apareceu preço ou desconto que não estava no rascunho'])
```

A função devolve o texto **e** a lista de problemas. Com problemas, o programa **não envia**: mostra para o atendente decidir.

!!! warning "A IA sugere, a pessoa decide"
    Respostas a clientes falam **em nome** da empresa. Use a IA para economizar tempo de escrita, mas deixe o atendente **ler e aprovar** antes de enviar, principalmente em reclamações.

### O tom

O dicionário `TONS` descreve cada tom em palavras ("formal e respeitoso, sem gírias nem emojis"). A descrição vai **dentro** das instruções: mudar o tom é mudar uma chave do dicionário.

O `reescrever_simulado()` só coloca uma saudação e um agradecimento em volta do rascunho: serve para testar o fluxo e mostrar a diferença para a IA, que reescreve de verdade.

---

## ⚠️ Erros comuns

- **Deixar a IA "completar"** a resposta com informações que ninguém decidiu.
- **Enviar sem ler**, principalmente reclamações.
- **Tom descrito numa palavra só** ("formal"): descreva o que isso significa (sem gírias? sem emojis? tratamento por "senhor"?).
- **Rascunho com dados pessoais** do cliente: o nome e o pedido bastam.

---

## Exercícios

### Básico (fixação)

Gere com o `reescrever_simulado()` a mesma resposta nos três tons e mostre lado a lado.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```python
    from reescrever import TONS, reescrever_simulado

    rascunho = "o bolo fica pronto às 16h, pode buscar"
    resultados = {tom: reescrever_simulado("Meu bolo fica pronto quando?", rascunho, tom)[0] for tom in TONS}
    for tom, texto in resultados.items():
        print(f"{tom:13} {texto}")
    ```

    As três versões trocam só a abertura. A IA de verdade muda também a escolha das palavras, mantendo "16h" e "pode buscar".

### Intermediário (aplicação)

Teste a `conferir()` com quatro respostas: uma boa; uma com `R$ 5,00`; uma com mais de 400 caracteres; uma vazia. Use o rascunho `"vamos trocar o sonho"`.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```python
    from reescrever import conferir

    rascunho = "vamos trocar o sonho"
    respostas = ["Olá! Vamos trocar o seu sonho. Obrigado!", "Trocamos o sonho e devolvemos R$ 5,00.",
                 "Olá! " * 100, "   "]
    problemas = [conferir(r, rascunho) for r in respostas]
    for p in problemas:
        print(p)
    ```

    Saídas: `[]`; `['apareceu preço ou desconto que não estava no rascunho']`; `['longa demais (500 caracteres)']`; `['resposta vazia']`.

### Avançado (desafio)

Se o **rascunho** já tiver um preço (por exemplo, "a troca custa R$ 5"), a resposta pode repeti-lo. Mas e se a IA **mudar** o valor para R$ 50? Melhore a `conferir()` (numa função nova) para exigir que **todos os valores** da resposta estejam no rascunho.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```python
    import re

    VALOR = re.compile(r"\d+(?:[.,]\d+)?")


    def valores_novos(texto: str, rascunho: str) -> set[str]:
        """Números da resposta que não aparecem no rascunho."""
        return set(VALOR.findall(texto)) - set(VALOR.findall(rascunho))


    rascunho = "a troca custa R$ 5, pode vir até as 18h"
    certo = valores_novos("A troca custa R$ 5 e você pode vir até as 18h.", rascunho)
    errado = valores_novos("A troca custa R$ 50 e você pode vir até as 18h.", rascunho)
    print(certo, errado)
    ```

    `set()` e `{'50'}`. Comparar os **números** do texto com os do rascunho pega preços, horários e quantidades trocados, um erro que as instruções sozinhas não impedem.

---

## 💡 Resumo

- Reescrever: o **conteúdo** vem do rascunho; a IA cuida do **tom** e da **forma**.
- Instruções proíbem acrescentar; o **código confere** (preços, tamanho, vazio).
- Com problemas, **não envia**: o atendente decide.

## ➡️ Próximo passo

**[04 — Regras ou IA?](04_regras_ou_ia.md)**.
