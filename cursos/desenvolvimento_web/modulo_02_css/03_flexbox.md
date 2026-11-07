# 03 — Flexbox

> **Curso:** Desenvolvimento Web  
> **Módulo:** 02 — CSS  
> **Tempo estimado:** 1 h 30 min  

---

## Objetivos

Ao final desta aula, você será capaz de:

- Pôr elementos **lado a lado** com `display: flex`.
- Distribuir o espaço com `justify-content` e alinhar com `align-items`.
- Separar os itens com `gap` e deixá-los quebrar de linha com `flex-wrap`.
- Fazer um item crescer com `flex`.

## Pré-requisitos

- [Aula 02](02_modelo_de_caixa.md) deste módulo.

---

## A ideia

O Flexbox organiza os **filhos** de uma caixa numa **linha** (ou coluna). Você aplica `display: flex` no **pai** (o *container*), e os filhos (os *itens*) se arrumam.

```html
<nav>
  <ul class="menu">
    <li><a href="#sobre">Sobre</a></li>
    <li><a href="#habilidades">Habilidades</a></li>
    <li><a href="#contato">Contato</a></li>
  </ul>
</nav>
```

```css
.menu {
  display: flex;
  gap: 16px;
  list-style: none;
  padding: 0;
}
```

Pronto: o menu fica na horizontal, com 16 px entre os links. `list-style: none` tira as bolinhas da lista.

---

## As propriedades do container

| Propriedade | Valores mais usados | Faz |
|---|---|---|
| `flex-direction` | `row` (padrão), `column` | Itens em linha ou em coluna |
| `justify-content` | `flex-start`, `center`, `flex-end`, `space-between`, `space-around` | Distribui no **eixo principal** (na horizontal, se for linha) |
| `align-items` | `stretch` (padrão), `center`, `flex-start`, `flex-end` | Alinha no **outro eixo** (na vertical, se for linha) |
| `gap` | `16px` | Espaço **entre** os itens |
| `flex-wrap` | `nowrap` (padrão), `wrap` | Deixa os itens irem para a linha de baixo quando não cabem |

### Cabeçalho clássico: nome à esquerda, menu à direita

```css
header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
}
```

### Centralizar de verdade (na horizontal e na vertical)

```css
.centro {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;   /* 100% da altura da tela */
}
```

!!! tip "Brinque para aprender"
    O jogo gratuito **Flexbox Froggy** (procure pelo nome) ensina as propriedades com sapinhos em vitórias-régias. Leva uns 20 minutos e fixa muito bem.

---

## As propriedades dos itens

| Propriedade | Exemplo | Faz |
|---|---|---|
| `flex` | `flex: 1;` | O item **cresce** para ocupar o espaço livre |
| `flex: 0 0 200px;` | — | Largura fixa de 200 px, sem crescer nem encolher |
| `align-self` | `align-self: flex-end;` | Alinha só aquele item, diferente dos outros |
| `order` | `order: -1;` | Muda a posição visual (use com cuidado: o leitor de tela segue o código) |

```css
.busca input { flex: 1; }   /* o campo ocupa o que sobrar ao lado do botão */
```

---

## Exercícios

### Básico (fixação)

Deixe o menu da página de apresentação na horizontal, sem bolinhas, com 24 px entre os links.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```css
    nav ul { display: flex; gap: 24px; list-style: none; padding: 0; }
    ```

### Intermediário (aplicação)

Faça o `<header>` mostrar o nome à esquerda e o menu à direita, alinhados pela linha do meio.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```css
    header { display: flex; justify-content: space-between; align-items: center; }
    ```
    Se o `<p>` com o subtítulo estiver no header, agrupe o `<h1>` e o `<p>` numa `<div>`: assim o header tem dois filhos (a div e o nav) e o `space-between` empurra um para cada lado.

### Avançado (desafio)

Monte três cartões lado a lado que, em telas estreitas, passem para a linha de baixo automaticamente, cada um com no mínimo 220 px.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```css
    .cartoes { display: flex; flex-wrap: wrap; gap: 16px; }
    .cartao { flex: 1 1 220px; }
    ```
    `flex: 1 1 220px` = cresce, encolhe e parte de 220 px. Quando três de 220 px não cabem, o `wrap` leva o último para baixo, e ele cresce para ocupar a linha.

---

## 💡 Resumo

- `display: flex` vai no **pai**; os filhos se alinham numa linha.
- `justify-content` distribui no eixo principal; `align-items` alinha no outro.
- `gap` separa; `flex-wrap: wrap` quebra a linha; `flex: 1` faz crescer.

## ➡️ Próximo passo

Na **[aula 04](04_grid_e_responsivo.md)** você monta grades com Grid e adapta a página ao celular.
