# 04 — Segurança e testes

> **Curso:** Introdução à IA  
> **Módulo:** 05 — Projeto: seu mini-assistente  
> **Tempo estimado:** 2 h  

---

## Objetivos

Ao final desta aula, você será capaz de:

- Escrever um **filtro** que impede mensagens com **CPF**, **telefone** ou **e-mail** de saírem do computador.
- Entender o básico de **expressões regulares** e os **limites** desse tipo de filtro.
- Escrever **testes automáticos** que conferem o assistente **sem internet e sem chave**.
- Testar o motor da API com um **cliente falso**.
- Avaliar as **respostas** do assistente com casos de teste.

## Pré-requisitos

- [Aula 03](03_conectando_a_uma_api.md): `motores.py` com os dois motores e `assistente.py` com `criar_motor()`.
- [Módulo 04, aula 01](../modulo_04_etica_e_privacidade/01_privacidade_e_dados_pessoais.md): dados pessoais.

---

## O filtro de segurança

Crie o arquivo `seguranca.py`:

```python title="seguranca.py"
"""Confere a mensagem antes de ela sair do computador."""
import re

PADROES = {
    "CPF": r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b",
    "telefone": r"\(?\b\d{2}\)?\s?9?\d{4}-?\d{4}\b",
    "e-mail": r"\b[\w.+-]+@[\w-]+\.[\w.]+\b",
}
LIMITE = 1500  # caracteres por mensagem


def problemas(texto: str) -> list[str]:
    """Lista o que impede a mensagem de ser enviada (vazia = pode enviar)."""
    achados = [nome for nome, padrao in PADROES.items() if re.search(padrao, texto)]
    if len(texto) > LIMITE:
        achados.append(f"mais de {LIMITE} caracteres")
    return achados
```

### Expressões regulares em 1 minuto

Uma **expressão regular** descreve um **padrão** de texto. As peças usadas aqui:

| Peça | Significa | No padrão do CPF |
|---|---|---|
| `\d` | um dígito | |
| `\d{3}` | exatamente 3 dígitos | os blocos `123`, `456`, `789` |
| `\.?` | um ponto **opcional** (`?` = pode ter ou não) | aceita `123.456` e `123456` |
| `-?` | um hífen opcional | aceita `-00` e `00` |
| `\b` | borda de palavra | não pega um pedaço de um número maior |
| `[\w.+-]+` | uma ou mais letras, números, `.`, `+` ou `-` | (no e-mail: a parte antes do `@`) |

`re.search(padrao, texto)` procura o padrão **em qualquer lugar** do texto.

!!! warning "O filtro ajuda, mas não pega tudo"
    Ele reconhece **formatos** (CPF, telefone, e-mail). **Não** reconhece um nome, um endereço escrito por extenso, uma doença, uma nota. Por isso as instruções da tela e as regras da sua carta (Módulo 04) continuam valendo: **o filtro é uma rede de proteção, não a única proteção**.

### Ligando o filtro na conversa

No `assistente.py`, importe o filtro e confira a mensagem **antes** de chamar o motor:

```python title="assistente.py"
"""Mini-assistente de estudos no terminal."""
import os

from dotenv import load_dotenv

from motores import MotorGemini, MotorSimulado
from seguranca import problemas

INSTRUCOES = (
    "Você é um tutor de estudos para estudantes brasileiros. Responda em português do Brasil, "
    "com frases curtas. Não dê a resposta pronta de exercícios: faça uma pergunta por vez para "
    "o estudante chegar à resposta. Se não souber algo, diga que não sabe. "
    "Recuse pedidos para fazer provas ou trabalhos inteiros."
)


def criar_motor():
    load_dotenv()
    if os.getenv("GEMINI_API_KEY"):
        return MotorGemini(INSTRUCOES, os.getenv("GEMINI_MODELO", "gemini-3.8-flash"))
    return MotorSimulado()


def conversar(motor, entrada=input, saida=print):
    saida("Mini-assistente de estudos. Comandos: /nova (conversa nova) e /sair.")
    while True:
        pergunta = entrada("Você: ").strip()
        if not pergunta:
            continue
        if pergunta == "/sair":
            saida("Até logo!")
            break
        if pergunta == "/nova":
            motor.nova_conversa()
            saida("(conversa nova)")
            continue
        achados = problemas(pergunta)
        if achados:
            saida(f"Assistente: não enviei a mensagem ({', '.join(achados)}). Ajuste e tente de novo.")
            continue
        try:
            saida("Assistente: " + motor.responder(pergunta))
        except Exception as erro:
            saida(f"Assistente: não consegui responder agora ({type(erro).__name__}). Tente de novo em instantes.")


if __name__ == "__main__":
    conversar(criar_motor())
```

(Se você fez o exercício avançado da aula 03, mantenha o `explicar_erro()` no `except`.)

---

## Testes automáticos

Testar à mão toda vez cansa e esquece casos. Um **arquivo de testes** confere tudo em segundos — e roda **sem internet e sem chave**, porque usa o motor simulado e um **cliente falso** no lugar da API.

```python title="teste_assistente.py"
"""Testes do mini-assistente: rodam sem internet e sem chave."""
from types import SimpleNamespace

from assistente import conversar
from motores import MotorGemini, MotorSimulado
from seguranca import problemas


def rodar(motor, mensagens):
    falas = []
    entradas = iter(mensagens)
    conversar(motor, entrada=lambda _: next(entradas), saida=falas.append)
    return falas


# 1. Motor simulado
m = MotorSimulado()
assert m.responder("Me explica a FOTOSSÍNTESE?").startswith("Vamos por partes")
assert m.responder("Quem ganhou a Copa?") == MotorSimulado.NAO_SEI
assert len(m.historico) == 2
m.nova_conversa()
assert m.historico == []

# 2. Segurança
assert problemas("Como resolvo uma equação do 2º grau?") == []
assert problemas("Meu CPF é 123.456.789-00") == ["CPF"]
assert problemas("me liga no (11) 98888-7777") == ["telefone"]
assert problemas("escreve para ana.souza@escola.example") == ["e-mail"]
assert problemas("a" * 1501) == ["mais de 1500 caracteres"]

# 3. Conversa completa
falas = rodar(MotorSimulado(), ["", "redação?", "meu email é a@b.com", "/nova", "/sair"])
assert falas[1] == "Assistente: Qual é a sua tese, em uma frase?"
assert "não enviei" in falas[2] and "e-mail" in falas[2]
assert falas[3] == "(conversa nova)" and falas[4] == "Até logo!"


# 4. Motor do Gemini com um cliente falso (não acessa a internet)
class InteracoesFalsas:
    def __init__(self):
        self.pedidos = []

    def create(self, **pedido):
        self.pedidos.append(pedido)
        return SimpleNamespace(id=f"id{len(self.pedidos)}", output_text=f"resposta {len(self.pedidos)}")


falso = InteracoesFalsas()
g = MotorGemini("instruções", "modelo-teste", cliente=SimpleNamespace(interactions=falso))
assert g.responder("oi") == "resposta 1"
assert "previous_interaction_id" not in falso.pedidos[0]
assert g.responder("e agora?") == "resposta 2"
assert falso.pedidos[1]["previous_interaction_id"] == "id1"
assert falso.pedidos[1]["system_instruction"] == "instruções"
g.nova_conversa()
g.responder("começo")
assert "previous_interaction_id" not in falso.pedidos[2]


# 5. Erro da API não derruba o programa
class Quebrado:
    def responder(self, _):
        raise RuntimeError("limite de uso")

    def nova_conversa(self):
        pass


falas = rodar(Quebrado(), ["oi", "/sair"])
assert "RuntimeError" in falas[1]

print("todos os testes passaram")
```

Rode com `python teste_assistente.py`. Se tudo estiver certo, aparece `todos os testes passaram`. Se um `assert` falhar, o Python mostra **qual linha** — e você sabe exatamente o que quebrou.

!!! tip "O cliente falso"
    `InteracoesFalsas` imita a parte da biblioteca do Google que o motor usa (`interactions.create`). Ele **guarda os pedidos** e devolve respostas inventadas. Assim o teste confere se o motor **manda o pedido certo** (instruções, id da conversa anterior) sem gastar a cota nem precisar de chave. (Se você fez o `explicar_erro()`, troque o teste 5 para conferir a sua mensagem.)

---

## Avaliando as respostas

Os testes conferem o **programa**. As **respostas** de uma IA de verdade variam (Módulo 01, aula 04) e precisam ser avaliadas por você. Use os seis casos da aula 01 e anote, para cada um: a resposta e se ela seguiu a regra (✔ ou ✘). Se uma regra falhar várias vezes, deixe as **instruções** mais claras (aula 03, exercício intermediário).

---

## ⚠️ Erros comuns

- **Conferir a mensagem depois de enviar.** O filtro tem de vir **antes** do `motor.responder()`.
- **Achar que o filtro protege de tudo.** Ele só reconhece formatos.
- **Testes que dependem da internet** — falham quando a rede cai e gastam a cota. Use o cliente falso.
- **Apagar um teste que falhou** em vez de consertar o programa.

---

## Exercícios

### Básico (fixação)

1. Rode `teste_assistente.py` e confira a mensagem `todos os testes passaram`.
2. **Quebre** o programa de propósito: no `MotorSimulado`, apague o `.lower()`. Rode os testes de novo. Qual teste falhou e por quê? Depois, desfaça a mudança.

<!-- gabarito -->
??? success "Gabarito — Básico"
    1. Saída: `todos os testes passaram`.
    2. Sem o `.lower()`, o texto “Me explica a FOTOSSÍNTESE?” fica em maiúsculas e não contém a chave “fotossíntese” (em minúsculas). O **primeiro teste** (`assert m.responder("Me explica a FOTOSSÍNTESE?").startswith("Vamos por partes")`) falha com `AssertionError`, e o Python mostra a linha. É exatamente para isso que o teste existe: pegar uma mudança que estragou algo sem você perceber.

### Intermediário (aplicação)

Faça o filtro bloquear também mensagens que contenham a palavra **senha** (com qualquer combinação de maiúsculas e minúsculas) e acrescente **dois testes**: um que bloqueia e um que deixa passar.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    Em `seguranca.py`, uma lista de palavras e mais uma verificação na função:

    ```python title="seguranca.py — palavras proibidas"
    PALAVRAS = ("senha", "password")


    def problemas(texto: str) -> list[str]:
        """Lista o que impede a mensagem de ser enviada (vazia = pode enviar)."""
        achados = [nome for nome, padrao in PADROES.items() if re.search(padrao, texto)]
        if any(p in texto.lower() for p in PALAVRAS):
            achados.append("senha")
        if len(texto) > LIMITE:
            achados.append(f"mais de {LIMITE} caracteres")
        return achados
    ```

    Testes novos:

    ```python title="teste_assistente.py — acrescentar na parte 2"
    assert problemas("minha SENHA é 1234") == ["senha"]
    assert problemas("como faço uma equação?") == []
    ```

### Avançado (desafio)

Um filtro que bloqueia **demais** atrapalha o estudo. Escreva testes que garantam que estas mensagens **não** são bloqueadas — e, se alguma for, ajuste o padrão:

- “Quanto é 15% de 80?”
- “A prova é dia 20/11/2026”
- “O ano de 1500”
- “Custa R$ 1.250,00”
- “A população é de 203 milhões”
- “A Lei 13.709/2018”

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```python title="teste_assistente.py — acrescentar na parte 2"
    for mensagem in [
        "Quanto é 15% de 80?",
        "A prova é dia 20/11/2026",
        "O ano de 1500",
        "Custa R$ 1.250,00",
        "A população é de 203 milhões",
        "A Lei 13.709/2018",
    ]:
        assert problemas(mensagem) == [], (mensagem, problemas(mensagem))
    ```

    Com os padrões da aula, **todas passam** (nenhuma tem o formato de CPF, telefone ou e-mail). O `, (mensagem, problemas(mensagem))` depois do `assert` faz o Python mostrar **qual** mensagem foi bloqueada e **por quê**, se algum dia um ajuste no padrão criar um **falso positivo** (Módulo 01, aula 02) — o mesmo tipo de erro dos filtros de spam.

---

## 💡 Resumo

- **Filtro** com expressões regulares para **CPF**, **telefone** e **e-mail**, aplicado **antes** de enviar — uma rede de proteção, não a única.
- **Testes automáticos** com `assert`, rodando **sem internet**: motor simulado, conversa completa e um **cliente falso** no lugar da API.
- Testes protegem contra mudanças que quebram algo sem você perceber; **falsos positivos** também precisam de teste.
- As **respostas** da IA real são avaliadas por você, com os casos da aula 01.

## ➡️ Próximo passo

**[05 — Projeto final: entregando o seu mini-assistente](05_projeto_final_entrega.md)**: personalizar, documentar, demonstrar e avaliar o seu assistente.
