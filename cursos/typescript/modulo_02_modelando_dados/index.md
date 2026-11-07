# Módulo 02 — Modelando dados

> **Curso:** TypeScript  
> **Módulo:** 02 · Modelando dados  
> **Descrição:** Descrever com tipos as coisas do mundo real (produtos, pedidos, usuários) de um jeito que impede estados impossíveis.

---

## 📋 Visão Geral do Módulo

No Módulo 01 você tipou valores soltos. Agora vai **modelar**: dizer que um pedido tem itens, que um pagamento é *pix* ou *cartão* (e nada mais), que um campo pode estar vazio e que uma função serve para qualquer tipo de lista. No projeto, monta um **carrinho de compras** em que o próprio compilador impede erros de regra.

---

## 📚 Capítulos

- [01. type × interface](01_type_e_interface.md)
- [02. Uniões, literais e narrowing](02_unioes_e_narrowing.md)
- [03. Valores opcionais e null](03_opcionais_e_null.md)
- [04. Generics](04_generics.md)
- [05. Projeto do módulo: carrinho de compras](05_projeto_carrinho.md)

---

## 🎯 Objetivos do Módulo

Ao final deste módulo, você será capaz de:

- Escolher entre `type` e `interface` e estender modelos.
- Usar **uniões** e **tipos literais** e estreitar tipos com *narrowing*.
- Lidar com valores que podem faltar usando `?.` e `??`.
- Escrever funções e tipos **genéricos**.
- Modelar regras de negócio de forma que o compilador as confira.

---

## 🧭 Antes de começar

- **Pré-requisitos:** [Módulo 01 — Fundamentos](../modulo_01_fundamentos/index.md).
- **Tempo estimado:** ~6 h (estimativa, ajuste ao ritmo da turma)
- **Ao final você terá:** um carrinho de compras tipado, com cupons e formas de pagamento, rodando no terminal.

## ✅ Checklist do módulo

- [ ] Estender uma `interface` com `extends` e um `type` com `&`.
- [ ] Criar uma união discriminada e tratá-la com `switch`.
- [ ] Usar `?.` e `??` sem medo de `undefined`.
- [ ] Escrever uma função genérica `primeiro<T>(lista: T[])`.

## ➡️ Próximo passo

Comece pela **[aula 01 — type × interface](01_type_e_interface.md)**.
