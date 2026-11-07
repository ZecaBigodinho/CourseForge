# 03 — Listas e tabelas

> **Curso:** Desenvolvimento Web  
> **Módulo:** 01 — HTML  
> **Tempo estimado:** 1 h 30 min  

---

## Objetivos

Ao final desta aula, você será capaz de:

- Criar listas **sem ordem**, **numeradas** e **aninhadas**.
- Montar **tabelas** com cabeçalho, corpo e legenda.
- Juntar células com `colspan` e `rowspan`.
- Saber quando **não** usar tabela.

## Pré-requisitos

- [Aula 02](02_textos_links_e_imagens.md) deste módulo.

---

## Listas

**Sem ordem** (`<ul>`, *unordered list*), quando a ordem não importa:

```html
<h2>Ingredientes</h2>
<ul>
  <li>3 cenouras</li>
  <li>3 ovos</li>
  <li>2 xícaras de farinha</li>
</ul>
```

**Numerada** (`<ol>`, *ordered list*), quando a ordem importa:

```html
<h2>Modo de preparo</h2>
<ol>
  <li>Bata as cenouras, os ovos e o óleo no liquidificador.</li>
  <li>Misture com a farinha e o açúcar.</li>
  <li>Asse por 40 minutos.</li>
</ol>
```

Cada item é um `<li>` (*list item*). Para uma lista **dentro** de um item, abra a nova lista **antes** de fechar o `</li>`:

```html
<ul>
  <li>Frutas
    <ul>
      <li>Maçã</li>
      <li>Banana</li>
    </ul>
  </li>
  <li>Verduras</li>
</ul>
```

!!! tip "Menus são listas"
    O menu de navegação de quase todo site é uma `<ul>` de links dentro de `<nav>`. No Módulo 02 o CSS deixa essa lista na horizontal.
    ```html
    <nav>
      <ul>
        <li><a href="index.html">Início</a></li>
        <li><a href="sobre.html">Sobre</a></li>
      </ul>
    </nav>
    ```

---

## Tabelas

Tabelas servem para **dados em linhas e colunas**, como horários, notas e preços:

```html
<table>
  <caption>Horário da turma — 1º A</caption>
  <thead>
    <tr>
      <th scope="col">Horário</th>
      <th scope="col">Segunda</th>
      <th scope="col">Terça</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">7h30</th>
      <td>Matemática</td>
      <td>Português</td>
    </tr>
    <tr>
      <th scope="row">8h20</th>
      <td>História</td>
      <td>Informática</td>
    </tr>
  </tbody>
</table>
```

| Tag | Significado |
|---|---|
| `<table>` | A tabela inteira |
| `<caption>` | A **legenda** (título da tabela) |
| `<thead>` / `<tbody>` / `<tfoot>` | Cabeçalho, corpo e rodapé |
| `<tr>` | Uma **linha** (*table row*) |
| `<th>` | Célula de **cabeçalho**; `scope="col"` ou `scope="row"` diz se ela titula a coluna ou a linha |
| `<td>` | Célula de **dado** |

Sem CSS, a tabela aparece sem bordas. Isso é normal: a aparência vem no Módulo 02.

### Juntar células

```html
<tr>
  <th scope="row">9h10</th>
  <td colspan="2">Intervalo</td>
</tr>
```

- `colspan="2"`: a célula ocupa **duas colunas**.
- `rowspan="2"`: a célula ocupa **duas linhas** (e a linha de baixo fica com uma célula a menos).

!!! warning "Tabela não é para montar layout"
    Antigamente se usavam tabelas para posicionar o site inteiro. Hoje isso é feito com CSS (Flexbox e Grid). Use tabela **só para dados tabulares**: leitores de tela leem a tabela célula por célula, com os cabeçalhos.

---

## Exercícios

### Básico (fixação)

Faça a receita de um prato de que você gosta, com a lista de **ingredientes** (sem ordem) e o **modo de preparo** (numerado).

<!-- gabarito -->
??? success "Gabarito — Básico"
    Um `<h1>` com o nome do prato; `<h2>Ingredientes</h2>` seguido de `<ul>` com um `<li>` por ingrediente; `<h2>Modo de preparo</h2>` seguido de `<ol>` com um `<li>` por passo. Se os passos aparecerem com números, a `<ol>` está certa.

### Intermediário (aplicação)

Monte uma tabela de **notas** com três alunos (inventados), as colunas *Aluno*, *1º bimestre*, *2º bimestre* e uma linha de **média da turma** no `<tfoot>`.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```html
    <table>
      <caption>Notas — Informática</caption>
      <thead>
        <tr><th scope="col">Aluno</th><th scope="col">1º bim.</th><th scope="col">2º bim.</th></tr>
      </thead>
      <tbody>
        <tr><th scope="row">Ana</th><td>8,0</td><td>9,0</td></tr>
        <tr><th scope="row">Bruno</th><td>7,0</td><td>6,5</td></tr>
        <tr><th scope="row">Carla</th><td>9,5</td><td>8,5</td></tr>
      </tbody>
      <tfoot>
        <tr><th scope="row">Média</th><td>8,2</td><td>8,0</td></tr>
      </tfoot>
    </table>
    ```

### Avançado (desafio)

No horário da turma, acrescente uma linha **Intervalo** que ocupe todas as colunas de dias, e uma aula de **Educação Física** que dure dois horários seguidos na segunda-feira.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    Intervalo: `<td colspan="2">Intervalo</td>` (o número de colunas de dias). Educação Física na segunda, nas linhas de 7h30 e 8h20: na primeira linha, `<td rowspan="2">Educação Física</td>`; na linha seguinte, **retire** a célula da segunda-feira (ela já está ocupada), deixando só a de terça.

---

## 💡 Resumo

- `<ul>` quando a ordem não importa; `<ol>` quando importa; itens em `<li>`.
- Menus de navegação são `<ul>` de links dentro de `<nav>`.
- Tabela: `<caption>`, `<thead>`, `<tbody>`, `<tr>`, `<th scope>` e `<td>`.
- `colspan` e `rowspan` juntam células; tabela só para **dados**, nunca para layout.

## ➡️ Próximo passo

Na **[aula 04](04_formularios.md)** você cria formulários para receber dados do visitante.
