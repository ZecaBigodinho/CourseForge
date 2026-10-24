# 04 — Alternativas gratuitas: LibreOffice e Google Workspace

> **Curso:** Pacote Office  
> **Módulo:** 04 — Trabalho em equipe e alternativas gratuitas  
> **Tempo estimado:** 2 h  

---

## Objetivos

Ao final desta aula, você será capaz de:

- Conhecer as opções **gratuitas** para editar documentos, planilhas e apresentações: **Office na web**, **LibreOffice** e **Google Workspace**.
- Instalar o LibreOffice com segurança e configurá-lo para trocar arquivos com quem usa o Microsoft Office.
- Usar o Google Docs, Planilhas e Apresentações e **converter** arquivos de e para o formato do Office.
- Saber **o que costuma quebrar** na troca entre programas e como se prevenir.
- Escolher a ferramenta certa para cada situação.

## Pré-requisitos

- [Aula 01](01_onedrive_nuvem_e_compartilhamento.md): nuvem e compartilhamento.
- Ter à mão um documento do Word, uma planilha do Excel e uma apresentação do PowerPoint dos módulos anteriores.

---

## As opções gratuitas

| Opção | O que é | Precisa de |
|---|---|---|
| **Office na web** | Word, Excel e PowerPoint no navegador, em [office.com](https://www.office.com) | Uma conta Microsoft **pessoal** gratuita (ou a da escola) e internet |
| **LibreOffice** | Pacote **instalado** no computador: **Writer** (textos), **Calc** (planilhas), **Impress** (apresentações), além de Draw e Base | Windows, macOS ou Linux; funciona **sem internet** |
| **Google Workspace** | **Docs**, **Planilhas** e **Apresentações** no navegador, com o **Drive** | Uma conta Google (gratuita, com **15 GB**) e internet |

!!! info "Pergunte à escola"
    Muitas escolas oferecem aos alunos uma licença de estudante do Microsoft 365 ligada ao e-mail institucional — às vezes só para a versão web, às vezes com os aplicativos para instalar. Antes de procurar alternativas, confira em [office.com](https://www.office.com) com o seu e-mail da escola.

---

## LibreOffice

### Instalar com segurança

1. Baixe **só** do site oficial: [libreoffice.org](https://www.libreoffice.org) ➔ *Baixe agora*. O site oferece a versão mais recente e uma versão anterior, mais testada; para estudar, as duas servem.
2. No Windows, aceite as opções padrão do instalador.
3. Opcional: instale também a **ajuda off-line** em português, na mesma página.

!!! danger "Cuidado com sites “de download”"
    Sites que oferecem o LibreOffice “grátis” fora do site oficial podem empacotar o instalador com propagandas ou programas indesejados. O LibreOffice é **gratuito** e **não** tem versão paga — se alguém está cobrando, é golpe.

### O jeito do LibreOffice

- **Interface:** por padrão, menus e barras de ferramentas. Para uma aparência parecida com a do Office: *Exibir ➔ Interface do usuário* ➔ **Em abas**.
- **Formatos próprios:** o LibreOffice salva, por padrão, no **ODF** (*OpenDocument*): `.odt` (texto), `.ods` (planilha), `.odp` (apresentação). É um **padrão aberto**, adotado também como norma brasileira (ABNT NBR ISO/IEC 26300).
- **Abre e salva no formato do Office:** `.docx`, `.xlsx` e `.pptx`. Ao salvar um arquivo do Office, ele pergunta se você quer manter o formato — escolha **Usar o formato do Word/Excel/PowerPoint**.
- **PDF:** o botão **Exportar diretamente como PDF** fica na barra de ferramentas.

### Configure para trocar arquivos com o Office

Se você vai mandar arquivos para quem usa Microsoft Office (o professor, o estágio), deixe o Office como formato padrão:

*Ferramentas ➔ Opções ➔ Carregar/Salvar ➔ Geral* ➔ em **Formato de arquivo padrão**, escolha *Documento de texto* ➔ **Sempre salvar como: Word 2007-365**; repita para *Planilha* (**Excel 2007-365**) e *Apresentação* (**PowerPoint 2007-365**).

!!! tip "Fontes compatíveis"
    Se o arquivo do Word usa Calibri ou Cambria e o computador não tem essas fontes, o LibreOffice usa **Carlito** e **Caladea**, que têm o **mesmo tamanho de letra** — o texto não “anda” de página. Arial e Times New Roman são substituídas por **Liberation Sans** e **Liberation Serif**, também com as mesmas medidas.

---

## Google Workspace

Em [drive.google.com](https://drive.google.com), *Novo* ➔ **Documentos**, **Planilhas** ou **Apresentações** do Google.

- **Salvamento automático** e **coautoria** em tempo real, como no OneDrive.
- **Compartilhar:** *Leitor*, *Comentarista* ou *Editor*; em *Acesso geral*, **Restrito** (só quem você adicionar) ou *Qualquer pessoa com o link*.
- **Modos de edição** (canto superior direito do Docs): **Editando**, **Sugerindo** (como o *Controlar Alterações* do Word) e **Visualizando**.
- **Histórico de versões:** *Arquivo ➔ Histórico de versões*.
- **Sem internet:** nas configurações do Drive, ative o modo **Off-line** (no navegador Chrome ou Edge) para editar sem conexão.

### Arquivos do Office no Google

- **Editar direto:** abra um `.docx`, `.xlsx` ou `.pptx` pelo Drive — ele é editado **no formato do Office** (aparece uma etiqueta `.DOCX` ao lado do nome).
- **Converter:** *Arquivo ➔ **Salvar como Documentos Google*** (ou Planilhas/Apresentações) para usar todos os recursos do Google.
- **Devolver no formato do Office:** *Arquivo ➔ **Fazer download*** ➔ *Microsoft Word (.docx)*, *Microsoft Excel (.xlsx)*, *Microsoft PowerPoint (.pptx)* ou **PDF**.

---

## O que costuma quebrar na troca

| Recurso | LibreOffice | Google Workspace |
|---|---|---|
| Texto, tabelas, estilos e sumário | Funciona bem | Funciona bem (sumário precisa ser atualizado) |
| Fontes que não existem no computador | Troca por fontes compatíveis | Troca pela fonte disponível mais parecida |
| Fórmulas comuns (`SOMA`, `SE`, `PROCV`, `CONT.SE`) | Funcionam | Funcionam |
| `PROCX`, `FILTRO`, `ÚNICO` | Funcionam no LibreOffice 24.8 ou mais novo | Funcionam (com os nomes em inglês, como `XLOOKUP`) |
| Tabela dinâmica | Vira *tabela dinâmica* do Calc | Vira *tabela dinâmica* do Planilhas; a segmentação de dados pode se perder |
| **Macros VBA** (`.xlsm`) | Nem sempre funcionam | **Não funcionam** |
| **SmartArt** | Vira um grupo de formas | Vira imagem (não dá para editar como diagrama) |
| Animações e transição **Transformar** | Animações simples funcionam; Transformar não | Animações simples funcionam; Transformar não |
| **Mala direta** do Word | Tem a sua própria (*Ferramentas ➔ Assistente de mala direta*) | Não tem nativa |

!!! tip "Regra de ouro da troca de arquivos"
    Combine **um** programa com o grupo para editar e use o **PDF** para entregar. Se for inevitável passar o arquivo de um programa para outro, **abra e confira** antes de enviar: numeração de páginas, sumário, fórmulas e slides animados são os primeiros a mudar.

---

## Qual escolher?

| Situação | Melhor opção |
|---|---|
| A escola fornece Microsoft 365 | **Office** (instalado ou na web) — é o que o curso usa |
| Computador sem internet ou internet ruim | **LibreOffice** |
| Trabalho em grupo, cada um no seu celular ou computador, ninguém com licença | **Google Workspace** (ou Office na web com contas pessoais) |
| Arquivo que o professor vai abrir no Word | Edite onde quiser, mas entregue em **PDF** (ou `.docx` conferido) |
| Planilha com macros | **Excel** |
| Software livre, sem conta em empresa nenhuma | **LibreOffice** |

---

??? note "Os mesmos comandos nos três programas"
    | Tarefa | Microsoft Office | LibreOffice | Google |
    |---|---|---|---|
    | Exportar PDF | *Arquivo ➔ Exportar ➔ Criar PDF/XPS* | *Arquivo ➔ Exportar como ➔ Exportar como PDF* | *Arquivo ➔ Fazer download ➔ PDF* |
    | Controlar alterações | *Revisão ➔ Controlar Alterações* | *Editar ➔ Rastrear alterações ➔ Gravar* | Modo **Sugerindo** |
    | Comentário | *Revisão ➔ Novo Comentário* | *Inserir ➔ Comentário* | *Inserir ➔ Comentário* |
    | Contar palavras | Barra de status | Barra de status | *Ferramentas ➔ Contagem de palavras* |
    | Tabela dinâmica | *Inserir ➔ Tabela Dinâmica* | *Inserir ➔ Tabela dinâmica* | *Inserir ➔ Tabela dinâmica* |
    | Apresentar | `F5` | `F5` | *Apresentação de slides* |

---

## ⚠️ Erros comuns

- **Baixar o LibreOffice de site “de downloads”.** Use só o site oficial.
- **Mandar `.odt` para quem só tem Word.** Às vezes abre, às vezes desconfigura. Salve em `.docx` ou mande o PDF.
- **Editar o mesmo arquivo em três programas diferentes.** Cada passagem muda um detalhe. Combine **um** programa.
- **Contar com a macro do Excel no Google Planilhas.** Ela não roda.
- **Esquecer de conferir o arquivo convertido.** Abra o `.docx` baixado do Google antes de mandar.

---

## Exercícios

### Básico (fixação)

1. Instale o **LibreOffice** pelo site oficial (ou, se não puder instalar, use o **Google Docs**).
2. Abra nele o **trabalho ABNT** do Módulo 01 (`.docx`) e anote o que mudou: fontes, numeração de páginas, sumário, quebras.
3. Exporte em **PDF** e compare com o PDF que você gerou no Word.

<!-- gabarito -->
??? success "Gabarito — Básico"
    1. [libreoffice.org](https://www.libreoffice.org) ➔ *Baixe agora* ➔ instale com as opções padrão. (No Google: [drive.google.com](https://drive.google.com) ➔ *Novo ➔ Upload de arquivo* ➔ abra o `.docx`.)
    2. *Arquivo ➔ Abrir* ➔ o `.docx`. O que **costuma** aparecer:
        - Fonte trocada se o computador não tem a original — em geral sem mudar a paginação.
        - **Sumário** com números certos, mas pode precisar atualizar: botão direito ➔ *Atualizar índice*.
        - **Numeração de páginas** por seção geralmente se mantém; confira a primeira página da introdução.
        - Recuos, espaçamentos e margens iguais.
    3. *Arquivo ➔ Exportar como ➔ Exportar como PDF* ➔ abra os dois PDFs lado a lado.

    **Se algo mudou:** é exatamente por isso que a entrega é em PDF — ele “congela” o documento como você o viu.

### Intermediário (aplicação)

1. No **Google Planilhas**, refaça a lista de compras da [aula 01 do Excel](../modulo_02_excel/01_celulas_formulas_e_referencias.md) com o total por item e o total geral.
2. Compartilhe a planilha com um colega como **Comentarista**; o colega deixa um comentário.
3. Faça o **download em `.xlsx`** e abra no Excel (ou no LibreOffice Calc). As fórmulas continuam funcionando?
4. No LibreOffice, configure o **formato padrão** de texto, planilha e apresentação para o formato do Office.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    1. *Novo ➔ Planilhas Google* ➔ cole a tabela em A1 ➔ **D2:** `=B2*C2` (arraste até D6) ➔ **D7:** `=SOMA(D2:D6)` ➔ **R$ 188,60**. Se o separador for vírgula em vez de ponto e vírgula, ajuste em *Arquivo ➔ Configurações ➔ Localidade: Brasil*.
    2. *Compartilhar* ➔ e-mail do colega ➔ **Comentarista** ➔ *Enviar*. O colega seleciona uma célula ➔ *Inserir ➔ Comentário*.
    3. *Arquivo ➔ Fazer download ➔ Microsoft Excel (.xlsx)* ➔ abra no Excel: as fórmulas aparecem na Barra de Fórmulas e o total é o mesmo. Os comentários também vão junto.
    4. *Ferramentas ➔ Opções ➔ Carregar/Salvar ➔ Geral* ➔ **Formato de arquivo padrão** ➔ *Documento de texto: Word 2007-365* · *Planilha: Excel 2007-365* · *Apresentação: PowerPoint 2007-365* ➔ *OK*. Daí em diante, o LibreOffice não pergunta mais o formato.

### Avançado (desafio)

Faça um **teste de compatibilidade** e registre em uma tabela (Programa · Arquivo · O que funcionou · O que quebrou):

1. A planilha com **macro** (`.xlsm`) e a de **tabela dinâmica** do Módulo 02, abertas no LibreOffice Calc **e** no Google Planilhas.
2. A apresentação com **SmartArt**, **gráfico** e transição **Transformar** do Módulo 03, aberta no LibreOffice Impress **e** no Google Apresentações.
3. Escreva uma **recomendação de três linhas** para um grupo em que só metade tem Microsoft Office.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    O que você deve encontrar (pode variar um pouco conforme as versões):

    | Programa | Arquivo | Funcionou | Quebrou |
    |---|---|---|---|
    | LibreOffice Calc | `.xlsm` com macro | Dados e fórmulas | A macro gravada pode não rodar (o Calc avisa sobre macros; o VBA tem suporte parcial) |
    | Google Planilhas | `.xlsm` com macro | Dados e fórmulas | A macro **não roda** |
    | LibreOffice Calc / Google Planilhas | tabela dinâmica | A tabela e os totais | Segmentação de dados; pode precisar recriar o filtro |
    | LibreOffice Impress | apresentação | Textos, imagens, gráfico (editável), transições simples | SmartArt vira grupo de formas; **Transformar** vira outra transição |
    | Google Apresentações | apresentação | Textos, imagens, transições simples | SmartArt vira imagem; gráfico vira imagem ou fica ligado à planilha; **Transformar** some |

    **Recomendação possível:** “Editem os textos no Google Docs ou no Office na web, onde todos conseguem coautoria. Gráficos e tabelas dinâmicas no Excel, por quem tem licença, e coloquem no documento como imagem. Entreguem tudo em PDF.”

---

## 💡 Resumo

- Três caminhos gratuitos: **Office na web**, **LibreOffice** (instalado, sem internet) e **Google Workspace** (no navegador, com 15 GB).
- LibreOffice: baixe **só** de libreoffice.org; formato **ODF** é padrão aberto; configure o **formato padrão do Office** para trocar arquivos.
- Google: coautoria, modo **Sugerindo**, **Fazer download** no formato do Office.
- Na troca, **macros**, **SmartArt**, **Transformar** e recursos novos são os que mais quebram. Combine **um** programa com o grupo e **entregue em PDF**.

## ➡️ Próximo passo

**[05 — Projeto do módulo: trabalho em grupo na nuvem](05_projeto_trabalho_em_grupo.md)**: organizar um trabalho de grupo do começo ao fim, com pasta compartilhada, coautoria, reunião e entrega.
