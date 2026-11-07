# Módulo 03 — Aplicação completa

> **Curso:** React  
> **Módulo:** 03 · Aplicação completa  
> **Descrição:** Organizar um app de verdade: onde fica cada estado, como compartilhá-lo sem passar props por toda parte e como publicar o resultado.

---

## 📋 Visão Geral do Módulo

Com vários componentes precisando dos mesmos dados (a busca, o carrinho), surgem as perguntas de todo projeto: **onde fica o estado?** **Como ele chega a quem precisa?** Neste módulo você aprende a **elevar o estado**, a usar o **Context** para dados que o app inteiro usa e a **publicar** o projeto. No projeto final, monta e publica o **catálogo de uma papelaria** com busca e carrinho.

---

## 📚 Capítulos

- [01. Componentizar e elevar o estado](01_elevar_o_estado.md)
- [02. Context: dados para o app inteiro](02_context.md)
- [03. Build e publicação](03_build_e_publicacao.md)
- [04. Projeto final: catálogo com busca e carrinho](04_projeto_catalogo.md)

---

## 🎯 Objetivos do Módulo

Ao final deste módulo, você será capaz de:

- Dividir uma tela em componentes e decidir **onde** cada estado mora.
- **Elevar o estado** para o pai comum e passar funções para os filhos.
- Criar um **Context** com Provider e um hook próprio (`useCarrinho`).
- Gerar o **build** e publicar no GitHub Pages com a opção `base` do Vite.

---

## 🧭 Antes de começar

- **Pré-requisitos:** [Módulo 02](../modulo_02_formularios_e_efeitos/index.md); a [aula de GitHub Pages do curso de Web](../../desenvolvimento_web/modulo_04_publicar/03_github_pages.md).
- **Tempo estimado:** ~7 h (estimativa, ajuste ao ritmo da turma)
- **Ao final você terá:** um catálogo com busca, filtro e carrinho, publicado na internet (requisito do certificado).

## ✅ Checklist do módulo

- [ ] Explicar por que a busca fica no `App` e o texto do formulário fica no `FormTarefa`.
- [ ] Criar um Context com valor tipado e um hook que avisa quando está fora do Provider.
- [ ] Configurar o `base` do Vite e testar com `npm run preview`.
- [ ] Publicar um projeto React no GitHub Pages.

## ➡️ Próximo passo

Comece pela **[aula 01 — Componentizar e elevar o estado](01_elevar_o_estado.md)**.
