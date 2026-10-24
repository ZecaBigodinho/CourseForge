# 05 — Integração e entrega final

> **Curso:** Pacote Office  
> **Módulo:** 05 — Projeto final integrado  
> **Tempo estimado:** 1 h 30 min  

---

## Objetivos

Ao final desta aula, você terá:

- Conferido que a **planilha**, o **currículo**, as **cartas** e a **apresentação** contam **a mesma história**.
- Montado o **pacote de entrega** na nuvem, em PDF, com as **permissões certas**.
- Enviado o **e-mail de candidatura** e preparado os **e-mails de cobrança**.
- Atualizado a planilha e visto o **painel** mudar sozinho.
- Feito a sua **autoavaliação** do projeto — e do curso.

## Pré-requisitos

- [Aulas 01 a 04](index.md) deste módulo.
- Do [Módulo 04](../modulo_04_equipe_e_alternativas/index.md): compartilhamento no OneDrive (aula 01) e e-mail formal (aula 02).

---

## Revisão de consistência

As quatro peças falam de **você**. Elas precisam concordar entre si:

| Item | Planilha | Currículo | Cartas | Apresentação |
|---|---|---|---|---|
| Nome e contato | — | ✓ | ✓ (assinatura) | ✓ (slides 1 e 6) |
| Objetivo / vaga | coluna *Vaga* | Objetivo | 1º parágrafo | slides 1 e 6 |
| Habilidades com prova | — | Habilidades e Projetos | 2º parágrafo | slides 3 e 4 |
| Busca organizada | Painel | — | — | slide 5 (gráfico) |

!!! tip "O teste da pessoa de fora"
    Peça para alguém que não conhece o projeto olhar **só os PDFs** por dois minutos e responder: “Quem é essa pessoa? O que ela sabe fazer? Que vaga ela procura?” Se as três respostas saírem iguais ao que você queria, a integração funcionou.

---

## O pacote de entrega

Na subpasta `04 Entrega` do projeto:

```text
04 Entrega/
├── curriculo_seu_nome.pdf
├── cartas_apresentacao.pdf
├── apresentacao_pessoal.pdf        (e, se quiser, o vídeo .mp4)
└── candidaturas.xlsx               (uma cópia da planilha)
```

- Os arquivos de trabalho (`.docx`, `.pptx`) ficam nas outras subpastas — **entrega é PDF**.
- **Permissões:** a pasta continua compartilhada **só com o professor**, como **leitor**. Para mandar o currículo a uma empresa, mande o **PDF anexado**, não o link da pasta (ela tem a sua planilha de candidaturas!).

---

## O e-mail de candidatura

Mesmo padrão da aula 02 do Módulo 04 — com o currículo anexado e a carta no corpo:

> **Para:** biblioteca@prefeitura.example  
> **Assunto:** Candidatura — Estágio administrativo — Ana Souza  
> **Anexo:** curriculo_ana_souza.pdf
>
> Prezada Sônia Prado,
>
> Gostaria de me candidatar à vaga de **Estágio administrativo** na **Biblioteca Municipal**. [Texto da carta.]
>
> Envio meu currículo em anexo e fico à disposição para uma conversa.
>
> Atenciosamente,  
> Ana Souza · (00) 00000-0000 · ana.souza@email.example

!!! info "Simulação"
    Se o projeto for simulado, mande o e-mail para o **professor** (ou um colega), mantendo o assunto e o texto como se fosse para a empresa.

### O e-mail de cobrança

Para as candidaturas enviadas há mais de 10 dias sem resposta (a lista do `FILTRO` da aula 02):

> **Assunto:** Candidatura — Jovem Aprendiz — vendas — Ana Souza
>
> Olá, Paulo Dias,
>
> Enviei meu currículo para a vaga de Jovem Aprendiz — vendas no dia 05/11. Gostaria de saber se o processo seletivo ainda está em andamento e se há algo mais que eu possa enviar.
>
> Obrigada pela atenção.  
> Ana Souza

Curto, educado e com as informações que a pessoa precisa para encontrar a sua candidatura.

---

## Atualize a planilha

Cada envio, cada resposta e cada cobrança vira uma atualização na planilha: **status** e **data**. O painel, a lista de cobrança e o gráfico mudam sozinhos — e o gráfico da apresentação também, se estiver vinculado.

---

## Extra (opcional): uma ponte com o Python

Quem fizer o curso de Python vai aprender a ler e escrever planilhas com a biblioteca **openpyxl**. Este pequeno programa lê a `candidaturas.xlsx` e escreve, para cada empresa a cobrar, o começo do e-mail de cobrança:

```python
from datetime import date
from openpyxl import load_workbook

HOJE = date(2026, 11, 20)  # na vida real: date.today()
PRAZO = 10                 # dias de espera antes de cobrar

planilha = load_workbook("candidaturas.xlsx", data_only=True)["Candidaturas"]

for empresa, contato, email, vaga, enviado, status in planilha.iter_rows(
        min_row=2, max_col=6, values_only=True):
    if status == "Enviado" and enviado is not None:
        dias = (HOJE - enviado.date()).days
        if dias > PRAZO:
            print(f"Cobrar {empresa} <{email}>: {dias} dias sem resposta")
            print(f"  Olá, {contato}! Envio esta mensagem para saber se há novidades "
                  f"sobre a vaga de {vaga}.")
```

Com a planilha da aula 02, a saída é:

```text
Cobrar Loja Tech Mais <vagas@techmais.example>: 15 dias sem resposta
  Olá, Paulo Dias! Envio esta mensagem para saber se há novidades sobre a vaga de Jovem Aprendiz — vendas.
Cobrar Supermercado Econômico <rh@economico.example>: 12 dias sem resposta
  Olá, Rafael Lima! Envio esta mensagem para saber se há novidades sobre a vaga de Jovem Aprendiz — estoque.
```

Para rodar: Python instalado, `pip install openpyxl`, o programa salvo na mesma pasta da planilha (com a aba chamada `Candidaturas`). É a mesma lógica da coluna *Dias sem resposta* e do `FILTRO` — escrita em outra linguagem.

---

## ⚠️ Erros comuns

- **Objetivo diferente** no currículo e na apresentação. Revise as quatro peças juntas.
- **Link da pasta do projeto** mandado para a empresa. Mande só o PDF do currículo.
- **Arquivo com nome genérico** (`curriculo.pdf`, `Documento1.pdf`). Coloque o seu nome.
- **Cobrar no dia seguinte** ao envio. Espere o prazo combinado (aqui, 10 dias).
- **Esquecer de atualizar a planilha** depois de enviar. Em uma semana, ninguém lembra quem recebeu o quê.

---

## Exercícios

### Básico (fixação)

1. Faça a **revisão de consistência** com a tabela da aula e corrija o que não bater.
2. Monte a pasta `04 Entrega` com os **PDFs** e a cópia da planilha, e confira as **permissões** da pasta do projeto.

<!-- gabarito -->
??? success "Gabarito — Básico"
    1. Abra as quatro peças lado a lado e passe linha por linha na tabela. As diferenças mais comuns: o objetivo foi reescrito no currículo e não na apresentação; a apresentação cita um curso que não está no currículo; a assinatura da carta tem outro e-mail.
    2. Gere os PDFs: Word (*Exportar ➔ Criar PDF/XPS*) para o currículo e para o documento das cartas mescladas; PowerPoint (*Exportar ➔ Criar PDF/XPS*) para a apresentação. Copie a planilha para `04 Entrega` (botão direito ➔ *Copiar para*, em onedrive.com). *Compartilhar ➔ Gerenciar acesso* na pasta do projeto: só o professor, como **leitor** — nenhum link “Qualquer pessoa”.

    **Teste da pessoa de fora:** mostre só os PDFs a alguém por dois minutos e faça as três perguntas da aula.

### Intermediário (aplicação)

1. Envie o **e-mail de candidatura** para a **Biblioteca Municipal** (na simulação, para o professor), com o currículo em PDF e a carta no corpo.
2. Na planilha, mude a **Biblioteca Municipal** e a **Farmácia Saúde** para *Enviado*, com a data **20/11/2026**, e anote o que muda no painel.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    1. Novo e-mail ➔ assunto “Candidatura — Estágio administrativo — Seu Nome” ➔ **anexe o PDF** (não o link) ➔ cole a carta da Biblioteca Municipal no corpo ➔ assinatura ➔ releia e **confira o anexo** ➔ *Enviar*.
    2. Na Tabela `Candidaturas`: *Enviado em* = `20/11/2026` e *Status* = **Enviado** nas duas linhas. O que muda:
        - *Dias sem resposta*: **0** nas duas.
        - Painel: **A enviar 0** · **Enviado 5** · Entrevista 2 · Recusado 1 · Aprovado 0.
        - **Enviadas: 8**. **Taxa de resposta: 37,5%** (3 respostas em 8 envios; 38% sem casas decimais) — caiu porque as novas ainda não tiveram tempo de responder.
        - A lista de cobrança **não muda** (as novas têm 0 dia): continua Loja Tech Mais e Supermercado Econômico.

### Avançado (desafio)

1. Escreva os **e-mails de cobrança** para as empresas da lista do `FILTRO` (na simulação, para o professor ou um colega).
2. Faça a **autoavaliação** do projeto com a tabela de critérios da aula 01: para cada critério, uma nota de 1 a 3 e uma frase justificando.
3. *(Opcional)* Se você tem Python instalado, rode o programa do **Extra** com a sua planilha e compare com a lista do `FILTRO`.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    1. Dois e-mails, um para **Loja Tech Mais** (Paulo Dias, enviado em 05/11) e um para **Supermercado Econômico** (Rafael Lima, enviado em 08/11), no modelo da aula: assunto com a vaga e o seu nome; a data em que você enviou; uma pergunta educada. Depois, anote na planilha que você cobrou (uma coluna nova *Cobrado em* ajuda).
    2. Modelo de autoavaliação:

        | Critério | Nota (1–3) | Justificativa |
        |---|---|---|
        | Planilha | 3 | Fórmulas, lista, destaques e painel funcionando; mudei um status e tudo atualizou |
        | Currículo | 2 | Uma página e estilos; ainda falta prova para “inglês básico” |
        | Cartas | 3 | Mala direta filtrada, com regra para a vaga de atendimento |
        | Apresentação | 2 | Gráfico e prints bons; passei de 3 minutos no primeiro ensaio |
        | Entrega | 3 | PDFs com nome claro; pasta só para o professor |
        | Integração | 3 | Mesmo objetivo e mesmas habilidades nas quatro peças |

    3. A saída do programa deve trazer as **mesmas empresas** da lista do `FILTRO`. Se aparecer `KeyError: 'Candidaturas'`, a aba da planilha tem outro nome; se aparecer `AttributeError` em `.date()`, alguma data foi digitada como texto (a mesma causa do `#VALOR!` no Excel).

---

## 💡 Resumo do módulo — e do curso

Você juntou as ferramentas em um trabalho só, como acontece na vida real:

- **Excel** organiza os dados e alimenta as outras peças.
- **Word** transforma esses dados em documentos personalizados — currículo e cartas.
- **PowerPoint** conta a sua história com provas e gráficos.
- **OneDrive** e **Outlook** guardam, compartilham e entregam com segurança.

Ao longo do curso, você aprendeu a usar o computador como **ferramenta de trabalho**: estilos em vez de formatação manual, fórmulas em vez de calculadora, slides limpos em vez de texto projetado, arquivos na nuvem com as permissões certas — e sempre uma alternativa gratuita quando a licença faltar.

## ➡️ Próximo passo

Volte à [apresentação do curso](../docs/index.md) para ver o que mais existe na plataforma. Para continuar automatizando planilhas e documentos, o **[curso de Python](../../python_para_desktop/docs/index.md)** é o caminho natural.
