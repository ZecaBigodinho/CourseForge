# 01 — Dados pessoais: o que nunca enviar

> **Curso:** IA na prática com Python  
> **Módulo:** 04 — Segurança, custos e testes  
> **Tempo estimado:** 1 h 30 min  

---

## 🎯 Objetivos

Ao final desta aula, você será capaz de:

- Explicar o que a **LGPD** chama de dado pessoal e de dado pessoal **sensível**.
- Decidir o que **nunca** vai para uma API de IA.
- **Mascarar** e-mail, cartão, CPF, CEP e telefone antes de enviar, e **barrar** mensagens com dados sensíveis.
- Trocar nomes por **apelidos** (pseudônimos) e devolver os nomes na resposta, no seu computador.

## Pré-requisitos

- [Módulo 02](../modulo_02_tarefas_uteis/index.md), em especial a `mascarar()` do [projeto de triagem](../modulo_02_tarefas_uteis/05_projeto_triagem.md).
- Recomendado: a aula [LGPD no dia a dia](../../seguranca_digital/modulo_04_cidadania_e_direitos/03_lgpd_no_dia_a_dia.md), do curso Segurança digital.

---

## Por que isso importa aqui

Quando o seu programa chama a API, o texto **sai do seu computador** e vai para os servidores de outra empresa. Como vimos no [Módulo 01](../modulo_01_api_de_ia/01_o_que_e_uma_api_de_ia.md#o-plano-gratuito-limites-privacidade-e-idade), no plano gratuito as mensagens **podem ser usadas** para melhorar os produtos e **lidas por revisores**. Se o programa é seu, mas os dados são **dos clientes** (ou dos alunos), a responsabilidade de protegê-los é **de quem usa os dados**: você, a padaria, a escola.

A **LGPD** (Lei nº 13.709/2018) dá as regras. Três ideias dela guiam este módulo:

| Ideia da LGPD | Onde está | No seu programa |
|---|---|---|
| **Dado pessoal** é qualquer informação que identifica uma pessoa (nome, CPF, telefone, e-mail, endereço, placa...) | art. 5º, I | Antes de enviar, pergunte: "isto identifica alguém?" |
| **Dado sensível** (saúde, religião, origem racial ou étnica, opinião política, vida sexual, biometria, genética, filiação a sindicato) tem proteção **maior** | art. 5º, II, e art. 11 | Mensagem com dado sensível **não vai** para a IA: uma pessoa responde |
| **Necessidade**: usar só o **mínimo** de dados para o objetivo | art. 6º, III | A IA precisa da **mensagem**, não do CPF, do telefone nem do nome |

E um cuidado a mais: dados de **crianças e adolescentes** devem ser tratados sempre no **melhor interesse** deles (art. 14). Num projeto da escola, **notas, nomes e fotos de alunos não vão** para a API gratuita, nunca.

## O que nunca vai, o que vai mascarado

| Situação | O que fazer |
|---|---|
| **Senhas, códigos de verificação, chaves de API** | Nunca vão, de ninguém. Se aparecer numa mensagem, ela fica para uma pessoa. |
| **Dado sensível** (ex.: "sou celíaca", "estou grávida", "tomo remédio X") | A mensagem **não vai** para a IA. |
| **E-mail, cartão, CPF, CEP, telefone** | Vão **mascarados**: `[e-mail]`, `[CPF]`... |
| **Nomes de clientes** que você conhece | Vão como **apelidos**: `[cliente 1]`. O mapa fica no seu computador. |
| **O resto da mensagem** | Vai, porque é o que a IA precisa para ajudar. |

## O código

A `mascarar()` do Módulo 02 vira o `privacidade.py`, com mais padrões e uma **avaliação** da mensagem:

```python title="privacidade.py"
"""Protege os dados pessoais ANTES de qualquer texto ir para a API."""
import re
import unicodedata
from dataclasses import dataclass, field

PADROES = [  # a ordem importa: o cartão (16 dígitos) vem antes do CPF e do telefone
    ("e-mail", re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")),
    ("cartão", re.compile(r"\b(?:\d{4}[ .-]?){3}\d{4}\b")),
    ("CPF", re.compile(r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b")),
    ("CEP", re.compile(r"\b\d{5}-\d{3}\b")),
    ("telefone", re.compile(r"(?:\(?\b\d{2}\)?\s*)?\b9?\d{4}-?\d{4}\b")),
]
SENSIVEIS = {  # pistas de dado pessoal SENSÍVEL (LGPD, art. 5º, II): a mensagem não vai para a IA
    "saúde": ["doenca", "diagnostico", "laudo", "remedio", "alergi", "alergic", "celiac",
              "diabet", "gravida", "gravidez", "intoleran"],
    "religião": ["religiao", "minha igreja", "meu terreiro"],
}
NUNCA = ["senha", "codigo de verificacao", "token"]  # segredo nunca vai, de ninguém


def sem_acento(texto: str) -> str:
    return unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode().lower()


@dataclass
class Avaliacao:
    texto: str                                          # o texto já mascarado
    trocados: list[str] = field(default_factory=list)   # tipos de dado trocados (e-mail, CPF...)
    sensiveis: list[str] = field(default_factory=list)  # motivos para NÃO enviar

    @property
    def pode_enviar(self) -> bool:
        return not self.sensiveis


def avaliar(texto: str) -> Avaliacao:
    """Mascara e-mail, cartão, CPF, CEP e telefone, e aponta o que não pode ir para a IA."""
    trocados = []
    for nome, padrao in PADROES:
        texto, quantos = padrao.subn(f"[{nome}]", texto)
        if quantos:
            trocados.append(nome)
    simples = sem_acento(texto)
    sensiveis = [tipo for tipo, pistas in SENSIVEIS.items() if any(p in simples for p in pistas)]
    sensiveis += [f"segredo ({p})" for p in NUNCA if p in simples]
    return Avaliacao(texto, trocados, sensiveis)


def pseudonimizar(texto: str, nomes: list[str]) -> tuple[str, dict[str, str]]:
    """Troca nomes conhecidos por apelidos ([cliente 1]...). O mapa fica SÓ no seu computador."""
    mapa = {}
    for i, nome in enumerate(nomes, start=1):
        apelido = f"[cliente {i}]"
        texto, quantos = re.subn(rf"\b{re.escape(nome)}\b", apelido, texto, flags=re.IGNORECASE)
        if quantos:
            mapa[apelido] = nome
    return texto, mapa


def restaurar(texto: str, mapa: dict[str, str]) -> str:
    """Devolve os nomes na resposta da IA, já no seu computador."""
    for apelido, nome in mapa.items():
        texto = texto.replace(apelido, nome)
    return texto
```

- **`subn()`** troca e diz **quantas** trocas fez: é assim que a avaliação sabe o que foi mascarado.
- As pistas de dados sensíveis são comparadas **sem acento** ("diabético", "DIABETICA" e "diabetes" caem na pista `diabet`).
- `pode_enviar` é uma **propriedade**: `avaliacao.pode_enviar`, sem parênteses.

```text
>>> avaliar("Me liga no (11) 98765-4321 ou ana.souza@example.com, CPF 123.456.789-09. Quero 2 bolos dia 14/11.")
Avaliacao(texto='Me liga no [telefone] ou [e-mail], CPF [CPF]. Quero 2 bolos dia 14/11.', trocados=['e-mail', 'CPF', 'telefone'], sensiveis=[])
>>> avaliar("Pago com o cartão 4111 1111 1111 1111, entrega no CEP 01310-100.").texto
'Pago com o cartão [cartão], entrega no CEP [CEP].'
>>> avaliar("Sou celíaca, o pão de queijo tem glúten?").pode_enviar
False
```

A data `14/11` e a quantidade `2` continuam: a IA precisa delas para entender o pedido.

### Nomes: apelidos que vão e voltam

Nomes não seguem um padrão que uma expressão regular reconheça. Mas, quando você **conhece** os nomes (o cadastro dos clientes), dá para trocá-los por apelidos antes de enviar e devolvê-los na resposta:

```text
>>> texto, mapa = pseudonimizar("A Ana pediu 2 bolos. ana vem buscar com o Bruno.", ["Ana", "Bruno", "Carla"])
>>> texto
'A [cliente 1] pediu 2 bolos. [cliente 1] vem buscar com o [cliente 2].'
>>> mapa
{'[cliente 1]': 'Ana', '[cliente 2]': 'Bruno'}
>>> restaurar("Olá, [cliente 1]! O bolo fica pronto às 16h.", mapa)
'Olá, Ana! O bolo fica pronto às 16h.'
```

A IA trabalha com `[cliente 1]`; o nome de verdade **nunca sai** do seu computador.

### O que os testes acharam

Testar com mensagens de verdade (inventadas, mas realistas) mostrou dois limites, e os dois ficaram assim de propósito:

- **`11987654321`**, um celular escrito sem espaços, vira **`[CPF]`**: tem 11 dígitos, como um CPF sem pontos. O rótulo sai errado, mas o número **foi mascarado**, que é o que importa.
- **"Não tenho alergia a nada"** é barrada como dado de saúde. É um **falso alarme**: a mensagem vai para uma pessoa responder. Errar para o lado da proteção custa pouco; deixar passar um dado de saúde custa muito.

!!! warning "Mascarar diminui o risco; não zera"
    Nomes que você não conhece, endereços escritos por extenso ("moro na casa azul perto da praça") e combinações de detalhes ainda podem identificar alguém. Para dados de clientes de verdade, o caminho seguro é um **plano pago** com termos de privacidade adequados (e um contrato), ou **não usar** a API para aquilo.

---

## ⚠️ Erros comuns

- **Mascarar depois de enviar**: a avaliação vem **antes** de qualquer chamada à API.
- **Mandar a linha inteira do cadastro** (nome, CPF, telefone, mensagem) quando a IA só precisa da mensagem.
- **Guardar o mapa de apelidos junto com o que vai para a API**: ele fica só no seu computador.
- **Achar que dado de saúde "não tem problema" porque o cliente escreveu por conta própria**: a proteção é para a pessoa, não para quem recebeu.
- **Usar dados de alunos** (nomes, notas, fotos) para "testar" a API gratuita.

---

## Exercícios

### Básico (fixação)

Avalie as quatro mensagens e mostre, para cada uma, o texto mascarado e se pode ir para a IA.

```text
Meu e-mail é bruno@example.com, vocês fazem bolo de aniversário?
Estou grávida e com desejo de sonho, tem hoje?
Quero 3 coxinhas para retirar às 17h.
O código de verificação que chegou é 482913, pode confirmar meu pedido?
```

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```python
    from privacidade import avaliar

    mensagens = [
        "Meu e-mail é bruno@example.com, vocês fazem bolo de aniversário?",
        "Estou grávida e com desejo de sonho, tem hoje?",
        "Quero 3 coxinhas para retirar às 17h.",
        "O código de verificação que chegou é 482913, pode confirmar meu pedido?",
    ]
    avaliacoes = [avaliar(m) for m in mensagens]
    for a in avaliacoes:
        print("pode enviar" if a.pode_enviar else f"NÃO ENVIAR ({', '.join(a.sensiveis)})", "|", a.texto)
    ```

    Só a primeira (com `[e-mail]`) e a terceira (sem nada a trocar) podem ir. A segunda tem dado de **saúde** (gravidez); a quarta, um **código de verificação**, que é um segredo: quem pede esse código quase sempre é golpista, e nenhum programa deve repassá-lo.

### Intermediário (aplicação)

Use `pseudonimizar()` e o `ClienteFalso` para "responder" à mensagem `"Oi, aqui é a Bruna, meu bolo de cenoura fica pronto que horas?"`. O falso responde `"Olá, [cliente 2]! O bolo fica pronto às 16h."`. Os nomes do cadastro são `Ana`, `Bruna` e `Carla`. Mostre o que foi para a API e a resposta final.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```python
    from cliente_falso import ClienteFalso
    from privacidade import pseudonimizar, restaurar

    mensagem = "Oi, aqui é a Bruna, meu bolo de cenoura fica pronto que horas?"
    texto, mapa = pseudonimizar(mensagem, ["Ana", "Bruna", "Carla"])
    falso = ClienteFalso("Olá, [cliente 2]! O bolo fica pronto às 16h.")
    resposta = falso.interactions.create(model="gemini-3.8-flash", input=texto)
    final = restaurar(resposta.output_text, mapa)
    print("Foi para a API:", falso.pedidos[0]["input"])
    print("Resposta final:", final)
    ```

    Para a API foi `Oi, aqui é a [cliente 2], meu bolo...`; a resposta final é `Olá, Bruna! O bolo fica pronto às 16h.`. A Bruna é o `[cliente 2]` porque é o **segundo** nome da lista; a Ana e a Carla não aparecem no mapa, porque não estavam na mensagem.

### Avançado (desafio)

O celular `11987654321` vira `[CPF]`. Acrescente à lista `PADROES` (sem mudar o resto) um padrão para **celular sem espaços** (2 dígitos de DDD, o 9 e mais 8 dígitos) que seja testado **antes** do CPF, e confira com `"Meu zap é 11987654321"` e `"CPF 12345678909"`.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```python
    import re

    import privacidade

    posicao_cpf = [nome for nome, _ in privacidade.PADROES].index("CPF")
    privacidade.PADROES.insert(posicao_cpf, ("telefone", re.compile(r"\b\d{2}9\d{8}\b")))

    textos = [privacidade.avaliar(t).texto for t in ["Meu zap é 11987654321", "CPF 12345678909"]]
    print(textos)
    ```

    `['Meu zap é [telefone]', 'CPF [CPF]']`. Um CPF que tenha o **9** na terceira posição também viraria `[telefone]`: com 11 dígitos soltos, não há como ter certeza. O rótulo pode errar; o número **nunca** passa sem máscara, e é isso que a lista garante.

---

## 💡 Resumo

- **LGPD:** dado pessoal identifica alguém; dado **sensível** tem proteção maior; use só o **necessário**.
- Segredos e dados sensíveis **não vão**; e-mail, cartão, CPF, CEP e telefone vão **mascarados**; nomes conhecidos, como **apelidos**.
- A **avaliação** vem antes de qualquer chamada. Na dúvida, a mensagem vai para uma pessoa.

## ➡️ Próximo passo

**[02 — Prompt injection: quando a mensagem tenta dar ordens](02_prompt_injection.md)**.
