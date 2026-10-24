# 04 — IA generativa e modelos de linguagem

> **Curso:** Introdução à IA  
> **Módulo:** 01 — O que é IA (sem mistério)  
> **Tempo estimado:** 1 h 30 min  

---

## Objetivos

Ao final desta aula, você será capaz de:

- Explicar o que é **IA generativa** e o que ela cria (texto, imagem, áudio, vídeo, código).
- Entender a ideia central de um **modelo de linguagem**: **prever a próxima palavra**.
- Explicar por que a mesma pergunta pode ter **respostas diferentes**.
- Explicar o que é **alucinação** e por que ela acontece.
- Conhecer os outros limites: **data de corte**, **janela de contexto** e o que muda quando o assistente **pesquisa na web**.

## Pré-requisitos

- [Aula 03](03_redes_neurais.md): redes neurais e treino com muitos exemplos.

---

## IA que cria

Até aqui, as IAs **reconheciam** e **decidiam**: spam ou não, rosto ou não. A **IA generativa** cria algo novo: um texto, uma imagem, uma música, uma voz, um vídeo, um programa.

| Cria | Exemplos de uso |
|---|---|
| **Texto** | Assistentes de IA (ChatGPT, Gemini, Copilot, Claude...): explicar, resumir, reescrever, traduzir |
| **Código** | Sugerir e explicar programas |
| **Imagem** | Ilustrações e fotos a partir de uma descrição |
| **Áudio e voz** | Narração, música, dublagem |
| **Vídeo** | Cenas curtas a partir de texto ou de imagens |

---

## O modelo de linguagem: o “completar” do celular, gigante

Lembra do teclado do celular que sugere a próxima palavra? Um **modelo de linguagem** (em inglês, *LLM*, “grande modelo de linguagem”) faz a mesma coisa, só que treinado com uma quantidade **enorme** de texto e com uma rede neural muito maior.

1. **Pré-treino:** o modelo lê uma quantidade gigantesca de textos (livros, sites, artigos, códigos) e aprende a responder uma pergunta só: **qual é o próximo pedaço de texto mais provável?** Fazendo isso bilhões de vezes, ele acaba aprendendo gramática, fatos, estilos e até a seguir um raciocínio.
2. **Ajuste para conversar:** depois, o modelo é treinado com exemplos de **boas conversas** e com **avaliações de pessoas** (“esta resposta é melhor que aquela”), para virar um assistente útil e educado e recusar pedidos perigosos.
3. **Na conversa:** a cada pedaço de texto, o modelo calcula as **probabilidades** dos próximos e escolhe um. Repete até terminar a resposta.

!!! info "Pedaços, não palavras"
    Os modelos trabalham com **tokens**: pedaços de texto, que podem ser uma palavra inteira, parte de uma palavra ou um sinal de pontuação. Para entender a ideia, pensar em “palavras” basta.

### Por que a mesma pergunta dá respostas diferentes

O modelo não escolhe sempre a palavra **mais** provável: ele **sorteia** entre as prováveis, com chances diferentes. Por isso a mesma pergunta pode ter respostas diferentes — e por isso o texto parece natural, e não repetitivo.

| “O céu hoje está…” | Chance |
|---|---|
| azul | 55% |
| nublado | 25% |
| cinza | 12% |
| escuro | 6% |
| laranja | 2% |

---

## Alucinação: quando o texto convence, mas é falso

O modelo é treinado para produzir um texto **provável** — não para dizer **a verdade**. Na maioria das vezes, o provável é também o verdadeiro. Mas, quando ele não tem a informação, continua produzindo o texto **com cara** de resposta certa. A isso chamamos **alucinação**.

Exemplos típicos:

- **Referências inventadas:** livro, autor, página ou link que **não existem**, no formato perfeito de referência.
- **Detalhes falsos** no meio de uma explicação certa: uma data, um número, um nome trocado.
- **Respostas sobre o que ele não sabe** (fatos muito recentes, assuntos muito locais) dadas com a mesma segurança.

!!! danger "A segurança do texto não diz nada"
    A IA escreve a resposta errada com a mesma confiança da certa. **Nunca** use uma informação importante (para um trabalho, uma decisão, a saúde, o dinheiro) sem conferir em uma fonte confiável. O Módulo 02 ensina como.

---

## Outros limites que você precisa conhecer

| Limite | O que é | Na prática |
|---|---|---|
| **Data de corte** | O modelo só conhece o que estava nos textos até a data do treino | Pode não saber de fatos recentes — ou achar que algo ainda vale |
| **Janela de contexto** | Quanto texto da conversa (e de arquivos enviados) o modelo consegue considerar de uma vez | Em conversas muito longas, ele pode “esquecer” o começo |
| **Contas e contagens** | O modelo prevê texto; não faz contas como uma calculadora | Pode errar contas, datas e contagens de letras; alguns assistentes usam uma ferramenta de cálculo para isso |
| **Sem saber que errou** | O modelo não confere a própria resposta no mundo real | Pedir “tem certeza?” não garante nada; confira fora |

!!! tip "Assistentes que pesquisam na web"
    Muitos assistentes já **buscam na internet** antes de responder e mostram as **fontes**. Isso ajuda muito com fatos recentes — mas a resposta continua sendo escrita pelo modelo. **Abra as fontes** e confira se elas dizem mesmo o que a resposta diz.

---

## Imagens, vozes e vídeos gerados

Os geradores de imagem aprendem com milhões de imagens e suas descrições. Muitos funcionam partindo de uma imagem de **ruído** (como chuvisco de TV) e “limpando” aos poucos, guiados pelo texto, até surgir a imagem pedida.

As mesmas técnicas permitem criar **vozes** e **vídeos** muito realistas de pessoas reais dizendo o que nunca disseram: os ***deepfakes***.

!!! warning "Desconfie de áudio e vídeo “bombásticos”"
    Antes de compartilhar um áudio ou vídeo chocante de uma pessoa conhecida, procure a notícia em veículos confiáveis. Golpes já usam vozes clonadas de familiares pedindo dinheiro: na dúvida, **ligue** para a pessoa. Uso de imagem e voz alheia sem autorização é tema do Módulo 04.

---

??? note "Para saber mais: o que é igual e o que muda entre os assistentes"
    | | Igual em todos | Muda de um para outro |
    |---|---|---|
    | Como funcionam | Modelo de linguagem que prevê o próximo texto | O tamanho do modelo, os dados e o ajuste |
    | Limites | Alucinação, data de corte, janela de contexto | A data de corte, o tamanho da janela, se pesquisam na web |
    | Recursos | Conversar, resumir, reescrever, explicar | Ler arquivos e imagens, gerar imagens, falar por voz, usar ferramentas |
    | Acesso | Versão gratuita com limites | Planos pagos, contas de escola e empresa, idade mínima |

---

## ⚠️ Erros comuns

- **Usar a IA como buscador de fatos** sem abrir nenhuma fonte.
- **Copiar uma referência bibliográfica** da IA sem conferir se o livro existe.
- **Achar que a resposta é a mesma para todo mundo.** Ela varia; por isso não serve como “prova” de nada.
- **Confiar mais porque o texto está bem escrito.** Escrever bem é justamente o que o modelo faz melhor.
- **Compartilhar áudio ou vídeo chocante** sem verificar a origem.

---

## Exercícios

### Básico (fixação)

1. Complete com a palavra que **você** acha mais provável e com uma **segunda** opção possível: “Para fazer um bolo, eu preciso de farinha, ovos e ___.” “Ontem eu fui ao médico porque estava com ___.”
2. Explique com suas palavras, usando a tabela do “céu”, por que um assistente pode dar respostas diferentes para a mesma pergunta.

<!-- gabarito -->
??? success "Gabarito — Básico"
    1. Respostas prováveis: “farinha, ovos e **açúcar**” (segunda opção: leite, manteiga); “estava com **dor**” / “**febre**” (segunda: gripe, tosse). Você acabou de fazer o que o modelo faz: escolher a continuação **mais provável** pelo que já viu em muitos textos.
    2. O modelo calcula a **chance** de cada próxima palavra e **sorteia** entre as prováveis, com as chances diferentes. Na maioria das vezes sai “azul”, mas às vezes sai “nublado” ou “cinza”. Como uma resposta inteira tem centenas de sorteios desses, duas respostas à mesma pergunta quase nunca são iguais.

### Intermediário (aplicação)

Um assistente de IA respondeu a um aluno:

> “Segundo o livro *A história da internet no Brasil*, de João Silva (Editora Exemplo, 2015, p. 42), a internet chegou às escolas públicas brasileiras em 1985.”

1. Quais **dois** sinais de possível alucinação você vê?
2. Como você **conferiria** essa informação? Liste **três** caminhos.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    1. **Referência muito específica** (autor, editora, ano e **página**) — formato perfeito, típico das referências inventadas. E um **fato suspeito**: em 1985 a internet ainda nem estava aberta ao público no Brasil (isso aconteceu nos anos 1990) — chegar às escolas públicas em 1985 é muito improvável.
    2. Caminhos para conferir:
        - Procurar o **livro** no catálogo de uma biblioteca, no Google Livros ou no site da editora. Se não existe, a referência foi inventada.
        - Procurar o **fato** em fontes confiáveis: sites de governo, universidades, enciclopédias, reportagens de veículos conhecidos.
        - Pedir ao assistente **o link** da fonte e **abrir** o link — se ele não abre ou não fala disso, descarte.

        E, para o trabalho, **cite a fonte que você conferiu**, nunca a resposta da IA.

### Avançado (desafio)

1. Faça a **mesma pergunta** duas vezes (em conversas novas) a um assistente de IA — ou a dois assistentes diferentes. Sugestão: “Explique em 5 linhas por que o céu é azul.” Compare: o que ficou **igual**, o que **mudou** e se alguma resposta tem um erro.
2. Explique para alguém da sua família, em **até cinco frases e sem nenhuma palavra técnica**, como funciona um assistente de IA e por que é preciso conferir o que ele diz.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    1. O esperado: a **ideia central** se repete (a luz do Sol se espalha no ar e o azul se espalha mais), mas as **frases**, a ordem e os exemplos mudam — é o sorteio entre as continuações prováveis. Se uma das respostas trouxer um detalhe que a outra não traz (um nome, um número), é esse detalhe que você deve conferir primeiro.
    2. Um exemplo:

        > “É um programa que leu uma quantidade enorme de textos e aprendeu a continuar frases do jeito mais provável. Por isso ele escreve muito bem e sabe de muitos assuntos. Mas ele não confere se o que escreve é verdade: quando não sabe, às vezes inventa, com a mesma segurança. Então ele é ótimo para explicar, dar ideias e revisar textos. Para fatos, datas, números e saúde, a gente confere em um lugar de confiança.”

        **Confira:** a sua explicação fala do **treino com textos**, de **continuar frases**, de **inventar quando não sabe** e de **conferir**.

---

## 💡 Resumo

- **IA generativa** cria texto, código, imagens, áudio e vídeo.
- **Modelo de linguagem:** treinado para prever o **próximo pedaço de texto**; depois, ajustado para conversar.
- Respostas **variam** porque o modelo **sorteia** entre as continuações prováveis.
- **Alucinação:** texto provável e convincente, mas falso — confira sempre o que importa.
- Limites: **data de corte**, **janela de contexto**, **contas**; assistentes com **busca na web** ajudam, mas as fontes precisam ser abertas.
- **Deepfakes:** áudio e vídeo falsos realistas — verifique antes de compartilhar.

## ➡️ Próximo passo

**[05 — Projeto do módulo: raio-X de uma IA do dia a dia](05_projeto_raio_x_de_uma_ia.md)**: investigar um sistema de IA que você usa e explicar como ele funciona para a turma.
