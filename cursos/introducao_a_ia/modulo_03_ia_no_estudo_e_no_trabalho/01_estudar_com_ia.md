# 01 — Estudar com IA

> **Curso:** Introdução à IA  
> **Módulo:** 03 — IA no estudo e no trabalho  
> **Tempo estimado:** 1 h 30 min  

---

## Objetivos

Ao final desta aula, você será capaz de:

- Diferenciar usar a IA para **aprender** de usar a IA para **não precisar aprender**.
- Pedir **explicações em níveis**, **resumos** do que você leu, **quiz** e **cartões de revisão**.
- Montar um **plano de estudo** com a IA e ajustá-lo à sua realidade.
- Usar uma ferramenta que responde **só com base nas suas fontes** (como o NotebookLM).
- Saber **quando não usar** IA nos estudos.

## Pré-requisitos

- [Módulo 02](../modulo_02_usando_assistentes/index.md): prompts C-T-F-R, modo tutor e verificação.

---

## Aprender × pular o aprendizado

Estudos sobre aprendizagem mostram que a gente aprende mais quando **se esforça para lembrar** e **explica com as próprias palavras** — e menos quando só relê ou copia. A IA pode ajudar nas duas direções:

| Uso que **ajuda** a aprender | Uso que **atrapalha** |
|---|---|
| Explicar de outro jeito o que você não entendeu | Pedir a resposta do exercício e copiar |
| Fazer perguntas para você responder (quiz, tutor) | Pedir o resumo de um texto que você **não leu** |
| Corrigir a **sua** explicação | Pedir a redação pronta |
| Montar um plano de revisão | Deixar a IA “estudar por você” |

!!! tip "A pergunta-teste"
    Depois de usar a IA, pergunte: **eu consigo fazer isso sozinho agora?** Se a resposta é não, a IA fez a tarefa — você não aprendeu.

---

## Cinco usos que funcionam

### 1. Explicação em níveis

```text
Explique [conceito] em três níveis: (1) para uma criança de 10 anos, (2) para um aluno
do [série], (3) com os termos técnicos do livro. Use um exemplo do dia a dia no nível 1.
```

Comece pelo nível mais simples e suba.

### 2. Resumo do que **você** leu

Leia o texto primeiro. Depois cole o texto (ou o trecho) e peça:

```text
Use apenas o texto entre ###. Faça um resumo em 5 tópicos e liste 3 conceitos-chave
com a definição de cada um, como estão no texto.
###
[texto]
###
```

Compare com o que **você** tinha entendido: onde vocês discordam, releia o texto.

### 3. Quiz e cartões de revisão

```text
Sobre [assunto], crie 8 perguntas de múltipla escolha no nível da prova do [série].
Mostre uma pergunta por vez, espere a minha resposta e me diga se acertei e por quê.
No final, faça uma lista dos temas que eu errei.
```

Cartões de revisão (pergunta na frente, resposta atrás) são ótimos para memorizar definições, datas e fórmulas — peça em formato de **tabela** e copie para um aplicativo de cartões ou para papel.

### 4. Plano de estudo

Use o **prompt modelo** de plano de estudo do seu caderno (Módulo 02) — e **ajuste** o plano à sua vida real: dias com trabalho, transporte, outras provas. A IA não sabe disso se você não contar.

### 5. Ferramentas que respondem só com as suas fontes

Algumas ferramentas trabalham **apenas** com os materiais que você envia (PDFs, textos, links) e mostram de que trecho saiu cada resposta. Um exemplo gratuito é o **NotebookLM**, do Google: você cria um “caderno” com as fontes da matéria e pede resumos, perguntas, mapas mentais e até um **resumo em áudio**, em formato de conversa.

!!! info "NotebookLM: idade e conta"
    Conferido em outubro de 2026: disponível em contas Google a partir de **13 anos** (ou a idade mínima do país) e, para alunos de qualquer idade, quando a escola usa o **Google Workspace for Education**. Nas contas escolares, o Google informa que as conversas e as fontes **não são usadas** para treinar os modelos. Como sempre, as regras podem mudar — confira.

---

## Quando **não** usar IA nos estudos

- **Em provas e avaliações** — a não ser que o professor permita, e do jeito que ele permitir.
- **Quando o objetivo da tarefa é treinar uma habilidade** (escrever uma redação, resolver contas, ler um livro): pular a tarefa é pular o aprendizado.
- **Quando você ainda não tentou.** Tente primeiro; use a IA quando travar.
- **Para fatos que vão para a nota sem conferir** (Módulo 02, aula 04).

---

??? note "Equivalentes e alternativas"
    | Tarefa | Com qualquer assistente | Ferramenta específica (gratuita) |
    |---|---|---|
    | Explicar e fazer quiz | Prompt de tutor (Módulo 02) | — |
    | Estudar com base nas suas fontes | Anexar o PDF + “use apenas este texto” | NotebookLM (Google) |
    | Cartões de revisão | Pedir uma tabela pergunta/resposta | Aplicativos de cartões (Anki, Quizlet e outros) |
    | Transcrever uma aula gravada | Algumas ferramentas aceitam áudio | Legendas automáticas do YouTube; transcrição do Word na web |

---

## ⚠️ Erros comuns

- **Resumo de texto não lido.** Você fica com a ideia da IA, não com a do texto — e não percebe se ela errou.
- **Quiz fácil demais.** Peça o **nível da prova** e questões que exijam explicar, não só decorar.
- **Plano de estudo impossível** (4 h por dia para quem trabalha). Ajuste.
- **Usar IA onde o professor proibiu.** Além de não aprender, é desonestidade acadêmica (Módulo 04).

---

## Exercícios

### Básico (fixação)

Escolha um conceito que você está estudando agora e peça uma **explicação em três níveis**. Depois, **sem olhar**, escreva com suas palavras, em até 5 linhas, o que entendeu. Peça ao assistente para **corrigir a sua explicação** (sem reescrever).

<!-- gabarito -->
??? success "Gabarito — Básico"
    Exemplo com “inflação”:

    - **Nível 1:** “É quando as coisas ficam mais caras com o tempo e o mesmo dinheiro compra menos — como quando o pão que custava R$ 1 passa a custar R$ 1,20.”
    - **Nível 2:** aumento geral e contínuo dos preços, medido por índices.
    - **Nível 3:** com os termos do livro (índice de preços, poder de compra, IPCA).

    **A parte que mais importa** é a sua explicação **sem olhar** e a correção dela. Um bom pedido: “Corrija a minha explicação abaixo: diga o que está certo, o que está errado ou incompleto, sem reescrever o texto.” Se a IA disse algo **diferente** do livro, confira no livro (Módulo 02, aula 04).

### Intermediário (aplicação)

Leia um texto do seu material (um capítulo, um artigo). Depois:

1. Peça um **resumo só com base no texto** e compare com o que você entendeu.
2. Peça um **quiz de 6 perguntas**, uma por vez, e responda.
3. Anote quantas você acertou e quais temas precisa revisar.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    O que conferir no registro:

    1. O prompt do resumo tem **“use apenas o texto entre ###”**. A comparação aponta **pelo menos uma** diferença entre o seu entendimento e o resumo — e o que o **texto** diz sobre ela.
    2. O quiz foi feito **uma pergunta por vez**; se o assistente mandou todas de uma vez, reforce: “Mostre só a próxima pergunta depois da minha resposta.”
    3. Exemplo de registro: “Acertei 4 de 6. Errei as duas sobre a Revolução Industrial na Inglaterra: revisar as causas (p. 58 a 60).”

### Avançado (desafio)

Monte um **material de estudo completo** para uma prova real: um **plano** para os dias que faltam (ajustado à sua rotina), **cartões de revisão** com 10 perguntas e respostas e um **quiz** de 8 questões no nível da prova. Se a sua conta permitir, monte também um caderno no **NotebookLM** com as fontes da matéria e compare as respostas dele com as do assistente comum.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    Critérios:

    - **Plano** com os dias reais até a prova e o tempo que você **realmente** tem (o seu prompt contou a sua rotina?).
    - **Cartões** em tabela (pergunta | resposta) e **conferidos** no material — a IA pode errar uma definição.
    - **Quiz** com pelo menos 3 perguntas que pedem **explicar** ou **aplicar**, não só decorar.
    - **Comparação** (se usou o NotebookLM): o NotebookLM mostra **o trecho da fonte** de cada resposta; o assistente comum responde com o que “sabe” — e pode trazer coisas que não estão no seu material. Para estudar para a prova do **seu** professor, responder com base nas **fontes da matéria** costuma ser mais seguro.

---

## 💡 Resumo

- A IA ajuda a **aprender** quando faz você **pensar** (explicar, responder, corrigir); atrapalha quando faz **por você**.
- Cinco usos: **explicação em níveis**, **resumo do que você leu**, **quiz e cartões**, **plano de estudo** e ferramentas que respondem **só com as suas fontes** (como o NotebookLM).
- **Não use** em provas (sem permissão), quando a tarefa é treinar uma habilidade e antes de tentar sozinho.

## ➡️ Próximo passo

**[02 — Escrever e comunicar no trabalho](02_escrever_e_comunicar.md)**: e-mails, atas, revisão de textos e tradução — com cuidado com os dados e com a autoria.
