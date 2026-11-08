# 02 — Extrair dados em JSON

> **Curso:** IA na prática com Python  
> **Módulo:** 02 — Tarefas úteis  
> **Tempo estimado:** 1 h 30 min  

---

## 🎯 Objetivos

Ao final desta aula, você será capaz de:

- Pedir à IA uma resposta em **JSON** que segue um **esquema** (os campos e tipos que você definir).
- Ler o JSON com `json.loads()` e **validar** cada campo (tipo, intervalo, data).
- Entender por que **validar** continua obrigatório mesmo com o esquema.
- Comparar com uma extração por **expressões regulares**, sem IA.

## Pré-requisitos

- [Aula 01](01_classificar_mensagens.md): classificar mensagens.

---

## Do texto livre para dados

"Bom dia! Quero encomendar 2 bolos de fubá para sábado, dia 14/11." Para virar uma linha na planilha de encomendas, essa mensagem precisa ser transformada em **dados**:

```json
{"produto": "bolo de fubá", "quantidade": 2, "data_entrega": "2026-11-14"}
```

**JSON** é um formato de texto para dados (o mesmo dos dicionários do Python, com aspas duplas). O Python lê com `json.loads()` e escreve com `json.dumps()`.

## O extrator

```python title="extrair.py"
"""Extrai os dados de um pedido (produto, quantidade, data) em JSON e confere tudo."""
import json
import re
from datetime import date, datetime, timedelta

INSTRUCOES = (
    "Você lê mensagens de clientes de uma padaria e extrai os dados do pedido. "
    "Use só o que está escrito na mensagem. Se a data não aparecer, deixe data_entrega vazia. "
    "Datas no formato AAAA-MM-DD; considere que hoje é {hoje}."
)

ESQUEMA = {  # o formato que a resposta TEM de seguir (JSON Schema)
    "type": "object",
    "properties": {
        "produto": {"type": "string", "description": "o que o cliente quer, no singular"},
        "quantidade": {"type": "integer", "description": "quantas unidades"},
        "data_entrega": {"type": "string", "description": "AAAA-MM-DD, ou vazio se não houver"},
    },
    "required": ["produto", "quantidade", "data_entrega"],
}


def validar(dados: dict, hoje: date) -> tuple[dict | None, str]:
    """Confere o que a IA devolveu. (pedido, "") se estiver tudo certo; (None, motivo) se não."""
    produto = str(dados.get("produto", "")).strip()
    quantidade = dados.get("quantidade")
    texto_data = str(dados.get("data_entrega", "")).strip()
    if not produto:
        return None, "sem produto"
    if not isinstance(quantidade, int) or not 1 <= quantidade <= 500:
        return None, f"quantidade estranha: {quantidade!r}"
    entrega = None
    if texto_data:
        try:
            entrega = datetime.strptime(texto_data, "%Y-%m-%d").date()
        except ValueError:
            return None, f"data inválida: {texto_data!r}"
        if not hoje <= entrega <= hoje + timedelta(days=180):
            return None, f"data fora do esperado: {entrega:%d/%m/%Y}"
    return {"produto": produto, "quantidade": quantidade, "data_entrega": entrega}, ""


def extrair_pedido(cliente, modelo: str, mensagem: str, hoje: date) -> tuple[dict | None, str]:
    resposta = cliente.interactions.create(
        model=modelo,
        input=mensagem,
        system_instruction=INSTRUCOES.format(hoje=hoje.isoformat()),
        generation_config={"thinking_level": "low"},
        response_format={"type": "text", "mime_type": "application/json", "schema": ESQUEMA},
    )
    try:
        dados = json.loads(resposta.output_text)
    except json.JSONDecodeError:
        return None, "a resposta não é um JSON válido"
    if not isinstance(dados, dict):
        return None, "o JSON não é um objeto"
    return validar(dados, hoje)


NUMEROS = {"um": 1, "uma": 1, "dois": 2, "duas": 2, "tres": 3, "três": 3, "meia duzia": 6, "uma duzia": 12}


def extrair_simulado(mensagem: str, hoje: date) -> tuple[dict | None, str]:
    """Sem IA: número + o que vem depois dele, e uma data dd/mm. Só funciona no jeito mais comum."""
    texto = mensagem.lower()
    achou = re.search(r"\b(\d+|um|uma|dois|duas|tr[eê]s)\s+([a-zà-ú]+(?:\s+de\s+[a-zà-ú]+)?)", texto)
    if not achou:
        return None, "não achei quantidade e produto"
    numero = achou.group(1)
    quantidade = int(numero) if numero.isdigit() else NUMEROS[numero]
    dados = {"produto": achou.group(2), "quantidade": quantidade, "data_entrega": ""}
    data = re.search(r"\b(\d{1,2})/(\d{1,2})\b", texto)
    if data:
        dia, mes = int(data.group(1)), int(data.group(2))
        ano = hoje.year if (mes, dia) >= (hoje.month, hoje.day) else hoje.year + 1
        dados["data_entrega"] = f"{ano:04d}-{mes:02d}-{dia:02d}"
    elif "amanhã" in texto or "amanha" in texto:
        dados["data_entrega"] = (hoje + timedelta(days=1)).isoformat()
    return validar(dados, hoje)
```

### O esquema e o `response_format`

O `ESQUEMA` é um **JSON Schema**: diz que a resposta é um objeto com `produto` (texto), `quantidade` (número inteiro) e `data_entrega` (texto), todos obrigatórios. Com ele no `response_format`, a API **força** a resposta a ter esse formato:

```python
response_format={"type": "text", "mime_type": "application/json", "schema": ESQUEMA}
```

As `description` de cada campo ajudam a IA a entender **o que** pôr ali ("no singular", "AAAA-MM-DD").

!!! info "Dica de versão"
    Esse é o formato atual da API de interações do Gemini (a partir da mudança de maio de 2026, o tipo `application/json` vai **dentro** do `response_format`). Exemplos antigos na internet usam `response_mime_type` separado.

### Por que validar se o esquema já obriga?

O esquema garante o **formato** (os campos e os tipos), não o **conteúdo**. A IA pode devolver `"quantidade": 0`, uma data no passado ou "14/11" em vez de "2026-11-14". A `validar()` confere o que importa para a padaria:

| Conferência | Por quê |
|---|---|
| Produto não vazio | Sem produto não há pedido |
| Quantidade inteira entre 1 e 500 | 0 ou 5000 bolos são quase certamente erro de leitura |
| Data no formato `AAAA-MM-DD` | `datetime.strptime` falha se vier em outro formato |
| Data entre hoje e daqui a 180 dias | Uma entrega no passado não faz sentido |

E se o texto nem for JSON (instabilidade, resposta cortada), o `json.loads()` falha e a função devolve o motivo, sem quebrar o programa.

!!! tip "Hoje é que dia?"
    A IA não sabe a data de hoje. "Sábado" e "amanhã" só viram uma data se o programa **disser** qual é o dia: por isso as instruções recebem `{hoje}`.

### A extração por regras

`extrair_simulado()` usa **expressões regulares**: um número (ou "um", "dois"...) seguido de uma palavra é o produto; `dd/mm` é a data; "amanhã" é hoje + 1. Funciona para as mensagens de treino:

```text
({'produto': 'bolos de fubá', 'quantidade': 2, 'data_entrega': datetime.date(2026, 11, 14)}, '')
({'produto': 'coxinhas', 'quantidade': 50, 'data_entrega': datetime.date(2026, 11, 20)}, '')
({'produto': 'torta de frango', 'quantidade': 1, 'data_entrega': datetime.date(2026, 11, 9)}, '')
```

Mas erra com "Quero **uma dúzia** de pães de queijo para **sexta**": entende **1** "dúzia de pães" e não acha a data. Pior do que falhar, ele **erra sem perceber**. A IA lida com o jeito variado de as pessoas escreverem (e a validação pega o que ainda escapar).

---

## ⚠️ Erros comuns

- **Pedir JSON só nas instruções**, sem o `response_format`: às vezes vem texto antes ou depois do JSON.
- **Não validar** o conteúdo: datas e quantidades absurdas vão parar na planilha.
- **Esquecer de dizer a data de hoje**: "amanhã" vira qualquer coisa.
- **`json.loads()` sem `try`**: uma resposta estranha derruba o programa.

---

## Exercícios

### Básico (fixação)

Teste a `validar()` com três pedidos: um certo, um com quantidade **0** e um com data **31/02/2027** (que não existe). Use `hoje = date(2026, 11, 8)`.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```python
    from datetime import date

    from extrair import validar

    hoje = date(2026, 11, 8)
    testes = [
        {"produto": "bolo de fubá", "quantidade": 2, "data_entrega": "2026-11-14"},
        {"produto": "bolo de fubá", "quantidade": 0, "data_entrega": ""},
        {"produto": "bolo de fubá", "quantidade": 2, "data_entrega": "2027-02-31"},
    ]
    resultados = [validar(t, hoje) for t in testes]
    for resultado in resultados:
        print(resultado)
    ```

    O primeiro passa; o segundo dá `quantidade estranha: 0`; o terceiro, `data inválida: '2027-02-31'` (o `strptime` sabe que fevereiro não tem 31 dias).

### Intermediário (aplicação)

Com o `ClienteFalso`, teste o `extrair_pedido()` em três situações: a IA devolve um JSON certo; devolve um texto que não é JSON; devolve um JSON com a data no formato `14/11/2026`.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```python
    import json
    from datetime import date

    from cliente_falso import ClienteFalso
    from extrair import extrair_pedido

    hoje = date(2026, 11, 8)
    respostas = [
        json.dumps({"produto": "coxinha", "quantidade": 50, "data_entrega": "2026-11-20"}),
        "Claro! O pedido é de 50 coxinhas.",
        json.dumps({"produto": "coxinha", "quantidade": 50, "data_entrega": "20/11/2026"}),
    ]
    resultados = [extrair_pedido(ClienteFalso(r), "gemini-3.8-flash", "mensagem", hoje) for r in respostas]
    for pedido, motivo in resultados:
        print(pedido, "|", motivo)
    ```

    O primeiro vira um pedido com `date(2026, 11, 20)`; o segundo, `a resposta não é um JSON válido`; o terceiro, `data inválida: '20/11/2026'`. O programa nunca quebra e sempre diz **por que** recusou.

### Avançado (desafio)

Acrescente ao esquema o campo **`observacao`** (texto opcional, por exemplo "sem açúcar") e faça a `validar()` aceitar a observação, limitando a **100 caracteres**. Teste com uma observação longa.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```python
    from datetime import date

    import extrair

    extrair.ESQUEMA["properties"]["observacao"] = {"type": "string", "description": "detalhe do pedido, ou vazio"}
    validar_original = extrair.validar


    def validar_com_observacao(dados: dict, hoje: date):
        pedido, motivo = validar_original(dados, hoje)
        if not pedido:
            return pedido, motivo
        observacao = str(dados.get("observacao", "")).strip()
        if len(observacao) > 100:
            return None, f"observação longa demais ({len(observacao)} caracteres)"
        pedido["observacao"] = observacao
        return pedido, ""


    hoje = date(2026, 11, 8)
    curto = validar_com_observacao({"produto": "bolo", "quantidade": 1, "data_entrega": "", "observacao": "sem açúcar"}, hoje)
    longo = validar_com_observacao({"produto": "bolo", "quantidade": 1, "data_entrega": "", "observacao": "x" * 150}, hoje)
    print(curto)
    print(longo)
    ```

    O campo **não** entrou em `required`: é opcional. A nova validação **reaproveita** a antiga (chama `validar_original`) e só acrescenta a regra nova.

---

## 💡 Resumo

- `response_format={"type": "text", "mime_type": "application/json", "schema": ESQUEMA}` força o **formato**.
- `json.loads()` com `try`, e **validar** o conteúdo: tipos, intervalos, datas.
- Diga a **data de hoje** nas instruções.
- Regras extraem o jeito comum de escrever; a IA lida com a variedade.

## ➡️ Próximo passo

**[03 — Reescrever com tom definido](03_reescrever_com_tom.md)**.

---

*Formato do `response_format` conferido em 08/11/2026 na documentação de saída estruturada da API de interações do Gemini e na biblioteca `google-genai` 2.34.0.*
