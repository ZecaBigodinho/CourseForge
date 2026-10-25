# 03 — Modelos, Slide Mestre e elementos visuais

> **Curso:** Pacote Office  
> **Módulo:** 03 — PowerPoint  
> **Tempo estimado:** 2 h  

---

## Objetivos

Ao final desta aula, você será capaz de:

- Diferenciar **tema** e **modelo** e salvar um modelo próprio (`.potx`).
- Usar o **Slide Mestre** para mudar todos os slides de uma vez: logotipo, fontes, rodapé e número do slide.
- Transformar listas em diagramas com **SmartArt**.
- Inserir **tabelas** legíveis.
- Levar **gráficos do Excel** para o PowerPoint — copiados ou **vinculados** à planilha.

## Pré-requisitos

- [Aula 02](02_design_de_slides.md): tema, cores e regras de um slide claro.
- Para os gráficos: [Módulo 02 — Excel](../modulo_02_excel/index.md), aula 03 (gráficos).

---

## Tema e modelo

- **Tema** (*Design ➔ Temas*): cores, fontes e fundo. Muda a aparência, não o conteúdo.
- **Modelo** (`.potx`): um arquivo “de partida” com tema, layouts, logotipo e até slides de exemplo. Ao abrir um modelo, o PowerPoint cria uma **apresentação nova** a partir dele — o modelo continua intacto.
- Modelos prontos: *Arquivo* ➔ **Novo** e pesquise (“escola”, “relatório”, “projeto”).
- **Salvar o seu:** *Arquivo ➔ Salvar como* ➔ tipo **Modelo do PowerPoint (`.potx`)**. Bom para a turma inteira usar o mesmo padrão em um trabalho em grupo.

---

## Slide Mestre

O **Slide Mestre** é o “molde” de todos os slides. Mudou ali, mudou na apresentação inteira.

1. *Exibir* ➔ **Slide Mestre**.
2. No painel da esquerda, o **slide grande do topo** é o mestre: o que você muda nele vale para **todos** os layouts. Os slides menores, embaixo, são os **layouts** (Slide de Título, Título e Conteúdo...): mudanças em um deles valem só para os slides com aquele layout.
3. Na guia *Slide Mestre*: **Fontes** e **Cores** do tema, **Estilos de Plano de Fundo**, e você pode inserir um logotipo ou uma faixa de cor no mestre.
4. *Fechar Modo de Exibição Mestre* para voltar aos slides.

### Rodapé e número do slide

*Inserir* ➔ **Cabeçalho e Rodapé** ➔ marque **Número do slide** e **Rodapé** (escreva, por exemplo, “Escola · Turma 2B · 2026”) ➔ marque **Não mostrar no slide de título** ➔ *Aplicar a Todos*. A posição e a fonte desses itens são definidas no Slide Mestre.

!!! warning "Formatou slide por slide? Use o mestre"
    Se você precisa repetir a mesma mudança em todos os slides (trocar a fonte do título, mover o logotipo), ela pertence ao **Slide Mestre**. Fazer à mão em cada slide dá trabalho e sempre sobra um diferente.

!!! tip "Slide fora do padrão? Redefinir"
    Se um slide ficou diferente do layout (caixas fora do lugar, fonte errada), *Página Inicial* ➔ **Redefinir** devolve as posições e a formatação do layout, sem apagar o texto.

---

## SmartArt

O **SmartArt** transforma uma lista em diagrama: processo, ciclo, hierarquia, comparação.

- **De um texto pronto:** clique no espaço com os tópicos ➔ *Página Inicial* ➔ **Converter em SmartArt** ➔ escolha o tipo.
- **Do zero:** *Inserir* ➔ **SmartArt**. O painel de texto ao lado funciona como a lista de tópicos: `Enter` cria um item, `Tab` cria um subitem.
- Na guia *Design do SmartArt*: **Alterar Cores** e **Estilos**; *Converter* volta para texto ou forma.

| Tipo | Quando usar | Exemplo |
|---|---|---|
| **Processo** | etapas em ordem | Pesquisar ➔ Escrever ➔ Revisar ➔ Entregar |
| **Ciclo** | algo que se repete | Ciclo da água |
| **Hierarquia** | quem está acima de quem | Organograma da escola |
| **Lista** | itens do mesmo nível, com destaque | Três atitudes contra o desperdício |
| **Relação** | partes que se juntam ou se sobrepõem | Diagrama de Venn |

!!! tip "Pouco texto também no SmartArt"
    Cada caixa do diagrama aguenta poucas palavras. Se a letra ficou minúscula, há texto demais — ou itens demais (o ideal é até 5 ou 6).

---

## Tabelas

*Inserir* ➔ **Tabela** e escolha linhas e colunas (ou cole uma tabela do Excel ou do Word).

- Poucas linhas e colunas: um slide não é planilha. Mostre só o que sustenta a mensagem.
- **Destaque** a linha ou o número que importa (negrito ou cor) — a plateia precisa saber para onde olhar.
- Guia *Design da Tabela*: estilos prontos e as opções **Linha de Cabeçalho**, **Linhas em Tiras**, **Linha de Total**.
- Números alinhados à **direita**, com o mesmo número de casas decimais.

---

## Gráficos: do Excel para o PowerPoint

Duas formas:

1. **Criar no PowerPoint:** *Inserir* ➔ **Gráfico** ➔ escolha o tipo. Abre uma pequena planilha para você digitar os dados.
2. **Copiar do Excel:** selecione o gráfico no Excel ➔ `Ctrl + C` ➔ no PowerPoint, *Página Inicial ➔ setinha de* **Colar** ➔ escolha uma opção:

| Opção de colagem | O que acontece |
|---|---|
| **Usar Tema de Destino e Inserir Pasta de Trabalho** | Copia o gráfico **e os dados** para dentro do PowerPoint, com as cores da apresentação. Não depende mais da planilha. |
| **Usar Tema de Destino e Vincular Dados** | O gráfico fica **ligado** à planilha: se os números mudarem no Excel, basta *Design do Gráfico* ➔ **Atualizar Dados**. |
| **Imagem** | Vira uma figura: não dá mais para editar os dados. |

!!! warning "Vínculo depende do arquivo"
    Gráfico vinculado precisa encontrar a planilha **no mesmo lugar**. Se você mover ou renomear o arquivo do Excel, ou mandar só o `.pptx` para outra pessoa, o vínculo se perde (o gráfico continua aparecendo, mas não atualiza). Para entregar, prefira **Inserir Pasta de Trabalho**.

Com o gráfico no slide, valem as regras da aula 03 do Excel: **título com a conclusão**, rótulos de dados, nada de 3D. No PowerPoint, aumente as letras do gráfico — pelo menos **18 pt**.

---

??? note "Equivalentes gratuitos: LibreOffice Impress e Google Apresentações"
    | Tarefa | LibreOffice Impress | Google Apresentações |
    |---|---|---|
    | Slide mestre | *Exibir ➔ Slide mestre* | *Slide ➔ Editar tema* |
    | Número do slide e rodapé | *Inserir ➔ Cabeçalho e rodapé* | *Inserir ➔ Números de slides* (rodapé: coloque no tema) |
    | Salvar modelo | *Arquivo ➔ Modelos ➔ Salvar como modelo* | Não tem; faça uma cópia do arquivo (*Arquivo ➔ Fazer uma cópia*) |
    | Diagramas | Não tem SmartArt; use formas ou *Inserir ➔ Fontwork* | *Inserir ➔ Diagrama* |
    | Gráfico ligado à planilha | *Inserir ➔ Objeto ➔ Objeto OLE* (do arquivo, com *Vincular ao arquivo*) | Gráfico copiado do Google Planilhas fica **vinculado** e mostra o botão *Atualizar* |

---

## ⚠️ Erros comuns

- **Mexer no layout pequeno achando que é o mestre.** A mudança aparece só em parte dos slides. O mestre é o slide **grande do topo**.
- **Logotipo colado em cada slide.** Ele fica em lugares diferentes e não sai de uma vez. Coloque no mestre.
- **Planilha inteira colada no slide.** Ninguém lê 15 linhas de números projetados. Mostre o resumo ou o gráfico.
- **Mandar a apresentação com gráficos vinculados** sem a planilha junto. Em outro computador, o gráfico não atualiza.

---

## Exercícios

### Básico (fixação)

Na sua apresentação do exercício intermediário da aula 01:

1. Pelo **Slide Mestre**, troque a fonte dos títulos de **todos** os slides e coloque uma faixa de cor ou o nome da escola no topo.
2. Coloque o **número do slide** e um **rodapé** com sua turma e o ano em todos os slides, **menos na capa**.

<!-- gabarito -->
??? success "Gabarito — Básico"
    1. *Exibir ➔ Slide Mestre* ➔ clique no **slide grande do topo** ➔ selecione o espaço do título ➔ escolha a fonte (ou, para trocar as fontes do tema todo: guia *Slide Mestre ➔ Fontes*). Para a faixa: *Inserir ➔ Formas ➔ Retângulo*, desenhe no topo do mestre e use uma cor do tema; se ela cobrir o título, botão direito ➔ *Enviar para Trás*. *Fechar Modo de Exibição Mestre*.
    2. *Inserir ➔ Cabeçalho e Rodapé* ➔ **Número do slide** ✓ ➔ **Rodapé** ✓ “Turma 2B · 2026” ➔ **Não mostrar no slide de título** ✓ ➔ *Aplicar a Todos*.

    **Confira:** passe pelos slides — todos com a mesma fonte, a mesma faixa e o número; a capa sem número e sem rodapé. Se a faixa não aparece na capa, está certo: o layout *Slide de Título* pode ter o plano de fundo próprio (no mestre, desmarque *Ocultar Gráficos de Plano de Fundo* nesse layout se quiser a faixa lá também).

### Intermediário (aplicação)

1. Crie um slide “Como fizemos o trabalho” com os tópicos *Escolher o tema*, *Pesquisar*, *Escrever*, *Revisar* e *Apresentar*, e transforme em um **SmartArt de processo**.
2. Crie um slide com uma **tabela** de 3 colunas e 4 linhas comparando três opções de algo (três celulares, três destinos de excursão...) e **destaque** a opção escolhida.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    1. *Novo Slide* (Título e Conteúdo) ➔ título “Como fizemos o trabalho” ➔ os 5 tópicos ➔ clique no texto ➔ *Página Inicial ➔ Converter em SmartArt ➔ Mais Elementos Gráficos SmartArt ➔ Processo* ➔ por exemplo, **Processo Básico** ou **Processo Contínuo em Seta**. *Design do SmartArt ➔ Alterar Cores* ➔ uma opção do tema.
    2. *Novo Slide* ➔ ícone de tabela no espaço reservado (ou *Inserir ➔ Tabela*) ➔ **3 colunas × 4 linhas**: cabeçalho e três opções. Em *Design da Tabela*, deixe **Linha de Cabeçalho** marcada. Selecione a linha da opção escolhida ➔ **negrito** e um *Sombreamento* de destaque.

    **Confira:** fonte de pelo menos 18 pt na tabela e no SmartArt; se não couber, corte texto.

### Avançado (desafio)

1. No Excel, monte a tabela abaixo (vendas da cantina por categoria, do [Módulo 02, aula 04](../modulo_02_excel/04_tabela_dinamica_e_automacao.md)) e um gráfico de **colunas agrupadas**. Leve o gráfico para um slide **vinculado** à planilha, com título que diga a conclusão.

    | Categoria | Fevereiro | Março |
    |---|---|---|
    | Bebida | 337,50 | 401,50 |
    | Doce | 150,00 | 152,00 |
    | Salgado | 533,00 | 639,50 |

2. No Excel, mude as vendas de **Doce em março** para **300,00** e atualize o gráfico no PowerPoint.
3. Salve a sua apresentação como **modelo** (`.potx`), sem os slides de conteúdo, para a turma usar.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    1. No Excel: cole a tabela em A1, selecione **A1:C4** ➔ *Inserir ➔ Gráfico de Colunas ➔ Colunas Agrupadas*. **Salve** a planilha (`vendas_cantina.xlsx`). Clique na borda do gráfico ➔ `Ctrl + C` ➔ no PowerPoint, slide *Somente Título* ➔ *Colar* ➔ **Usar Tema de Destino e Vincular Dados**. Título do slide, por exemplo: “Salgados vendem mais que bebidas e doces juntos” (R$ 1.172,50 contra R$ 1.041,00). Aumente as letras do gráfico para 18 pt ou mais.
    2. No Excel, **C3** = `300` ➔ salve. No PowerPoint, clique no gráfico ➔ *Design do Gráfico* ➔ **Atualizar Dados** ➔ a coluna de Doce em março sobe. Repare: o título continua verdadeiro? (Salgado R$ 1.172,50 contra R$ 1.189,00 de bebidas e doces — **não** é mais verdade.) Gráfico vinculado atualiza os números, mas **o título é você que revisa**.
    3. Faça uma cópia da apresentação, apague os slides de conteúdo (deixe capa e um slide de exemplo) ➔ *Arquivo ➔ Salvar como* ➔ tipo **Modelo do PowerPoint (`.potx`)**. Para testar: abra o `.potx` — o PowerPoint cria uma apresentação nova “Apresentação1” a partir dele.

---

## 💡 Resumo

- **Tema** = aparência; **modelo** (`.potx`) = ponto de partida completo.
- **Slide Mestre:** o slide grande do topo vale para tudo; os layouts, para os slides com aquele layout.
- **Cabeçalho e Rodapé** coloca número e rodapé em todos os slides — menos na capa, se você pedir.
- **SmartArt** transforma listas em processos, ciclos e hierarquias.
- Gráfico do Excel: **inserir pasta de trabalho** para entregar; **vincular** para atualizar com a planilha. O título com a conclusão é sempre responsabilidade sua.

## ➡️ Próximo passo

**[04 — Transições, animações e a hora de apresentar](04_transicoes_animacoes_e_apresentacao.md)**: movimento com moderação e as ferramentas que deixam você seguro na frente da turma.
