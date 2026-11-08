# 03 — Imagens em lote com Pillow

> **Curso:** Automação com Python  
> **Módulo:** 03 — Documentos e PDFs  
> **Tempo estimado:** 1 h 30 min  

---

## 🎯 Objetivos

Ao final desta aula, você será capaz de:

- Abrir imagens com **Pillow** e ler tamanho, formato e modo de cor.
- **Reduzir** fotos mantendo a proporção, para enviar por e-mail ou postar.
- **Converter** PNG com transparência em JPG sem deixar o fundo preto.
- Colocar uma **marca-d'água** de texto.
- Ler a **data em que a foto foi tirada** (EXIF), como prometido no [Módulo 01](../modulo_01_arquivos_e_pastas/04_renomear_fotos_pela_data.md).

## Pré-requisitos

- [Aula 01](01_documentos_word.md): Pillow instalado e a pasta `treino_docs/fotos` criada.

---

## O básico do Pillow

```python
from PIL import Image

with Image.open("treino_docs/fotos/IMG_0101.jpg") as foto:
    print(foto.size)     # (3000, 2000): largura e altura em pixels
    print(foto.format)   # JPEG
    print(foto.mode)     # RGB (PNG com transparência: RGBA)
```

| Comando | Faz |
|---|---|
| `Image.open(caminho)` | Abre a imagem (use com `with`, que fecha o arquivo no fim) |
| `foto.thumbnail((1600, 1600))` | Reduz para caber em 1600 × 1600, **mantendo a proporção** (nunca aumenta) |
| `foto.resize((largura, altura))` | Muda para o tamanho exato (pode distorcer) |
| `ImageOps.fit(foto, (300, 300))` | Recorta no centro e reduz para o tamanho exato, sem distorcer |
| `foto.convert("RGB")` | Muda o modo de cor |
| `foto.save(caminho, quality=85)` | Salva; o formato vem da extensão (`.jpg`, `.png`, `.webp`) |
| `ImageDraw.Draw(foto).text((x, y), texto, fill=..., font_size=...)` | Escreve na imagem |

!!! info "Por que reduzir?"
    Uma foto de celular tem cerca de 4000 × 3000 pixels e 3 a 5 MB. Para mandar 30 fotos por e-mail, postar ou colocar num documento, 1600 pixels no lado maior são mais que suficientes, e o arquivo cai para algumas centenas de KB.

## O script completo

```python title="preparar_fotos.py"
"""Prepara fotos para enviar ou postar: reduz, converte para JPG, põe marca-d'água e renomeia pela data."""
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps

ORIGEM = Path("treino_docs") / "fotos"
DESTINO = Path("treino_docs") / "saida" / "fotos_prontas"
TAMANHO_MAXIMO = 1600  # pixels no lado maior
MARCA = "Oficina de Canva 2026"
EXTENSOES = {".jpg", ".jpeg", ".png", ".webp"}


def data_da_foto(foto: Image.Image, arquivo: Path) -> datetime:
    """Data em que a foto foi tirada (EXIF); se não houver, a data de modificação do arquivo."""
    texto = foto.getexif().get_ifd(0x8769).get(0x9003)  # DateTimeOriginal
    if texto:
        return datetime.strptime(texto, "%Y:%m:%d %H:%M:%S")
    return datetime.fromtimestamp(arquivo.stat().st_mtime)


def preparar(arquivo: Path) -> tuple[Path, tuple[int, int]]:
    with Image.open(arquivo) as original:
        quando = data_da_foto(original, arquivo)
        foto = ImageOps.exif_transpose(original)       # endireita fotos tiradas com o celular "deitado"
        foto.thumbnail((TAMANHO_MAXIMO, TAMANHO_MAXIMO))  # reduz mantendo a proporção
        if foto.mode != "RGB":                          # JPG não tem transparência:
            fundo = Image.new("RGB", foto.size, "white")   # o transparente vira branco
            fundo.paste(foto, mask=foto.convert("RGBA").getchannel("A"))
            foto = fundo
    desenho = ImageDraw.Draw(foto)
    tamanho_letra = max(16, foto.width // 40)
    x, y = 20, foto.height - tamanho_letra - 20
    desenho.text((x + 2, y + 2), MARCA, fill="black", font_size=tamanho_letra)  # sombra
    desenho.text((x, y), MARCA, fill="white", font_size=tamanho_letra)
    # Data + nome original: nunca repete, e rodar de novo só refaz o mesmo arquivo
    destino = DESTINO / f"{quando:%Y-%m-%d_%H%M%S}_{arquivo.stem}.jpg"
    foto.save(destino, quality=85, optimize=True)
    return destino, foto.size


def main() -> None:
    DESTINO.mkdir(parents=True, exist_ok=True)
    total_antes = total_depois = 0
    for arquivo in sorted(ORIGEM.iterdir()):
        if arquivo.suffix.lower() not in EXTENSOES:
            continue
        destino, tamanho = preparar(arquivo)
        antes, depois = arquivo.stat().st_size, destino.stat().st_size
        total_antes, total_depois = total_antes + antes, total_depois + depois
        print(f"{arquivo.name:16} -> {destino.name:24} {tamanho[0]}x{tamanho[1]}  "
              f"{antes / 1024:6.0f} KB -> {depois / 1024:4.0f} KB")
    print(f"\nTotal: {total_antes / 1024:.0f} KB -> {total_depois / 1024:.0f} KB")


if __name__ == "__main__":
    main()
```

```text
IMG_0101.jpg     -> 2026-09-12_140510_IMG_0101.jpg 1600x1067     140 KB ->   33 KB
IMG_0102.jpg     -> 2026-09-12_140742_IMG_0102.jpg 1600x1067     142 KB ->   33 KB
IMG_0103.jpg     -> 2026-09-13_093000_IMG_0103.jpg 1600x1067     143 KB ->   34 KB
IMG_0104.jpg     -> 2026-11-08_172740_IMG_0104.jpg 1600x1067     144 KB ->   34 KB
print_tela.png   -> 2026-11-08_172741_print_tela.jpg 1600x1067      48 KB ->   46 KB

Total: 617 KB -> 181 KB
```

### O que cada parte resolve

**A data verdadeira (EXIF).** Câmeras e celulares gravam, **dentro** da foto, os dados **EXIF**: modelo do aparelho, configurações e a data e hora em que a foto foi **tirada** (`DateTimeOriginal`). Ela não muda quando você copia o arquivo, ao contrário da data de modificação. O código `0x8769` é a "gaveta" de dados da câmera dentro do EXIF, e `0x9003` é o campo da data. A `IMG_0104.jpg` (foto editada, sem EXIF) e o PNG (prints não têm EXIF) caem no plano B: a data de modificação.

**Fotos "deitadas".** O celular grava a foto sempre na mesma posição e anota no EXIF como ela deve ser girada. Alguns programas ignoram essa anotação, e a foto aparece de lado. O `ImageOps.exif_transpose()` gira de verdade.

**Transparência.** JPG não tem transparência. Um simples `convert("RGB")` num PNG transparente pode deixar o fundo **preto**. O script cria um fundo **branco** e cola a imagem por cima, usando a transparência como **máscara** (`getchannel("A")`): o transparente vira branco.

**Marca-d'água legível.** O texto é escrito duas vezes: em preto, deslocado 2 pixels (a **sombra**), e em branco por cima. Assim ele aparece sobre fundos claros e escuros. O tamanho da letra acompanha a largura da foto (`foto.width // 40`).

**Rodar de novo não duplica.** O nome de saída junta a data e o nome original (`2026-09-12_140510_IMG_0101.jpg`): é sempre o mesmo para a mesma foto. Rodando de novo, o arquivo da pasta `saida` é **refeito**, não duplicado. Aqui, substituir não é problema: os originais nunca são tocados, e a saída pode ser recriada a qualquer momento.

!!! warning "Fotos têm dados pessoais"
    O EXIF de fotos de celular pode guardar também a **localização** (GPS) de onde a foto foi tirada. Ao reduzir e salvar sem passar o `exif=` no `save()`, como neste script, esses dados **não** vão para a cópia: é um jeito simples de não espalhar a localização de casa ao postar. E lembre: foto de pessoas é dado pessoal ([Segurança digital](../../seguranca_digital/modulo_04_cidadania_e_direitos/03_lgpd_no_dia_a_dia.md)).

---

## ⚠️ Erros comuns

- **`OSError: cannot write mode RGBA as JPEG`**: tentou salvar PNG transparente como JPG sem converter.
- **Fundo preto** depois de converter: use o fundo branco com máscara, como no script.
- **Foto de lado**: faltou o `ImageOps.exif_transpose()`.
- **`PIL.UnidentifiedImageError`**: o arquivo não é uma imagem que o Pillow conhece (ou está corrompido). Filtre pelas extensões e use `try`/`except` se a pasta for bagunçada.
- **Usar `resize()` e distorcer** a foto: para reduzir, use `thumbnail()`; para um tamanho exato, `ImageOps.fit()`.

---

## Exercícios

### Básico (fixação)

Mostre o **nome**, o **tamanho** (largura × altura) e o **modo de cor** de cada imagem da pasta `treino_docs/fotos`.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```python
    from pathlib import Path

    from PIL import Image

    for arquivo in sorted(Path("treino_docs", "fotos").iterdir()):
        with Image.open(arquivo) as foto:
            print(f"{arquivo.name:16} {foto.width}x{foto.height}  {foto.mode}")
    ```

    As JPG aparecem como `RGB`; o `print_tela.png`, como `RGBA` (o A é o canal de transparência).

### Intermediário (aplicação)

Liste as fotos mostrando a **data EXIF** de cada uma ou, se não houver, a mensagem `sem data EXIF`.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```python
    from datetime import datetime
    from pathlib import Path

    from PIL import Image

    sem_data = []
    for arquivo in sorted(Path("treino_docs", "fotos").iterdir()):
        with Image.open(arquivo) as foto:
            texto = foto.getexif().get_ifd(0x8769).get(0x9003)
        if texto:
            quando = datetime.strptime(texto, "%Y:%m:%d %H:%M:%S")
            print(f"{arquivo.name:16} {quando:%d/%m/%Y %H:%M}")
        else:
            sem_data.append(arquivo.name)
            print(f"{arquivo.name:16} sem data EXIF")
    ```

    Três fotos têm data (12 e 13/09/2026); `IMG_0104.jpg` e `print_tela.png`, não. Repare que o EXIF guarda a data com dois-pontos (`2026:09:12`), por isso o formato do `strptime` é `%Y:%m:%d`.

### Avançado (desafio)

Gere uma **miniatura quadrada** de 300 × 300 pixels de cada foto (para usar como foto de perfil ou num crachá), recortada no centro, em `treino_docs/saida/miniaturas/`, sempre em JPG.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```python
    from pathlib import Path

    from PIL import Image, ImageOps

    destino = Path("treino_docs") / "saida" / "miniaturas"
    destino.mkdir(parents=True, exist_ok=True)

    for arquivo in sorted(Path("treino_docs", "fotos").iterdir()):
        with Image.open(arquivo) as foto:
            quadrada = ImageOps.fit(ImageOps.exif_transpose(foto), (300, 300))
        if quadrada.mode != "RGB":
            fundo = Image.new("RGB", quadrada.size, "white")
            fundo.paste(quadrada, mask=quadrada.convert("RGBA").getchannel("A"))
            quadrada = fundo
        quadrada.save(destino / f"{arquivo.stem}.jpg", quality=85)
        print(f"{arquivo.name} -> {arquivo.stem}.jpg")
    ```

    O `ImageOps.fit()` corta as sobras dos lados (a foto é mais larga que alta) e reduz, sem distorcer. O tratamento da transparência é o mesmo do script da aula.

---

## 💡 Resumo

- `Image.open()` (com `with`), `thumbnail()` para reduzir, `ImageOps.fit()` para tamanho exato, `save(quality=85)`.
- PNG transparente ➔ JPG: fundo **branco** + `paste` com a **máscara** da transparência.
- **EXIF** guarda a data em que a foto foi tirada (`get_ifd(0x8769).get(0x9003)`); `exif_transpose()` endireita a foto.
- Saída com nome **determinado** (data + nome original): rodar de novo refaz, não duplica.
- Salvar sem o `exif=` remove os dados da câmera, inclusive a localização.

## ➡️ Próximo passo

**[04 — Certificados e crachás em lote](04_certificados_e_crachas.md)**.
