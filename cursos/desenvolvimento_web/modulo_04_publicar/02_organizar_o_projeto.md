# 02 — Organizar o projeto

> **Curso:** Desenvolvimento Web  
> **Módulo:** 04 — Publicar  
> **Tempo estimado:** 1 h  

---

## Objetivos

Ao final desta aula, você será capaz de:

- Organizar um site em pastas (`css/`, `js/`, `imagens/`) com caminhos relativos.
- Dar nomes de arquivo que funcionam em qualquer servidor.
- Escrever um `README.md` que apresenta o projeto.
- Preparar a página para aparecer bem no Google e quando o link é compartilhado.

## Pré-requisitos

- [Aula 01](01_fetch_e_apis.md) deste módulo.

---

## A estrutura de pastas

```text
portfolio/
├── index.html
├── projetos.html
├── README.md
├── css/
│   └── style.css
├── js/
│   └── script.js
└── imagens/
    ├── foto.jpg
    └── cardapio.png
```

Com os arquivos em pastas, os caminhos mudam:

```html
<link rel="stylesheet" href="css/style.css">
<script src="js/script.js" defer></script>
<img src="imagens/foto.jpg" alt="…">
```

!!! warning "Regras de nome que evitam dor de cabeça"
    - **Página inicial** sempre `index.html`: é a que o servidor abre sozinho.
    - Só **minúsculas**, sem espaço e sem acento: `minha-foto.jpg`. No seu Windows, `Foto.JPG` e `foto.jpg` são o mesmo arquivo, mas no servidor do GitHub **não são**, e a imagem some.
    - Caminhos **relativos** (`imagens/foto.jpg`), nunca `C:\Users\…`.

---

## `README.md`

O `README.md` é a “capa” do projeto no GitHub. Ele é escrito em **Markdown**:

```markdown
# Portfólio da Ana Souza

Site com os projetos que fiz no curso de Desenvolvimento Web.

## Projetos
- Página de apresentação (HTML)
- Cardápio responsivo (CSS)
- Lista de tarefas (JavaScript)

## Tecnologias
HTML, CSS e JavaScript, sem bibliotecas.

Veja no ar: https://anasouza.github.io
```

---

## Aparecer bem no Google e no WhatsApp

No `<head>` de cada página:

```html
<meta name="description" content="Portfólio da Ana Souza: projetos de HTML, CSS e JavaScript.">
<meta property="og:title" content="Portfólio da Ana Souza">
<meta property="og:description" content="Projetos de HTML, CSS e JavaScript.">
<meta property="og:image" content="https://anasouza.github.io/imagens/capa.png">
<link rel="icon" href="imagens/icone.png">
```

- `description`: o resumo que aparece embaixo do título no Google.
- `og:` (*Open Graph*): título, descrição e imagem que aparecem quando alguém **compartilha o link** no WhatsApp ou nas redes. A imagem precisa do endereço completo.
- `icon`: o ícone da aba (*favicon*).

---

## Exercícios

### Básico (fixação)

Reorganize o projeto do cardápio (Módulo 02) com a pasta `css/` e ajuste o `<link>`.

<!-- gabarito -->
??? success "Gabarito — Básico"
    Mova `style.css` para `css/style.css` e troque para `<link rel="stylesheet" href="css/style.css">`. Se a página ficar sem estilo, o caminho está errado: confira no `F12` ➔ **Rede**, que mostra o arquivo em vermelho (404).

### Intermediário (aplicação)

Escreva o `README.md` da sua lista de tarefas, com o que ela faz e como usar.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    Um título (`# Lista de tarefas`), um parágrafo sobre o que faz, uma lista com as funções (adicionar, marcar, apagar, guarda no navegador) e uma seção “Como usar” (abrir o `index.html` no navegador). Markdown simples basta.

### Avançado (desafio)

Uma imagem aparece no seu computador, mas não no site publicado. O código é `<img src="Imagens/Foto.JPG">` e o arquivo é `imagens/foto.jpg`. Explique e corrija.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    O Windows não diferencia maiúsculas de minúsculas; o servidor do GitHub Pages diferencia. Para ele, `Imagens/Foto.JPG` não existe. Corrija para `<img src="imagens/foto.jpg" alt="…">`, exatamente igual ao nome do arquivo.

---

## 💡 Resumo

- Pastas `css/`, `js/`, `imagens/` e caminhos relativos.
- `index.html`; nomes em minúsculas, sem espaço e sem acento.
- `README.md` em Markdown apresenta o projeto.
- `description`, `og:` e `icon` cuidam do Google, do WhatsApp e da aba.

## ➡️ Próximo passo

Na **[aula 03](03_github_pages.md)** você publica o site.
