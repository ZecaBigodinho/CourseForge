# Módulo 03 — Documentos e PDFs

> **Curso:** Automação com Python  
> **Módulo:** 03 · Documentos e PDFs  
> **Descrição:** Preencher modelos do Word, gerar PDFs, tratar imagens em lote e emitir certificados, declarações e crachás a partir de uma planilha.

---

## 📋 Visão Geral do Módulo

Declarações, certificados, crachás, listas de presença, fotos para enviar: documentos que se repetem para cada pessoa de uma lista. Neste módulo você instala **python-docx**, **fpdf2** e **Pillow**, preenche um **modelo do Word** com marcadores `{{nome}}`, desenha um **certificado em PDF**, prepara **fotos em lote** (reduzir, converter, marca-d'água e a data verdadeira do EXIF) e monta **certificados e crachás** para a turma inteira. No projeto, um script emite **certificado com código de validação** para quem tem 75% de frequência, **declaração em Word** para os demais e um **relatório** de tudo o que foi emitido.

---

## 📚 Capítulos

- [01. Documentos do Word com python-docx](01_documentos_word.md)
- [02. Gerando PDFs com fpdf2](02_pdf_com_fpdf2.md)
- [03. Imagens em lote com Pillow](03_imagens_em_lote.md)
- [04. Certificados e crachás em lote](04_certificados_e_crachas.md)
- [05. Projeto do módulo: emissão de certificados e declarações](05_projeto_emissao.md)

---

## 🎯 Objetivos do Módulo

Ao final deste módulo, você será capaz de:

- Criar documentos do Word e preencher modelos com dados de uma planilha.
- Desenhar PDFs em milímetros, com fontes, cores, linhas e tabelas.
- Reduzir, converter e marcar imagens em lote, lendo a data EXIF.
- Gerar documentos em lote com nomes de arquivo seguros e folhas de crachás.
- Reaproveitar funções entre scripts com `import` e `main()`.

---

## 🧭 Antes de começar

- **Pré-requisitos:** [Módulo 02](../modulo_02_planilhas/index.md) (ambiente virtual e planilhas).
- **Tempo estimado:** ~8 h (estimativa, ajuste ao ritmo da turma)
- **Ao final você terá:** certificados com código de validação, declarações, crachás e fotos prontas, gerados a partir de uma planilha.

## ✅ Checklist do módulo

- [ ] Instalei `python-docx==1.2.0`, `fpdf2==2.8.9` e `pillow==12.3.0` no ambiente virtual.
- [ ] Gerei uma declaração em Word para cada participante a partir do modelo.
- [ ] Desenhei um certificado em PDF e sei resolver o erro de caractere fora da fonte.
- [ ] Preparei as fotos de treino: menores, em JPG, com marca-d'água e nome pela data EXIF.
- [ ] Emiti os certificados e as declarações do projeto e validei um código pelo relatório.

## ➡️ Próximo passo

Comece pela **[aula 01 — Documentos do Word com python-docx](01_documentos_word.md)**.
