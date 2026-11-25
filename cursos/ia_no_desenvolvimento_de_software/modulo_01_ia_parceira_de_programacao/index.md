# Módulo 01 — IA como parceira de programação

> **Curso:** IA no desenvolvimento de software  
> **Módulo:** 01 · IA como parceira de programação  
> **Descrição:** Usar assistentes de IA gratuitos para entender código, gerar testes e corrigir defeitos, sempre conferindo com o pytest.

---

## 📋 Visão Geral do Módulo

A IA escreve código em segundos, mas não sabe qual é a **regra do seu sistema**. Se você pedir testes mostrando só o código, ela escreve testes que **concordam com o defeito**. Neste módulo você aprende a dar à IA o **requisito**, a rodar os testes que ela sugere e a decidir, com base no resultado, o que corrigir. A IA propõe; quem aprova é o teste e é você.

---

## 📚 Capítulos

- [01. Onde a IA entra no desenvolvimento](01_onde_a_ia_entra.md)
- [02. Prática: testes e correção com IA](02_pratica_testes_com_ia.md)
- [03. Revisão, registro e autoavaliação](03_revisao_e_autoavaliacao.md)

---

## 🎯 Objetivos do Módulo

Ao final deste módulo, você será capaz de:

- Identificar em que etapas do desenvolvimento a IA ajuda e quais riscos ela traz.
- Escrever um pedido com papel, contexto, requisito e formato de resposta.
- Gerar testes **a partir do requisito**, rodar com o pytest e interpretar as falhas.
- Corrigir o defeito com ajuda da IA e revisar a correção com um checklist.
- Registrar o resultado dos testes numa tabela.

---

## ⏱️ Roteiro da aula (20 minutos)

| Tempo | Momento | O que acontece |
|---|---|---|
| 0–2 min | **Abertura** | Pergunta para a turma: "Quem já usou IA para programar? Ela já errou com vocês?" Apresentação dos objetivos. |
| 2–7 min | **Conceito** ([aula 01](01_onde_a_ia_entra.md)) | Onde a IA entra no ciclo; ferramentas gratuitas; riscos; a anatomia de um bom pedido. |
| 7–17 min | **Prática** ([aula 02](02_pratica_testes_com_ia.md)) | Explicar o código com a IA → gerar testes do requisito → rodar e ver falhar → corrigir → rodar e ver passar. |
| 17–20 min | **Fechamento** ([aula 03](03_revisao_e_autoavaliacao.md)) | Checklist de revisão, tabela de testes, pergunta de verificação e dúvidas. |

!!! tip "Sem internet ou sem IA?"
    A [aula 02](02_pratica_testes_com_ia.md) traz **respostas de exemplo** para cada pedido. A prática funciona igual, porque o que decide é o **pytest**, que roda no seu computador.

---

## 🧭 Antes de começar

- **Pré-requisitos:** Python básico (funções, listas, `if`) e o pytest instalado: `pip install pytest`.
- **Tempo estimado:** 20 min de aula + ~1 h para os exercícios.
- **Ao final você terá:** a função `situacao_final` corrigida, 9 testes automáticos passando e uma tabela de registro dos testes.

## ✅ Checklist do módulo

- [ ] Sei citar três etapas do desenvolvimento em que a IA ajuda e três riscos.
- [ ] Escrevi um pedido com papel, contexto, requisito e formato.
- [ ] Rodei os testes gerados e vi o defeito aparecer.
- [ ] Corrigi, rodei de novo e vi todos os testes passarem.
- [ ] Revisei a correção com o checklist e registrei o resultado.
