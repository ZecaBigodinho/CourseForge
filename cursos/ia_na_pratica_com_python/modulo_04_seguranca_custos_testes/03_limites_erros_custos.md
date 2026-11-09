# 03 — Limites, erros e custos

> **Curso:** IA na prática com Python  
> **Módulo:** 04 — Segurança, custos e testes  
> **Tempo estimado:** 1 h 30 min  

---

## 🎯 Objetivos

Ao final desta aula, você será capaz de:

- Separar os erros da API que **valem uma nova tentativa** dos que **não adiantam**.
- Esperar e tentar de novo com **espera crescente**.
- Pôr um **limite de gasto** (chamadas e tokens) no seu programa.
- Guardar respostas na **memória** para não pagar duas vezes pela mesma pergunta.
- **Estimar o custo** de uma tarefa em tokens.

## Pré-requisitos

- [Aula 02](02_prompt_injection.md) e o `erros_ia.py` do [Módulo 01](../modulo_01_api_de_ia/02_primeira_chamada.md#explicando-os-erros).

---

## Os limites do plano gratuito

O plano gratuito tem limites de **pedidos por minuto**, de **tokens por minuto** e de **pedidos por dia**, que mudam com o tempo e com o modelo (os seus aparecem no **Google AI Studio**). Quando um deles acaba, a API responde **429** (`RESOURCE_EXHAUSTED`):

- Se foi o limite **por minuto**, esperar um pouco resolve.
- Se foi o limite **por dia**, só amanhã. Tentar de novo sem parar só gasta tempo.

## Quais erros vale repetir

| Código | O que é | Tentar de novo? |
|---|---|---|
| **400** | O pedido está errado (parâmetro inválido, texto grande demais) | **Não**: vai dar o mesmo erro. Corrija o código. |
| **401 / 403** | Chave recusada | **Não**: confira o `.env`. |
| **404** | Modelo não encontrado | **Não**: confira o nome do modelo. |
| **408** | A resposta demorou demais | Sim |
| **429** | Limite de uso | Sim, **esperando**; se continuar, pare (pode ser o limite do dia) |
| **500, 502, 503, 504** | Problema do lado do Google | Sim, esperando |
| Sem internet | `ConnectionError`, `TimeoutError` | Sim, poucas vezes |

!!! info "A biblioteca já tenta de novo, rapidinho"
    Conferido na `google-genai` 2.34.0: nos erros passageiros (408, 429, 5xx), a própria biblioteca refaz o pedido algumas vezes, com esperas curtas, por **no máximo uns 30 segundos**. Quando um erro chega ao seu programa, ela **já tentou**. A camada abaixo serve para o que a biblioteca não faz: esperas **maiores** (para a janela de um minuto passar), um **limite de gasto** decidido por você e a **memória** de respostas, tudo **testável** sem internet.

## O cliente seguro

O `ClienteSeguro` **envolve** o cliente de verdade e tem o **mesmo jeito** dele (`cliente.interactions.create`). Assim, as funções dos módulos anteriores (`classificar()`, `extrair_pedido()`, `responder()`) funcionam com ele **sem mudar nada**.

```python title="cliente_seguro.py"
"""Envolve o cliente da API com proteções: nova tentativa, limite de gasto e memória de respostas.

Tem o mesmo jeito do cliente de verdade (cliente.interactions.create), então os programas
dos módulos anteriores funcionam com ele sem mudar nada.
"""
import json
import time
from types import SimpleNamespace

REPETIR = {408, 429, 500, 502, 503, 504}  # vale esperar e tentar de novo; 400, 401, 403 e 404, não


class LimiteAtingido(Exception):
    """O programa chegou ao limite de chamadas ou de tokens que VOCÊ definiu."""


def vale_repetir(erro: Exception) -> bool:
    codigo = getattr(erro, "code", None) or getattr(erro, "status_code", None)
    return codigo in REPETIR or isinstance(erro, (ConnectionError, TimeoutError))


class ClienteSeguro:
    def __init__(self, cliente, max_chamadas: int = 50, max_tokens: int = 100_000,
                 tentativas: int = 2, espera: float = 20.0, dormir=time.sleep):
        self.cliente = cliente
        self.max_chamadas, self.max_tokens = max_chamadas, max_tokens
        self.tentativas, self.espera = tentativas, espera
        self.dormir = dormir           # nos testes, uma função que só anota a espera
        self.chamadas = self.tokens = self.do_cache = 0
        self.cache = {}
        self.interactions = SimpleNamespace(create=self._criar)

    def _criar(self, **pedido):
        chave = json.dumps(pedido, sort_keys=True, ensure_ascii=False, default=str)
        if chave in self.cache:        # pedido igual a um anterior: não gasta nada
            self.do_cache += 1
            return self.cache[chave]
        espera = self.espera
        for tentativa in range(1, self.tentativas + 1):
            if self.chamadas >= self.max_chamadas:
                raise LimiteAtingido(f"limite de {self.max_chamadas} chamadas nesta execução")
            if self.tokens >= self.max_tokens:
                raise LimiteAtingido(f"limite de {self.max_tokens} tokens nesta execução")
            self.chamadas += 1
            try:
                resposta = self.cliente.interactions.create(**pedido)
                break
            except Exception as erro:
                if tentativa == self.tentativas or not vale_repetir(erro):
                    raise                # não adianta (ou já tentou): o erro segue para o programa
                self.dormir(espera)
                espera *= 2              # espera cada vez maior: 20 s, 40 s...
        self.tokens += resposta.usage.total_tokens
        if "previous_interaction_id" not in pedido:   # conversa não vai para a memória
            self.cache[chave] = resposta
        return resposta

    def resumo(self) -> str:
        return f"{self.chamadas} chamadas, {self.tokens} tokens, {self.do_cache} respostas da memória"
```

| Peça | O que faz |
|---|---|
| **`vale_repetir()`** | Olha o **código** do erro (`code`, nos erros da `google-genai`) e decide se adianta tentar de novo. |
| **Espera crescente** | 20 s, depois 40 s... Dá tempo de a janela de um minuto passar sem martelar a API. |
| **`max_chamadas` e `max_tokens`** | O **seu** limite de gasto. Um erro no programa (um laço que não para) não consome a cota inteira. |
| **Memória (`cache`)** | Pedido **igual** a um anterior devolve a resposta guardada, sem chamar a API. |
| **`dormir`** | Em vez de esperar de verdade, os testes passam uma função que só **anota** a espera. |

A memória vale só para pedidos **iguais** (mesma mensagem, mesmas instruções, mesmo modelo) e não guarda conversas (`previous_interaction_id`), em que a mesma frase pode pedir respostas diferentes.

### Testando sem esperar e sem internet

Os erros da biblioteca podem ser criados à mão, o que permite testar o 429 sem gastar nada. Este `ClienteFalso` falha **uma vez** e depois responde:

```python
from google.genai import errors

from cliente_falso import ClienteFalso
from cliente_seguro import ClienteSeguro
from erros_ia import explicar_erro

limite = errors.ClientError(429, {"error": {"code": 429, "status": "RESOURCE_EXHAUSTED", "message": "Quota exceeded"}})
falhas = [limite]


def instavel(pedido: dict) -> str:
    if falhas:
        raise falhas.pop()
    return "dúvida"


esperas = []
seguro = ClienteSeguro(ClienteFalso(instavel), dormir=esperas.append)
print(seguro.interactions.create(model="gemini-3.8-flash", input="Vocês abrem no feriado?").output_text)
print(seguro.interactions.create(model="gemini-3.8-flash", input="Vocês abrem no feriado?").output_text)
print("Esperas:", esperas, "|", seguro.resumo())
print(explicar_erro(limite))
```

```text
dúvida
dúvida
Esperas: [20.0] | 2 chamadas, 6 tokens, 1 respostas da memória
o limite de uso do plano gratuito acabou. Espere alguns minutos (ou até amanhã).
```

A primeira pergunta deu 429, esperou 20 s (de mentira) e deu certo na segunda tentativa: as **2 chamadas** são essas duas tentativas (a que falhou também conta, porque gasta um pedido do limite por minuto). A segunda pergunta, **igual**, veio da memória: nenhuma chamada a mais. A `explicar_erro()` do Módulo 01 já entende os erros da biblioteca.

## Quanto custa

No plano gratuito, a conta é em **cota**: cada token gasto é um token a menos até o limite renovar. Num plano pago, a conta é em **dinheiro**, com preço por **milhão de tokens**, diferente para entrada e saída:

```text
custo = tokens de entrada × preço de entrada ÷ 1.000.000  +  tokens de saída × preço de saída ÷ 1.000.000
```

Os preços mudam com frequência e variam por modelo: confira sempre a página de preços oficial. O que **não muda** é o que faz a conta subir:

| O que gasta | Onde está | Como gastar menos |
|---|---|---|
| **Entrada**: instruções + mensagem + histórico + trechos | `usage.total_input_tokens` | Instruções curtas, só os trechos certos ([Módulo 03](../modulo_03_documentos/03_buscar_trechos.md)), `/nova` nas conversas |
| **Saída**: a resposta | `usage.total_output_tokens` | Pedir respostas curtas ("no máximo 3 frases") |
| **Raciocínio** do modelo | `usage.total_thought_tokens` | `thinking_level` baixo nas tarefas simples |
| **Chamadas que nem precisavam** | | Regras antes da IA ([Módulo 02](../modulo_02_tarefas_uteis/04_regras_ou_ia.md)), memória, não chamar sem trecho |

O `usage.total_tokens` soma tudo, e é ele que o `ClienteSeguro` conta.

---

## ⚠️ Erros comuns

- **Tentar de novo sem parar** (`while True`): no limite do dia, o programa fica preso; num erro 400, nunca vai dar certo.
- **Tentar de novo sem esperar**: piora o 429.
- **Repetir erros de chave ou de modelo**: o problema está no `.env`, não na internet.
- **Rodar um laço com a API sem limite de gasto**: um erro de programação consome a cota inteira.
- **Testar esperando de verdade**: use o `dormir` falso; o teste roda em milissegundos.

---

## Exercícios

### Básico (fixação)

Crie um erro falso com o atributo `code` e mostre, para os códigos 400, 401, 404, 408, 429, 500 e 503, se vale tentar de novo.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```python
    from cliente_seguro import vale_repetir


    class ErroAPI(Exception):
        def __init__(self, code: int):
            super().__init__(f"erro {code}")
            self.code = code


    codigos = [400, 401, 404, 408, 429, 500, 503]
    decisoes = {c: vale_repetir(ErroAPI(c)) for c in codigos}
    for codigo, repetir in decisoes.items():
        print(codigo, "tentar de novo" if repetir else "não adianta")
    ```

    400, 401 e 404 **não adiantam** (pedido errado, chave, modelo); 408, 429, 500 e 503 **valem** uma nova tentativa com espera.

### Intermediário (aplicação)

Use o `ClienteSeguro` com a `classificar()` do Módulo 02 (sem mudar nada nela) para classificar as cinco mensagens abaixo com um `ClienteFalso`. Quantas chamadas foram feitas e quantas respostas vieram da memória?

```text
Vocês abrem no feriado?
Quero 2 bolos de fubá.
Vocês abrem no feriado?
Quero 2 bolos de fubá.
kkkkk
```

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```python
    from classificar import classificar
    from cliente_falso import ClienteFalso
    from cliente_seguro import ClienteSeguro

    mensagens = ["Vocês abrem no feriado?", "Quero 2 bolos de fubá.", "Vocês abrem no feriado?",
                 "Quero 2 bolos de fubá.", "kkkkk"]
    seguro = ClienteSeguro(ClienteFalso("dúvida"))
    categorias = [classificar(seguro, "gemini-3.8-flash", m) for m in mensagens]
    print(categorias)
    print(seguro.resumo())
    ```

    **3** chamadas e **2** respostas da memória: as mensagens repetidas não gastaram nada. A `classificar()` nem sabe que está usando o cliente seguro: ela só chama `cliente.interactions.create`, e o cliente seguro tem o mesmo jeito.

### Avançado (desafio)

Escreva `custo(entrada, saida, preco_entrada, preco_saida)`, com os preços **por milhão** de tokens, e estime a triagem de **1.000 mensagens** com 300 tokens de entrada e 60 de saída cada uma, com os preços **de exemplo** de US$ 0,50 (entrada) e US$ 3,00 (saída). Depois, calcule de novo supondo que as regras resolvem **60%** das mensagens sem IA.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```python
    def custo(entrada: int, saida: int, preco_entrada: float, preco_saida: float) -> float:
        """Custo em dólares; os preços são por milhão de tokens."""
        return entrada * preco_entrada / 1_000_000 + saida * preco_saida / 1_000_000


    mensagens = 1000
    so_ia = custo(mensagens * 300, mensagens * 60, 0.50, 3.00)
    com_regras = custo(int(mensagens * 0.4) * 300, int(mensagens * 0.4) * 60, 0.50, 3.00)
    print(f"Só IA: US$ {so_ia:.2f} | Regras + IA: US$ {com_regras:.2f}")
    ```

    `Só IA: US$ 0.33 | Regras + IA: US$ 0.13`. Os preços são **inventados** para a conta (confira os reais na página oficial), mas a lição vale com qualquer preço: a **saída** costuma custar mais caro por token, e cada chamada que as regras evitam é custo a menos. No plano gratuito, a mesma conta mostra quanto da **cota** a tarefa consome.

---

## 💡 Resumo

- **Repita** só os erros passageiros (408, 429, 5xx, sem internet), **esperando** cada vez mais; **pare** nos outros.
- O `ClienteSeguro` tem o mesmo jeito do cliente de verdade e acrescenta **novas tentativas**, **limite de gasto** e **memória**.
- Custo = tokens de **entrada** + **saída** (+ raciocínio). Menos chamadas e textos mais curtos gastam menos.

## ➡️ Próximo passo

**[04 — Testes automáticos com o pytest](04_testes_automaticos.md)**.
