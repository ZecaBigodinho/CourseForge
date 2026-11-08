# 03 — Instruções de sistema e ajustes

> **Curso:** IA na prática com Python  
> **Módulo:** 01 — Conversando com um modelo por API  
> **Tempo estimado:** 1 h 30 min  

---

## 🎯 Objetivos

Ao final desta aula, você será capaz de:

- Usar as **instruções de sistema** (`system_instruction`) para definir o papel, o tom e as regras da IA.
- Separar **instruções** (fixas do programa) de **pedido** (o que muda a cada vez).
- Usar o **nível de raciocínio** (`thinking_level`) para equilibrar qualidade, tempo e tokens.
- Saber por que a **temperatura** fica no padrão nos modelos Gemini 3.

## Pré-requisitos

- [Aula 02](02_primeira_chamada.md): a primeira chamada e o cliente falso.

---

## Instruções de sistema × pedido

| | Instruções de sistema | Pedido (`input`) |
|---|---|---|
| O que é | O **papel** e as **regras** da IA no seu programa | A tarefa da vez |
| Quem escreve | Você, programador, uma vez | O usuário, ou o programa a cada item |
| Exemplo | "Você escreve legendas para uma padaria, em até 2 frases, sem inventar preços." | "Legenda do bolo de fubá." |

Separar os dois é como o **C-T-F-R** (contexto, tarefa, formato, restrições) da [Introdução à IA](../../introducao_a_ia/modulo_02_usando_assistentes/index.md): o contexto, o formato e as restrições vão nas **instruções**; a tarefa, no **pedido**. Assim o usuário não precisa repetir as regras, e elas não "se perdem" no meio da conversa.

## Comparando instruções

```python title="comparar_instrucoes.py"
import os
import sys

from dotenv import load_dotenv
from google import genai

from erros_ia import explicar_erro

PEDIDO = "Escreva a legenda de um post anunciando o bolo de fubá da Padaria Pão Quente."
REGRAS = " Escreva em português do Brasil, em no máximo 2 frases, sem inventar preços nem promoções."
INSTRUCOES = {
    "formal": "Você escreve para uma padaria tradicional, com tom educado e sóbrio, sem emojis." + REGRAS,
    "descontraído": "Você escreve para uma padaria de bairro, com tom alegre e próximo, com 1 emoji." + REGRAS,
}


def pedir(cliente, modelo: str, instrucoes: str) -> str:
    resposta = cliente.interactions.create(
        model=modelo,
        input=PEDIDO,
        system_instruction=instrucoes,
        generation_config={"thinking_level": "low"},
    )
    return resposta.output_text


def main() -> int:
    load_dotenv()
    if not os.getenv("GEMINI_API_KEY"):
        print("Falta a GEMINI_API_KEY no arquivo .env (veja a aula 01).")
        return 1
    cliente = genai.Client()
    modelo = os.getenv("GEMINI_MODELO", "gemini-3.8-flash")
    for estilo, instrucoes in INSTRUCOES.items():
        print(f"\n=== {estilo} ===")
        for vez in (1, 2):  # o mesmo pedido duas vezes: as respostas variam
            try:
                print(f"{vez}. {pedir(cliente, modelo, instrucoes)}")
            except Exception as erro:
                print(f"A API não respondeu: {explicar_erro(erro)}")
                return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

Rode com a chave configurada e compare as quatro legendas. O que você deve observar:

- As duas legendas do mesmo estilo **não são idênticas**: o modelo escolhe palavras de um jeito que varia a cada pedido.
- Mesmo variando, cada estilo **segue as instruções**: o formal sem emojis, o descontraído com um emoji, os dois com no máximo 2 frases.
- Nenhuma legenda deve trazer preço ou promoção: a restrição está nas instruções. Se aparecer, a instrução precisa ficar mais clara (ou o programa precisa conferir a resposta: veja o desafio).

!!! warning "As instruções valem só para aquele pedido"
    Na API de interações do Gemini, `system_instruction` e `generation_config` valem **para cada pedido**: numa conversa ([aula 04](04_conversa_e_motores.md)), mande de novo a cada mensagem. Os motores do curso já fazem isso.

## Os ajustes: `generation_config`

| Ajuste | O que faz | Neste curso |
|---|---|---|
| `thinking_level` | Quanto o modelo "pensa" antes de responder: `"minimal"`, `"low"`, `"medium"` ou `"high"` | `"low"` para tarefas simples (resumir, classificar): mais rápido e gasta menos tokens. `"high"` para problemas com várias etapas. |
| `max_output_tokens` | Limite de tamanho da resposta | Use com folga: em modelos que raciocinam, um limite baixo pode cortar a resposta no meio. Para respostas curtas, prefira pedir o tamanho **nas instruções** ("em até 2 frases"). |
| `temperature` | O quanto as escolhas de palavras variam | **Deixe no padrão.** A documentação do Google recomenda manter a temperatura em **1,0** nos modelos Gemini 3: valores mais baixos podem causar repetições e piorar o raciocínio. |

!!! info "E se eu quiser respostas sempre iguais?"
    Em muitos tutoriais antigos, a receita era "temperatura 0". Nos modelos atuais do Gemini, o caminho é outro: instruções **bem específicas** (formato fixo, exemplos de resposta) e, quando o programa precisa de dados exatos, pedir **JSON** e conferir o resultado (Módulo 02 do curso).

---

## ⚠️ Erros comuns

- **Regras do programa no pedido do usuário**: o usuário pode apagar ou contrariar. Regras fixas vão nas **instruções**.
- **Instruções vagas** ("seja legal"): diga o tom, o tamanho, o formato e o que **não** fazer.
- **Baixar a temperatura** em modelos Gemini 3 para "ficar mais certinho".
- **`max_output_tokens` pequeno demais**: resposta cortada ou vazia.
- **Esperar que as instruções garantam tudo**: são fortes, mas não absolutas. Para regras importantes, o programa confere a resposta.

---

## Exercícios

### Básico (fixação)

Escreva as **instruções de sistema** para um assistente que tira dúvidas de **matemática** de alunos do 9º ano: tom paciente, explicação em passos numerados, no máximo 5 passos, e sem dar só a resposta final. Teste com o `ClienteFalso` e confira que as instruções foram no pedido.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```python
    from cliente_falso import ClienteFalso

    INSTRUCOES = ("Você ajuda alunos do 9º ano com matemática. Seja paciente e explique em passos numerados, "
                  "no máximo 5 passos. Não dê só a resposta final: mostre o raciocínio. "
                  "Responda em português do Brasil.")

    cliente = ClienteFalso("1. Primeiro, ...")
    cliente.interactions.create(model="gemini-3.8-flash", input="Como resolvo 2x + 3 = 11?",
                                system_instruction=INSTRUCOES, generation_config={"thinking_level": "low"})
    pedido = cliente.pedidos[0]
    print(pedido["system_instruction"])
    ```

    Repare que a **tarefa** (a equação) está no `input`, e o **jeito de responder** nas instruções. Para outra dúvida, só o `input` muda.

### Intermediário (aplicação)

Com o `ClienteFalso`, confira que o `comparar_instrucoes.py` faz **4 pedidos**, que os dois primeiros usam as instruções do estilo formal e os dois últimos as do descontraído, e que **todos** levam `thinking_level: "low"`.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```python
    import os
    import runpy

    import google.genai as genai

    from cliente_falso import ClienteFalso

    os.environ["GEMINI_API_KEY"] = "chave-falsa-para-teste"
    falso = ClienteFalso("Legenda de teste.")
    genai.Client = lambda *args, **kwargs: falso   # o programa vai usar o falso

    try:
        runpy.run_path("comparar_instrucoes.py", run_name="__main__")
    except SystemExit:
        pass

    estilos = ["formal" if "sóbrio" in p["system_instruction"] else "descontraído" for p in falso.pedidos]
    print(estilos)
    print({p["generation_config"]["thinking_level"] for p in falso.pedidos})
    ```

    `runpy.run_path` roda o arquivo como se fosse pelo terminal. Antes, trocamos `genai.Client` pelo falso: o programa nem percebe. Saída: `['formal', 'formal', 'descontraído', 'descontraído']` e `{'low'}`.

### Avançado (desafio)

As instruções dizem "sem inventar preços", mas a IA pode errar. Escreva a função `tem_preco(texto)` que detecta preços (`R$ 10`, `R$12,90`, `10 reais`) numa legenda, para o programa **descartar** a resposta e pedir de novo.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```python
    import re

    PRECO = re.compile(r"R\$\s*\d+([.,]\d{2})?|\d+([.,]\d{2})?\s*reais", re.IGNORECASE)


    def tem_preco(texto: str) -> bool:
        return bool(PRECO.search(texto))


    exemplos = {
        "Bolo de fubá quentinho te esperando!": False,
        "Bolo de fubá por R$ 12,90!": True,
        "Só hoje: 10 reais o bolo!": True,
        "Bolo de fubá, receita da vó.": False,
    }
    resultados = {texto: tem_preco(texto) for texto in exemplos}
    for texto, achou in resultados.items():
        print(f"{achou!s:5} {texto}")
    ```

    Instruções **orientam**; o código **confere**. Para regras que não podem falhar (preço errado num anúncio, dado pessoal numa resposta), essa dupla é o padrão: se `tem_preco()` for verdadeiro, o programa pede de novo ou avisa uma pessoa.

---

## 💡 Resumo

- **Instruções de sistema** = papel, tom, formato e regras (fixos); **pedido** = a tarefa da vez.
- `system_instruction` e `generation_config` vão em **cada** pedido.
- `thinking_level` (`"low"` para tarefas simples); `max_output_tokens` com folga; **temperatura no padrão** nos Gemini 3.
- Instruções orientam; para regras importantes, o **código confere** a resposta.

## ➡️ Próximo passo

**[04 — Conversa com memória e motores](04_conversa_e_motores.md)**.

---

*Parâmetros conferidos em 08/11/2026 na biblioteca `google-genai` 2.34.0 e no guia do Gemini 3 do Google (recomendação de temperatura).*
