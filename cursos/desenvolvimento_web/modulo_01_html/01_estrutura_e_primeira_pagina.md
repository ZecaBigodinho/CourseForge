# 01 — Estrutura e primeira página

> **Curso:** Desenvolvimento Web  
> **Módulo:** 01 — HTML  
> **Tempo estimado:** 1 h 30 min  

---

## Objetivos

Ao final desta aula, você será capaz de:

- Explicar o papel do **HTML**, do **CSS** e do **JavaScript** numa página.
- Preparar a pasta do projeto e o **VS Code** (com a extensão Live Server).
- Escrever a **estrutura básica** de um arquivo HTML e entender cada linha.
- Usar **tags**, **atributos** e **comentários**.

## Pré-requisitos

- Saber criar pastas e abrir um navegador.

---

## Como uma página chega até você

Quando você abre um site, o navegador baixa um arquivo de texto em **HTML** e o “desenha” na tela. Junto vêm arquivos de **CSS** (aparência) e **JavaScript** (comportamento).

| Linguagem | Papel | Comparação com uma casa |
|---|---|---|
| **HTML** | O que tem na página | Paredes, portas e cômodos |
| **CSS** | Como aparece | Pintura e decoração |
| **JavaScript** | O que faz | Interruptores e campainha |

HTML **não é** uma linguagem de programação: é uma linguagem de **marcação**. Ela não faz contas nem toma decisões; só diz o que é cada parte do conteúdo.

---

## Preparar o ambiente

1. Instale o **[VS Code](https://code.visualstudio.com/)**.
2. No VS Code, abra a aba **Extensões** (`Ctrl + Shift + X`), procure **Live Server** e instale. Ela abre a página no navegador e **atualiza sozinha** quando você salva.
3. Crie uma pasta `curso-web` em *Documentos* e, dentro dela, `aula01`.
4. No VS Code: **Arquivo ➔ Abrir Pasta** ➔ escolha `curso-web`.

---

## A estrutura básica

Crie o arquivo `aula01/index.html` e digite:

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Minha primeira página</title>
</head>
<body>
  <h1>Olá, mundo!</h1>
  <p>Esta é a minha primeira página na web.</p>
</body>
</html>
```

Salve (`Ctrl + S`), clique com o botão direito no arquivo ➔ **Open with Live Server**. O navegador abre mostrando o título grande e o parágrafo.

| Linha | O que faz |
|---|---|
| `<!DOCTYPE html>` | Avisa que é HTML moderno (HTML5). Sempre a primeira linha |
| `<html lang="pt-BR">` | Começa a página e diz o idioma (ajuda leitores de tela e o tradutor) |
| `<head>` | **Informações sobre** a página, que não aparecem no corpo |
| `<meta charset="UTF-8">` | Faz os **acentos** aparecerem certos (ç, ã, é) |
| `<meta name="viewport" …>` | Ajusta a página à largura do **celular** |
| `<title>` | O texto da **aba** do navegador e do resultado no Google |
| `<body>` | **Tudo o que aparece** na página |

!!! tip "Atalho do VS Code"
    Num arquivo `.html` vazio, digite `!` e tecle `Tab`: o VS Code escreve a estrutura básica inteira (troque `lang="en"` por `lang="pt-BR"`).

---

## Tags, atributos e comentários

Uma **tag** marca um pedaço de conteúdo. A maioria tem **abertura** e **fechamento**:

```html
<p>Um parágrafo.</p>
```

Algumas não têm conteúdo e por isso não fecham, como `<meta>`, `<img>` e `<br>`.

Um **atributo** dá informação extra à tag e fica **dentro da abertura**, no formato `nome="valor"`:

```html
<html lang="pt-BR">
```

Um **comentário** é uma anotação que o navegador ignora:

```html
<!-- Isto não aparece na página -->
```

!!! warning "Tags dentro de tags: feche na ordem certa"
    Uma tag aberta dentro de outra deve fechar **antes** dela: `<p>Texto <strong>forte</strong></p>` está certo; `<p>Texto <strong>forte</p></strong>` está errado. Use a **indentação** (o recuo com espaços) para enxergar quem está dentro de quem.

---

## Ver o código de qualquer site

Em qualquer página, tecle `Ctrl + U` para ver o HTML dela, ou `F12` para abrir as **Ferramentas do desenvolvedor**. Na guia **Elementos**, passe o mouse sobre o código e veja a parte correspondente acender na página. É a melhor forma de aprender com sites de verdade.

---

## Exercícios

### Básico (fixação)

Mude o `<title>` para o seu nome e o `<h1>` para “Bem-vindo à minha página”. Confira a aba do navegador.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```html
    <title>Ana Souza</title>
    ...
    <h1>Bem-vindo à minha página</h1>
    ```
    O `<title>` aparece **na aba**, não dentro da página. Com o Live Server, basta salvar para ver a mudança.

### Intermediário (aplicação)

Apague a linha `<meta charset="UTF-8">`, salve e observe os acentos. Depois coloque a linha de volta.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    Sem o `charset`, alguns navegadores podem mostrar “pÃ¡gina” no lugar de “página”: eles “adivinham” a codificação e erram. Com `<meta charset="UTF-8">` (e o arquivo salvo em UTF-8, o padrão do VS Code), os acentos sempre aparecem certos.

### Avançado (desafio)

Encontre e corrija os três erros deste código:

```html
<html>
<head>
  <title>Teste<title>
</head>
<body>
  <p>Texto <strong>importante</p></strong>
</body>
```

<!-- gabarito -->
??? success "Gabarito — Avançado"
    1. Falta `<!DOCTYPE html>` na primeira linha (e o ideal é `<html lang="pt-BR">`).
    2. O `<title>` não fecha: o certo é `</title>`, com a barra.
    3. As tags estão fechadas fora de ordem: `<p>Texto <strong>importante</strong></p>`.

    Também falta fechar `</html>` no fim.

---

## 💡 Resumo

- HTML = conteúdo; CSS = aparência; JavaScript = comportamento.
- Estrutura básica: `<!DOCTYPE html>`, `<html lang="pt-BR">`, `<head>` (charset, viewport, title) e `<body>`.
- Tags abrem e fecham **na ordem certa**; atributos ficam na abertura.
- `Ctrl + U` e `F12` mostram o HTML de qualquer site.

## ➡️ Próximo passo

Na **[aula 02](02_textos_links_e_imagens.md)** você escreve textos, cria links e coloca imagens.
