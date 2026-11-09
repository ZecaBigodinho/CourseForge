# Módulo 04 — Segurança, custos e testes

> **Curso:** IA na prática com Python  
> **Módulo:** 04 · Segurança, custos e testes  
> **Descrição:** Proteger dados pessoais, resistir a prompt injection, controlar erros, limites e custos da API e testar tudo sem gastar a cota.

---

## 📋 Visão Geral do Módulo

Um programa com IA que conversa com clientes precisa de mais do que respostas boas: precisa **não vazar** dados pessoais, **não obedecer** a quem tenta dar ordens pela mensagem, **não quebrar** quando a API falha e **não gastar** mais do que deve. Neste módulo você monta essas proteções em camadas, à luz da **LGPD**, e aprende a **testá-las** com o **pytest**, sem chamar a API, inclusive com uma IA de mentira que erra de propósito. No projeto, a **bateria de testes** do Atendente da Padaria Pão Quente (o projeto final do curso) fica pronta **antes** do atendente.

---

## 📚 Capítulos

- [01. Dados pessoais: o que nunca enviar](01_dados_pessoais.md)
- [02. Prompt injection: quando a mensagem tenta dar ordens](02_prompt_injection.md)
- [03. Limites, erros e custos](03_limites_erros_custos.md)
- [04. Testes automáticos com o pytest](04_testes_automaticos.md)
- [05. Projeto do módulo: bateria de testes do atendente](05_projeto_bateria_de_testes.md)

---

## 🎯 Objetivos do Módulo

Ao final deste módulo, você será capaz de:

- Decidir, com base na LGPD, o que nunca vai para a API, e mascarar ou trocar por apelidos o que vai.
- Explicar o prompt injection e montar defesas em camadas, com o código conferindo a saída.
- Tratar os erros da API: repetir só os passageiros, com espera crescente, e pôr um limite de gasto.
- Estimar o custo de uma tarefa em tokens e gastar menos.
- Testar programas com IA usando o pytest, fixtures e IAs falsas, sem chamar a API.

---

## 🧭 Antes de começar

- **Pré-requisitos:** [Módulos 01](../modulo_01_api_de_ia/index.md), [02](../modulo_02_tarefas_uteis/index.md) e [03](../modulo_03_documentos/index.md). Instale `pytest==8.4.2` no ambiente virtual.
- **Tempo estimado:** ~8 h (estimativa, ajuste ao ritmo da turma)
- **Ao final você terá:** um rascunho seguro do atendente da padaria, com uma bateria de 13 casos e 29 testes automáticos.

## ✅ Checklist do módulo

- [ ] Mascarei e-mail, cartão, CPF, CEP e telefone e barrei uma mensagem com dado de saúde.
- [ ] Vi a IA "cair" numa injeção e o código segurar.
- [ ] Testei o 429 sem esperar e sem internet, e vi a memória evitar chamadas repetidas.
- [ ] Rodei `python -m pytest testes` e vi os testes passarem.
- [ ] Rodei a bateria do atendente e entendi por que o caso 13 falha sem IA.

## ➡️ Próximo passo

Comece pela **[aula 01 — Dados pessoais: o que nunca enviar](01_dados_pessoais.md)**.
