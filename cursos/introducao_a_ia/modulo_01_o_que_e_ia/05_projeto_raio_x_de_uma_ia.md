# 05 — Projeto do módulo: raio-X de uma IA do dia a dia

> **Curso:** Introdução à IA  
> **Módulo:** 01 — O que é IA (sem mistério)  
> **Tempo estimado:** 2 h  

---

## Objetivos

Ao final deste projeto, você terá:

- Escolhido um **sistema de IA** que você ou a sua comunidade usam.
- Feito o **raio-X** dele: o que entra, o que sai, com que exemplos aprendeu, que tipo de aprendizado usa, que erros comete e quem pode ser prejudicado.
- Conferido as informações em **fontes confiáveis** — inclusive o que um assistente de IA disse sobre ele.
- Apresentado o raio-X para a turma em **3 minutos**, com uma **opinião fundamentada**: vale a pena? Com que cuidados?

## Pré-requisitos

- [Aulas 01 a 04](index.md) deste módulo.
- Para a entrega: um editor de texto e um de apresentações (Word e PowerPoint, ou as alternativas gratuitas do [curso de Pacote Office](../../pacote_office/docs/index.md)).

---

## Escolha o sistema

Algumas ideias — escolha algo que você **usa** ou que **afeta** você:

| Área | Exemplos |
|---|---|
| Celular | Desbloqueio por rosto, teclado que sugere palavras, organização de fotos por pessoa |
| Entretenimento | Recomendação de vídeos, músicas ou séries; filtros de rosto das redes sociais |
| Comunicação | Filtro de spam, tradutor, legendas automáticas, assistente de IA |
| Cidade e serviços | Mapa com trânsito, câmeras que leem placas, atendimento automático por chat |
| Escola e trabalho | Correção automática, detector de plágio, triagem de currículos, previsão de estoque |
| Dinheiro | Alerta de fraude no cartão, análise de crédito |

---

## A ficha do raio-X

| Pergunta | O que responder |
|---|---|
| **1. O que é e onde está?** | Nome, aplicativo ou serviço, quem usa |
| **2. Que tarefa faz?** | Reconhecer, prever, recomendar, decidir ou criar (aula 01) |
| **3. O que entra?** | As **características** que o sistema observa (aula 02) |
| **4. O que sai?** | A previsão, decisão ou criação |
| **5. Como aprendeu?** | Tipo de aprendizado e **exemplos** prováveis do treino (aula 02) |
| **6. Que técnica usa?** | Se é uma rede neural, um modelo de linguagem, outro tipo — ou “não informado” (aulas 03 e 04) |
| **7. Que erros comete?** | **Falso positivo** e **falso negativo**, alucinação, o que for o caso |
| **8. Quem pode ser prejudicado?** | Grupos com menos exemplos nos dados, decisões difíceis de contestar (**viés**, **caixa-preta**) |
| **9. Quem confere?** | Existe revisão humana? Como contestar uma decisão? |
| **10. Vale a pena?** | Benefícios × riscos, e com que cuidados você usaria |

!!! tip "Quando não dá para saber"
    Muitas empresas não contam como os seus sistemas funcionam. Tudo bem escrever “**não informado**” — e dizer o que você **supõe** e **por quê**. Separar o que é **fato conferido** do que é **suposição** é parte da nota.

---

## Pesquisa com responsabilidade

1. **Fontes primárias:** a página de ajuda ou de privacidade da empresa costuma explicar, em linguagem simples, o que o sistema usa (“recomendamos com base no que você assistiu...”).
2. **Reportagens e estudos:** veículos de imprensa conhecidos, universidades, órgãos públicos.
3. **Assistente de IA (com cuidado):** pode ajudar a **entender** termos e a ter **ideias**, mas tudo o que ele afirmar sobre o sistema precisa ser **conferido** nas fontes 1 e 2 (aula 04). Anote o que ele disse e o que você conferiu.

!!! warning "Cite as fontes que você abriu"
    No slide final, liste as fontes **que você leu** (com link e data de acesso). “Pesquisei no assistente de IA” não é fonte; a página que você abriu e conferiu é.

---

## A entrega

- **Ficha** (1 página, Word ou similar) com as 10 respostas.
- **Apresentação** de **3 slides**, para falar em **3 minutos**:
    1. **O sistema** e a tarefa (com uma imagem ou um print — com crédito).
    2. **Como funciona:** entra ➔ aprendeu com ➔ sai (um diagrama simples).
    3. **Riscos, cuidados e a sua opinião**, com as fontes no rodapé.

---

## ✅ Checklist de entrega

- [ ] As **10 perguntas** da ficha respondidas, separando **fato** de **suposição**.
- [ ] Pelo menos **duas fontes** confiáveis abertas e citadas, com data de acesso.
- [ ] Se usou assistente de IA: o que ele disse e **o que foi conferido**.
- [ ] **Erros possíveis** e **quem pode ser prejudicado** explicados com exemplos.
- [ ] Opinião final **fundamentada** (não só “é bom” ou “é ruim”).
- [ ] 3 slides com pouco texto e títulos que afirmam; apresentação em até 3 minutos.

---

## Exercícios

O projeto tem três entregas, uma por nível. Faça na ordem.

### Básico (fixação)

Escolha o sistema e preencha a **ficha do raio-X** com o que você já sabe pelas aulas e pelo uso do dia a dia (perguntas 1 a 7).

<!-- gabarito -->
??? success "Gabarito — Básico"
    Um exemplo preenchido — **recomendação de vídeos** de uma plataforma:

    | Pergunta | Resposta |
    |---|---|
    | 1. O que é | A lista “recomendados para você” de uma plataforma de vídeos, usada por bilhões de pessoas |
    | 2. Tarefa | **Recomendar** (prever o que você vai querer assistir) |
    | 3. Entra | O que você assistiu, por quanto tempo, curtidas, pesquisas, o que pulou; o que pessoas parecidas assistiram |
    | 4. Sai | Uma lista **ordenada** de vídeos |
    | 5. Como aprendeu | **Supervisionado**, com o histórico de milhões de usuários: “quem viu A e B costumou assistir C até o fim”. *(Suposição baseada na página de ajuda da empresa.)* |
    | 6. Técnica | Redes neurais (a empresa já publicou artigos sobre isso) — detalhes **não informados** |
    | 7. Erros | Recomendar algo que não interessa (falso positivo); esconder algo que interessaria (falso negativo); prender a pessoa em um único assunto |

    **Confira:** a tarefa usa um dos cinco verbos da aula 01; “entra” são **características**; e há pelo menos uma **suposição** marcada como tal.

### Intermediário (aplicação)

Complete as perguntas **8 a 10** e faça a **pesquisa**: pelo menos **duas fontes** confiáveis. Se usar um assistente de IA, anote **uma afirmação** dele e diga se você conseguiu **confirmar** ou não.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    Continuando o exemplo:

    | Pergunta | Resposta |
    |---|---|
    | 8. Quem pode ser prejudicado | Quem passa muito tempo na plataforma (o sistema premia o tempo assistido); adolescentes expostos a conteúdo cada vez mais extremo; criadores pequenos, que aparecem menos |
    | 9. Quem confere | A pessoa pode marcar “não tenho interesse”, pausar ou apagar o histórico; não há como saber o motivo exato de cada recomendação (**caixa-preta**) |
    | 10. Vale a pena? | Sim, para descobrir conteúdo — com cuidados: limitar o tempo, usar o “não tenho interesse”, buscar de propósito outros assuntos e conferir informações em outras fontes |

    **Fontes (exemplo do formato):** página de ajuda da plataforma sobre recomendações (link, acessado em dd/mm/aaaa); reportagem de um veículo conhecido sobre o efeito das recomendações em adolescentes (link, data).

    **Registro do assistente:** “O assistente disse que a plataforma usa o tempo de exibição como um dos principais sinais. **Confirmado** na página de ajuda da empresa.” — ou “**Não consegui confirmar**; não usei no trabalho.”

### Avançado (desafio)

Monte os **3 slides**, ensaie e **apresente em 3 minutos**. Depois da apresentação, um colega faz **uma pergunta difícil** sobre o seu sistema (por exemplo: “Você deixaria esse sistema decidir sobre você sem nenhuma revisão humana?”) e você responde com base no raio-X.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    - **Slide 1** — título que afirma: “A plataforma escolhe o próximo vídeo por você”; imagem ou print com crédito.
    - **Slide 2** — diagrama simples: *histórico e cliques* ➔ *modelo treinado com milhões de pessoas* ➔ *lista recomendada*.
    - **Slide 3** — “Ótima para descobrir, ruim para quem perde o controle do tempo”: dois riscos, dois cuidados, fontes no rodapé.
    - **Ensaio** com cronômetro: 3 minutos (as técnicas estão no [Módulo 03 do curso de Office](../../pacote_office/modulo_03_powerpoint/index.md)).
    - **Resposta à pergunta difícil** — use o raio-X: diga **que erros** o sistema comete, **quem** é prejudicado e **que revisão** existe (ou não). Exemplo: “Para recomendar vídeos, aceito sem revisão, porque o erro é pequeno e eu posso ignorar. Para decidir uma vaga de emprego, não: o erro é grave e eu precisaria saber o motivo e poder contestar.”

    **Critérios que o professor costuma olhar:** as 10 perguntas respondidas; fato separado de suposição; fontes abertas e citadas; riscos e prejudicados explicados; opinião fundamentada; apresentação clara e no tempo.

---

## 💡 Resumo do módulo

Você saiu da “mágica” para o funcionamento:

- **IA** reconhece, prevê, recomenda, decide e cria — quase sempre **aprendendo com exemplos**.
- **Aprendizado de máquina:** dados, características, rótulos, treino e teste; supervisionado, não supervisionado e por reforço.
- **Redes neurais:** pesos ajustados no treino; muitas camadas = **aprendizado profundo**.
- **IA generativa:** prevê o próximo pedaço de texto; escreve bem, **alucina** às vezes e precisa ser **conferida**.
- Toda IA **erra** e pode carregar **viés**: pergunte sempre **o que entra, o que sai, com que exemplos aprendeu e quem confere**.

## ➡️ Próximo passo

**[Módulo 02 — Usando assistentes de IA bem](../modulo_02_usando_assistentes/index.md)**: como escrever bons pedidos (*prompts*), reconhecer os limites e verificar as respostas.
