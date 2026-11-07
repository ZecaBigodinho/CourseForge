# 01 — Seletores, cores e fontes

> **Curso:** Desenvolvimento Web  
> **Módulo:** 02 — CSS  
> **Tempo estimado:** 1 h 30 min  

---

## Objetivos

Ao final desta aula, você será capaz de:

- Ligar um arquivo **CSS** ao HTML.
- Escrever **regras** com seletor, propriedade e valor.
- Escolher elementos por **tag**, **classe** e **`id`**, e entender a **cascata**.
- Definir **cores**, **fontes** e tamanhos com as unidades certas.

## Pré-requisitos

- [Módulo 01 — HTML](../modulo_01_html/index.md) completo.

---

## Ligar o CSS ao HTML

Crie `style.css` na mesma pasta do `index.html` e ligue os dois dentro do `<head>`:

```html
<link rel="stylesheet" href="style.css">
```

Um arquivo de CSS separado vale para **todas** as páginas que o ligarem: trocar uma cor num lugar muda o site inteiro.

## Anatomia de uma regra

```css
h1 {
  color: #4f35b5;
  font-size: 2rem;
}
```

- `h1` é o **seletor**: escolhe quem recebe o estilo.
- Entre chaves, cada linha é uma **declaração**: `propriedade: valor;`, sempre com **ponto e vírgula**.
- Comentários em CSS: `/* assim */`.

---

## Seletores

| Seletor | Escolhe | Exemplo |
|---|---|---|
| Tag | Todos os elementos daquela tag | `p { }` |
| Classe (`.`) | Quem tem `class="destaque"` | `.destaque { }` |
| `id` (`#`) | O elemento com `id="contato"` (único na página) | `#contato { }` |
| Descendente (espaço) | `a` que está **dentro** de `nav` | `nav a { }` |
| Grupo (vírgula) | Vários de uma vez | `h1, h2 { }` |
| Estado (`:`) | Link com o mouse em cima | `a:hover { }` |

```html
<p class="destaque">Promoção de hoje!</p>
<p class="destaque aviso">Um elemento pode ter várias classes.</p>
```

!!! tip "Prefira classes"
    Use **classes** para estilizar: podem ser reaproveitadas em vários elementos. Deixe o `id` para links internos (`#contato`) e, no Módulo 03, para o JavaScript.

### A cascata

Quando duas regras mandam no mesmo elemento:

1. A mais **específica** vence: `id` > classe > tag.
2. Empate? Vence a que vem **por último** no arquivo.
3. Algumas propriedades (cor, fonte) são **herdadas**: definidas no `body`, valem para tudo dentro dele.

---

## Cores

| Forma | Exemplo | Observação |
|---|---|---|
| Nome | `red`, `white` | Poucas opções |
| Hexadecimal | `#4f35b5` | A mais comum; a mesma do Canva e do CorelDRAW |
| RGB | `rgb(79 53 181)` | Vermelho, verde, azul de 0 a 255 |
| Com transparência | `rgb(79 53 181 / 50%)` | O último valor é a opacidade |

```css
body {
  background-color: #f7f5ff;
  color: #222;
}
```

!!! warning "Contraste"
    Texto cinza-claro em fundo branco é difícil de ler. Confira o contraste em sites de verificação (procure por “contrast checker”): para texto comum, a razão deve ser de pelo menos **4,5 : 1**.

---

## Fontes e unidades

```css
body {
  font-family: "Segoe UI", Arial, sans-serif;
  font-size: 1rem;
  line-height: 1.5;
}
h1 {
  font-weight: 700;
  text-align: center;
}
```

- `font-family`: uma lista de fontes, da preferida à mais garantida. Sempre termine com uma **genérica** (`sans-serif`, `serif`, `monospace`).
- `line-height: 1.5`: espaço entre linhas confortável para leitura.

| Unidade | Significado | Use para |
|---|---|---|
| `px` | Pixels, tamanho fixo | Bordas, detalhes |
| `rem` | Múltiplo da fonte padrão do navegador (em geral 16 px) | **Fontes** e espaços: respeita quem aumenta a letra no navegador |
| `%` | Porcentagem do elemento “pai” | Larguras |

### Fontes do Google Fonts

Em [fonts.google.com](https://fonts.google.com), escolha uma fonte, copie o `<link>` para o `<head>` (antes do seu `style.css`) e use o nome dela no `font-family`.

---

## Exercícios

### Básico (fixação)

Ligue um `style.css` à página de apresentação do Módulo 01 e deixe o fundo levemente colorido, o texto cinza-escuro e o `<h1>` na cor `#4f35b5`.

<!-- gabarito -->
??? success "Gabarito — Básico"
    No `<head>`: `<link rel="stylesheet" href="style.css">`. No `style.css`:
    ```css
    body { background-color: #f7f5ff; color: #333; }
    h1 { color: #4f35b5; }
    ```
    Se nada mudou, confira o nome do arquivo e se o `<link>` está dentro do `<head>`.

### Intermediário (aplicação)

Faça os links do menu ficarem sem sublinhado e mudarem de cor quando o mouse passa por cima, sem afetar os outros links da página.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```css
    nav a { text-decoration: none; color: #4f35b5; }
    nav a:hover { color: #e8781e; }
    ```
    O seletor `nav a` pega só os links **dentro** do `<nav>`.

### Avançado (desafio)

Este parágrafo fica de que cor? Explique.

```html
<p id="aviso" class="alerta">Atenção</p>
```
```css
#aviso { color: green; }
.alerta { color: red; }
p { color: blue; }
```

<!-- gabarito -->
??? success "Gabarito — Avançado"
    **Verde.** O seletor de `id` é o mais específico dos três, então vence mesmo vindo antes no arquivo. A ordem só desempata regras de mesma especificidade.

---

## 💡 Resumo

- `<link rel="stylesheet" href="style.css">` no `<head>`; regras `seletor { propriedade: valor; }`.
- Seletores: tag, `.classe`, `#id`, descendente, grupo, `:hover`. Prefira classes.
- Cascata: `id` > classe > tag; empate, vence a última.
- Cores em hexadecimal; fontes com lista e genérica; tamanhos de fonte em `rem`.

## ➡️ Próximo passo

Na **[aula 02](02_modelo_de_caixa.md)** você controla espaços, bordas e tamanhos.
