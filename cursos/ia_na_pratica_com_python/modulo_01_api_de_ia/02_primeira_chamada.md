# 02 — A primeira chamada

> **Curso:** IA na prática com Python  
> **Módulo:** 01 — Conversando com um modelo por API  
> **Tempo estimado:** 1 h 30 min  

---

## 🎯 Objetivos

Ao final desta aula, você será capaz de:

- Fazer um pedido ao Gemini com `client.interactions.create()` e ler a resposta.
- Ver quantos **tokens** o pedido gastou.
- Transformar os erros da API (chave, modelo, limite, internet) em **mensagens claras**.
- Testar o programa com um **cliente falso**, sem chave, sem internet e sem gastar a cota.

## Pré-requisitos

- [Aula 01](01_o_que_e_uma_api_de_ia.md): projeto preparado (e, no caminho com chave, o `.env`).

---

## Explicando os erros

Antes da chamada, uma função que transforma qualquer erro da API numa frase que o usuário entende. Ela vai ser usada em todos os programas do curso.

```python title="erros_ia.py"
"""Transforma os erros da API numa mensagem que qualquer pessoa entende."""


def explicar_erro(erro: Exception) -> str:
    codigo = getattr(erro, "status_code", None) or getattr(erro, "code", None)
    texto = str(erro).lower()
    if codigo in (401, 403) or "api key" in texto or "api_key" in texto:
        return "a chave não foi aceita. Confira a GEMINI_API_KEY no arquivo .env."
    if codigo == 404 or "not found" in texto:
        return "o modelo não foi encontrado. Confira o nome em GEMINI_MODELO no .env."
    if codigo == 429 or "resource_exhausted" in texto:
        return "o limite de uso do plano gratuito acabou. Espere alguns minutos (ou até amanhã)."
    if isinstance(codigo, int) and codigo >= 500:
        return "o serviço de IA está com problemas agora. Tente de novo mais tarde."
    if isinstance(erro, (ConnectionError, TimeoutError, OSError)) or "connect" in texto:
        return "não consegui falar com a API. A internet está funcionando?"
    return f"erro inesperado ({type(erro).__name__}): {erro}"
```

- `getattr(erro, "status_code", None)` pega o **código HTTP** do erro, se ele tiver: **401/403** (chave recusada), **404** (modelo não existe), **429** (limite), **500+** (problema do lado do Google).
- Quando não há código (sem internet, por exemplo), a função olha o **tipo** e o **texto** do erro.
- O último `return` mostra o erro original: nunca esconda o que não reconhece.

## A primeira chamada

```python title="primeira_chamada.py"
import os
import sys

from dotenv import load_dotenv
from google import genai

from erros_ia import explicar_erro

load_dotenv()
if not os.getenv("GEMINI_API_KEY"):
    print("Falta a GEMINI_API_KEY no arquivo .env (veja a aula 01).")
    sys.exit(1)

cliente = genai.Client()  # lê a chave da variável GEMINI_API_KEY
modelo = os.getenv("GEMINI_MODELO", "gemini-3.8-flash")

try:
    resposta = cliente.interactions.create(
        model=modelo,
        input="Explique o que é uma API em duas frases, para um aluno do ensino médio.",
    )
except Exception as erro:
    print(f"A API não respondeu: {explicar_erro(erro)}")
    sys.exit(1)

print(resposta.output_text)
uso = resposta.usage
print(f"\nTokens: {uso.total_input_tokens} de entrada + {uso.total_output_tokens} de saída "
      f"= {uso.total_tokens}")
```

Com chave no `.env`:

```powershell
python primeira_chamada.py
```

O texto da resposta **muda a cada execução** (é assim que esses modelos funcionam), mas o formato é este, seguido da contagem de tokens:

```text
Tokens: 17 de entrada + 41 de saída = 58
```

| Parte | Faz |
|---|---|
| `genai.Client()` | Cria a conexão com a API, lendo a chave da variável `GEMINI_API_KEY` (que o `load_dotenv()` trouxe do `.env`) |
| `interactions.create(model=..., input=...)` | Manda o pedido para o modelo escolhido e espera a resposta |
| `resposta.output_text` | O texto da resposta |
| `resposta.usage.total_input_tokens` / `total_output_tokens` / `total_tokens` | Quantos tokens o pedido gastou (entrada, saída e total) |

!!! note "Os números do exemplo"
    A linha de tokens acima é um exemplo do formato. Os números de verdade dependem do modelo e da resposta; em modelos que "pensam" antes de responder, o total também inclui esses tokens de raciocínio.

## Testando sem a API: o cliente falso

Para testar o programa **sem gastar a cota** (e para quem está no caminho sem chave), usamos um **cliente falso**: um objeto com o **mesmo jeito** do cliente de verdade (`cliente.interactions.create(...)` devolvendo algo com `id`, `output_text` e `usage`), mas que responde na hora, sem internet.

```python title="cliente_falso.py"
"""Um cliente FALSO da API, para testar os programas sem internet, sem chave e sem gastar nada."""
from itertools import count
from types import SimpleNamespace


class ClienteFalso:
    def __init__(self, resposta="Resposta de teste.", erro: Exception | None = None):
        self.resposta = resposta
        self.erro = erro
        self.pedidos = []  # tudo o que o programa mandou, para conferir depois
        self._ids = count(1)
        self.interactions = SimpleNamespace(create=self._criar)

    def _criar(self, **pedido):
        self.pedidos.append(pedido)
        if self.erro:
            raise self.erro
        texto = self.resposta(pedido) if callable(self.resposta) else self.resposta
        entrada = len(str(pedido.get("input", ""))) // 4
        saida = len(texto) // 4
        return SimpleNamespace(
            id=f"falso-{next(self._ids)}",
            output_text=texto,
            usage=SimpleNamespace(total_input_tokens=entrada, total_output_tokens=saida,
                                  total_tokens=entrada + saida),
        )
```

- `SimpleNamespace` cria um objeto com os atributos que você passar: é um jeito rápido de imitar a resposta da API.
- O falso **guarda os pedidos** em `self.pedidos`: dá para conferir **o que** o programa mandou (modelo, instruções, texto).
- `erro=` faz o falso **falhar** de propósito, para testar as mensagens de erro.
- `resposta=` pode ser um texto fixo ou uma **função** que monta a resposta a partir do pedido.

!!! tip "Como o cliente falso entra no programa"
    O `primeira_chamada.py` cria o cliente com `genai.Client()`. Num teste, dá para trocar essa função pelo falso **antes** de rodar o programa (é o que os exercícios fazem). Nos próximos programas, o cliente vai ser um **parâmetro** (`cliente=None`), o que deixa o teste ainda mais simples.

---

## ⚠️ Erros comuns

- **`Falta a GEMINI_API_KEY`**: o `.env` não existe, está em outra pasta ou a linha está escrita errado (`GEMINI_API_KEY=valor`, sem espaços nem aspas).
- **"a chave não foi aceita"**: chave copiada pela metade, com espaço, ou apagada no AI Studio.
- **"o modelo não foi encontrado"**: o nome em `GEMINI_MODELO` está errado ou o modelo foi aposentado.
- **"o limite de uso ... acabou"** (429): espere. Nos testes, use o cliente falso.
- **Rodar a chamada real dentro de um laço** "para testar": cada volta gasta a cota. Teste com o falso.

---

## Exercícios

### Básico (fixação)

Usando o `ClienteFalso`, faça um pedido "de mentira" e mostre o **texto** e o **total de tokens** da resposta.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```python
    from cliente_falso import ClienteFalso

    cliente = ClienteFalso("Fotossíntese é como a planta faz o próprio alimento usando a luz.")
    resposta = cliente.interactions.create(model="gemini-3.8-flash", input="O que é fotossíntese?")
    print(resposta.output_text)
    print("tokens:", resposta.usage.total_tokens)
    ```

    O código que usa o cliente é **igual** ao de verdade: só a criação (`ClienteFalso(...)` em vez de `genai.Client()`) muda. É por isso que o falso serve para testar.

### Intermediário (aplicação)

Teste a `explicar_erro()` com quatro erros "fabricados": um com `status_code = 401`, um com `429`, um `ConnectionError` e um `ValueError("algo estranho")`. Mostre a mensagem de cada um.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```python
    from erros_ia import explicar_erro


    class ErroDaApi(Exception):
        def __init__(self, mensagem: str, status_code: int):
            super().__init__(mensagem)
            self.status_code = status_code


    erros = [ErroDaApi("invalid key", 401), ErroDaApi("RESOURCE_EXHAUSTED", 429),
             ConnectionError("sem rede"), ValueError("algo estranho")]
    mensagens = [explicar_erro(e) for e in erros]
    for mensagem in mensagens:
        print(mensagem)
    ```

    Saem: chave não aceita, limite de uso, internet e `erro inesperado (ValueError): algo estranho`. Testar a função de erro com erros fabricados é o único jeito seguro de ver todos os casos, sem precisar estourar o limite de verdade.

### Avançado (desafio)

Escreva a função `perguntar(cliente, modelo, pergunta)` que faz o pedido e devolve uma tupla `(texto, tokens)`, ou `(None, mensagem_de_erro)` se a API falhar. Teste com o `ClienteFalso` funcionando e com ele falhando.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```python
    from cliente_falso import ClienteFalso
    from erros_ia import explicar_erro


    def perguntar(cliente, modelo: str, pergunta: str) -> tuple[str | None, int | str]:
        try:
            resposta = cliente.interactions.create(model=modelo, input=pergunta)
        except Exception as erro:
            return None, explicar_erro(erro)
        return resposta.output_text, resposta.usage.total_tokens


    ok = perguntar(ClienteFalso("Resposta."), "gemini-3.8-flash", "Oi?")
    falha = perguntar(ClienteFalso(erro=TimeoutError("demorou")), "gemini-3.8-flash", "Oi?")
    print(ok)
    print(falha)
    ```

    Receber o `cliente` como **parâmetro** (em vez de criar dentro da função) é o que permite testar com o falso. O `TimeoutError` cai no caso de internet: `(None, 'não consegui falar com a API. A internet está funcionando?')`.

---

## 💡 Resumo

- `genai.Client()` + `client.interactions.create(model=..., input=...)`; a resposta vem em `output_text` e os tokens em `usage`.
- `explicar_erro()` traduz 401/403, 404, 429, 500+ e falta de internet em mensagens claras.
- O **cliente falso** imita a API: teste sem chave, sem internet e sem gastar a cota.

## ➡️ Próximo passo

**[03 — Instruções de sistema e ajustes](03_instrucoes_e_ajustes.md)**.
