# 05 — Projeto final: entregando o seu mini-assistente

> **Curso:** Introdução à IA  
> **Módulo:** 05 — Projeto: seu mini-assistente  
> **Tempo estimado:** 2 h 30 min  

---

## Objetivos

Ao final deste projeto, você terá:

- O mini-assistente **personalizado** para uma disciplina ou área de trabalho, com nome, regras e temas próprios.
- Um **aviso** na tela de que o usuário está falando com um programa e não deve enviar dados pessoais.
- Um **README** que explica o que o assistente faz, como instalar, os dois caminhos e as limitações.
- Os **testes** passando e a **avaliação** das respostas registrada.
- Uma **demonstração** de 3 minutos e um **relatório de responsabilidade**, ligado à carta do Módulo 04.

## Pré-requisitos

- [Aulas 01 a 04](index.md) deste módulo.
- A [carta de uso responsável](../modulo_04_etica_e_privacidade/05_projeto_carta_de_uso_responsavel.md) do Módulo 04.

---

## O que entregar

```text
mini_assistente/
├── assistente.py          # a conversa (com o aviso na tela)
├── motores.py             # MotorSimulado e MotorGemini
├── seguranca.py           # o filtro
├── teste_assistente.py    # os testes (todos passando)
├── requirements.txt
├── .env.example           # modelo, sem a chave
├── .gitignore             # .env, .venv/, __pycache__/
└── README.md              # a documentação
```

!!! danger "Nunca entregue o `.env`"
    Ao compactar a pasta ou enviar para o GitHub, confira que o **`.env`** (com a chave) e a pasta **`.venv`** **não** foram junto. Se a chave vazar, apague-a no Google AI Studio e crie outra.

### O README

O `README.md` é a “capa” do projeto. Deve ter:

1. **O que é:** o assistente, a área e o público.
2. **Como instalar e rodar:** ambiente virtual, `pip install -r requirements.txt`, `python assistente.py`.
3. **Os dois caminhos:** sem `.env` usa o motor simulado; com `.env` (18+, chave própria) usa a API.
4. **Regras do assistente:** as da sua especificação (aula 01).
5. **Limitações:** o que ele **não** faz e os erros conhecidos — o filtro não pega nomes; a IA pode errar e alucinar; o motor simulado só conhece alguns temas.
6. **Testes:** como rodar `python teste_assistente.py`.
7. **Uso de IA na construção:** a sua **declaração de uso** (Módulo 04, aula 02), se você usou um assistente para escrever ou entender o código.

### O relatório de responsabilidade

Uma página respondendo, com base na carta do Módulo 04:

| Pergunta | Base |
|---|---|
| Que **dados** o assistente pode receber e o que acontece com eles? | Módulo 04, aula 01; termos da API (aula 03) |
| Como ele evita **cola** e promove o **aprendizado**? | Módulo 04, aula 02; modo tutor |
| Que **erros** ele pode cometer e quem pode ser prejudicado? | Módulo 01; Módulo 04, aula 04 |
| Quem pode usar cada caminho (**idade**) e por quê? | Aula 01 deste módulo |
| O que ele cumpre (ou não) da **carta** da turma? | Módulo 04, aula 05 |

---

## ✅ Checklist de entrega

- [ ] Assistente **personalizado** (nome, área, instruções ou temas).
- [ ] **Aviso** na tela: é um programa e não deve receber dados pessoais.
- [ ] `python teste_assistente.py` mostra **todos os testes passaram**, com pelo menos **dois testes novos** seus.
- [ ] **Avaliação** dos seis casos da aula 01 registrada (✔/✘).
- [ ] **README** com as 7 partes.
- [ ] **Relatório de responsabilidade** de uma página.
- [ ] Entrega **sem** `.env` e **sem** `.venv`.
- [ ] **Demonstração** de 3 minutos.

---

## Exercícios

O projeto tem três entregas, uma por nível. Faça na ordem.

### Básico (fixação)

**Personalize** o assistente para a sua área: um **nome**, as instruções (caminho B) ou os temas (caminho A) e um **aviso** na primeira mensagem da tela. Rode os testes e ajuste os que dependiam dos textos antigos.

<!-- gabarito -->
??? success "Gabarito — Básico"
    Exemplo de aviso, na primeira linha do `conversar()`:

    ```python title="assistente.py — primeira mensagem"
    saida("Tutora Bia (Biologia) — um programa de computador, não uma pessoa. "
          "Não escreva dados pessoais. Comandos: /nova e /sair.")
    ```

    Se você mudou as respostas do motor simulado, os testes que conferem textos antigos (“Vamos por partes”, “Qual é a sua tese”) **vão falhar** — isso é esperado. Atualize os `assert` para os textos novos: o teste deve acompanhar o comportamento que você **quer**.

    **Confira:** o aviso diz que é um **programa** e pede para **não** enviar dados pessoais (transparência e privacidade, Módulo 04).

### Intermediário (aplicação)

Escreva o **README** com as 7 partes e faça a **avaliação** dos seis casos de teste da aula 01 (✔/✘ para cada regra). Acrescente **dois testes automáticos** seus.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    Um começo de README (o seu deve falar do **seu** assistente):

    ```text title="README.md"
    # Tutora Bia — mini-assistente de Biologia

    Tutora de estudos de Biologia do 1º ano, no terminal. Faz perguntas em vez de dar
    respostas prontas. Projeto do curso Introdução à IA (CourseForge · IF).

    ## Como rodar
    1. python -m venv .venv  e ative o ambiente
    2. pip install -r requirements.txt
    3. python assistente.py

    ## Dois caminhos
    - Sem .env: motor simulado (respostas por palavras-chave, sem internet). Para todos.
    - Com .env (copie o .env.example): API do Gemini. Só para maiores de 18, com chave própria.

    ## Regras
    Não dá respostas prontas; diz quando não sabe; recusa provas; bloqueia CPF, telefone e e-mail.

    ## Limitações
    O filtro não reconhece nomes nem endereços. A IA pode errar e inventar: confira no livro.
    O motor simulado só conhece 5 temas.

    ## Testes
    python teste_assistente.py

    ## Uso de IA na construção
    Usei o assistente da escola para entender expressões regulares; o código final é meu.
    ```

    **Avaliação:** uma tabela com os seis casos e ✔/✘ — e, para cada ✘, o que você mudou. **Testes novos:** por exemplo, um tema novo do seu motor e a palavra “senha” (aula 04).

### Avançado (desafio)

**Demonstre** o assistente em **3 minutos** (para a turma ou para um colega): uma pergunta do tema, uma fora do tema, uma mensagem com dado pessoal sendo bloqueada e os testes rodando. Entregue também o **relatório de responsabilidade**.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    **Roteiro de demonstração (3 minutos):**

    1. (30 s) O problema: “Estudar Biologia sozinho é difícil; a Tutora Bia faz perguntas para ajudar a pensar.”
    2. (1 min) Conversa ao vivo: pergunta do tema ➔ resposta em forma de pergunta; pergunta fora do tema ➔ “não sei”; mensagem com um e-mail inventado ➔ **bloqueada**.
    3. (30 s) `python teste_assistente.py` ➔ “todos os testes passaram”.
    4. (1 min) Limitações e cuidados: quem pode usar cada caminho, o que o filtro não pega, por que conferir as respostas.

    **Relatório — o que o professor confere:** as cinco perguntas respondidas com base nos módulos; a regra de **idade** explicada; os **termos** do plano gratuito citados (dados podem ser usados e lidos); pelo menos **um risco** real e o que você fez para reduzi-lo; ligação clara com a **carta** da turma.

    **Critérios que o professor costuma olhar:** programa funcionando nos dois caminhos (ou no A, para menores); testes passando, com testes novos; README completo; nenhum segredo entregue; aviso e filtro funcionando; demonstração clara e no tempo; relatório que mostra **responsabilidade**, não só técnica.

---

## 💡 Resumo do módulo — e do curso

Você construiu uma ferramenta de IA **e** pensou nas consequências dela:

- **Arquitetura** com motores trocáveis: **simulado** para todos, **API** para maiores de 18 com chave própria.
- **Chave** no `.env`, fora do Git; **instruções de sistema**; conversa com memória; erros tratados.
- **Filtro** de dados pessoais e **testes** sem internet.
- **README**, **aviso** de transparência e **relatório de responsabilidade**.

Ao longo do curso, você foi do “o que é IA?” ao uso **crítico, produtivo e responsável**: entender como funciona (Módulo 01), pedir e conferir (Módulo 02), usar no estudo e no trabalho (Módulo 03), respeitar pessoas, leis e autoria (Módulo 04) — e construir (Módulo 05).

## ➡️ Próximo passo

Volte à [apresentação do curso](../docs/index.md). Para ir além na programação, o **[curso de Python](../../python_para_desktop/docs/index.md)** ensina interfaces gráficas, banco de dados e projetos maiores — o seu mini-assistente pode ganhar uma janela e guardar o progresso de estudo.
