# 02 — Escrevendo bons pedidos (prompts)

> **Curso:** Introdução à IA  
> **Módulo:** 02 — Usando assistentes de IA bem  
> **Tempo estimado:** 1 h 30 min  

---

## Objetivos

Ao final desta aula, você será capaz de:

- Explicar o que é um **prompt** e por que a forma de pedir muda tanto a resposta.
- Usar a receita **C-T-F-R**: **Contexto**, **Tarefa**, **Formato** e **Restrições**.
- **Refinar** uma resposta em vez de aceitar a primeira.
- Pedir para o assistente **fazer perguntas** antes de responder.
- Dividir uma tarefa grande em **etapas**.

## Pré-requisitos

- [Aula 01](01_conhecendo_os_assistentes.md): um assistente de IA que você possa usar.

---

## O que é um prompt

**Prompt** é o que você escreve (ou fala) para o assistente: a pergunta, o pedido, as instruções e os textos que você cola. O assistente não sabe quem você é, para que precisa nem o que já sabe — ele só tem o que está no prompt (e na conversa). Por isso:

> **Pedido vago ➔ resposta genérica. Pedido claro ➔ resposta útil.**

Compare:

| Prompt vago | Prompt claro |
|---|---|
| “Fale sobre fotossíntese.” | “Sou aluno do 1º ano do ensino médio e tenho prova de Biologia amanhã. Explique a **fotossíntese** em até **10 linhas**, com uma **analogia do dia a dia**, e termine com **3 perguntas** para eu testar se entendi. Não use termos que não estejam no livro do ensino médio.” |

---

## A receita C-T-F-R

| Letra | Pergunta | Exemplos |
|---|---|---|
| **C — Contexto** | Quem é você, para que é, quem vai ler? | “Sou professor de Matemática do 8º ano.” · “Trabalho no atendimento de uma loja de roupas.” · “É para um cartaz da feira de ciências.” |
| **T — Tarefa** | O que exatamente o assistente deve fazer? Use um **verbo** claro. | Explicar, resumir, reescrever, comparar, listar, corrigir, criar exercícios, revisar |
| **F — Formato** | Como você quer a resposta? | Tabela, lista, 5 tópicos, um parágrafo, até 100 palavras, tom formal, linguagem simples |
| **R — Restrições** | O que evitar, que nível, que fonte usar? | “Sem termos técnicos.” · “Use só o texto que vou colar.” · “Não invente dados; se não souber, diga.” |

Não precisa de todas as letras em todo pedido — mas, quando a resposta vier ruim, quase sempre falta uma delas.

!!! tip "“Se não souber, diga que não sabe”"
    Essa frase nas restrições não elimina as alucinações (Módulo 01), mas ajuda: o assistente passa a admitir mais vezes quando não tem a informação. Ainda assim, **confira** o que for importante (aula 04).

### Exemplos para o estudo e para o trabalho

**Estudo:**

```text
Contexto: estou no 2º ano do ensino médio, estudando para a prova de História.
Tarefa: crie um resumo sobre as causas da Primeira Guerra Mundial.
Formato: 5 tópicos curtos e, no final, uma linha do tempo com 4 datas.
Restrições: linguagem simples; não invente datas — se tiver dúvida, avise.
```

**Trabalho:**

```text
Contexto: sou atendente de uma loja de roupas e um cliente reclamou por e-mail
que a entrega atrasou 5 dias.
Tarefa: escreva uma resposta pedindo desculpas e oferecendo frete grátis na próxima compra.
Formato: e-mail curto, até 8 linhas, tom cordial e profissional.
Restrições: não prometa data de entrega; não use a palavra "infelizmente".
```

Você não precisa escrever “Contexto:”, “Tarefa:”... — pode ser texto corrido. Os rótulos só ajudam a não esquecer nada.

---

## Refinar: a primeira resposta é um rascunho

Raramente a primeira resposta é a ideal. Continue a conversa com pedidos curtos:

| Problema | Pedido de ajuste |
|---|---|
| Longa demais | “Resuma em 3 linhas.” |
| Difícil demais | “Explique de novo para alguém de 12 anos.” |
| Genérica | “Dê um exemplo com futebol.” · “Use o caso de uma padaria.” |
| Formato errado | “Coloque em uma tabela com as colunas X e Y.” |
| Tom errado | “Deixe mais formal.” · “Menos entusiasmado.” |
| Faltou algo | “Acrescente as desvantagens.” |

!!! info "Peça perguntas antes"
    Para tarefas maiores, termine o prompt com: **“Antes de responder, faça-me as perguntas que precisar para fazer um bom trabalho.”** O assistente pergunta o que falta (público, tamanho, objetivo) e a resposta final sai bem melhor.

---

## Tarefas grandes: uma etapa de cada vez

Pedir “faça um trabalho completo sobre energia solar” gera um texto genérico (e, na escola, não é o seu trabalho — Módulo 04). Divida:

1. “Me ajude a escolher um **recorte** para um trabalho sobre energia solar no Brasil: sugira 5 perguntas de pesquisa.”
2. “Para a pergunta 3, que **tipos de fonte** eu deveria procurar?”
3. “Li estas duas fontes [cole os trechos]. Me ajude a organizar um **roteiro** de 4 seções.”
4. “Revise este parágrafo que **eu** escrevi: aponte problemas de clareza, sem reescrever.”

Cada etapa é um prompt pequeno, fácil de conferir — e **você** continua no controle.

---

??? note "Os mesmos princípios em qualquer assistente"
    A receita C-T-F-R funciona em ChatGPT, Gemini, Copilot, Claude ou qualquer outro. Diferenças práticas:

    - Alguns assistentes têm **instruções personalizadas** (aula 01): coloque lá o contexto fixo (“Sou professor de Matemática...”) e não precisa repetir em todo prompt.
    - Nos assistentes dentro do Word, do Excel ou do Gmail, o **contexto** já inclui o documento aberto — mas ainda vale dizer a tarefa, o formato e as restrições.

---

## ⚠️ Erros comuns

- **Pedido de uma linha para uma tarefa complexa.** A resposta vem genérica.
- **Esquecer o público:** a explicação vem difícil (ou infantil) demais.
- **Aceitar a primeira resposta.** Refine.
- **Colar textos de outras pessoas ou dados pessoais** no prompt (aula 01).
- **Pedir o trabalho pronto** em vez de pedir ajuda em cada etapa — você não aprende e corre o risco de plágio.

---

## Exercícios

### Básico (fixação)

Reescreva cada prompt vago com a receita **C-T-F-R**:

1. “Me explica equação do 2º grau.”
2. “Faz um e-mail pro meu chefe.”
3. “Dá ideias de redação.”

<!-- gabarito -->
??? success "Gabarito — Básico"
    Respostas possíveis (as suas podem ser diferentes, desde que tenham as quatro partes):

    1. “Sou aluno do 9º ano e não entendi a fórmula de Bhaskara. **Explique** como resolver uma equação do 2º grau **passo a passo**, com **um exemplo resolvido** e **dois para eu tentar** (com as respostas no final). **Sem pular etapas** e com números inteiros.”
    2. “Trabalho como auxiliar administrativo e preciso **pedir ao meu chefe** para sair 2 horas mais cedo na sexta para uma consulta médica. **Escreva um e-mail** curto (até 6 linhas), **tom respeitoso**, oferecendo compensar as horas na segunda. **Não detalhe** o motivo da consulta.”
    3. “Vou fazer uma redação do ENEM sobre o tema que o professor deu: ‘os desafios da mobilidade urbana no Brasil’. **Sugira 5 ângulos** possíveis para a tese, cada um em **uma frase**, e **um repertório** (dado, lei ou fato) que eu possa **pesquisar** para cada um. **Não escreva a redação.**”

    **Confira:** tem **quem é você** (C), **um verbo** (T), **como quer** (F) e **o que evitar** (R).

### Intermediário (aplicação)

Escolha **um** dos seus prompts do exercício básico e use-o em um assistente. Depois, faça **três refinamentos** seguidos (por exemplo: mais curto, outro exemplo, outro formato). Registre o prompt, os três pedidos de ajuste e, em uma frase, **o que melhorou** a cada um.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    Um registro possível (com o prompt 1):

    | Pedido | O que melhorou |
    |---|---|
    | Prompt C-T-F-R original | Explicação completa, mas longa |
    | “Resuma a explicação em 5 passos numerados.” | Ficou fácil de seguir e de revisar antes da prova |
    | “Troque o exemplo por um com números menores.” | As contas ficaram simples e deu para conferir de cabeça |
    | “Coloque os dois exercícios em uma tabela: equação, Δ, raízes.” | Formato bom para estudar e conferir |

    **Confira as contas:** se o assistente resolveu equações, **refaça uma** você mesmo (ou com a calculadora). Modelos de linguagem podem errar contas (Módulo 01, aula 04).

### Avançado (desafio)

Crie um **prompt modelo** — um prompt reutilizável, com **lacunas** entre colchetes — para uma tarefa que você faz com frequência (estudar para provas, responder clientes, planejar a semana, preparar aulas...). Teste-o em **duas** situações diferentes, preenchendo as lacunas, e ajuste o modelo até ele funcionar bem nas duas.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    Um exemplo de prompt modelo para estudar:

    ```text
    Sou aluno do [série/curso] e tenho prova de [disciplina] sobre [assunto] em [prazo].
    1. Antes de tudo, faça-me 3 perguntas rápidas para descobrir o que eu já sei.
    2. Depois, monte um plano de estudo de [número] dias, com até [tempo] por dia,
       em uma tabela: dia, tema, atividade, como vou saber que aprendi.
    3. No fim, crie [número] questões no estilo da prova, com gabarito separado.
    Use linguagem simples. Não invente conteúdo que não esteja em livros do [série].
    Se não tiver certeza de algo, avise.
    ```

    Teste 1: “[1º ano] [Química] [ligações químicas] [3 dias]”. Teste 2: “[9º ano] [Geografia] [clima do Brasil] [1 semana]”.

    **O que costuma precisar de ajuste:** o tempo por dia (o assistente exagera), o nível das questões (peça “no nível da prova do [série]”) e a frase das 3 perguntas iniciais (sem ela, o plano fica genérico). Guarde o modelo pronto: ele vai para o **caderno de prompts** do projeto deste módulo.

---

## 💡 Resumo

- **Prompt** é tudo o que você dá ao assistente; ele só sabe o que está ali.
- Receita **C-T-F-R**: **Contexto**, **Tarefa** (verbo), **Formato**, **Restrições**.
- A primeira resposta é um **rascunho**: **refine** com pedidos curtos.
- Em tarefas grandes, peça **perguntas antes** e trabalhe **em etapas**.
- Prompts que funcionam viram **modelos reutilizáveis**.

## ➡️ Próximo passo

**[03 — Técnicas que fazem diferença](03_tecnicas_que_fazem_diferenca.md)**: dar exemplos, pedir o passo a passo, transformar o assistente em tutor e trabalhar com textos e arquivos.
