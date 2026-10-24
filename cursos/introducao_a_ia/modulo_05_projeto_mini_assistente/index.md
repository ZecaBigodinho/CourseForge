# Módulo 05 — Projeto: seu mini-assistente

> **Curso:** Introdução à IA  
> **Módulo:** 05 · Projeto: seu mini-assistente  
> **Descrição:** Um tutor de estudos em Python, com dois motores — um simulado, para todos, e um com a API de um modelo de IA com plano gratuito, para maiores de 18 —, filtro de dados pessoais, testes e documentação.

---

## 📋 Visão Geral do Módulo

É o projeto de encerramento do curso: você vai **construir** um mini-assistente de estudos que conversa no terminal e segue as regras que aprendeu — faz perguntas em vez de dar respostas prontas, diz quando não sabe, recusa “fazer a prova” e **não deixa** dados pessoais saírem do computador.

O programa tem dois **motores** com o mesmo jeito de usar:

- **Motor simulado** — respostas por palavras-chave, **sem internet, sem conta, sem chave**. Para **todos**.
- **Motor com API** — um modelo de IA do Google pela API, com **plano gratuito**. Para **maiores de 18 anos**, com chave própria, como exigem os termos da API (conferidos em outubro de 2026).

!!! warning "Idade e dados"
    Menores de 18 fazem o projeto **inteiro** com o motor simulado — a aprendizagem de programação, segurança e testes é a mesma. E ninguém, em nenhum caminho, envia dados pessoais: no plano gratuito, as mensagens podem ser usadas pela empresa e lidas por revisores.

---

## 📚 Capítulos

- [01. Planejando o mini-assistente](01_planejando_o_mini_assistente.md)
- [02. O motor simulado e a conversa](02_motor_simulado_e_conversa.md)
- [03. Conectando a uma API de IA](03_conectando_a_uma_api.md)
- [04. Segurança e testes](04_seguranca_e_testes.md)
- [05. Projeto final: entregando o seu mini-assistente](05_projeto_final_entrega.md)

---

## 🎯 Objetivos do Módulo

Ao final deste módulo, você será capaz de:

- Planejar um assistente de IA com **regras** de comportamento e uma **arquitetura** simples.
- Programar um **laço de conversa** e **motores** trocáveis em Python.
- Usar uma **API de IA** com a chave protegida no **`.env`**, instruções de sistema e memória da conversa.
- Proteger os usuários com um **filtro** de dados pessoais e avisos de **transparência**.
- Escrever **testes automáticos** que rodam sem internet, inclusive com um **cliente falso**.
- **Documentar**, demonstrar e avaliar a **responsabilidade** do que você construiu.

---

## 🧭 Antes de começar

- **Pré-requisitos:** os [Módulos 01 a 04](../docs/index.md) deste curso. **Recomendado:** o Módulo 01 do [curso de Python](../../python_para_desktop/docs/index.md) (ou fazer em dupla com quem programa).
- **Tempo estimado:** ~10 h (programação, testes, documentação e demonstração — estimativa; ajuste ao ritmo da turma)
- **Ao final você terá:** um mini-assistente de estudos funcionando, testado e documentado, e um relatório de responsabilidade.

## ✅ Checklist do módulo

Antes de concluir o curso, confira se você consegue:

- [ ] Explicar a arquitetura: conversa ➔ filtro ➔ motor ➔ resposta.
- [ ] Acrescentar temas e comandos ao motor simulado.
- [ ] Explicar por que a chave fica no `.env` e o `.env` fica fora do Git.
- [ ] Explicar quem pode usar o caminho com API e por quê.
- [ ] Rodar os testes e escrever um teste novo.
- [ ] Mostrar o filtro bloqueando um dado pessoal — e dizer o que ele não pega.

## ➡️ Próximo passo

Concluiu o curso? Volte à [apresentação do curso](../docs/index.md) — e, para seguir programando, conheça o **[curso de Python](../../python_para_desktop/docs/index.md)**.
