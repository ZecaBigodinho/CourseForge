# Módulo 03 — IA com os seus documentos

> **Curso:** IA na prática com Python  
> **Módulo:** 03 · IA com os seus documentos  
> **Descrição:** Ler PDF e TXT, dividir em trechos, buscar os trechos certos e responder só com base no documento, citando a fonte.

---

## 📋 Visão Geral do Módulo

A IA não conhece o regulamento da **sua** escola: se você perguntar, ela inventa. Neste módulo você aprende a técnica que resolve isso (**RAG**, geração com busca): **ler** o documento com o **pypdf**, **dividir** em trechos com título e página, **buscar** os trechos que combinam com a pergunta (sem IA, contando palavras) e fazer a IA responder **só** com eles, dizendo **"não encontrei"** quando o documento não responde e **citando a fonte**. No projeto, o **tira-dúvidas do regulamento** funciona com ou sem IA, registra as perguntas e tem uma **avaliação** da busca com perguntas de teste.

---

## 📚 Capítulos

- [01. Lendo PDF e TXT](01_ler_documentos.md)
- [02. Dividir em trechos](02_dividir_em_trechos.md)
- [03. Buscar os trechos certos](03_buscar_trechos.md)
- [04. Responder só com base no documento](04_responder_com_fonte.md)
- [05. Projeto do módulo: tira-dúvidas do regulamento](05_projeto_tira_duvidas.md)

---

## 🎯 Objetivos do Módulo

Ao final deste módulo, você será capaz de:

- Ler o texto de PDFs e TXTs, página por página, e reconhecer PDFs escaneados.
- Dividir documentos em trechos que fazem sentido sozinhos, com título e página.
- Buscar trechos por palavras, conhecendo os limites (sinônimos e coincidências).
- Fazer a IA responder só com os trechos, conferir os trechos citados e mostrar a fonte.
- Avaliar a busca com perguntas de teste antes de colocar em uso.

---

## 🧭 Antes de começar

- **Pré-requisitos:** [Módulos 01](../modulo_01_api_de_ia/index.md) e [02](../modulo_02_tarefas_uteis/index.md). Instale `pypdf==6.21.4` (e `fpdf2==2.8.9` para criar o regulamento de treino).
- **Tempo estimado:** ~7 h (estimativa, ajuste ao ritmo da turma)
- **Ao final você terá:** um tira-dúvidas de documentos testado, que cita a fonte e sabe dizer "não encontrei".

## ✅ Checklist do módulo

- [ ] Li o regulamento de treino página por página.
- [ ] Dividi em trechos com título e página.
- [ ] Vi a busca acertar, não achar (sinônimo) e achar errado (coincidência).
- [ ] O responder recusa ids inventados e não chama a IA quando não há trechos.
- [ ] Rodei a avaliação e melhorei a busca com sinônimos.

## ➡️ Próximo passo

Comece pela **[aula 01 — Lendo PDF e TXT](01_ler_documentos.md)**.
