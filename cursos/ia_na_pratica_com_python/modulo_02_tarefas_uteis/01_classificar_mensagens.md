# 01 — Classificar mensagens

> **Curso:** IA na prática com Python  
> **Módulo:** 02 — Tarefas úteis  
> **Tempo estimado:** 1 h 30 min  

---

## 🎯 Objetivos

Ao final desta aula, você será capaz de:

- Usar a IA para **classificar** textos em **categorias fixas**.
- Escrever instruções que deixam a resposta **fácil de conferir** (uma palavra da lista).
- **Normalizar** e **validar** a resposta: o que não for uma categoria conhecida vai para **revisão**.
- Comparar com um classificador **por regras** (palavras-chave), sem IA.

## Pré-requisitos

- [Módulo 01](../modulo_01_api_de_ia/index.md), com o `erros_ia.py` e o `cliente_falso.py` na pasta.

---

## A tarefa: triagem de mensagens

A Padaria Pão Quente recebe mensagens pelo site e pelas redes. Alguém precisa separar o que é **pedido** (urgente), **reclamação** (atenção!), **dúvida**, **elogio** e o resto. As mensagens de treino (inventadas) ficam em `mensagens_exemplo.csv`:

```text
id;data;mensagem
1;03/11/2026;Bom dia! Quero encomendar 2 bolos de fubá para sábado, dia 14/11.
2;03/11/2026;Vocês abrem no feriado?
3;04/11/2026;O pão de ontem veio queimado e ninguém me atendeu no balcão. Muito chato.
4;04/11/2026;Parabéns pelo atendimento, o bolo de cenoura estava maravilhoso!
5;05/11/2026;Preciso de 50 coxinhas para uma festa no dia 20/11, dá?
6;05/11/2026;Qual o horário de vocês no domingo?
7;06/11/2026;Vi uma promoção de outra padaria, vocês cobrem o preço?
8;06/11/2026;Comprei um sonho e veio sem recheio, quero meu dinheiro de volta.
9;07/11/2026;Quero 1 torta de frango pra amanhã
10;07/11/2026;kkkkk
```

Classificar é uma das tarefas em que a IA mais ajuda: as pessoas escrevem do jeito delas ("dá?", "pra amanhã", "kkkkk"), e uma lista de palavras-chave nunca cobre tudo.

## O classificador

```python title="classificar.py"
"""Classifica mensagens de clientes em categorias fixas."""
import unicodedata

CATEGORIAS = ["pedido", "dúvida", "reclamação", "elogio", "outro"]

INSTRUCOES = (
    "Você classifica mensagens de clientes de uma padaria. Responda com UMA palavra, "
    "exatamente uma destas: pedido, dúvida, reclamação, elogio, outro. "
    "pedido = quer encomendar ou comprar; dúvida = pergunta sobre horário, produto ou serviço; "
    "reclamação = problema com produto ou atendimento; elogio = satisfação; outro = o resto."
)


def sem_acento(texto: str) -> str:
    return unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode().lower()


def normalizar(resposta: str) -> str:
    """'Reclamação.' / ' RECLAMACAO ' -> 'reclamação'; fora da lista -> 'revisar'."""
    limpa = sem_acento(resposta).strip().strip(".!\"'")
    for categoria in CATEGORIAS:
        if limpa == sem_acento(categoria):
            return categoria
    return "revisar"


def classificar(cliente, modelo: str, mensagem: str) -> str:
    resposta = cliente.interactions.create(
        model=modelo,
        input=mensagem,
        system_instruction=INSTRUCOES,
        generation_config={"thinking_level": "low"},
    )
    return normalizar(resposta.output_text)


PALAVRAS = {  # o motor simulado: regras por palavras-chave (aula 04 compara com a IA)
    "reclamação": ["queimado", "veio sem", "ninguem me atendeu", "dinheiro de volta", "estragado", "atrasou"],
    "pedido": ["quero", "encomendar", "preciso de", "reservar"],
    "elogio": ["parabens", "maravilhoso", "adorei", "otimo"],
    "dúvida": ["?"],
}


def classificar_simulado(mensagem: str) -> str:
    texto = sem_acento(mensagem)
    for categoria, palavras in PALAVRAS.items():  # a ordem importa: reclamação vem antes de pedido
        if any(sem_acento(p) in texto for p in palavras):
            return categoria
    return "outro"
```

### Três decisões importantes

**1. Categorias fixas e explicadas.** As instruções dizem **exatamente** quais palavras valem e o que cada uma significa. "Classifique a mensagem" sem lista faz a IA inventar categorias ("pedido urgente", "sugestão"...) e o programa não consegue usar.

**2. Uma palavra só.** Pedir só a categoria deixa a resposta **curta** (menos tokens) e **fácil de conferir**.

**3. Normalizar e validar.** Mesmo pedindo uma palavra, a resposta pode vir como `Reclamação.`, `RECLAMACAO` ou "É um pedido". A `normalizar()` tira acentos, maiúsculas e pontuação e compara com a lista. O que **não** bater vira **`"revisar"`**: uma pessoa olha. O programa nunca "chuta" uma categoria.

```text
>>> [normalizar(x) for x in ['Reclamação.', ' RECLAMACAO ', 'Dúvida', 'É um pedido', 'elogio!']]
['reclamação', 'reclamação', 'dúvida', 'revisar', 'elogio']
```

### O classificador por regras (sem IA)

`classificar_simulado()` procura **palavras-chave**. Com as mensagens de treino, ele acerta todas as 10, mas repare em dois detalhes:

- **A ordem das regras importa.** A mensagem 8 ("quero meu dinheiro de volta") tem "quero", que é de **pedido**; como **reclamação** é testada antes, ela é classificada certo.
- **A mensagem 7** ("vocês cobrem o preço?") foi para **dúvida** só por causa do `?`. Uma frase como "Vi uma promoção de outra padaria e quero que cubram o preço" iria para **pedido**. Regras são frágeis com frases novas: é aí que a IA ajuda (e a [aula 04](04_regras_ou_ia.md) mostra como juntar os dois).

---

## ⚠️ Erros comuns

- **Categorias que se misturam** ("problema" e "reclamação"): a IA não sabe qual escolher. Deixe as categorias bem diferentes e explicadas.
- **Confiar na resposta sem conferir**: sempre `normalizar()` e mandar o resto para revisão.
- **Esquecer a categoria "outro"**: sem ela, a IA força mensagens estranhas numa categoria errada.
- **Mandar dados pessoais** junto com a mensagem para o plano gratuito (o projeto, na [aula 05](05_projeto_triagem.md), tira antes).

---

## Exercícios

### Básico (fixação)

Usando o `classificar_simulado()`, conte quantas mensagens do `mensagens_exemplo.csv` há em cada categoria.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```python
    import csv
    from collections import Counter

    from classificar import classificar_simulado

    with open("mensagens_exemplo.csv", encoding="utf-8") as arq:
        mensagens = [linha["mensagem"] for linha in csv.DictReader(arq, delimiter=";")]
    contagem = Counter(classificar_simulado(m) for m in mensagens)
    print(contagem.most_common())
    ```

    Resultado: pedido 3, dúvida 3, reclamação 2, elogio 1, outro 1.

### Intermediário (aplicação)

Teste o `classificar()` (com IA) usando o `ClienteFalso` com quatro respostas diferentes: `"Pedido."`, `"RECLAMACAO"`, `"sugestão"` e `"elogio"`. Quais viram `"revisar"`?

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```python
    from classificar import classificar
    from cliente_falso import ClienteFalso

    respostas = ["Pedido.", "RECLAMACAO", "sugestão", "elogio"]
    resultados = [classificar(ClienteFalso(r), "gemini-3.8-flash", "mensagem de teste") for r in respostas]
    print(resultados)
    ```

    `['pedido', 'reclamação', 'revisar', 'elogio']`. A "sugestão" não está na lista: em vez de virar uma categoria nova, vai para uma pessoa revisar. É assim que se testa a **validação** sem gastar a cota.

### Avançado (desafio)

A padaria quer separar **"encomenda"** (para outro dia) de **"pedido"** (para hoje). Mude as `CATEGORIAS` e as `INSTRUCOES` (numa cópia) e escreva o texto da instrução explicando a diferença. Teste a `normalizar()` com `"Encomenda"`.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```python
    import classificar

    classificar.CATEGORIAS = ["encomenda", "pedido", "dúvida", "reclamação", "elogio", "outro"]
    classificar.INSTRUCOES = (
        "Você classifica mensagens de clientes de uma padaria. Responda com UMA palavra, exatamente uma destas: "
        "encomenda, pedido, dúvida, reclamação, elogio, outro. "
        "encomenda = quer comprar para OUTRO dia (tem data futura, 'amanhã', 'sábado'); "
        "pedido = quer comprar para HOJE ou sem data; dúvida = pergunta; reclamação = problema; "
        "elogio = satisfação; outro = o resto."
    )
    print(classificar.normalizar("Encomenda"), classificar.normalizar("encomendas"))
    ```

    `encomenda` é aceita; `encomendas` (plural) vai para `revisar`, porque não é uma palavra da lista. A diferença entre as categorias precisa estar **explicada com exemplos** ("amanhã", "sábado"): é isso que a IA usa para decidir.

---

## 💡 Resumo

- Classificar: **categorias fixas**, explicadas nas instruções, e resposta de **uma palavra**.
- **Normalize e valide**: o que não for da lista vai para **revisar**, nunca para um chute.
- Regras por palavras-chave funcionam no comum e quebram com frases novas.

## ➡️ Próximo passo

**[02 — Extrair dados em JSON](02_extrair_json.md)**.
