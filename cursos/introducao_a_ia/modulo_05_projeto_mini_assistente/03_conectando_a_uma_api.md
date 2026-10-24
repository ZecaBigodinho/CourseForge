# 03 — Conectando a uma API de IA

> **Curso:** Introdução à IA  
> **Módulo:** 05 — Projeto: seu mini-assistente  
> **Tempo estimado:** 2 h  

---

## Objetivos

Ao final desta aula, você será capaz de:

- Explicar o que é uma **API** e uma **chave de API**.
- Guardar a chave com segurança no **`.env`** e mantê-la **fora do Git**.
- Escrever o **`MotorGemini`**, que conversa com um modelo de IA do Google e **lembra** da conversa.
- Escolher o motor **automaticamente**: com chave, o da API; sem chave, o simulado.
- **Tratar erros** da API (chave errada, limite de uso, sem internet) sem o programa quebrar.

## Pré-requisitos

- [Aula 02](02_motor_simulado_e_conversa.md): `motores.py` e `assistente.py` funcionando.
- **Para criar a chave: 18 anos ou mais** e uma conta Google pessoal (aula 01). Quem segue o **caminho A** faz a aula inteira **sem** chave: o programa continua usando o motor simulado.

---

## O que é uma API

Uma **API** é uma “porta” que um programa usa para conversar com outro. Em vez de você digitar no site do assistente, o **seu programa** manda a pergunta pela internet e recebe a resposta.

A **chave de API** é como uma **senha** do seu programa: identifica quem está usando, controla os limites do plano gratuito e, nos planos pagos, a cobrança. Por isso:

!!! danger "A chave é uma senha"
    **Nunca** coloque a chave dentro do código, em prints, em mensagens ou no GitHub. Quem tem a sua chave usa a API **em seu nome**. Se ela vazar, **apague-a** no site onde foi criada e crie outra.

---

## Caminho B: criando a chave (18 anos ou mais)

1. Entre no **Google AI Studio** ([aistudio.google.com](https://aistudio.google.com)) com a sua conta Google pessoal e aceite os termos.
2. Procure a opção para **criar uma chave de API** (*Get API key* / *Criar chave de API*) e copie a chave.
3. Na pasta do projeto, crie o arquivo **`.env`**:

    ```text title=".env"
    GEMINI_API_KEY=cole-aqui-a-sua-chave
    GEMINI_MODELO=gemini-3.8-flash
    ```

4. Crie também o **`.gitignore`**, para o Git nunca enviar o `.env` nem o ambiente virtual:

    ```text title=".gitignore"
    .env
    .venv/
    __pycache__/
    ```

!!! info "O nome do modelo muda"
    `gemini-3.8-flash` é o modelo usado na documentação oficial em **outubro de 2026**. As empresas lançam modelos novos e aposentam os antigos com frequência: se aparecer um erro de modelo não encontrado, confira o nome atual na documentação da API e troque **só** a linha `GEMINI_MODELO` no `.env`.

### Limites e privacidade do plano gratuito

- O plano gratuito tem **limites** de pedidos por minuto e por dia. Quando acabam, a API responde com um erro (código **429**) até o limite renovar.
- No plano gratuito, conforme os termos conferidos em outubro de 2026, o Google pode **usar as mensagens** para melhorar os produtos e elas podem ser **lidas por revisores**. É mais um motivo para o filtro de dados pessoais da aula 04.
- Você **não** precisa cadastrar cartão para usar o plano gratuito.

---

## O motor da API

Acrescente ao `motores.py`, depois do `MotorSimulado`:

```python title="motores.py — acrescentar no final"
class MotorGemini:
    """Responde com um modelo de IA do Google, pela API (exige chave própria, 18 anos ou mais)."""

    def __init__(self, instrucoes: str, modelo: str, cliente=None):
        if cliente is None:
            from google import genai
            cliente = genai.Client()  # lê a chave da variável GEMINI_API_KEY
        self.cliente = cliente
        self.instrucoes = instrucoes
        self.modelo = modelo
        self.ultima = None  # id da última resposta, para a IA lembrar da conversa

    def responder(self, pergunta: str) -> str:
        pedido = {"model": self.modelo, "system_instruction": self.instrucoes, "input": pergunta}
        if self.ultima:
            pedido["previous_interaction_id"] = self.ultima
        resposta = self.cliente.interactions.create(**pedido)
        self.ultima = resposta.id
        return resposta.output_text

    def nova_conversa(self):
        self.ultima = None
```

O que cada parte faz:

| Parte | Para quê |
|---|---|
| `genai.Client()` | Cria a conexão com a API, usando a chave do ambiente (`GEMINI_API_KEY`) |
| `system_instruction` | As **instruções de sistema**: o “papel” e as regras do assistente (o C-T-F-R do Módulo 02, fixo para toda a conversa) |
| `previous_interaction_id` | O **id** da resposta anterior: é assim que a API sabe que a pergunta continua a mesma conversa |
| `output_text` | O texto da resposta |
| `nova_conversa()` | Esquece o id: a próxima pergunta começa uma conversa nova |
| `cliente=None` | Permite, nos **testes**, passar um cliente **falso**, sem internet (aula 04) |

!!! tip "Mesmo “jeito” do motor simulado"
    `MotorGemini` tem os mesmos métodos `responder()` e `nova_conversa()` do `MotorSimulado`. Por isso o `conversar()` funciona com os dois sem mudar nada.

---

## Escolhendo o motor e tratando erros

Atualize o `assistente.py`:

```python title="assistente.py"
"""Mini-assistente de estudos no terminal."""
import os

from dotenv import load_dotenv

from motores import MotorGemini, MotorSimulado

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
        try:
            saida("Assistente: " + motor.responder(pergunta))
        except Exception as erro:
            saida(f"Assistente: não consegui responder agora ({type(erro).__name__}). Tente de novo em instantes.")


if __name__ == "__main__":
    conversar(criar_motor())
```

- `load_dotenv()` lê o `.env` e coloca a chave no ambiente. **Sem** `.env` (caminho A), `criar_motor()` devolve o **motor simulado** — o mesmo programa serve para os dois caminhos.
- O `try/except` captura qualquer erro do motor (chave errada, limite, internet) e mostra uma mensagem, em vez de o programa **quebrar** no meio da conversa.

---

??? note "Equivalentes e alternativas"
    | Situação | O que fazer |
    |---|---|
    | Outra API de IA com plano gratuito | Leia os termos (idade, limites, dados), instale a biblioteca dela e escreva um `MotorOutro` com `responder()` e `nova_conversa()` |
    | A biblioteca do Google mudou | Ajuste **só** o `MotorGemini` conforme a documentação oficial; o resto do programa não muda |
    | Sem internet na hora da aula | O programa usa o motor simulado se não houver `.env`; para forçar, renomeie o `.env` |

---

## ⚠️ Erros comuns

- **Chave dentro do código** ou em print — e depois no GitHub.
- **Esquecer o `.gitignore`** antes do primeiro `git add`.
- **`.env` na pasta errada:** o `load_dotenv()` procura na pasta onde você roda o programa.
- **Espaços ou aspas** na linha da chave (`GEMINI_API_KEY = "..."` pode dar problema): escreva `NOME=valor`.
- **Usar o plano gratuito com dados pessoais.** Lembre dos termos: as mensagens podem ser lidas.

---

## Exercícios

### Básico (fixação)

(Todos.) Crie o **`.gitignore`** do projeto e um arquivo **`.env.example`** — um modelo **sem a chave**, para quem for usar o seu projeto saber o que preencher. Se você usa Git, confira com `git status` que o `.env` **não** aparece.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```text title=".gitignore"
    .env
    .venv/
    __pycache__/
    ```

    ```text title=".env.example"
    # Copie este arquivo para .env e preencha (só para maiores de 18, com chave própria).
    GEMINI_API_KEY=
    GEMINI_MODELO=gemini-3.8-flash
    ```

    O `.env.example` **vai** para o Git (não tem segredo); o `.env`, **não**. Com o `.gitignore` certo, o `git status` mostra o `.env.example` e **não** mostra o `.env` nem a pasta `.venv`.

### Intermediário (aplicação)

Adapte o assistente para **outra disciplina** ou para uma **área do trabalho** (por exemplo, um tutor de Excel para auxiliares administrativos):

- **Caminho B:** reescreva as `INSTRUCOES` e teste com três perguntas — uma do tema, uma fora do tema e um pedido de “faça para mim”.
- **Caminho A:** reescreva as `RESPOSTAS` (ou os `TEMAS`) do motor simulado com cinco palavras-chave da nova área e teste as mesmas três situações.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    **Caminho B — instruções de exemplo:**

    ```python title="assistente.py — novas instruções"
    INSTRUCOES = (
        "Você é um tutor de Excel para auxiliares administrativos iniciantes. Use o Excel em "
        "português, com funções em português e ponto e vírgula. Explique com exemplos de "
        "escritório. Não monte a planilha inteira: faça perguntas e dê dicas, um passo por vez. "
        "Se a pergunta não for sobre planilhas, diga que só ajuda com Excel."
    )
    ```

    Registre as três respostas. O que conferir: a do tema vem como **pergunta ou dica** (não como solução completa); a de fora do tema é **recusada** com educação; o pedido de “faça para mim” é **redirecionado** para o passo a passo. Se alguma regra não foi seguida, deixe a instrução mais **explícita** e teste de novo — como no refinamento de prompts do Módulo 02.

    **Caminho A:** as palavras-chave devem cobrir os termos da área (“soma”, “procx”, “tabela dinâmica”, “gráfico”, “fórmula”) e as respostas devem ser **perguntas de tutor**. Inclua uma chave para o “faça para mim” (por exemplo, “faça”), **antes** das outras.

### Avançado (desafio)

A mensagem de erro atual diz só o **nome** do erro (por exemplo, `BadRequestError`), que não ajuda o usuário. Escreva uma função `explicar_erro(erro)` que devolva uma mensagem clara para: **chave inválida**, **limite de uso** (código 429) e **qualquer outro** erro — e use-a no `except`.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```python title="assistente.py — função nova"
    def explicar_erro(erro):
        texto = str(erro)
        if "API key not valid" in texto or "API_KEY_INVALID" in texto:
            return "a chave não é válida. Confira o GEMINI_API_KEY no arquivo .env."
        if "429" in texto or "RESOURCE_EXHAUSTED" in texto:
            return "o limite de uso do plano gratuito acabou. Espere alguns minutos (ou até amanhã)."
        return f"não consegui responder agora ({type(erro).__name__}). Tente de novo em instantes."
    ```

    E, no `except`:

    ```python title="assistente.py — no except"
    except Exception as erro:
        saida("Assistente: " + explicar_erro(erro))
    ```

    **Teste sem gastar a cota:** coloque uma chave **inventada** no `.env` e mande “oi” — a API recusa a chave e o assistente mostra “a chave não é válida...”. Para o limite, teste a função diretamente: `explicar_erro(Exception("Error code: 429 - RESOURCE_EXHAUSTED"))`.

---

## 💡 Resumo

- **API** = porta entre programas; **chave** = senha do seu programa, guardada no **`.env`** e fora do Git (**`.gitignore`**).
- **Caminho B** (18+): chave no Google AI Studio; plano gratuito com **limites** e mensagens que **podem ser lidas**.
- `MotorGemini`: **instruções de sistema**, `previous_interaction_id` para lembrar da conversa e `output_text`.
- `criar_motor()` escolhe o motor pelo `.env`; `try/except` evita que o programa quebre.

## ➡️ Próximo passo

**[04 — Segurança e testes](04_seguranca_e_testes.md)**: o filtro que impede dados pessoais de saírem do computador e os testes que rodam sem internet.
