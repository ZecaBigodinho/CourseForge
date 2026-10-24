# 02 — O motor simulado e a conversa

> **Curso:** Introdução à IA  
> **Módulo:** 05 — Projeto: seu mini-assistente  
> **Tempo estimado:** 2 h  

---

## Objetivos

Ao final desta aula, você será capaz de:

- Escrever o **motor simulado**: uma classe que responde por **palavras-chave**.
- Escrever o **laço de conversa** no terminal, com os comandos `/nova` e `/sair`.
- Entender por que a função de conversa recebe `entrada` e `saida` como **parâmetros**.
- Ampliar o motor com novos temas e comandos.

## Pré-requisitos

- [Aula 01](01_planejando_o_mini_assistente.md): a especificação e o ambiente prontos.
- Python básico: `if`, `for`, `while`, funções, dicionários e listas. Classes simples ajudam (o [Módulo 02 do curso de Python](../../python_para_desktop/modulo_07_poo/index.md) explica), mas a aula mostra tudo o que você precisa.

---

## O motor simulado

Crie o arquivo `motores.py`:

```python title="motores.py"
"""Motores do mini-assistente: um simulado (sem internet) e um com a API do Gemini."""


class MotorSimulado:
    """Responde por palavras-chave. Funciona sem conta, sem chave e sem internet."""

    RESPOSTAS = {
        "fotossíntese": "Vamos por partes: de onde você acha que a planta tira energia?",
        "equação": "Qual seria o primeiro passo para deixar o x sozinho de um lado?",
        "redação": "Qual é a sua tese, em uma frase?",
    }
    NAO_SEI = "Ainda não sei ajudar com isso. Tente perguntar sobre fotossíntese, equação ou redação."

    def __init__(self):
        self.historico = []

    def responder(self, pergunta: str) -> str:
        self.historico.append(pergunta)
        texto = pergunta.lower()
        for chave, resposta in self.RESPOSTAS.items():
            if chave in texto:
                return resposta
        return self.NAO_SEI

    def nova_conversa(self):
        self.historico.clear()
```

Como funciona:

- `RESPOSTAS` é um **dicionário**: a palavra-chave e a resposta (no estilo tutor: uma **pergunta** de volta).
- `responder()` guarda a pergunta no **histórico**, passa o texto para **minúsculas** (assim “FOTOSSÍNTESE” também funciona) e devolve a resposta da **primeira** palavra-chave encontrada. Se nenhuma aparece, devolve `NAO_SEI` — o motor **diz que não sabe** em vez de inventar.
- `nova_conversa()` limpa o histórico.

!!! info "Isso é IA?"
    Não: é um programa com **regras escritas** (Módulo 01, aula 01). É de propósito — ele deixa você construir e testar o resto do assistente sem conta, sem internet e sem custo. Na aula 03, quem tem 18 anos ou mais troca por um modelo de IA de verdade.

---

## A conversa no terminal

Crie o arquivo `assistente.py` (esta é a **primeira versão**; ele cresce nas próximas aulas):

```python title="assistente.py"
"""Mini-assistente de estudos no terminal."""
from motores import MotorSimulado


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
        saida("Assistente: " + motor.responder(pergunta))


if __name__ == "__main__":
    conversar(MotorSimulado())
```

Rode com `python assistente.py` e converse.

- O `while True` repete até o `/sair` (`break`). Mensagens **vazias** são ignoradas (`continue`).
- `conversar()` recebe **qualquer** motor: só precisa ter `responder()` e `nova_conversa()`.

!!! tip "Por que `entrada=input` e `saida=print`?"
    Normalmente, a função usa o teclado (`input`) e a tela (`print`). Mas, nos **testes** da aula 04, vamos passar no lugar uma lista de mensagens prontas e guardar as respostas — assim os testes rodam **sozinhos**, sem ninguém digitar. Deixar as dependências como parâmetro é o que torna o programa **testável**.

---

??? note "Equivalentes e alternativas"
    | Situação | Como fazer |
    |---|---|
    | Ambiente on-line de Python (sem instalar) | Os dois arquivos funcionam iguais; alguns ambientes pedem tudo em um arquivo só — cole a classe antes da função |
    | Interface gráfica em vez do terminal | Possível com Tkinter ou CustomTkinter ([Módulo 03 do curso de Python](../../python_para_desktop/modulo_02_interfaces_graficas/index.md)): o motor continua o mesmo |

---

## ⚠️ Erros comuns

- **Esquecer o `.lower()`**: “Fotossíntese” com F maiúsculo não é encontrada.
- **Chave com acento diferente**: “fotossintese” (sem acento) não bate com “fotossíntese”. Acrescente as duas formas, se precisar.
- **Ordem das chaves:** a **primeira** encontrada vence. Palavras mais específicas (como “prova”) vêm primeiro.
- **Esquecer o `break`** no `/sair`: o programa nunca termina.

---

## Exercícios

### Básico (fixação)

Acrescente ao motor: (1) uma resposta para **porcentagem**; (2) uma resposta que **recuse** fazer a **prova**, e que funcione mesmo em “Faça a minha prova de equação”.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```python title="motores.py — novo dicionário RESPOSTAS"
    RESPOSTAS = {
        "prova": "Não posso fazer a sua prova, mas posso ajudar você a estudar. Que tema vai cair?",
        "fotossíntese": "Vamos por partes: de onde você acha que a planta tira energia?",
        "equação": "Qual seria o primeiro passo para deixar o x sozinho de um lado?",
        "redação": "Qual é a sua tese, em uma frase?",
        "porcentagem": "Se 100% é o todo, quanto vale 1%? Comece por aí.",
    }
    ```

    **Por que “prova” é a primeira:** em “Faça a minha prova de equação” aparecem as duas palavras. Como a **primeira** chave encontrada vence, “prova” precisa vir antes de “equação” — senão o assistente ajudaria com a equação da prova.

### Intermediário (aplicação)

Crie o comando **`/historico`**, que mostra **quantas perguntas** foram feitas na conversa atual. Teste: duas perguntas, `/historico`, `/nova`, `/historico`.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    Dentro do `while`, junto com os outros comandos:

    ```python title="assistente.py — novo comando"
    if pergunta == "/historico":
        saida(f"(você fez {len(motor.historico)} pergunta(s) nesta conversa)")
        continue
    ```

    E atualize a primeira mensagem: `"Comandos: /nova, /historico e /sair."`

    **Teste:** “redação”, “equação”, `/historico` ➔ `(você fez 2 pergunta(s) nesta conversa)`; `/nova`; `/historico` ➔ `(você fez 0 pergunta(s) nesta conversa)`. Os comandos **não** entram no histórico, porque o `continue` volta ao começo antes do `responder()`.

### Avançado (desafio)

Hoje cada resposta tem **uma** palavra-chave. Reescreva o motor para que cada **tema** tenha **várias** palavras (por exemplo, fotossíntese, clorofila e planta levam à mesma resposta), sem repetir a resposta no código.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    Uma solução: uma lista de **temas**, cada um com uma **tupla** de palavras e a resposta.

    ```python title="motores.py — MotorSimulado com temas"
    class MotorSimulado:
        """Responde por palavras-chave. Funciona sem conta, sem chave e sem internet."""

        TEMAS = [
            (("fotossíntese", "clorofila", "planta"), "Vamos por partes: de onde você acha que a planta tira energia?"),
            (("equação", "bhaskara", "incógnita"), "Qual seria o primeiro passo para deixar o x sozinho de um lado?"),
            (("redação", "dissertação", "tese"), "Qual é a sua tese, em uma frase?"),
        ]
        NAO_SEI = "Ainda não sei ajudar com isso. Tente perguntar sobre fotossíntese, equação ou redação."

        def __init__(self):
            self.historico = []

        def responder(self, pergunta: str) -> str:
            self.historico.append(pergunta)
            texto = pergunta.lower()
            for palavras, resposta in self.TEMAS:
                if any(p in texto for p in palavras):
                    return resposta
            return self.NAO_SEI

        def nova_conversa(self):
            self.historico.clear()
    ```

    `any(...)` é verdadeiro se **pelo menos uma** palavra do tema aparece no texto. **Teste:** “O que é clorofila?” e “fórmula de Bhaskara” devem cair nos temas certos; “futebol”, no `NAO_SEI`.

---

## 💡 Resumo

- `MotorSimulado`: dicionário de **palavras-chave**, texto em minúsculas, primeira chave vence, `NAO_SEI` quando não sabe.
- `conversar()`: laço `while True` com `/nova` e `/sair`, que funciona com **qualquer** motor.
- `entrada` e `saida` como parâmetros deixam o programa **testável**.
- Ordem das chaves importa; temas com várias palavras deixam o motor mais útil.

## ➡️ Próximo passo

**[03 — Conectando a uma API de IA](03_conectando_a_uma_api.md)**: o motor com um modelo de IA de verdade (18 anos ou mais) e a chave guardada com segurança.
