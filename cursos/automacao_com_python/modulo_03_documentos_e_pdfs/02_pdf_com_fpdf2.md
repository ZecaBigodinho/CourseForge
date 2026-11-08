# 02 — Gerando PDFs com fpdf2

> **Curso:** Automação com Python  
> **Módulo:** 03 — Documentos e PDFs  
> **Tempo estimado:** 1 h 30 min  

---

## 🎯 Objetivos

Ao final desta aula, você será capaz de:

- Criar um PDF com **fpdf2**: página, fonte, cor, texto, linhas e retângulos.
- Posicionar elementos em **milímetros** numa folha A4.
- Desenhar um **certificado** completo numa função reaproveitável.
- Resolver o erro de **caracteres fora da fonte** (travessão, emojis, símbolos).

## Pré-requisitos

- [Aula 01](01_documentos_word.md): bibliotecas instaladas e arquivos de treino.

!!! question "Word ou PDF?"
    **Word** quando alguém ainda vai **editar** o documento (uma declaração que a secretaria confere e ajusta). **PDF** quando o documento está **pronto** e não deve mudar (certificado, comprovante, crachá para imprimir): abre igual em qualquer aparelho e não "desconfigura".

---

## Como o fpdf2 pensa

O fpdf2 funciona como uma **caneta** sobre a folha: você escolhe a posição, a fonte e a cor, e escreve. A posição é medida em **milímetros** a partir do canto **superior esquerdo**. Uma folha A4 deitada (*landscape*) tem **297 mm** de largura e **210 mm** de altura.

| Comando | Faz |
|---|---|
| `FPDF(orientation="landscape", format="A4")` | Documento novo (A4 deitado; sem `orientation`, em pé) |
| `pdf.add_page()` | Começa uma página |
| `pdf.set_font("Helvetica", "B", 20)` | Fonte, estilo (`""`, `"B"` negrito, `"I"` itálico, `"BI"`) e tamanho |
| `pdf.set_text_color(r, g, b)` / `set_draw_color` / `set_fill_color` | Cor do texto, das linhas, do preenchimento |
| `pdf.cell(largura, altura, texto, align="C")` | Uma linha de texto numa "caixa"; `largura=0` vai até a margem direita |
| `pdf.multi_cell(largura, altura, texto)` | Texto que **quebra** em várias linhas |
| `pdf.set_xy(x, y)`, `pdf.set_y(y)`, `pdf.ln(mm)` | Move a caneta; `ln` pula para baixo |
| `pdf.rect(x, y, w, h)`, `pdf.line(x1, y1, x2, y2)` | Retângulo e linha |
| `pdf.image(caminho, x, y, w)` | Uma imagem (logotipo, assinatura digitalizada) |
| `pdf.output(caminho)` | Grava o arquivo |

## O certificado

```python title="certificado.py"
from datetime import date
from pathlib import Path

from fpdf import FPDF

ROXO = (79, 53, 181)
MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho",
         "agosto", "setembro", "outubro", "novembro", "dezembro"]


def desenhar_certificado(pdf: FPDF, nome: str, curso: str, carga: int, dia: date) -> None:
    """Acrescenta ao PDF uma página A4 deitada com o certificado."""
    pdf.add_page()
    # Moldura dupla
    pdf.set_draw_color(*ROXO)
    pdf.set_line_width(1.5)
    pdf.rect(10, 10, 277, 190)
    pdf.set_line_width(0.4)
    pdf.rect(14, 14, 269, 182)
    # Título
    pdf.set_y(40)
    pdf.set_font("Helvetica", "B", 34)
    pdf.set_text_color(*ROXO)
    pdf.cell(0, 16, "CERTIFICADO", align="C", new_x="LMARGIN", new_y="NEXT")
    # Texto
    pdf.set_text_color(30, 30, 30)
    pdf.set_font("Helvetica", "", 15)
    pdf.ln(10)
    pdf.cell(0, 10, "Certificamos que", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "B", 26)
    pdf.cell(0, 16, nome, align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 15)
    pdf.set_x(40)
    pdf.multi_cell(217, 9, f"concluiu a {curso}, com carga horária de {carga} horas.", align="C")
    # Data e assinatura
    pdf.ln(18)
    data = f"{dia.day} de {MESES[dia.month - 1]} de {dia.year}"
    pdf.cell(0, 8, f"Cidade Exemplo, {data}.", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.line(108, 168, 189, 168)
    pdf.set_xy(108, 170)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(81, 6, "Prof. Pedro Paulo - Responsável", align="C")


def main() -> None:
    pdf = FPDF(orientation="landscape", format="A4")
    pdf.set_auto_page_break(False)
    desenhar_certificado(pdf, "Ana Souza", "Oficina de Canva para Pequenos Negócios", 20, date.today())
    destino = Path("treino_docs") / "saida" / "certificado_teste.pdf"
    destino.parent.mkdir(exist_ok=True)
    pdf.output(destino)
    print(f"Salvo: {destino}")


if __name__ == "__main__":
    main()
```

Rode `python certificado.py` e abra `treino_docs/saida/certificado_teste.pdf`: moldura dupla roxa, **CERTIFICADO** em destaque, o nome em negrito, o texto centralizado, a data por extenso e a linha de assinatura.

### Detalhes do código

- **`new_x="LMARGIN", new_y="NEXT"`** no `cell()`: depois de escrever, a caneta volta para a margem esquerda e desce para a **próxima linha**. Sem isso, ela fica à direita do texto que acabou de escrever.
- **`set_auto_page_break(False)`**: sem isso, ao chegar perto do fim da folha, o fpdf2 cria **outra página** sozinho. Num certificado de uma página só, desligamos.
- **`pdf.set_x(40)` + `multi_cell(217, ...)`**: o texto que pode ficar comprido (o nome do curso) quebra em várias linhas dentro de uma faixa de 217 mm centralizada (40 + 217 + 40 = 297).
- **A função recebe o `pdf` pronto** e só **acrescenta uma página**. Assim, a mesma função serve para um PDF com um certificado ou com cinquenta ([aula 04](04_certificados_e_crachas.md)).

!!! tip "Quer um logotipo?"
    `pdf.image("logo.png", x=20, y=20, w=30)` coloca a imagem com 30 mm de largura (a altura acompanha). Use PNG com fundo transparente para ficar bonito sobre a folha branca.

## Acentos funcionam; travessão e emojis, não

As fontes que já vêm no fpdf2 (Helvetica, Times, Courier) só conhecem os caracteres do **Latin-1**: letras com acento, `ç`, `ã`, `º`, `ª`... tudo o que o português usa no dia a dia. Mas **não** conhecem o travessão (`—`), aspas curvas (`“ ”`), o símbolo `✓` nem emojis:

```text
FPDFUnicodeEncodingException: Character "—" at index 6 in text is outside the range of characters
supported by the font used: "helvetica". Please consider using a Unicode font.
```

Duas saídas:

1. **Trocar o caractere:** use hífen (`-`) no lugar do travessão (foi o que o certificado fez em "Prof. Pedro Paulo - Responsável").
2. **Usar uma fonte TrueType** (`.ttf`) do Windows, que tem todos os caracteres:

```python
pdf.add_font("Arial", "", r"C:\Windows\Fonts\arial.ttf")
pdf.add_font("Arial", "B", r"C:\Windows\Fonts\arialbd.ttf")
pdf.set_font("Arial", "", 14)
pdf.cell(0, 10, "Curso — módulo 1")
```

!!! info "Fontes e direitos"
    As fontes do Windows podem ser usadas nos documentos que você cria no seu computador. Para distribuir a fonte junto com um programa, prefira fontes livres, como as do Google Fonts (Inter, Roboto, Open Sans), baixando o `.ttf` do site oficial.

---

## ⚠️ Erros comuns

- **`FPDFUnicodeEncodingException`**: caractere fora da fonte (veja acima).
- **Texto saindo da folha**: use `multi_cell` para textos que podem ser longos, ou diminua a fonte.
- **Página extra em branco**: faltou `set_auto_page_break(False)`.
- **Tudo escrito na mesma linha**: faltou `new_y="NEXT"` (ou `ln()`) depois do `cell`.
- **`FPDFException: No page open`**: escreveu antes do `add_page()`.

---

## Exercícios

### Básico (fixação)

Usando a função `desenhar_certificado()` do `certificado.py` (com `import`), gere o certificado do **Bruno Lima** em `treino_docs/saida/certificado_bruno.pdf`.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```python
    from datetime import date
    from pathlib import Path

    from fpdf import FPDF

    from certificado import desenhar_certificado

    pdf = FPDF(orientation="landscape", format="A4")
    pdf.set_auto_page_break(False)
    desenhar_certificado(pdf, "Bruno Lima", "Oficina de Canva para Pequenos Negócios", 20, date.today())
    destino = Path("treino_docs") / "saida" / "certificado_bruno.pdf"
    destino.parent.mkdir(exist_ok=True)
    pdf.output(destino)
    ```

    Como o `certificado.py` tem o `if __name__ == "__main__":`, importar não gera o certificado de teste da Ana: só a função é usada.

### Intermediário (aplicação)

Gere uma **lista de presença** em PDF (A4 em pé) com o título "Lista de presença — Oficina de Canva" e uma tabela com as colunas **Nº**, **Nome** e **Assinatura**, uma linha para cada participante da planilha. Use a fonte **Arial** do Windows (por causa do travessão) e o recurso de tabela do fpdf2 (`pdf.table()`).

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```python
    from pathlib import Path

    from fpdf import FPDF
    from openpyxl import load_workbook

    planilha = load_workbook(Path("treino_docs") / "participantes.xlsx")["Participantes"]
    nomes = [nome for nome, *_ in planilha.iter_rows(min_row=2, values_only=True)]

    pdf = FPDF(format="A4")
    pdf.add_font("Arial", "", r"C:\Windows\Fonts\arial.ttf")
    pdf.add_font("Arial", "B", r"C:\Windows\Fonts\arialbd.ttf")
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 12, "Lista de presença — Oficina de Canva", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    pdf.set_font("Arial", "", 11)
    with pdf.table(col_widths=(12, 80, 98), line_height=9) as tabela:
        tabela.row(["Nº", "Nome", "Assinatura"])
        for numero, nome in enumerate(nomes, start=1):
            tabela.row([str(numero), nome, ""])

    destino = Path("treino_docs") / "saida" / "lista_presenca.pdf"
    destino.parent.mkdir(exist_ok=True)
    pdf.output(destino)
    ```

    O `pdf.table()` desenha as bordas e põe a primeira linha em destaque (cabeçalho). Os valores das células precisam ser **texto** (`str(numero)`). Se a lista passar de uma página, a tabela continua na próxima, repetindo o cabeçalho.

### Avançado (desafio)

Altere uma **cópia** do `certificado.py` para aceitar o parâmetro `tipo`: `"conclusão"` (texto atual, "concluiu a...") ou `"participação"` (título **DECLARAÇÃO** e o texto "participou da..."). Gere um exemplo de cada.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```python
    from datetime import date
    from pathlib import Path

    from fpdf import FPDF

    ROXO = (79, 53, 181)
    MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho",
             "agosto", "setembro", "outubro", "novembro", "dezembro"]


    def desenhar_documento(pdf: FPDF, nome: str, curso: str, carga: int, dia: date, tipo: str) -> None:
        titulo, verbo = {"conclusão": ("CERTIFICADO", "concluiu a"),
                         "participação": ("DECLARAÇÃO", "participou da")}[tipo]
        pdf.add_page()
        pdf.set_draw_color(*ROXO)
        pdf.set_line_width(1.5)
        pdf.rect(10, 10, 277, 190)
        pdf.set_y(45)
        pdf.set_font("Helvetica", "B", 34)
        pdf.set_text_color(*ROXO)
        pdf.cell(0, 16, titulo, align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.set_text_color(30, 30, 30)
        pdf.set_font("Helvetica", "B", 26)
        pdf.ln(12)
        pdf.cell(0, 16, nome, align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 15)
        pdf.set_x(40)
        pdf.multi_cell(217, 9, f"{verbo} {curso}, com carga horária de {carga} horas.", align="C")
        pdf.ln(14)
        pdf.cell(0, 8, f"Cidade Exemplo, {dia.day} de {MESES[dia.month - 1]} de {dia.year}.", align="C")


    pdf = FPDF(orientation="landscape", format="A4")
    pdf.set_auto_page_break(False)
    for tipo in ("conclusão", "participação"):
        desenhar_documento(pdf, "Ana Souza", "Oficina de Canva", 20, date.today(), tipo)
    destino = Path("treino_docs") / "saida" / "dois_tipos.pdf"
    destino.parent.mkdir(exist_ok=True)
    pdf.output(destino)
    ```

    Um **dicionário** escolhe o título e o verbo conforme o `tipo`: para acrescentar um terceiro tipo (por exemplo, "monitoria"), basta uma linha nova no dicionário. Saem duas páginas no mesmo PDF. Um `tipo` que não existe dá `KeyError`, o que é bom: melhor parar do que emitir um documento com o texto errado.

---

## 💡 Resumo

- fpdf2 desenha em **milímetros**, a partir do canto superior esquerdo; A4 deitado = 297 × 210 mm.
- `cell` (uma linha), `multi_cell` (texto que quebra), `rect`, `line`, `image`; `new_y="NEXT"` desce a caneta.
- Uma função que **recebe o `pdf` e acrescenta uma página** serve para um ou para muitos documentos.
- Fontes padrão: acentos sim; travessão, aspas curvas e emojis não. Para isso, `add_font()` com uma fonte `.ttf`.

## ➡️ Próximo passo

**[03 — Imagens em lote com Pillow](03_imagens_em_lote.md)**: reduzir, converter, marca-d'água e a data verdadeira das fotos.
