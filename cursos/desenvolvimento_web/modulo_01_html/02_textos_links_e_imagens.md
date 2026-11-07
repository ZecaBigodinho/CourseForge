# 02 — Textos, links e imagens

> **Curso:** Desenvolvimento Web  
> **Módulo:** 01 — HTML  
> **Tempo estimado:** 1 h 30 min  

---

## Objetivos

Ao final desta aula, você será capaz de:

- Organizar o texto com **títulos** (`<h1>` a `<h6>`) e **parágrafos**.
- Dar **ênfase** com `<strong>` e `<em>`.
- Criar **links** para outros sites, para outras páginas suas e para e-mail.
- Inserir **imagens** com texto alternativo (`alt`).

## Pré-requisitos

- [Aula 01](01_estrutura_e_primeira_pagina.md) deste módulo.

---

## Títulos e parágrafos

```html
<h1>Receitas da Vó Ana</h1>
<h2>Bolos</h2>
<p>O bolo de cenoura é o mais pedido da família.</p>
<h2>Salgados</h2>
<p>A coxinha leva frango desfiado e catupiry.</p>
```

- Os títulos vão de `<h1>` (o mais importante) a `<h6>`. Use **um só `<h1>`** por página, com o assunto principal.
- Não pule níveis: depois de `<h2>` vem `<h3>`, não `<h4>`.
- Escolha o título pela **importância**, não pelo tamanho da letra. O tamanho se ajusta com CSS no Módulo 02.

!!! info "Por que a ordem dos títulos importa"
    Leitores de tela (usados por pessoas cegas) e o Google navegam pelos títulos como se fossem um **sumário**. Títulos fora de ordem bagunçam esse sumário.

### Ênfase e quebras

| Tag | Uso | Aparece como |
|---|---|---|
| `<strong>` | Texto **importante** | negrito |
| `<em>` | Texto com **ênfase** na fala | itálico |
| `<br>` | Quebra de linha dentro de um parágrafo (endereço, poema) | nova linha |
| `<hr>` | Mudança de assunto | linha horizontal |

```html
<p><strong>Atenção:</strong> as inscrições acabam <em>amanhã</em>.</p>
<p>Rua das Flores, 123<br>São Paulo – SP</p>
```

!!! warning "Espaços e `Enter` não contam"
    Vários espaços seguidos ou linhas em branco no código viram **um espaço só** na página. Para separar blocos, use outro `<p>`; para quebrar a linha, `<br>`.

---

## Links

A tag `<a>` (de *anchor*, âncora) cria um link. O destino vai no atributo `href`:

```html
<a href="https://developer.mozilla.org/pt-BR/">Documentação da MDN</a>
```

| Tipo de link | Exemplo de `href` |
|---|---|
| Outro site | `https://www.exemplo.com` (sempre com `https://`) |
| Outra página sua, na mesma pasta | `contato.html` |
| Página numa subpasta | `projetos/cardapio.html` |
| Voltar uma pasta | `../index.html` |
| Parte da mesma página | `#contato` (vai até o elemento com `id="contato"`) |
| E-mail | `mailto:ana.souza@example.com` |
| Telefone (no celular) | `tel:+5511900000000` |

Para abrir em **outra aba**, acrescente `target="_blank"`:

```html
<a href="https://www.exemplo.com" target="_blank" rel="noopener">Abre em outra aba</a>
```

!!! tip "Texto do link que faz sentido sozinho"
    Prefira “**Baixe o cardápio em PDF**” a “clique aqui”. Leitores de tela podem listar só os links da página, e “clique aqui” repetido não diz nada.

---

## Imagens

```html
<img src="imagens/bolo.jpg" alt="Bolo de cenoura com cobertura de chocolate" width="400" height="300">
```

| Atributo | Para quê |
|---|---|
| `src` | O caminho do arquivo (mesmas regras do `href`) |
| `alt` | **Texto alternativo**: descreve a imagem para quem não pode vê-la e aparece se ela não carregar |
| `width` / `height` | Tamanho em pixels; reserva o espaço e evita a página “pular” enquanto carrega |

- Guarde as imagens numa pasta `imagens/` ao lado do `index.html`.
- Nomes de arquivo **sem espaços e sem acentos**: `bolo-cenoura.jpg`, não `Bolo de Cenoura.JPG`.
- Imagem só decorativa (um enfeite)? Use `alt=""` (vazio): o leitor de tela pula.

Para uma imagem com **legenda**:

```html
<figure>
  <img src="imagens/bolo.jpg" alt="Bolo de cenoura com cobertura de chocolate">
  <figcaption>O campeão de pedidos da família.</figcaption>
</figure>
```

!!! danger "Direitos autorais"
    Não use imagens copiadas do Google. Use fotos **suas** ou de bancos gratuitos com licença livre (como Unsplash e Pexels), e confira a licença.

---

## Exercícios

### Básico (fixação)

Faça uma página “Meu filme favorito” com um `<h1>`, dois `<h2>` (*Sinopse* e *Por que eu gosto*) e um parágrafo em cada.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```html
    <h1>Meu filme favorito</h1>
    <h2>Sinopse</h2>
    <p>Um resumo de duas ou três frases, sem contar o final.</p>
    <h2>Por que eu gosto</h2>
    <p>O que você achou da história, dos personagens e da trilha.</p>
    ```

### Intermediário (aplicação)

Acrescente ao fim da página: um link para a página do filme num site de críticas, que abra em outra aba, e um link “Fale comigo” que abra o programa de e-mail.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```html
    <p><a href="https://www.exemplo.com/filme" target="_blank" rel="noopener">Ver críticas do filme</a></p>
    <p><a href="mailto:ana.souza@example.com">Fale comigo</a></p>
    ```

### Avançado (desafio)

Crie duas páginas, `index.html` e `sobre.html`, na mesma pasta, cada uma com um link para a outra. Na `sobre.html`, coloque uma imagem com legenda usando `<figure>`.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    Em `index.html`: `<a href="sobre.html">Sobre mim</a>`. Em `sobre.html`: `<a href="index.html">Voltar ao início</a>`. A imagem:
    ```html
    <figure>
      <img src="imagens/eu.jpg" alt="Ana Souza sorrindo, de camiseta azul" width="300" height="300">
      <figcaption>Eu, na formatura do curso técnico.</figcaption>
    </figure>
    ```
    Se a imagem não aparecer, confira o **nome exato** do arquivo e a pasta: `imagens/` precisa estar ao lado da `sobre.html`.

---

## 💡 Resumo

- Um `<h1>` por página; títulos em ordem; `<p>` para parágrafos.
- `<strong>` = importante; `<em>` = ênfase; espaços extras no código são ignorados.
- `<a href="...">` liga a sites (`https://`), páginas suas, e-mail (`mailto:`) e partes da página (`#id`).
- `<img>` sempre com **`alt`**; nomes de arquivo sem espaço nem acento.

## ➡️ Próximo passo

Na **[aula 03](03_listas_e_tabelas.md)** você organiza informações em listas e tabelas.
