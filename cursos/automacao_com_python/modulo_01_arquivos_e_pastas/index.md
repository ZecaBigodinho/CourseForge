# Módulo 01 — Arquivos e pastas

> **Curso:** Automação com Python  
> **Módulo:** 01 · Arquivos e pastas  
> **Descrição:** Listar, copiar, mover e renomear arquivos em lote com segurança: simulação, sem sobrescrever e com relatório para desfazer.

---

## 📋 Visão Geral do Módulo

O módulo começa pelo que vale automatizar e pelas **regras de segurança**, e cria uma **pasta de treino** com arquivos de mentira para praticar sem medo. Depois você aprende a enxergar pastas e arquivos com `pathlib`, a copiar, mover e renomear **sem sobrescrever nada** e a **simular** antes de mexer. Com isso, renomeia fotos em lote pela data (e vê dois bugs que só o teste revelou) e monta o projeto do módulo: um **organizador de pastas** com plano, confirmação, relatório CSV e **desfazer**.

---

## 📚 Capítulos

- [01. O que vale automatizar e a pasta de treino](01_o_que_vale_automatizar.md)
- [02. Caminhos e listas de arquivos com `pathlib`](02_pathlib.md)
- [03. Criar, copiar, mover e renomear com segurança](03_mover_copiar_com_seguranca.md)
- [04. Renomear fotos em lote pela data](04_renomear_fotos_pela_data.md)
- [05. Projeto do módulo: organizador de pastas com relatório](05_projeto_organizador.md)

---

## 🎯 Objetivos do Módulo

Ao final deste módulo, você será capaz de:

- Decidir o que vale automatizar e seguir as quatro regras de segurança.
- Usar `Path`, `iterdir()`, `glob()`, `rglob()` e `stat()` para listar e analisar pastas.
- Copiar, mover e renomear com `shutil` e `Path` sem sobrescrever arquivos.
- Escrever scripts com modo de simulação que podem rodar duas vezes sem estragar nada.
- Gravar e ler relatórios CSV que abrem no Excel e permitem desfazer.

---

## 🧭 Antes de começar

- **Pré-requisitos:** Python básico ([Módulo 01 do curso Python para Desktop](../../python_para_desktop/modulo_01_fundamentos/index.md)) e VS Code.
- **Tempo estimado:** ~7 h 30 min (estimativa, ajuste ao ritmo da turma)
- **Ao final você terá:** um organizador de pastas testado, com relatório e desfazer, e um renomeador de fotos.

## ✅ Checklist do módulo

- [ ] Criei a pasta de treino e sei recriá-la do zero.
- [ ] Listo uma pasta mostrando nome, extensão, tamanho e data.
- [ ] Movo arquivos com `SIMULAR` e sem sobrescrever (`destino_livre`).
- [ ] Renomeei as fotos de treino pela data, e rodar de novo não muda nada.
- [ ] Organizei a pasta de treino e desfiz pelo relatório.

## ➡️ Próximo passo

Comece pela **[aula 01 — O que vale automatizar e a pasta de treino](01_o_que_vale_automatizar.md)**.
