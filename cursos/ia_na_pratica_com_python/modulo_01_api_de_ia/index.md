# Módulo 01 — Conversando com um modelo por API

> **Curso:** IA na prática com Python  
> **Módulo:** 01 · Conversando com um modelo por API  
> **Descrição:** A primeira chamada ao Gemini pelo Python, com chave segura, tratamento de erros, instruções de sistema, conversa com memória e testes sem gastar a cota.

---

## 📋 Visão Geral do Módulo

Você vai entender o que são **API**, **chave** e **tokens**, os **limites** e a **privacidade** do plano gratuito e escolher o seu caminho: **com chave** (18+) ou **sem chave** (motor simulado). Depois faz a **primeira chamada** ao Gemini, transforma os erros em mensagens claras e aprende a testar com um **cliente falso**. Com as **instruções de sistema** e o **nível de raciocínio**, controla o jeito de responder; com o **`previous_interaction_id`**, a IA lembra da conversa. No projeto, monta um **resumidor de textos** que funciona com a IA de verdade ou com o motor simulado.

---

## 📚 Capítulos

- [01. O que é uma API de IA](01_o_que_e_uma_api_de_ia.md)
- [02. A primeira chamada](02_primeira_chamada.md)
- [03. Instruções de sistema e ajustes](03_instrucoes_e_ajustes.md)
- [04. Conversa com memória e motores](04_conversa_e_motores.md)
- [05. Projeto do módulo: resumidor de textos](05_projeto_resumidor.md)

---

## 🎯 Objetivos do Módulo

Ao final deste módulo, você será capaz de:

- Explicar API, chave, tokens, limites e privacidade do plano gratuito.
- Chamar o Gemini com `google-genai` e tratar os erros da API.
- Separar instruções de sistema e pedido, e usar o `thinking_level`.
- Manter uma conversa com memória e trocar o motor sem mudar o programa.
- Testar programas de IA com um cliente falso, sem chave e sem cota.

---

## 🧭 Antes de começar

- **Pré-requisitos:** Python básico e ambiente virtual. Recomendado: [Introdução à IA](../../introducao_a_ia/docs/index.md).
- **Tempo estimado:** ~8 h (estimativa, ajuste ao ritmo da turma)
- **Ao final você terá:** um resumidor de textos testado, que usa a IA ou o motor simulado.

## ✅ Checklist do módulo

- [ ] Instalei `google-genai==2.34.0` e `python-dotenv==1.2.1` e protegi o `.env` com o `.gitignore`.
- [ ] Fiz a primeira chamada (com chave) ou rodei o exemplo com o cliente falso (sem chave).
- [ ] Sei o que fazer com os erros de chave, modelo, limite e internet.
- [ ] Escrevi instruções de sistema com papel, tom, formato e restrições.
- [ ] O resumidor funciona e grava o resumo ao lado do texto.

## ➡️ Próximo passo

Comece pela **[aula 01 — O que é uma API de IA](01_o_que_e_uma_api_de_ia.md)**.
