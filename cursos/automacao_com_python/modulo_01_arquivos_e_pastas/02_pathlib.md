# 02 — Caminhos e listas de arquivos com `pathlib`

> **Curso:** Automação com Python  
> **Módulo:** 01 — Arquivos e pastas  
> **Tempo estimado:** 1 h 30 min  

---

## 🎯 Objetivos

Ao final desta aula, você será capaz de:

- Representar pastas e arquivos com `Path` e juntar caminhos com `/`.
- Listar o conteúdo de uma pasta com `iterdir()` e procurar arquivos com `glob()` e `rglob()`.
- Ler o **nome**, a **extensão**, o **tamanho** e a **data** de um arquivo.
- Fazer um **resumo** de uma pasta: quantos arquivos de cada tipo e quanto espaço ocupam.

## Pré-requisitos

- [Aula 01](01_o_que_vale_automatizar.md): a pasta `treino` criada com o `criar_treino.py`.

!!! info "Esta aula só lê"
    Nenhum script desta aula muda arquivos: eles só **olham**. Pode rodar à vontade.

---

## `Path`: um caminho que o Python entende

O módulo `pathlib` (já vem com o Python) tem a classe `Path`, que representa um caminho de pasta ou de arquivo.

```python
from pathlib import Path

pasta = Path("treino") / "Downloads"
arquivo = pasta / "boletim_2026_1bim.pdf"

print(arquivo)            # treino\Downloads\boletim_2026_1bim.pdf
print(arquivo.name)       # boletim_2026_1bim.pdf
print(arquivo.stem)       # boletim_2026_1bim
print(arquivo.suffix)     # .pdf
print(arquivo.parent)     # treino\Downloads
print(arquivo.exists())   # True
print(arquivo.is_file())  # True
print(pasta.is_dir())     # True
```

| Atributo / método | O que devolve |
|---|---|
| `/` | Junta partes do caminho (funciona no Windows, no Linux e no Mac) |
| `.name` | Nome com extensão |
| `.stem` | Nome sem extensão |
| `.suffix` | Extensão, com o ponto (`.pdf`). Arquivo sem extensão: `""` |
| `.parent` | A pasta onde o arquivo está |
| `.exists()`, `.is_file()`, `.is_dir()` | Se existe, se é arquivo, se é pasta |
| `.resolve()` | O caminho completo (absoluto), a partir do disco |

!!! tip "Esqueça as barras invertidas"
    No Windows, caminhos usam `\`, que dentro de textos Python tem significado especial (`"\n"` é quebra de linha!). Com `Path` e `/`, você nunca precisa digitar `\`.

## Listando uma pasta: `iterdir()`

```python title="listar.py"
from pathlib import Path

pasta = Path("treino") / "Downloads"

for arquivo in sorted(pasta.iterdir()):
    if arquivo.is_file():
        tamanho_kb = arquivo.stat().st_size / 1024
        print(f"{arquivo.name:32} {arquivo.suffix:6} {tamanho_kb:8.1f} KB")
```

```text
anotacoes.txt                    .txt      191.4 KB
apresentacao_ciencias.pptx       .pptx     118.2 KB
boletim_2026_1bim.pdf            .pdf        1.0 KB
certificado_canva.pdf            .pdf      219.7 KB
...
sem_extensao                               250.0 KB
trabalho_historia.docx           .docx       3.9 KB
video_formatura.mp4              .mp4       47.9 KB
```

- `iterdir()` devolve **tudo** o que está dentro da pasta (arquivos e subpastas), sem ordem garantida; o `sorted()` organiza por nome.
- `arquivo.stat()` traz as informações do arquivo; `st_size` é o tamanho em **bytes** (÷ 1024 = KB; ÷ 1024 de novo = MB).
- `{arquivo.name:32}` reserva 32 espaços para o nome, deixando as colunas alinhadas.

!!! info "Maiúsculas e minúsculas no Windows"
    No Windows, `sorted()` com caminhos ignora maiúsculas (por isso `IMG_0042.JPG` aparece no meio da lista) e o sistema trata `foto.JPG` e `foto.jpg` como o **mesmo** nome. Para comparar extensões, use sempre `.suffix.lower()`.

## Procurando arquivos: `glob()` e `rglob()`

`glob()` procura por um **padrão** dentro da pasta; `rglob()` procura também em **todas as subpastas**.

```python title="procurar_pdfs.py"
from pathlib import Path

pasta = Path("treino")
for pdf in sorted(pasta.rglob("*.pdf")):
    print(pdf)
```

```text
treino\Downloads\boletim_2026_1bim.pdf
treino\Downloads\certificado_canva.pdf
treino\Downloads\contrato_estagio.pdf
```

| Padrão | Encontra |
|---|---|
| `"*.pdf"` | Todos os arquivos terminados em `.pdf` |
| `"IMG_*"` | Tudo o que começa com `IMG_` |
| `"*2026*"` | Tudo que tem `2026` no nome |
| `"*"` | Tudo |

## Datas dos arquivos

O `stat()` também guarda a **data da última modificação** (`st_mtime`), como um número de segundos. O `datetime.fromtimestamp()` transforma em data e hora:

```python title="datas_das_fotos.py"
from datetime import datetime
from pathlib import Path

for foto in sorted(Path("treino", "Fotos").iterdir()):
    momento = datetime.fromtimestamp(foto.stat().st_mtime)
    print(f"{foto.name:32} {momento:%d/%m/%Y %H:%M}")
```

```text
DSC_1234.JPG                     20/05/2026 08:00
foto.png                         01/06/2026 12:30
IMG_0001.jpg                     14/03/2026 09:12
IMG_0002.jpg                     14/03/2026 09:12
IMG_0003.jpg                     15/03/2026 17:40
WhatsApp Image 2026-04-02.jpeg   02/04/2026 20:03
```

O `:%d/%m/%Y %H:%M` dentro da f-string é o **formato** da data: dia/mês/ano hora:minuto.

!!! warning "Data de modificação não é sempre a data da foto"
    Ao copiar ou baixar um arquivo, a data de modificação pode mudar. Para fotos de verdade, a data **em que a foto foi tirada** fica guardada dentro da imagem (nos dados EXIF), e o Módulo 03 mostra como ler. Aqui, a data de modificação basta para aprender.

## Resumo de uma pasta

Juntando tudo: quantos arquivos de cada tipo e quanto espaço ocupam. O `Counter` (do módulo `collections`) conta repetições.

```python title="resumo_pasta.py"
from collections import Counter
from pathlib import Path

pasta = Path("treino") / "Downloads"
arquivos = [a for a in pasta.iterdir() if a.is_file()]

tipos = Counter(a.suffix.lower() or "(sem extensão)" for a in arquivos)
total_mb = sum(a.stat().st_size for a in arquivos) / 1024 / 1024

print(f"{len(arquivos)} arquivos, {total_mb:.1f} MB no total")
for extensao, quantidade in tipos.most_common():
    print(f"  {extensao:15} {quantidade}")
```

```text
16 arquivos, 1.4 MB no total
  .pdf            3
  .txt            2
  .jpg            2
  .pptx           1
  ...
```

Repare em `a.suffix.lower() or "(sem extensão)"`: se a extensão for vazia (`""`), o `or` usa o texto da direita.

---

## ⚠️ Erros comuns

- **`FileNotFoundError: ... 'treino\\Downloads'`**: a pasta não existe **a partir de onde o terminal está**. Confira com `print(Path("treino").resolve())` e rode `criar_treino.py` se preciso.
- **`NotADirectoryError`** ao usar `iterdir()`: o caminho é de um arquivo, não de uma pasta.
- **Comparar `.suffix == ".jpg"`** e não achar `IMG_0042.JPG`: use `.suffix.lower()`.
- **Esquecer os parênteses**: `arquivo.is_file` (sem `()`) é sempre "verdadeiro", porque é o método, não o resultado.

---

## Exercícios

### Básico (fixação)

Escreva um script que mostre o nome de todos os arquivos `.txt` da pasta `treino/Downloads`, usando `glob()`.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```python
    from pathlib import Path

    for arquivo in sorted(Path("treino", "Downloads").glob("*.txt")):
        print(arquivo.name)
    ```

    Saída: `anotacoes.txt` e `lista_compras.txt`.

### Intermediário (aplicação)

Mostre os **3 maiores arquivos** de toda a pasta `treino` (incluindo subpastas), do maior para o menor, com o tamanho em KB.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```python
    from pathlib import Path

    arquivos = [a for a in Path("treino").rglob("*") if a.is_file()]
    maiores = sorted(arquivos, key=lambda a: a.stat().st_size, reverse=True)[:3]

    for arquivo in maiores:
        print(f"{arquivo.name:32} {arquivo.stat().st_size / 1024:8.1f} KB")
    ```

    `key=lambda a: a.stat().st_size` diz ao `sorted()` para ordenar pelo tamanho; `reverse=True` põe o maior primeiro; `[:3]` pega os três primeiros. Saída: `sem_extensao` (250,0 KB), `certificado_canva.pdf` (219,7 KB) e `anotacoes.txt` (191,4 KB).

### Avançado (desafio)

Para a pasta `treino/Downloads`, mostre **quanto espaço cada extensão ocupa** (em KB), da que ocupa mais para a que ocupa menos. Arquivos sem extensão entram como `(sem extensão)`.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```python
    from collections import defaultdict
    from pathlib import Path

    espaco = defaultdict(int)
    for arquivo in Path("treino", "Downloads").iterdir():
        if arquivo.is_file():
            espaco[arquivo.suffix.lower() or "(sem extensão)"] += arquivo.stat().st_size

    for extensao, total in sorted(espaco.items(), key=lambda par: par[1], reverse=True):
        print(f"{extensao:15} {total / 1024:8.1f} KB")
    ```

    O `defaultdict(int)` começa cada extensão com 0, então dá para somar direto com `+=`. Os `.pdf` (três arquivos) e os `.txt` (dois) ficam no topo, junto com o arquivo `(sem extensão)`.

---

## 💡 Resumo

- `Path` representa caminhos; `/` junta partes; `.name`, `.stem`, `.suffix`, `.parent` separam as partes.
- `iterdir()` lista uma pasta; `glob()` procura por padrão; `rglob()` procura também nas subpastas.
- `stat().st_size` é o tamanho em bytes; `datetime.fromtimestamp(stat().st_mtime)` é a data de modificação.
- Compare extensões com `.suffix.lower()`.

## ➡️ Próximo passo

**[03 — Criar, copiar, mover e renomear com segurança](03_mover_copiar_com_seguranca.md)**: agora os scripts vão **mexer** nos arquivos, com simulação e sem sobrescrever nada.
