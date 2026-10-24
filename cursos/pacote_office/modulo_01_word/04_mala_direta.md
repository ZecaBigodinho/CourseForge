# 04 — Mala direta: certificados e etiquetas em lote

> **Curso:** Pacote Office  
> **Módulo:** 01 — Word  
> **Tempo estimado:** 1 h 30 min  

---

## Objetivos

Ao final desta aula, você será capaz de:

- Explicar como a mala direta junta um **documento modelo** e uma **lista de dados**.
- Preparar a lista de dados no **Excel**.
- Gerar **certificados** e **etiquetas** em lote.
- Filtrar destinatários, usar **regras condicionais** e corrigir o formato de **datas e números**.

## Pré-requisitos

- [Aula 01](01_primeiros_passos_e_formatacao.md): formatação básica.
- Saber digitar dados numa planilha do Excel (o [Módulo 02 — Excel](../modulo_02_excel/index.md) aprofunda).

!!! warning "Precisa do Word instalado"
    A mala direta fica na aba **Correspondências**, que existe no Word **instalado** no computador. O Word na web (navegador) não tem essa aba. Se estiver no navegador, clique em **Editando ➔ Abrir no Aplicativo da Área de Trabalho**.

---

## Como funciona

A mala direta junta duas coisas:

```mermaid
flowchart LR
    A["📄 Modelo no Word<br/>Certificamos que «Nome»..."] --> C{"Mala direta"}
    B["📊 Lista no Excel<br/>Nome | Curso | Data"] --> C
    C --> D["Certificado da Ana"]
    C --> E["Certificado do Bruno"]
    C --> F["... um por linha da planilha"]
```

O modelo tem **campos** (como «Nome»). Para cada linha da planilha, o Word cria uma cópia do modelo com os dados daquela linha.

---

## 1) Preparar a lista no Excel

Regras para a planilha não dar problema:

- **Primeira linha = nomes das colunas**, curtos e sem espaços: `Nome`, `Curso`, `Carga`, `Data`.
- Uma pessoa por linha, **sem linhas em branco** no meio.
- Os dados começam na célula **A1**, na **primeira aba**.

Exemplo (salve como `participantes.xlsx`):

| Nome | Curso | Carga | Data |
|---|---|---|---|
| Ana Souza | Pacote Office | 40 | 24/10/2026 |
| Bruno Lima | Pacote Office | 40 | 24/10/2026 |
| Carla Dias | Introdução à IA | 20 | 24/10/2026 |

!!! tip "Feche o Excel antes de conectar"
    Se a planilha estiver aberta, o Word pode não conseguir lê-la. Salve e feche.

---

## 2) Montar o modelo e conectar

1. No Word, crie o modelo do certificado: *Layout ➔ Orientação ➔ Paisagem*, título “CERTIFICADO” e o texto com espaços para os dados.
2. *Correspondências ➔ Iniciar Mala Direta ➔ **Cartas***.
3. *Selecionar Destinatários ➔ **Usar uma Lista Existente*** ➔ escolha `participantes.xlsx` ➔ a aba (ex.: *Planilha1$*) ➔ marque **A primeira linha de dados contém cabeçalhos de coluna**.
4. Clique onde vai o nome ➔ *Inserir Campo de Mesclagem* ➔ **Nome**. Repita com **Curso**, **Carga** e **Data**.

O texto fica assim:

> Certificamos que **«Nome»** concluiu o curso **«Curso»**, com carga horária de «Carga» horas, em «Data».

5. *Visualizar Resultados*: as setas mostram cada certificado com os dados reais.

---

## 3) Concluir

*Concluir e Mesclar*:

- **Editar Documentos Individuais** ➔ *Todos*: cria um documento novo com **todos** os certificados, um por página. Revise, salve e exporte em PDF.
- **Imprimir Documentos**: manda direto para a impressora.

---

## Etiquetas

Mesmo processo, outro tipo: *Iniciar Mala Direta ➔ **Etiquetas*** ➔ escolha o fabricante e o modelo da folha de etiquetas (ex.: *Pimaco*, código impresso na caixa). Insira os campos na primeira etiqueta e clique em **Atualizar Etiquetas** para repetir nas demais.

---

## Filtros, regras e formatos

- **Filtrar**: *Editar Lista de Destinatários* ➔ clique na seta de uma coluna (ex.: *Curso*) ➔ escolha um valor. Só esses entram na mesclagem.
- **Regras**: *Regras ➔ **Se...Então...Senão***. Ex.: se *Carga* for maior ou igual a 40, escreva “com carga horária ampliada”; senão, nada.
- **Datas e números com formato errado** (ex.: a data aparece como `10/24/2026`): pressione `Alt + F9` para ver os códigos dos campos e acrescente o formato dentro das chaves:

    ```text
    { MERGEFIELD Data \@ "dd/MM/yyyy" }
    ```

    Depois `Alt + F9` de novo. Outra saída é deixar a coluna como **Texto** no Excel antes de conectar.

---

??? note "Equivalentes gratuitos: LibreOffice Writer e Google Docs"
    | Tarefa | LibreOffice Writer | Google Docs |
    |---|---|---|
    | Mala direta | *Ferramentas ➔ Assistente de mala direta* (aceita `.xlsx`, `.ods` e `.csv`) | Não tem nativo — precisa de um complemento (*Extensões ➔ Complementos*) |
    | Etiquetas | *Arquivo ➔ Novo ➔ Etiquetas* | Complemento |

---

## ⚠️ Erros comuns

- **Linha em branco no meio da planilha**: a mesclagem para ali ou gera um certificado vazio.
- **Cabeçalho com espaços ou acentos estranhos** (`Nome do Aluno `): o campo fica difícil de achar. Prefira `Nome`.
- **Esquecer de visualizar** antes de concluir e imprimir 40 certificados com erro.
- **Editar o documento final em vez do modelo**: correções no modelo e mescle de novo.

---

## Exercícios

### Básico (fixação)

Crie a planilha `participantes.xlsx` da aula (com seus colegas no lugar dos nomes) e gere os **certificados** em paisagem com os campos *Nome*, *Curso*, *Carga* e *Data*. Visualize todos antes de concluir e exporte o resultado em PDF.

<!-- gabarito -->
??? success "Gabarito — Básico"
    1. No Excel: cabeçalhos em A1:D1 (`Nome`, `Curso`, `Carga`, `Data`), um participante por linha, sem linhas vazias. Salve e **feche**.
    2. No Word: *Layout ➔ Orientação ➔ Paisagem*. Escreva “CERTIFICADO” (centralizado, grande) e o texto da aula.
    3. *Correspondências ➔ Iniciar Mala Direta ➔ Cartas* ➔ *Selecionar Destinatários ➔ Usar uma Lista Existente* ➔ `participantes.xlsx` ➔ *Planilha1$* ➔ cabeçalhos marcados.
    4. Insira os quatro campos com *Inserir Campo de Mesclagem*.
    5. *Visualizar Resultados* e passe pelas setas.
    6. *Concluir e Mesclar ➔ Editar Documentos Individuais ➔ Todos* ➔ no documento novo, *Arquivo ➔ Exportar ➔ Criar PDF*.

    **Confira:** o PDF tem uma página por linha da planilha.

### Intermediário (aplicação)

Com a mesma planilha:

1. Gere **etiquetas** com *Nome* e *Curso* para uma folha de etiquetas.
2. Gere certificados **só** de quem fez *Pacote Office*.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    1. Documento novo ➔ *Iniciar Mala Direta ➔ Etiquetas* ➔ escolha o modelo da folha (ex.: Pimaco, código da caixa) ➔ *Selecionar Destinatários ➔ Usar uma Lista Existente*. Na primeira etiqueta: **«Nome»** `Enter` «Curso». Clique em **Atualizar Etiquetas** ➔ *Visualizar* ➔ *Concluir e Mesclar*.
    2. No documento dos certificados: *Editar Lista de Destinatários* ➔ seta da coluna **Curso** ➔ **Pacote Office**. Visualize: os outros cursos sumiram. *Concluir e Mesclar*.

    **Para voltar a todos:** seta da coluna ➔ **(Todos)**.

### Avançado (desafio)

1. A data dos certificados está saindo como `10/24/2026`. Corrija para `24/10/2026` **sem mexer na planilha**.
2. Acrescente uma regra: se a carga horária for **40 ou mais**, o certificado ganha a frase “**com aproveitamento integral do curso**”; senão, nada.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    1. `Alt + F9` mostra os códigos. O campo da data fica assim: `{ MERGEFIELD Data }`. Mude para:

        ```text
        { MERGEFIELD Data \@ "dd/MM/yyyy" }
        ```

        `Alt + F9` de novo ➔ *Visualizar Resultados*: aparece `24/10/2026`. (`MM` maiúsculo é mês; `mm` minúsculo seria minuto.)
    2. Posicione o cursor depois de «Carga» horas ➔ *Regras ➔ Se...Então...Senão* ➔ *Nome do campo*: **Carga**, *Comparação*: **Maior que ou igual a**, *Comparar com*: **40**, *Inserir este texto*: “ com aproveitamento integral do curso”, *Caso contrário*: (vazio) ➔ *OK*.

    **Confira:** visualize uma pessoa com carga 40 (frase aparece) e uma com 20 (não aparece).

---

## 💡 Resumo

- Mala direta = **modelo** (com campos «...») + **lista** (planilha) ➔ um documento por linha.
- Planilha limpa: cabeçalhos na linha 1, sem linhas vazias, arquivo fechado.
- *Visualizar Resultados* **antes** de concluir.
- **Filtros** escolhem quem entra; **Regras** mudam o texto conforme os dados; `\@ "dd/MM/yyyy"` corrige datas.
- Só no Word **instalado**.

## ➡️ Próximo passo

**[05 — Projeto do módulo](05_projeto_trabalho_abnt.md)**: junte tudo num trabalho escolar completo no padrão ABNT.
