<div align="center">

# 🎓 CourseForge — Python para Desktop

[![Acessar Curso](https://img.shields.io/badge/📖_Acessar_Curso-GitHub_Pages-7c4dff?style=for-the-badge)](https://zecabigodinho.github.io/curso-python/)
[![Status](https://img.shields.io/badge/Status-Atualizado-00bfa5?style=for-the-badge)]()
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)]()
[![MkDocs](https://img.shields.io/badge/MkDocs-Material-526CFE?style=for-the-badge&logo=materialformkdocs&logoColor=white)]()
[![License](https://img.shields.io/badge/Licença-Educacional-E91E63?style=for-the-badge)]()

**Curso completo de Python aplicado ao desenvolvimento Desktop — da lógica de programação até a criação de aplicações com interface gráfica, banco de dados, integração com serviços em nuvem, programação orientada a objetos (POO), central de revisão visual e versionamento profissional com Git & GitHub.**

[Acessar o Curso](https://zecabigodinho.github.io/CourseForge/) · [Reportar Problema](https://github.com/ZecaBigodinho/CourseForge/issues) · [Catálogo](https://zecabigodinho.github.io/CourseForge/catalogo/)

</div>

---

## 📋 Sobre o Projeto

Este repositório contém o material completo do curso **Python para Desktop**, hospedado via GitHub Pages e construído com [MkDocs Material](https://squidfunk.github.io/mkdocs-material/). O conteúdo é utilizado em aulas presenciais e online seguindo a metodologia **Project Based Learning (PBL)** — os alunos aprendem construindo um sistema real do início ao fim.

O repositório também inclui a plataforma **CourseForge** (organizada no diretório `src/`) + o motor de automação **CourseForge Hermes & Watcher**, permitindo gerar, publicar e revisar conteúdos didáticos altamente didáticos e visuais com IA.

### ✨ Destaques

- 🛠️ **Começa pelo ambiente (Módulo 00)** — instalação do Python 3, VS Code, extensões e ambientes virtuais (`venv`) passo a passo
- 📚 **6 módulos na trilha principal (00 a 05) + Git & GitHub (bônus)**, com **45+ capítulos** de conteúdo prático
- 🧊 **POO antes das interfaces** — a base para o MVC/CRUD do Projeto Finalizador
- 🎓 **Certificado com regra única** — entrega e apresentação do Projeto Final do Curso
- 🧠 **Central de Revisão Visual & Fixação** — 14 aulas didáticas com metáforas do mundo real, diagramas `Mermaid.js` e solução de erros comuns
- 🏗️ **Project Based Learning** — construção incremental de um sistema desktop profissional (MVC + SQLite + Nuvem)
- 🌐 **Site responsivo** acessível de qualquer dispositivo via GitHub Pages
- 🌙 **Modo escuro/claro** com tema Material Design
- 🤖 **CourseForge CLI & Hermes Automation** — pipeline de geração com IA e atualizações em segundo plano

---

## 🌐 Acesse o Curso

### 👉 [**zecabigodinho.github.io/CourseForge**](https://zecabigodinho.github.io/CourseForge/)

O material está hospedado no **GitHub Pages** e pode ser acessado de qualquer computador, tablet ou celular.

---

## 🗂️ Cursos da Plataforma

| Curso | Situação |
|-------|----------|
| [Python para Desktop](https://zecabigodinho.github.io/CourseForge/python_para_desktop/docs/) | ✅ Disponível |
| [Pacote Office](https://zecabigodinho.github.io/CourseForge/pacote_office/docs/) | ✅ Disponível |
| [Introdução à IA](https://zecabigodinho.github.io/CourseForge/introducao_a_ia/docs/) | ✅ Disponível |

Cada curso tem uma **ficha** em `cursos/<curso>/.courseforge.yaml` (ordem, situação, nível, público, pré-requisitos, objetivos e certificado). O **Catálogo de cursos** (`cursos/catalogo.md`) é gerado a partir dessas fichas por `python main.py publicar` — não edite a página à mão.

---

## 📚 Conteúdo do Curso de Python

O curso está dividido em **6 módulos na trilha principal (00 a 05)**, **1 módulo bônus (06)** e a **Central de Revisão Visual** como material de apoio. Siga a ordem abaixo — é a mesma do menu do site.

### 🛠️ Módulo 00 — Configuração do VS Code & Ambiente
> Comece por aqui · 2 capítulos

| # | Capítulo | Descrição |
|---|----------|-----------|
| 01 | Instalando o VS Code do Zero | Instalação do Python 3 ("Add to PATH"), VS Code, extensões indispensáveis e atalhos |
| 02 | Ambientes Virtuais (`venv`) | Criando e ativando `venv`, resolução do erro do PowerShell e `pip install` |

---

### 🐍 Módulo 01 — Fundamentos de Python
> Os alicerces da linguagem · 11 capítulos

| # | Capítulo | Descrição |
|---|----------|-----------|
| 01 | Variáveis | Tipos de dados, atribuição e conversão |
| 02 | Operadores | Aritméticos, lógicos, comparação e atribuição |
| 03 | If / Else | Estruturas condicionais e tomada de decisão |
| 04 | Repetições | Laços `for`, `while` e controle de fluxo |
| 05 | Funções | Definição, parâmetros, retorno e escopo |
| 06 | Módulos | Importação, organização e criação de módulos |
| 07 | Coleções | Listas, dicionários, tuplas e sets |
| 08 | Strings | Manipulação, formatação e métodos |
| 09 | Arquivos | Leitura, escrita e manipulação de arquivos |
| 10 | Exceções | Tratamento de erros com `try/except` |
| 11 | Mini-projeto: Sistema no Terminal | Consolidação de todos os conceitos em um sistema CLI |

---

### 🧊 Módulo 02 — Programação Orientada a Objetos (POO)
> Paradigma POO, métodos, propriedades e desenvolvimento de aplicações · 3 capítulos

| # | Capítulo | Descrição |
|---|----------|-----------|
| 01 | Estudo do Paradigma POO | Classes, Objetos, Instanciação e estado da entidade |
| 02 | Métodos e Propriedades | O construtor `__init__`, `self`, encapsulamento e `@property` |
| 03 | Desenvolvimento Prático com POO | Modelagem de sistema real com composição e regras de negócio |

---

### 🖥️ Módulo 03 — Interfaces Gráficas
> Criando janelas e aplicações visuais · 5 capítulos

| # | Capítulo | Descrição |
|---|----------|-----------|
| 01 | Tkinter Básico | Janelas, widgets, botões e inputs |
| 02 | Layout Managers | `pack`, `grid`, `place` e organização |
| 03 | Eventos e Interatividade | Bindings, callbacks e validação |
| 04 | CustomTkinter | Interfaces modernas e estilizadas |
| 05 | Projeto Prático | Aplicação completa com UI profissional |

---

### 🗄️ Módulo 04 — Banco de Dados
> Persistência e integração de dados · 4 capítulos

| # | Capítulo | Descrição |
|---|----------|-----------|
| 01 | Introdução ao SQLite | Criação de tabelas e consultas SQL |
| 02 | Integração com Interface | Conectando banco de dados à UI |
| 03 | Variáveis de Ambiente | Proteção de credenciais com `.env` |
| 04 | Projeto de Dados | Interface + SQLite + `.env` em MVC — ensaio geral para o Projeto Finalizador |

---

### 🏗️ Módulo 05 — Projeto Finalizador
> Construção incremental de um sistema completo · 13 capítulos

| # | Capítulo | Descrição |
|---|----------|-----------|
| 01 | Introdução ao Projeto | Planejamento e escopo do sistema |
| 02 | Arquitetura do Sistema | Estrutura de pastas e MVC |
| 03 | Tela de Login | Autenticação com validação |
| 04 | Menu Principal | Janela principal com navegação entre módulos |
| 05 | Múltiplas Janelas | Gerenciamento de janelas filhas e modais |
| 06 | Cadastro de Alunos | Formulário com validação de campos |
| 07 | SQLite Local | Conexão, criação de tabelas e persistência |
| 08 | CRUD Completo | Inserir, listar, atualizar e deletar dados |
| 09 | Banco em Nuvem | Conexão com banco relacional na nuvem |
| 10 | Integração e Testes | Conectando UI + Banco + Validações |
| 11 | Refatoração e Entrega | Limpeza de código e tratamento de erros |
| 12 | Projeto Final do Curso | Entrega e apresentação do sistema — **libera o certificado** |
| 13 | Exercício Bônus | Aplicação web com Streamlit + Neon Database |

---

### 🔀 Módulo 06 — Git & GitHub (Bônus)
> Versionamento, colaboração e portfólio · 2 capítulos

| # | Capítulo | Descrição |
|---|----------|-----------|
| 01 | Criando Projeto Profissional | Git init, commits, .gitignore e repositório no GitHub |
| 02 | Publicando o Projeto Final | README profissional, releases e portfólio |

---

### 🧠 Central de Revisão Visual & Fixação Didática
> Material didático com analogias do cotidiano, fluxogramas Mermaid e guia de erros

| # | Aula de Revisão | Tema & Metáfora Visual |
|---|-----------------|------------------------|
| 01 | Tomada de Decisão (`if/elif/else`) | O *Guarda de Trânsito no Semáforo Inteligente* |
| 02 | Memória, Variáveis e Tipos | O *Armazém de Caixas Etiquetadas* (`int`, `float`, `str`, `bool`) |
| 03 | Operadores Aritméticos e Lógicos | A *Balança da Comparação* e a Catraca de Entrada (`and`/`or`/`not`) |
| 04 | Laços de Repetição (`for`/`while`) | A *Esteira de Fábrica* (`for`) vs *Tanque de Combustível* (`while`) |
| 05 | Funções, Parâmetros e `return` | A *Máquina de Fazer Suco* (Processador e retorno) |
| 06 | Módulos e Organização de Código | A *Caixa de Ferramentas com Compartimentos* |
| 07 | Coleções (Listas, Dicionários, Tuplas)| O *Gaveteiro Numerado* (`[ ]`) vs *Armário de Etiquetas* (`{ }`) |
| 08 | Strings e Manipulação de Textos | O *Trem de Caracteres* e limpadores de texto (`.strip()`, `.split()`) |
| 09 | Manipulação de Arquivos | O *Caderno de Anotações* (`with open`) e persistência JSON/CSV |
| 10 | Tratamento de Erros (`try/except`) | A *Rede de Segurança do Circo* e resiliência |
| 11 | Interfaces Gráficas (Tkinter/CustomTkinter) | A *Árvore de Componentes & Layouts* (`pack`/`grid`) |
| 12 | Banco de Dados SQLite & SQL | O *Arquivo Morto com Secretário SQL* (CRUD Completo) |
| 13 | Versionamento com Git & GitHub | A *Máquina do Tempo do Código* (`add`, `commit`, `push`) |
| 14 | Programação Orientada a Objetos (POO) | A *Planta Industrial de Automóveis* (`class`, `self`, `@property`) |

---

## 🎓 Certificado

O certificado é liberado por **um único requisito**: entregar e apresentar o **Projeto Final do Curso** (capítulo 12 do Módulo 05 — Projeto Finalizador). O Mini-projeto (Módulo 01) e o Projeto de Dados (Módulo 04) são etapas de prática; o Módulo 06 é bônus.

---

## 🏗️ Estrutura do Repositório

```text
curso-python/
├── cursos/              # Conteúdo dos cursos e módulos em Markdown
├── mkdocs/              # Configuração e estilo customizado do MkDocs
├── src/                 # Plataforma CourseForge (Engine CLI, utilitários, templates)
│   ├── config/          # Arquivos de configuração global
│   ├── converter/       # Conversores de formato
│   ├── generators/      # Geradores de módulos, capítulos e prompts
│   ├── models/          # Modelos e enums do domínio
│   ├── prompts/         # Templates de prompts para IA
│   ├── templates/       # Templates Jinja2 para arquivos Markdown
│   └── utils/           # Utilitários de logging, UI e gerenciamento de arquivos
├── hermes/              # API de background e fila de automação
├── tests/               # Suíte de testes unitários
├── main.py              # Ponto de entrada da plataforma CourseForge
├── courseforge_watcher.py # Serviço watcher de automação no PC
└── README.md            # Documentação principal
```

---

## 🛠️ Instalação e Execução Local

Para testar ou desenvolver o material no seu computador:

```bash
# 1. Clonar o repositório
git clone https://github.com/ZecaBigodinho/curso-python.git
cd curso-python

# 2. Instalar dependências Python
pip install -r requirements.txt

# 3. Executar o servidor de desenvolvimento MkDocs
python -m mkdocs serve -f mkdocs/mkdocs.yml
```

O site estará disponível localmente em **`http://localhost:8000`**.

---

## 🚀 Publicação no GitHub Pages

Para publicar as atualizações no site oficial:

```bash
# 1. Regenerar o menu (mkdocs.yml é gerado — não edite à mão) e validar links
python main.py publicar

# 2. Publicar no GitHub Pages
python -m mkdocs gh-deploy -f mkdocs/mkdocs.yml
```

> A ordem dos módulos no menu vem de `ordem_modulos` em `cursos/<curso>/.courseforge.yaml`; os títulos vêm do `# H1` de cada aula.

---

## 👤 Autor e Contato

**Prof. Pedro Paulo IF** · [pedropaulo4hire@gmail.com](mailto:pedropaulo4hire@gmail.com)

Dúvidas sobre o conteúdo ou erros encontrados: abra uma [issue](https://github.com/ZecaBigodinho/curso-python/issues) ou envie um e-mail.

---

## 📄 Licença

Este projeto é destinado a fins **educacionais**. O código fonte e o material didático podem ser utilizados livremente por alunos e professores.
