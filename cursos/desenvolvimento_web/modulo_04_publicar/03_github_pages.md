# 03 — Publicar no GitHub Pages

> **Curso:** Desenvolvimento Web  
> **Módulo:** 04 — Publicar  
> **Tempo estimado:** 1 h 30 min  

---

## Objetivos

Ao final desta aula, você será capaz de:

- Criar um **repositório** no GitHub e enviar os arquivos do site.
- Ligar o **GitHub Pages** e acessar o endereço do site.
- **Atualizar** o site depois de mudar os arquivos.

## Pré-requisitos

- [Aula 02](02_organizar_o_projeto.md) deste módulo e uma conta gratuita no [GitHub](https://github.com).

---

## O que é o GitHub Pages

O GitHub guarda projetos (repositórios). O **GitHub Pages** transforma um repositório com HTML, CSS e JavaScript num **site público e gratuito**. O endereço fica:

| Nome do repositório | Endereço do site |
|---|---|
| `seu-usuario.github.io` | `https://seu-usuario.github.io` |
| qualquer outro, ex.: `cardapio` | `https://seu-usuario.github.io/cardapio/` |

!!! danger "Tudo fica público"
    Repositório público + Pages = qualquer pessoa vê **todos** os arquivos. Não envie senhas, documentos ou fotos de outras pessoas sem permissão.

---

## Caminho 1: pelo site do GitHub (sem instalar nada)

1. No GitHub, clique em **New repository**.
2. Nome: `seu-usuario.github.io` (troque pelo seu usuário, exatamente). Marque **Public** ➔ **Create repository**.
3. Na página do repositório, clique em **uploading an existing file**, arraste **o conteúdo** da pasta do portfólio (o `index.html` tem de ficar na raiz, não dentro de outra pasta) ➔ **Commit changes**.
4. Vá em **Settings ➔ Pages**. Em *Build and deployment*, *Source*: **Deploy from a branch**; *Branch*: **main** e pasta **/ (root)** ➔ **Save**.
5. Espere um ou dois minutos e acesse `https://seu-usuario.github.io`. O andamento aparece na guia **Actions**.

## Caminho 2: pelo Git, no terminal

Se você já fez o módulo de Git (no curso de Python para Desktop), dentro da pasta do projeto:

```bash
git init
git add .
git commit -m "Primeira versão do portfólio"
git branch -M main
git remote add origin https://github.com/seu-usuario/seu-usuario.github.io.git
git push -u origin main
```

Depois, ligue o Pages como no passo 4.

---

## Atualizar o site

| Pelo site do GitHub | Pelo Git |
|---|---|
| **Add file ➔ Upload files** (substitui os arquivos com o mesmo nome) ➔ *Commit changes* | `git add .` ➔ `git commit -m "o que mudou"` ➔ `git push` |

O site se atualiza sozinho em um ou dois minutos. Se a mudança não aparecer, recarregue com `Ctrl + F5` (ignora o que o navegador guardou).

!!! tip "Página em branco ou 404?"
    Confira: o `index.html` está na **raiz** do repositório? O nome do repositório está certinho? Os caminhos respeitam maiúsculas e minúsculas (aula 02)?

---

## Exercícios

### Básico (fixação)

Publique a sua página de apresentação do Módulo 01 e mande o link para um colega abrir no celular.

<!-- gabarito -->
??? success "Gabarito — Básico"
    Repositório `seu-usuario.github.io` ➔ envie o `index.html` (e a pasta `imagens/`) ➔ **Settings ➔ Pages ➔ main / (root) ➔ Save** ➔ aguarde e abra `https://seu-usuario.github.io`.

### Intermediário (aplicação)

Publique o cardápio num **segundo** repositório chamado `cardapio` e descubra o endereço dele.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    Mesmo processo, num repositório `cardapio`. O endereço fica `https://seu-usuario.github.io/cardapio/`. Os caminhos relativos (`css/style.css`) continuam funcionando porque são relativos à pasta do site.

### Avançado (desafio)

Mude a cor principal do cardápio publicado e confira a atualização no ar. Quanto tempo levou? O que fazer se o navegador mostrar a versão antiga?

<!-- gabarito -->
??? success "Gabarito — Avançado"
    Altere a variável no `style.css`, envie de novo (upload ou `git push`) e acompanhe em **Actions**: em geral leva de 1 a 2 minutos. Se a cor antiga continuar, é o **cache** do navegador: `Ctrl + F5` ou abra numa janela anônima.

---

## 💡 Resumo

- GitHub Pages publica HTML, CSS e JS de graça a partir de um repositório público.
- `seu-usuario.github.io` vira o seu endereço principal; outros repositórios viram subpastas.
- Settings ➔ Pages ➔ branch **main**, pasta **/ (root)**.
- Atualizar = enviar os arquivos de novo; `Ctrl + F5` contra o cache.

## ➡️ Próximo passo

Na **[aula 04](04_projeto_portfolio.md)** você monta e publica o seu portfólio.
