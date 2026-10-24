# 03 — Técnicas que fazem diferença

> **Curso:** Introdução à IA  
> **Módulo:** 02 — Usando assistentes de IA bem  
> **Tempo estimado:** 1 h 30 min  

---

## Objetivos

Ao final desta aula, você será capaz de:

- **Dar exemplos** no prompt para o assistente seguir um padrão.
- Pedir o **passo a passo** em problemas que exigem raciocínio.
- Transformar o assistente em **tutor**, que faz perguntas em vez de dar a resposta pronta.
- Pedir **crítica** e **simulações** (entrevista, debate, cliente difícil).
- Trabalhar com **textos e arquivos**, mandando o assistente responder **só com base neles**.

## Pré-requisitos

- [Aula 02](02_escrevendo_bons_prompts.md): a receita C-T-F-R e o refinamento.

---

## 1. Mostre exemplos

Quando você quer um **padrão** (um formato, uma classificação, um estilo), mostrar dois ou três exemplos funciona melhor do que explicar.

```text
Classifique cada comentário de cliente como ELOGIO, RECLAMAÇÃO ou DÚVIDA.

Exemplos:
"Chegou rápido e bem embalado!" → ELOGIO
"Paguei e até agora nada." → RECLAMAÇÃO
"Vocês entregam em Niterói?" → DÚVIDA

Agora classifique:
"O tamanho M serve em quem veste 40?"
"A cor veio diferente da foto."
```

O assistente segue o padrão dos exemplos — inclusive o formato da resposta (`→ CATEGORIA`).

---

## 2. Peça o passo a passo

Em problemas de matemática, lógica ou planejamento, peça para o assistente **mostrar as etapas**: “Resolva passo a passo, explicando cada etapa.” Assim você consegue **conferir** onde ele errou, se errar. Muitos assistentes têm também um **modo de raciocínio** (aula 01), que “pensa” mais antes de responder.

!!! warning "Passo a passo não é prova de que está certo"
    Uma explicação bem organizada pode ter um erro no meio — e o resultado final sai errado com toda a confiança. Confira as contas com a **calculadora** ou a **planilha** (Módulo 02 do curso de Office).

---

## 3. O assistente como tutor

Para **aprender** (e não só ter a resposta), peça que ele **não** dê a resposta:

```text
Quero aprender a resolver este problema, não só saber a resposta:
"Um produto custava R$ 80,00 e teve 15% de desconto. Quanto passou a custar?"
Aja como um tutor paciente: não me dê a resposta. Faça uma pergunta por vez
para eu chegar sozinho na solução. Se eu errar, me dê uma dica, não a resposta.
```

É o jeito de usar IA que mais ajuda nos estudos — e o que menos tem risco de virar “cola”.

---

## 4. Peça crítica e simulações

| Técnica | Prompt de exemplo |
|---|---|
| **Crítica** | “Aponte os 3 pontos mais fracos da argumentação deste texto que **eu** escrevi. Não reescreva o texto.” |
| **Lista de verificação** | “Confira se este e-mail tem: saudação, pedido claro, prazo e assinatura. Diga o que falta.” |
| **Entrevista simulada** | “Aja como entrevistador de uma vaga de Jovem Aprendiz administrativo. Faça uma pergunta de cada vez e, no final, me dê um retorno sobre as minhas respostas.” |
| **Outro ponto de vista** | “Quais seriam os melhores argumentos **contra** a minha opinião?” |
| **Cliente difícil** | “Aja como um cliente irritado com um atraso. Quero treinar o atendimento.” |

!!! tip "Papel + objetivo"
    “Aja como [papel]” funciona melhor com um **objetivo** claro: “Aja como professor de português e corrija só a pontuação” é melhor que “Aja como professor”.

---

## 5. Trabalhe com textos e arquivos

Você pode **colar um texto** ou **anexar um arquivo** (PDF, planilha, imagem) e pedir que o assistente trabalhe **sobre ele**:

```text
Use APENAS o texto entre as linhas ### para responder.
Se a resposta não estiver no texto, diga "o texto não informa".
Para cada resposta, copie o trecho do texto que a sustenta.

###
[cole aqui o texto]
###

Perguntas: ...
```

- As **linhas `###`** (ou aspas) separam claramente o texto das instruções.
- Pedir o **trecho que sustenta** a resposta facilita a conferência.
- “Diga ‘o texto não informa’” reduz as invenções — mas **confira** mesmo assim.

!!! danger "Cuidado com o que você anexa"
    Antes de colar ou anexar, pergunte: **posso compartilhar isto?** Contrato da empresa, prova que ainda vai ser aplicada, dados de alunos ou clientes, documento pessoal — não. Use a **conta institucional** quando a tarefa for da escola ou do trabalho (aula 01).

---

??? note "Técnicas em uma linha"
    | Técnica | Frase para o prompt |
    |---|---|
    | Exemplos | “Siga o padrão destes exemplos: ...” |
    | Passo a passo | “Resolva passo a passo, explicando cada etapa.” |
    | Tutor | “Não me dê a resposta; faça uma pergunta por vez.” |
    | Crítica | “Aponte os pontos fracos, sem reescrever.” |
    | Simulação | “Aja como [papel] para eu treinar [objetivo].” |
    | Só o texto | “Use apenas o texto entre ###; se não estiver lá, diga.” |
    | Perguntas antes | “Antes de responder, faça-me as perguntas necessárias.” |

---

## ⚠️ Erros comuns

- **Explicar um padrão em vez de mostrar.** Dois exemplos valem mais que um parágrafo de instruções.
- **Aceitar o passo a passo sem conferir.** O erro pode estar escondido em uma etapa.
- **Pedir a resposta pronta quando o objetivo é aprender.** Use o modo tutor.
- **Pedir “corrija meu texto”** e receber outro texto, que não é mais seu. Peça **apontamentos**, não reescrita.
- **Anexar o que não podia** ser compartilhado.

---

## Exercícios

### Básico (fixação)

Use a técnica dos **exemplos** para fazer o assistente classificar as frases abaixo como **FATO** (pode ser conferido) ou **OPINIÃO** (depende de quem fala). Dê **dois exemplos** de cada no prompt.

1. “O Brasil tem 26 estados e um Distrito Federal.”
2. “O melhor jogador de futebol de todos os tempos é brasileiro.”
3. “A água ferve a 100 °C ao nível do mar.”
4. “As aulas on-line são mais cansativas que as presenciais.”

<!-- gabarito -->
??? success "Gabarito — Básico"
    Um prompt possível:

    ```text
    Classifique cada frase como FATO (pode ser conferido em fontes) ou OPINIÃO (depende de quem fala).
    Exemplos:
    "São Paulo é a cidade mais populosa do Brasil." → FATO
    "Um litro tem mil mililitros." → FATO
    "Matemática é a matéria mais legal." → OPINIÃO
    "Filmes antigos são melhores que os novos." → OPINIÃO
    Agora classifique: [as 4 frases]
    ```

    Classificação esperada: 1. **FATO** · 2. **OPINIÃO** · 3. **FATO** · 4. **OPINIÃO** (pode virar fato se houver uma **pesquisa** medindo o cansaço — vale discutir com a turma).

    **Confira:** o assistente respondeu no **mesmo formato** dos exemplos (`→ FATO`)? Esse é o efeito da técnica.

### Intermediário (aplicação)

Use o **modo tutor** com o problema do desconto (R$ 80,00 com 15% de desconto) — ou com um problema da sua matéria. Responda às perguntas do assistente **sem pedir a resposta**. Registre quantas perguntas ele fez, onde você errou e qual dica ajudou.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    Um caminho típico do tutor:

    1. “O que significa 15% de desconto?” ➔ tirar 15 partes de cada 100.
    2. “Quanto é 15% de 80?” ➔ 80 × 0,15 = **12**.
    3. “E o novo preço?” ➔ 80 − 12 = **R$ 68,00**.
    4. Muitas vezes ele mostra o atalho: 80 × 0,85 = 68.

    **Resposta certa: R$ 68,00.** Se o assistente **deu a resposta logo de cara**, reforce no prompt: “Não me dê a resposta em nenhuma hipótese; faça uma pergunta por vez e espere a minha resposta.”

### Avançado (desafio)

Cole no assistente o regulamento abaixo e peça para ele responder **só com base no texto**, citando o trecho de cada resposta e dizendo “o texto não informa” quando for o caso.

```text
REGULAMENTO DA FEIRA DE CIÊNCIAS (fictício)
1. Os grupos devem ter de 3 a 5 estudantes da mesma turma.
2. As inscrições vão até 15 de setembro, pelo formulário da secretaria.
3. Cada grupo terá uma mesa e uma tomada. Experimentos com fogo são proibidos.
4. A apresentação para a banca dura até 7 minutos.
5. Os três primeiros colocados recebem medalhas.
```

Perguntas: (a) Um grupo pode ter 6 estudantes? (b) Até quando vão as inscrições? (c) Posso fazer um experimento com uma vela acesa? (d) Qual é o prêmio em dinheiro do primeiro lugar? (e) Quanto tempo dura a apresentação?

<!-- gabarito -->
??? success "Gabarito — Avançado"
    Respostas esperadas:

    | Pergunta | Resposta | Trecho |
    |---|---|---|
    | (a) | **Não.** | Item 1: “de 3 a 5 estudantes” |
    | (b) | **15 de setembro.** | Item 2 |
    | (c) | **Não**, porque vela acesa é fogo. | Item 3: “Experimentos com fogo são proibidos” |
    | (d) | **O texto não informa** (só fala em medalhas). | Item 5 |
    | (e) | **Até 7 minutos.** | Item 4 |

    **A pergunta (d) é o teste:** se o assistente **inventou** um valor em dinheiro, ele **alucinou** mesmo com a instrução. Anote isso — e lembre que a conferência final é sempre sua.

---

## 💡 Resumo

- **Exemplos** no prompt ensinam um padrão melhor que explicações.
- **Passo a passo** deixa o raciocínio à vista — e conferível.
- **Modo tutor:** perguntas em vez de respostas prontas; o melhor uso para aprender.
- **Crítica e simulações** treinam você para provas, entrevistas e atendimentos.
- **Só o texto:** delimite com `###`, peça o trecho e o “não informa” — e confira.

## ➡️ Próximo passo

**[04 — Conferindo as respostas](04_conferindo_as_respostas.md)**: como verificar o que a IA disse antes de usar, compartilhar ou entregar.
