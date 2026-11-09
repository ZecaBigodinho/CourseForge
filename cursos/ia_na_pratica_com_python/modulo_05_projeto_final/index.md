# Módulo 05 — Projeto final

> **Curso:** IA na prática com Python  
> **Módulo:** 05 · Projeto final  
> **Descrição:** O Atendente da Padaria Pão Quente: responde com os dados reais, anota encomendas com regras, registra tudo numa planilha e funciona em lote, no terminal e numa janela, com ou sem IA.

---

## 📋 Visão Geral do Módulo

É hora de juntar o curso inteiro num programa de verdade. O **Atendente da Padaria Pão Quente** recebe as mensagens dos clientes, responde dúvidas **só** com o cardápio e o horário, transforma pedidos em **encomendas** (com o total calculado pelo programa, nunca pela IA), passa para a equipe tudo o que precisa de uma pessoa, dizendo **por quê**, e registra cada atendimento numa **planilha**. Ele usa as proteções do Módulo 04 e é provado pela **bateria de testes** e pelo **pytest**. A entrega e a demonstração do atendente liberam o **certificado** do curso.

---

## 📚 Capítulos

- [01. Planejando o atendente](01_planejando_o_atendente.md)
- [02. Encomendas com regras](02_encomendas_com_regras.md)
- [03. Registro e linha de comando](03_registro_e_linha_de_comando.md)
- [04. A janela do atendente](04_a_janela.md)
- [05. Entrega e certificado](05_entrega_e_certificado.md)

---

## 🎯 Objetivos do Módulo

Ao final deste módulo, você será capaz de:

- Planejar um programa com IA dizendo o que ele faz e o que ele **não** faz.
- Separar o trabalho: a IA extrai e escreve; o código confere, decide e calcula.
- Registrar atendimentos numa planilha seguindo a LGPD.
- Oferecer o mesmo programa em lote, no terminal (`argparse` com subcomandos) e numa janela (CustomTkinter).
- Entregar um projeto com README, testes, relatório e demonstração.

---

## 🧭 Antes de começar

- **Pré-requisitos:** [Módulos 01 a 04](../docs/index.md#ementa), com os arquivos do [projeto do Módulo 04](../modulo_04_seguranca_custos_testes/05_projeto_bateria_de_testes.md). Instale `openpyxl==3.1.5` e `customtkinter==5.2.2` no ambiente virtual.
- **Tempo estimado:** ~8 h, mais a demonstração (estimativa, ajuste ao ritmo da turma)
- **Ao final você terá:** o atendente completo, com 42 testes automáticos, a bateria com relatório e o certificado do curso.

## ✅ Checklist do módulo

- [ ] Montei a pasta do projeto com as peças dos módulos anteriores.
- [ ] Vi uma encomenda válida com o total do cardápio e três pedidos irem para revisar com o motivo.
- [ ] Rodei o lote, a conversa e a janela, e conferi as três abas da planilha.
- [ ] `python -m pytest testes` passa e a bateria gerou o relatório.
- [ ] Fiz uma melhoria própria, com um caso novo na bateria.
- [ ] Escrevi o README e fiz a demonstração.

## ➡️ Próximo passo

Comece pela **[aula 01 — Planejando o atendente](01_planejando_o_atendente.md)**.
