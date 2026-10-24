# 05 — Projeto do módulo: trabalho em grupo na nuvem

> **Curso:** Pacote Office  
> **Módulo:** 04 — Trabalho em equipe e alternativas gratuitas  
> **Tempo estimado:** 2 h 30 min (mais o tempo do trabalho do grupo)  

---

## Objetivos

Ao final deste projeto, o seu grupo terá:

- Uma **pasta compartilhada** na nuvem, organizada e com as **permissões certas**.
- Uma **planilha de tarefas** que mostra quem faz o quê, até quando — e destaca o que está atrasado.
- Um **documento escrito em coautoria**, com comentários resolvidos e o histórico mostrando a participação de cada um.
- Uma **reunião on-line** com pauta e ata.
- A **entrega** por e-mail formal, com PDF e link — e o **encerramento** do projeto, revendo os acessos.

## Pré-requisitos

- [Aulas 01 a 04](index.md) deste módulo.
- Um grupo de **3 ou 4 pessoas** e um tema de trabalho (combine com o professor; pode ser o tema de uma disciplina).

---

## Escolha a trilha

O projeto pode ser feito com qualquer um dos dois conjuntos de ferramentas. **O grupo inteiro usa a mesma trilha.**

| Etapa | Trilha Microsoft | Trilha Google |
|---|---|---|
| Pasta compartilhada | OneDrive (ou aba *Arquivos* de um canal do Teams) | Google Drive |
| Documento | Word (instalado ou na web) | Google Docs |
| Planilha de tarefas | Excel | Google Planilhas |
| Reunião | Teams | Google Meet |
| Chat do grupo | Chat do Teams | Google Chat |
| Entrega | Outlook | Gmail |

!!! info "Ninguém do grupo tem Microsoft Office?"
    A trilha Google funciona só com contas gratuitas. A trilha Microsoft também funciona com contas pessoais, usando o **Office na web** (aula 04).

---

## A organização do grupo

### Papéis

| Papel | Responsabilidade |
|---|---|
| **Coordenador(a)** | Cria a pasta, dá os acessos, marca as reuniões |
| **Redator(a)-chefe** | Cuida da estrutura do documento e da revisão final |
| **Responsável pelos prazos** | Mantém a planilha de tarefas atualizada |
| **Responsável pela entrega** | Gera o PDF, escreve e envia o e-mail de entrega |

Em grupos de 3, uma pessoa acumula dois papéis. **Todos escrevem uma parte do documento.**

### A pasta

```text
Trabalho Grupo 3 - História/
├── 01 Pesquisa/        (links, PDFs, anotações)
├── 02 Documento/       (o trabalho em coautoria)
├── 03 Entrega/         (o PDF final)
└── Tarefas             (a planilha de tarefas)
```

### A planilha de tarefas

| Tarefa | Responsável | Prazo | Status |
|---|---|---|---|
| Pesquisar fontes | Ana | 10/11/2026 | Concluída |
| Escrever introdução | Bruno | 14/11/2026 | Fazendo |
| ... | ... | ... | A fazer |

- **Status** com **lista suspensa**: *A fazer*, *Fazendo*, *Concluída*.
- **Formatação condicional** que pinta a linha de vermelho quando o prazo passou e a tarefa não está concluída.
- Uma célula com o **% concluído**.

---

## ✅ Checklist de entrega

- [ ] Pasta com a estrutura combinada, compartilhada **só com o grupo** (*Pessoas específicas* / *Restrito*), com permissão de **edição**.
- [ ] Planilha de tarefas com lista suspensa, destaque de atrasos e % concluído.
- [ ] Documento com uma parte escrita por **cada** integrante — o **histórico de versões** mostra isso.
- [ ] Pelo menos **3 comentários** trocados entre o grupo, todos **resolvidos** no final.
- [ ] Uma **reunião on-line** com pauta enviada antes e ata postada depois.
- [ ] **E-mail de entrega** formal, com o PDF anexado e o link do documento com permissão de **leitura**.
- [ ] Depois da entrega: acessos revistos e **retrospectiva** do grupo.

---

## Exercícios

O projeto tem três entregas, uma por nível. Faça na ordem.

### Básico (fixação)

**Montar a estrutura:** escolham a trilha e os papéis; o coordenador cria a pasta com as subpastas, compartilha só com o grupo e cria a **planilha de tarefas** com as tarefas do trabalho, a lista suspensa de status, o destaque de atrasos e o % concluído.

<!-- gabarito -->
??? success "Gabarito — Básico"
    1. **Pasta:** OneDrive ➔ *Adicionar novo ➔ Pasta* (Google Drive: *Novo ➔ Nova pasta*) ➔ crie as subpastas. *Compartilhar* a pasta principal ➔ **Pessoas específicas** + *Pode editar* (Google: e-mails como **Editor**, *Acesso geral:* **Restrito**).
    2. **Planilha** na pasta: cabeçalhos em A1:D1 (`Tarefa`, `Responsável`, `Prazo`, `Status`); uma tarefa por linha, todas com responsável e prazo.
    3. **Lista suspensa** em D2:D20: Excel: *Dados ➔ Validação de Dados ➔ Lista* ➔ `A fazer;Fazendo;Concluída` · Google: *Inserir ➔ Menu suspenso* ➔ as três opções.
    4. **Atrasos** em A2:D20 — formatação condicional por fórmula, preenchimento vermelho claro:

        ```text
        =E($D2<>"Concluída";$C2<HOJE();$C2<>"")
        ```

        Google: *Formatar ➔ Formatação condicional* ➔ *A fórmula personalizada é* ➔ a mesma fórmula.
    5. **% concluído** (em F1, formato de porcentagem):

        ```text
        =CONT.SE(D2:D20;"Concluída")/CONT.VALORES(A2:A20)
        ```

    **Teste:** coloque um prazo de ontem em uma tarefa *A fazer* — a linha fica vermelha. Mude para *Concluída* — volta ao normal e o % sobe.

### Intermediário (aplicação)

**Produzir em equipe:** cada integrante escreve a **sua parte** no mesmo documento (coautoria); o redator-chefe comenta as partes com **@menções** e os autores respondem e resolvem. No meio do trabalho, o grupo faz uma **reunião on-line** de até 30 minutos, com pauta, e posta a **ata** no chat.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    - **Documento:** criado na subpasta `02 Documento` — assim já herda o compartilhamento. Estrutura combinada antes (títulos de cada parte com o nome do responsável, por exemplo “2.1 Causas — Bruno”), e cada um escreve **só na sua parte**.
    - **Comentários:** selecione o trecho ➔ *Novo Comentário* (Google: *Inserir ➔ Comentário*) ➔ “@Bruno, falta a fonte deste dado” ➔ o autor corrige, **responde** (“Incluí a referência”) e **resolve**.
    - **Reunião:** convite pelo calendário (Teams ou Meet) com a pauta: 1. o que cada um já fez, 2. dificuldades, 3. próximos prazos. Durante: microfone mudo, mão levantada, um compartilha a planilha de tarefas.
    - **Ata** no chat do grupo:

        > **Ata — reunião de 18/11/2026 (25 min)**  
        > Presentes: Ana, Bruno, Carla, Diego.  
        > Situação: 60% das tarefas concluídas; introdução atrasada.  
        > Decisões: Diego ajuda Bruno na introdução; revisão final em 26/11.  
        > Próxima reunião: 25/11, 18h.

    - **Planilha:** o responsável pelos prazos atualiza os status **depois** da reunião.

### Avançado (desafio)

**Entregar e encerrar:** o redator-chefe faz a revisão final e confere que não sobrou comentário nem alteração pendente; o responsável pela entrega gera o **PDF** na pasta `03 Entrega` e manda o **e-mail formal** ao professor, com o grupo em cópia. Depois, o coordenador **revê os acessos** da pasta e o grupo faz uma **retrospectiva** de 10 minutos.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    1. **Revisão final:** Word: *Revisão ➔ Painel de Revisão* vazio e comentários resolvidos · Google Docs: sem sugestões pendentes (*Ferramentas ➔ Analisar alterações sugeridas*) e comentários resolvidos. Ortografia, sumário atualizado.
    2. **PDF:** *Arquivo ➔ Exportar ➔ Criar PDF/XPS* (Google: *Arquivo ➔ Fazer download ➔ PDF*) ➔ salve em `03 Entrega` ➔ **abra o PDF e confira**.
    3. **E-mail** (modelo da aula 02): assunto com turma, disciplina e grupo; PDF **anexado**; link do documento com permissão de **leitura** (*Pode exibir* / *Leitor*); grupo em **Cc**; assinatura.
    4. **Acessos:** *Compartilhar ➔ Gerenciar acesso* — só o grupo (e o professor, como leitor) deve aparecer; remova links “Qualquer pessoa”, se alguém criou.
    5. **Participação:** *Histórico de versões* do documento mostra quem editou e quando — é a prova de que todos escreveram.
    6. **Retrospectiva** (postada no chat), três perguntas:
        - O que funcionou bem e vamos repetir?
        - O que atrapalhou?
        - O que vamos fazer diferente no próximo trabalho?

    **Critérios que o professor costuma olhar:** entrega no prazo e no formato pedido; participação de todos (histórico); organização da pasta; e-mail correto; reflexão honesta na retrospectiva.

---

## 💡 Resumo do módulo

Você aprendeu a trabalhar **com outras pessoas** usando as ferramentas do escritório — pagas ou gratuitas:

- **Nuvem** com permissões certas: um arquivo só, todos no mesmo lugar.
- **Coautoria** com comentários, @menções e histórico de versões.
- **E-mail** formal, agenda com convites e atenção aos golpes.
- **Teams** (ou Google Chat e Meet) para conversar, reunir e entregar tarefas.
- **LibreOffice** e **Google Workspace** como alternativas — sabendo o que muda na troca de arquivos.
- **Organização de grupo:** papéis, tarefas com prazo, reunião com pauta e ata, entrega e retrospectiva.

## ➡️ Próximo passo

**Módulo 05 — Projeto final integrado** *(em preparação)*: currículo no Word, planilha de controle no Excel e apresentação no PowerPoint, usados juntos.
