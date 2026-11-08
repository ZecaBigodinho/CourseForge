# 01 — Documentos do Word com python-docx

> **Curso:** Automação com Python  
> **Módulo:** 03 — Documentos e PDFs  
> **Tempo estimado:** 1 h 30 min  

---

## 🎯 Objetivos

Ao final desta aula, você será capaz de:

- Instalar as bibliotecas do módulo: **python-docx**, **fpdf2** e **Pillow**.
- Criar um documento do Word com **títulos**, **parágrafos**, **listas** e **tabelas**.
- Preencher um **modelo** com marcadores `{{nome}}`, `{{data}}`... e gerar um documento para cada pessoa da planilha.
- Escrever a **data por extenso** em português.

## Pré-requisitos

- [Módulo 02](../modulo_02_planilhas/index.md): ambiente virtual, openpyxl e leitura de planilhas.

---

## Instalando as bibliotecas

Com o ambiente virtual ativado ([Módulo 02, aula 01](../modulo_02_planilhas/01_ler_planilhas.md#o-ambiente-virtual-e-o-openpyxl)):

```powershell
python -m pip install python-docx==1.2.0 fpdf2==2.8.9 pillow==12.3.0
```

| Biblioteca | Para que serve | Aula |
|---|---|---|
| **python-docx** (`import docx`) | Ler e escrever documentos do Word (`.docx`) | 01 |
| **fpdf2** (`from fpdf import FPDF`) | Gerar PDFs desenhando texto, linhas e imagens | 02, 04, 05 |
| **Pillow** (`from PIL import Image`) | Abrir, reduzir, converter e editar imagens | 03 |

!!! info "O nome do pip e o nome do import são diferentes"
    Instala-se `python-docx`, mas importa-se `docx`; instala-se `pillow`, mas importa-se `PIL`. Não instale um pacote chamado só `docx`: é outro, antigo, que não funciona com o código deste curso.

## Os arquivos de treino

Este script cria a pasta `treino_docs` com a **planilha de participantes** de uma oficina (10 pessoas inventadas, com a frequência de cada uma), o **modelo** de declaração em Word e algumas **fotos** (usadas na [aula 03](03_imagens_em_lote.md)).

```python title="criar_treino_documentos.py"
"""Cria os arquivos de treino do Módulo 03: planilha de participantes, modelo do Word e fotos."""
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from openpyxl import Workbook
from PIL import Image, ImageDraw

TREINO = Path("treino_docs")

PARTICIPANTES = [  # nome, matrícula, frequência (%)
    ("Ana Souza", 2026001, 100), ("Bruno Lima", 2026002, 85), ("Carla Mendes", 2026003, 95),
    ("Diego Rocha", 2026004, 60), ("Elisa Prado", 2026005, 90), ("Felipe Torres", 2026006, 75),
    ("Gabriela Nunes", 2026007, 40), ("Heitor Alves", 2026008, 100), ("Isabela Costa", 2026009, 80),
    ("João Pedro Melo", 2026010, 70),
]

FOTOS = {  # nome do arquivo: (cor, data em que a foto foi tirada, gravada nos dados EXIF)
    "IMG_0101.jpg": ("#4F35B5", "2026:09:12 14:05:10"),
    "IMG_0102.jpg": ("#00796B", "2026:09:12 14:07:42"),
    "IMG_0103.jpg": ("#E8781E", "2026:09:13 09:30:00"),
    "IMG_0104.jpg": ("#C62828", None),               # sem data EXIF (foto editada)
    "print_tela.png": ("#2E7D32", None),             # PNG com fundo transparente
}


def criar_planilha() -> None:
    livro = Workbook()
    aba = livro.active
    aba.title = "Participantes"
    aba.append(["Nome", "Matrícula", "Frequência (%)"])
    for linha in PARTICIPANTES:
        aba.append(list(linha))
    info = livro.create_sheet("Curso")
    for chave, valor in [("Curso", "Oficina de Canva para Pequenos Negócios"), ("Carga horária", 20),
                         ("Início", "01/09/2026"), ("Fim", "30/09/2026"), ("Responsável", "Prof. Pedro Paulo")]:
        info.append([chave, valor])
    livro.save(TREINO / "participantes.xlsx")


def criar_modelo() -> None:
    doc = Document()
    titulo = doc.add_heading("DECLARAÇÃO DE PARTICIPAÇÃO", level=1)
    titulo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_paragraph(
        "Declaramos, para os devidos fins, que {{nome}}, matrícula {{matricula}}, participou da "
        "{{curso}}, realizada de {{inicio}} a {{fim}}, com carga horária de {{carga}} horas e "
        "frequência de {{frequencia}}%."
    )
    doc.add_paragraph("Cidade Exemplo, {{data}}.")
    doc.add_paragraph()
    assinatura = doc.add_paragraph("_______________________________\n{{responsavel}}")
    assinatura.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.save(TREINO / "modelo_declaracao.docx")


def criar_fotos() -> None:
    pasta = TREINO / "fotos"
    pasta.mkdir()
    for nome, (cor, data) in FOTOS.items():
        if nome.endswith(".png"):  # fundo transparente, só o círculo colorido
            foto = Image.new("RGBA", (3000, 2000), (0, 0, 0, 0))
            ImageDraw.Draw(foto).ellipse((600, 100, 2400, 1900), fill=cor)
        else:
            foto = Image.new("RGB", (3000, 2000), cor)
        desenho = ImageDraw.Draw(foto)
        desenho.ellipse((900, 400, 2100, 1600), fill="#FFFFFF")
        desenho.text((1300, 950), nome, fill="#000000", font_size=90)
        if nome.endswith(".png"):
            foto.save(pasta / nome)
            continue
        exif = Image.Exif()
        if data:
            exif.get_ifd(0x8769)[0x9003] = data  # DateTimeOriginal: quando a foto foi tirada
        foto.save(pasta / nome, quality=95, exif=exif)


def main() -> None:
    if TREINO.exists():
        print(f"A pasta '{TREINO}' já existe. Apague-a se quiser começar do zero.")
        return
    TREINO.mkdir()
    criar_planilha()
    criar_modelo()
    criar_fotos()
    print(f"Arquivos de treino criados em: {TREINO.resolve()}")


if __name__ == "__main__":
    main()
```

Rode `python criar_treino_documentos.py` e abra o `modelo_declaracao.docx` no Word: os marcadores entre chaves duplas (`{{nome}}`, `{{curso}}`...) são os lugares que o script vai preencher.

!!! tip "Faça o seu próprio modelo no Word"
    Na vida real, o modelo é feito **no Word**, com o timbre da escola ou da empresa, e o Python só preenche. Basta escrever os marcadores `{{assim}}` onde devem entrar os dados. Veja o cuidado com a formatação no fim desta aula.

## Criando um documento do zero

```python title="primeiro_documento.py"
from pathlib import Path

from docx import Document
from docx.shared import Pt

doc = Document()
doc.add_heading("Lista de materiais da oficina", level=1)
doc.add_paragraph("Traga estes itens no primeiro dia:")
for item in ["Celular com o Canva instalado", "Caderno", "Fone de ouvido"]:
    doc.add_paragraph(item, style="List Bullet")

tabela = doc.add_table(rows=1, cols=2, style="Table Grid")
tabela.rows[0].cells[0].text = "Dia"
tabela.rows[0].cells[1].text = "Assunto"
for dia, assunto in [("01/09", "Conhecendo o Canva"), ("08/09", "Cardápio"), ("15/09", "Posts")]:
    linha = tabela.add_row().cells
    linha[0].text, linha[1].text = dia, assunto

aviso = doc.add_paragraph().add_run("Dúvidas: fale com a secretaria.")
aviso.italic = True
aviso.font.size = Pt(9)

destino = Path("treino_docs") / "saida" / "materiais.docx"
destino.parent.mkdir(exist_ok=True)
doc.save(destino)
print(f"Salvo: {destino}")
```

| Comando | Faz |
|---|---|
| `Document()` | Documento novo, em branco |
| `Document("modelo.docx")` | Abre um documento existente |
| `doc.add_heading(texto, level=1)` | Título (nível 0 a 9) |
| `doc.add_paragraph(texto, style=...)` | Parágrafo; `style="List Bullet"` faz lista com marcadores |
| `doc.add_table(rows, cols, style="Table Grid")` | Tabela com bordas; `add_row()` acrescenta linhas |
| `paragrafo.add_run(texto)` | Um trecho do parágrafo com formatação própria (`.bold`, `.italic`, `.font.size`) |
| `doc.add_page_break()` | Quebra de página |
| `doc.save(caminho)` | Salva (e substitui se já existir) |

## Preenchendo o modelo: uma declaração para cada participante

```python title="preencher_declaracoes.py"
from datetime import date
from pathlib import Path

from docx import Document
from openpyxl import load_workbook

PASTA = Path("treino_docs")
MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho",
         "agosto", "setembro", "outubro", "novembro", "dezembro"]


def data_por_extenso(dia: date) -> str:
    return f"{dia.day} de {MESES[dia.month - 1]} de {dia.year}"


def substituir(doc, valores: dict[str, str]) -> None:
    """Troca {{chave}} pelo valor em todos os parágrafos (e nas tabelas) do documento."""
    paragrafos = list(doc.paragraphs)
    for tabela in doc.tables:
        for linha in tabela.rows:
            for celula in linha.cells:
                paragrafos.extend(celula.paragraphs)
    for paragrafo in paragrafos:
        if "{{" not in paragrafo.text:
            continue
        texto = paragrafo.text
        for chave, valor in valores.items():
            texto = texto.replace("{{" + chave + "}}", str(valor))
        # O texto pode estar espalhado em vários "pedaços" (runs): junta tudo no primeiro
        for run in paragrafo.runs[1:]:
            run.text = ""
        paragrafo.runs[0].text = texto


def main() -> None:
    livro = load_workbook(PASTA / "participantes.xlsx")
    curso = {chave: valor for chave, valor in livro["Curso"].iter_rows(values_only=True)}
    saida = PASTA / "saida" / "declaracoes"
    saida.mkdir(parents=True, exist_ok=True)

    for nome, matricula, frequencia in livro["Participantes"].iter_rows(min_row=2, values_only=True):
        doc = Document(PASTA / "modelo_declaracao.docx")
        substituir(doc, {
            "nome": nome, "matricula": matricula, "frequencia": frequencia,
            "curso": curso["Curso"], "inicio": curso["Início"], "fim": curso["Fim"],
            "carga": curso["Carga horária"], "responsavel": curso["Responsável"],
            "data": data_por_extenso(date.today()),
        })
        destino = saida / f"declaracao_{matricula}.docx"
        doc.save(destino)
        print(f"{nome:18} -> {destino.name}")


if __name__ == "__main__":
    main()
```

```text
Ana Souza          -> declaracao_2026001.docx
Bruno Lima         -> declaracao_2026002.docx
Carla Mendes       -> declaracao_2026003.docx
...
```

Abra a `declaracao_2026001.docx`: *"Declaramos, para os devidos fins, que Ana Souza, matrícula 2026001, participou da Oficina de Canva para Pequenos Negócios, realizada de 01/09/2026 a 30/09/2026, com carga horária de 20 horas e frequência de 100%."*

### Entendendo a função `substituir()`

No Word, um parágrafo é dividido em **runs**: pedaços de texto com a mesma formatação. Um marcador como `{{nome}}` pode ficar **partido** em vários runs (`{{` num, `nome` noutro, `}}` noutro), por exemplo quando você corrige uma letra no meio dele ou o corretor ortográfico marca a palavra. Se o script trocasse run por run, não acharia o marcador.

Por isso a função trabalha com o **texto do parágrafo inteiro** (`paragrafo.text`), faz as trocas e põe o resultado no **primeiro** run, apagando os outros.

!!! warning "O preço da simplicidade"
    Como o texto vai todo para o primeiro run, o parágrafo fica com a formatação do **começo** dele. Se o seu modelo tiver, no **mesmo parágrafo**, uma palavra em negrito e outra normal **junto com um marcador**, essa diferença se perde. A solução prática: deixe cada marcador num parágrafo com formatação uniforme (o nome do aluno em negrito pode ficar num parágrafo só dele).

### Data por extenso

O Python escreve as datas em inglês (`November`). A função `data_por_extenso()` usa uma lista com os meses em português: `MESES[dia.month - 1]` (o `- 1` porque a lista começa no índice 0 e janeiro é o mês 1).

### Por que `main()`?

O código que **faz** o trabalho está dentro de `main()`, e não solto no arquivo. Assim, outro script pode **importar** as funções `substituir()` e `data_por_extenso()` sem gerar as declarações de novo. O projeto do módulo ([aula 05](05_projeto_emissao.md)) faz exatamente isso, e a [aula 04](04_certificados_e_crachas.md) mostra o que acontece quando esquecemos.

---

## ⚠️ Erros comuns

- **`ModuleNotFoundError: No module named 'docx'`**: o ambiente virtual não está ativado, ou foi instalado o pacote errado. Use `pip install python-docx`.
- **`PackageNotFoundError`** ao abrir o modelo: o arquivo não é um `.docx` (é `.doc` antigo ou `.odt`). Abra no Word e salve como `.docx`.
- **Marcador que não foi trocado**: o nome no dicionário está diferente do modelo (`{{Nome}}` × `{{nome}}`), ou há espaço dentro das chaves (`{{ nome }}`). Veja o desafio desta aula.
- **`PermissionError` ao salvar**: o documento está aberto no Word.

---

## Exercícios

### Básico (fixação)

Crie `treino_docs/saida/aviso.docx` com o título **"Aviso"** e um parágrafo informando que a próxima aula da oficina será no laboratório 2.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```python
    from pathlib import Path

    from docx import Document

    doc = Document()
    doc.add_heading("Aviso", level=1)
    doc.add_paragraph("A próxima aula da Oficina de Canva será no laboratório 2.")

    destino = Path("treino_docs") / "saida" / "aviso.docx"
    destino.parent.mkdir(exist_ok=True)
    doc.save(destino)
    ```

### Intermediário (aplicação)

Escreva um script que liste **todos os marcadores** `{{...}}` que existem no `modelo_declaracao.docx`, sem repetir, em ordem alfabética. Use o módulo `re`.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```python
    import re
    from pathlib import Path

    from docx import Document

    doc = Document(Path("treino_docs") / "modelo_declaracao.docx")
    texto = "\n".join(p.text for p in doc.paragraphs)
    marcadores = sorted(set(re.findall(r"\{\{(\w+)\}\}", texto)))
    print(marcadores)
    ```

    Saída: `['carga', 'curso', 'data', 'fim', 'frequencia', 'inicio', 'matricula', 'nome', 'responsavel']`. Na expressão, `\{\{` são as chaves "de verdade" (a barra tira o significado especial) e `(\w+)` captura o nome. Esse script ajuda a conferir se o dicionário do `substituir()` tem todas as chaves.

### Avançado (desafio)

Escreva a função `marcadores_sobrando(doc)`, que devolve a lista de marcadores que **continuam** no documento depois do `substituir()`. Teste preenchendo o modelo **sem** a chave `"data"`: a função deve avisar `['data']`.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```python
    import re
    from pathlib import Path

    from docx import Document

    from preencher_declaracoes import substituir


    def marcadores_sobrando(doc) -> list[str]:
        texto = "\n".join(p.text for p in doc.paragraphs)
        return sorted(set(re.findall(r"\{\{(\w+)\}\}", texto)))


    doc = Document(Path("treino_docs") / "modelo_declaracao.docx")
    substituir(doc, {"nome": "Ana Souza", "matricula": 2026001, "frequencia": 100,
                     "curso": "Oficina de Canva", "inicio": "01/09/2026", "fim": "30/09/2026",
                     "carga": 20, "responsavel": "Prof. Pedro Paulo"})
    sobrando = marcadores_sobrando(doc)
    if sobrando:
        print(f"Atenção: faltou preencher {sobrando}")
    ```

    Saída: `Atenção: faltou preencher ['data']`. Num script de verdade, use essa conferência antes do `doc.save()` e **não salve** o documento com marcadores sobrando: melhor um erro na tela do que uma declaração com `{{data}}` impressa.

---

## 💡 Resumo

- `pip install python-docx fpdf2 pillow` (com as versões fixas); importa-se `docx`, `fpdf` e `PIL`.
- `Document()` cria; `add_heading`, `add_paragraph`, `add_table`, `add_run` montam; `save()` grava.
- **Modelo + marcadores `{{chave}}` + `substituir()`** = um documento por linha da planilha.
- O texto do parágrafo inteiro vai para o primeiro run: mantenha a formatação uniforme onde há marcadores.
- Código dentro de `main()` deixa as funções **importáveis** sem efeitos colaterais.

## ➡️ Próximo passo

**[02 — Gerando PDFs com fpdf2](02_pdf_com_fpdf2.md)**: um certificado bonito, desenhado com o Python.
