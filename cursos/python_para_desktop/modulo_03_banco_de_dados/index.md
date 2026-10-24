# Módulo 04 — Banco de Dados e Configurações

> **Curso:** python_para_desktop  
> **Módulo:** 04 · trilha principal (00 a 05)  
> **Descrição:** Neste módulo final, você aprenderá a conectar suas interfaces a um banco de dados relacional (SQLite), gerenciar senhas com `.env`, organizar o código na arquitetura MVC e empacotar tudo num executável.

---

## 📋 Visão Geral do Módulo

Para que uma aplicação desktop seja profissional, não basta ser bonita. Ela precisa salvar dados permanentemente (persistência) e proteger chaves e configurações. Você irá consolidar o aprendizado no Projeto de Dados, uma aplicação empacotável que prepara o terreno para o Projeto Finalizador.

---

## 📚 Capítulos

- [01. Introdução a Banco de Dados com SQLite](01_introducao_sqlite.md)
- [02. Integração SQLite e Interface Gráfica](02_integracao_interface.md)
- [03. Variáveis de Ambiente com .env](03_variaveis_ambiente.md)
- [04. Projeto de Dados: Arquitetura Completa](04_projeto_final.md)

---

## 🎯 Objetivos do Módulo

Ao final deste módulo, você será capaz de:

- Criar tabelas, inserir e consultar dados em bancos SQLite.
- Conectar elementos gráficos (como Treeview e campos de formulário) ao banco de dados com segurança (contra SQL Injection).
- Proteger credenciais e chaves usando variáveis de ambiente (`.env`).
- Estruturar aplicações completas utilizando o padrão MVC (Model-View-Controller).
- Empacotar sua aplicação com o PyInstaller para distribuí-la como executável sem depender de instalações complexas.

---

!!! note "Organização"
    Os capítulos deste módulo formam o alicerce final para a construção de sistemas profissionais.
    Acompanhe-os e feche o módulo com o Projeto de Dados — o próximo passo é o Projeto Finalizador (Módulo 05), que libera o certificado.

---

## 🧭 Antes de começar

- **Pré-requisitos:** [Módulo 03](../modulo_02_interfaces_graficas/index.md) — interfaces gráficas.
- **Tempo estimado:** ~12 h (leitura, exemplos e exercícios — estimativa; ajuste ao ritmo da turma)
- **Ao final você terá:** o **Projeto de Dados**: interface + SQLite + `.env` em MVC, empacotado como executável.

## ✅ Checklist do módulo

Antes de seguir, confira se você consegue:

- [ ] Crio tabelas e faço consultas SQL (`SELECT`, `INSERT`, `UPDATE`, `DELETE`).
- [ ] Uso parâmetros (`?`) nas consultas — nunca monto SQL juntando textos.
- [ ] Ligo formulários e tabelas da interface ao banco.
- [ ] Guardo configurações no `.env` e deixo o `.env` fora do Git.
- [ ] Separei o projeto em Model, View e Controller.
- [ ] Gerei o executável com o PyInstaller.

## ➡️ Próximo passo

**[Módulo 05 — Projeto Finalizador](../modulo_04_projeto_finalizador/index.md)** — junte tudo no sistema da equipe — é ele que libera o certificado.
