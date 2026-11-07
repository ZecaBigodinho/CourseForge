# 05 — Projeto do módulo: página de apresentação

> **Curso:** Desenvolvimento Web  
> **Módulo:** 01 — HTML  
> **Tempo estimado:** 2 h  

---

## Objetivos

Ao final deste projeto, você terá:

- Uma página `index.html` com a sua **apresentação**, organizada com tags **semânticas**.
- Lista, tabela, imagem, links e um **formulário de contato**.
- A página **validada** no validador do W3C, sem erros.

## Pré-requisitos

- Aulas [01](01_estrutura_e_primeira_pagina.md) a [04](04_formularios.md) deste módulo.

---

## Tags semânticas

Até agora, tudo ficou solto no `<body>`. Sites de verdade dividem a página em **regiões**, com tags que dizem o papel de cada parte:

| Tag | Região |
|---|---|
| `<header>` | Cabeçalho: nome, logotipo, menu |
| `<nav>` | Menu de navegação |
| `<main>` | O conteúdo principal (um por página) |
| `<section>` | Uma seção do conteúdo, com seu próprio título |
| `<article>` | Um conteúdo que faz sentido sozinho (post, notícia) |
| `<footer>` | Rodapé: contato, direitos, redes |

Elas não mudam a aparência, mas ajudam leitores de tela, o Google e quem for mexer no código depois. No Módulo 02, cada região vai ganhar o seu estilo.

---

## O modelo

Crie a pasta `apresentacao/` com `index.html` e uma subpasta `imagens/`. Use este esqueleto e **troque pelo seu conteúdo** (ou use dados inventados, como os da Ana):

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Ana Souza — Apresentação</title>
</head>
<body>
  <header>
    <h1>Ana Souza</h1>
    <p>Estudante de desenvolvimento web</p>
    <nav>
      <ul>
        <li><a href="#sobre">Sobre</a></li>
        <li><a href="#habilidades">Habilidades</a></li>
        <li><a href="#contato">Contato</a></li>
      </ul>
    </nav>
  </header>

  <main>
    <section id="sobre">
      <h2>Sobre mim</h2>
      <img src="imagens/foto.jpg" alt="Ana Souza sorrindo, em frente a uma estante de livros" width="200" height="200">
      <p>Tenho 17 anos e estou aprendendo a criar sites. Gosto de desenho, música e jogos.</p>
    </section>

    <section id="habilidades">
      <h2>O que estou aprendendo</h2>
      <ul>
        <li>HTML</li>
        <li>CSS (em breve)</li>
        <li>JavaScript (em breve)</li>
      </ul>
      <table>
        <caption>Meu plano de estudos</caption>
        <thead>
          <tr><th scope="col">Mês</th><th scope="col">Assunto</th></tr>
        </thead>
        <tbody>
          <tr><th scope="row">Novembro</th><td>HTML</td></tr>
          <tr><th scope="row">Dezembro</th><td>CSS</td></tr>
        </tbody>
      </table>
    </section>

    <section id="contato">
      <h2>Contato</h2>
      <form action="#">
        <label for="nome">Seu nome</label>
        <input type="text" id="nome" name="nome" required>
        <label for="email">Seu e-mail</label>
        <input type="email" id="email" name="email" required>
        <label for="mensagem">Mensagem</label>
        <textarea id="mensagem" name="mensagem" rows="4" required></textarea>
        <button type="submit">Enviar</button>
      </form>
    </section>
  </main>

  <footer>
    <p>E-mail: <a href="mailto:ana.souza@example.com">ana.souza@example.com</a></p>
  </footer>
</body>
</html>
```

!!! danger "Dados pessoais na internet"
    No Módulo 04 esta página vai para a internet. Não coloque endereço, telefone pessoal, escola ou documentos. Um e-mail para contato basta, e você pode usar um apelido.

---

## Validar

1. Abra o **[Validador do W3C](https://validator.w3.org/#validate_by_input)** ➔ guia **Validate by Direct Input**.
2. Cole o seu código ➔ **Check**.
3. Corrija cada **Error** (e leia os *Warnings*). Os mais comuns: tag sem fechar, `<img>` sem `alt`, `id` repetido, `<label for>` que não bate com nenhum `id`.

---

## Entrega

1. A pasta `apresentacao/` compactada (`index.html` + `imagens/`).
2. Um print do validador mostrando **nenhum erro**.

### Critérios de avaliação

| Critério | O que se espera |
|---|---|
| Estrutura | `<!DOCTYPE>`, `lang="pt-BR"`, charset, viewport e `<title>` |
| Semântica | `<header>`, `<nav>`, `<main>` com `<section>`s e `<footer>`; um só `<h1>` |
| Conteúdo | Lista, tabela com `<caption>` e `<th>`, imagem com `alt`, links internos (`#`) e `mailto:` |
| Formulário | Cada campo com `<label for>`; campos obrigatórios com `required` |
| Validação | Nenhum erro no validador do W3C |

---

## Exercícios extras

### Básico (fixação)

Acrescente uma seção **Meus hobbies** com uma lista e um link no menu que leve até ela.

<!-- gabarito -->
??? success "Gabarito — Básico"
    No `<main>`: `<section id="hobbies"><h2>Meus hobbies</h2><ul><li>…</li></ul></section>`. No `<nav>`: `<li><a href="#hobbies">Hobbies</a></li>`. O valor do `href` (`#hobbies`) tem de ser igual ao `id` da seção.

### Intermediário (aplicação)

Crie uma segunda página, `projetos.html`, com o mesmo `<header>` e `<footer>`, e coloque no menu das duas páginas um link para a outra.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    Copie o esqueleto, troque o `<title>` e o conteúdo do `<main>`. No menu: `<a href="projetos.html">Projetos</a>` e, em `projetos.html`, `<a href="index.html">Início</a>`. Os links com `#` só funcionam dentro da mesma página: em `projetos.html` use `index.html#contato`.

### Avançado (desafio)

Navegue pela sua página **só com o teclado** (`Tab`, `Shift + Tab`, `Enter`, barra de espaço). Consegue chegar a todos os links e preencher e enviar o formulário? Anote o que travou e corrija.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    Com HTML correto, o `Tab` passa por todos os links, campos e o botão, na ordem do código, e `Enter` envia. Se algo não recebe foco, geralmente é um “botão” feito com `<div>` ou `<span>` em vez de `<button>` ou `<a>`. Se a ordem parece estranha, a ordem do código não segue a ordem visual. Essa é a base da **acessibilidade**.

---

## 💡 Resumo

- Regiões semânticas: `<header>`, `<nav>`, `<main>`, `<section>`, `<footer>`.
- Links com `#id` levam a uma seção da mesma página.
- Valide no W3C e teste a navegação só com o teclado.
- Na internet, só os dados que você quer tornar públicos.

## ➡️ Próximo passo

Você terminou o **Módulo 01**. Volte ao [índice do módulo](index.md) e confira o checklist. O **Módulo 02 — CSS**, que vai deixar esta página bonita, está em produção.
