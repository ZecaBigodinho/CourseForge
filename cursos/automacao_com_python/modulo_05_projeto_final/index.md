# Módulo 05 — Projeto final: Secretaria automática

> **Curso:** Automação com Python  
> **Módulo:** 05 · Projeto final  
> **Descrição:** Um pacote Python com linha de comando e testes que, a partir da planilha da turma, gera boletim, certificados e e-mails.

---

## 📋 Visão Geral do Módulo

O projeto final junta os quatro módulos anteriores numa ferramenta só: a **Secretaria automática**. Você planeja a entrada e as saídas, organiza o código num **pacote** (`dados.py`, `documentos.py`, `emails.py`, `cli.py`), cria uma **linha de comando** com o `argparse` (`python -m secretaria tudo turma.xlsx`) e escreve **testes automáticos** com o **pytest**. No fim, escreve o README, faz a demonstração e entrega o projeto que libera o certificado do curso.

---

## 📚 Capítulos

- [01. Planejando a Secretaria automática](01_planejando_a_secretaria.md)
- [02. O pacote e as regras da escola](02_pacote_e_dados.md)
- [03. Documentos e e-mails](03_documentos_e_emails.md)
- [04. Linha de comando e testes](04_linha_de_comando_e_testes.md)
- [05. Demonstração, entrega e certificado](05_entrega_e_certificado.md)

---

## 🎯 Objetivos do Módulo

Ao final deste módulo, você será capaz de:

- Planejar uma automação maior: entrada, saídas, o que ela faz e o que não faz.
- Organizar o código num pacote com imports relativos, `__main__.py` e `dataclass`.
- Criar uma linha de comando com `argparse`, com ajuda automática.
- Escrever testes automáticos com pytest, usando `parametrize` e fixtures.
- Documentar o projeto num README e apresentá-lo.

---

## 🧭 Antes de começar

- **Pré-requisitos:** [Módulos 01 a 04](../docs/index.md), com as bibliotecas instaladas no ambiente virtual.
- **Tempo estimado:** ~8 h, mais a preparação da demonstração (estimativa, ajuste ao ritmo da turma)
- **Ao final você terá:** a Secretaria automática funcionando, testada e documentada, e o certificado do curso.

## ✅ Checklist do módulo

- [ ] A estrutura do pacote está criada e a planilha de treino existe.
- [ ] `python -m secretaria tudo treino_secretaria/turma_1A.xlsx` gera boletim, certificados, rascunhos e log.
- [ ] O envio para o servidor de teste funciona com `--enviar`.
- [ ] `python -m pytest testes` passa.
- [ ] O README está pronto e fiz pelo menos uma melhoria própria.

## ➡️ Próximo passo

Comece pela **[aula 01 — Planejando a Secretaria automática](01_planejando_a_secretaria.md)**.
