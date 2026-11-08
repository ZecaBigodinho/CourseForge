# 03 — Criar, copiar, mover e renomear com segurança

> **Curso:** Automação com Python  
> **Módulo:** 01 — Arquivos e pastas  
> **Tempo estimado:** 1 h 30 min  

---

## 🎯 Objetivos

Ao final desta aula, você será capaz de:

- Criar pastas com `mkdir()`.
- Copiar com `shutil.copy2()`, mover com `shutil.move()` e renomear com `rename()`.
- Saber **quando** cada comando **sobrescreve** um arquivo (e evitar isso).
- Escrever a função `destino_livre()`, que nunca deixa um arquivo apagar outro.
- Usar o **modo de simulação** antes de mexer em qualquer coisa.

## Pré-requisitos

- [Aula 02](02_pathlib.md): `Path`, `iterdir()` e `glob()`.

!!! warning "A partir daqui, os scripts mexem em arquivos"
    Rode tudo na pasta `treino`. Se algo der errado, apague a `treino` e rode o `criar_treino.py` de novo ([aula 01](01_o_que_vale_automatizar.md#a-pasta-de-treino)).

---

## Os quatro comandos

```python title="operacoes.py"
import shutil
from pathlib import Path

base = Path("treino")

# Criar pastas (parents: cria as do meio; exist_ok: não reclama se já existir)
copias = base / "Copias" / "2026"
copias.mkdir(parents=True, exist_ok=True)

# Copiar (o original continua lá; copy2 preserva a data do arquivo)
shutil.copy2(base / "Downloads" / "anotacoes.txt", copias / "anotacoes.txt")

# Renomear (dentro da mesma pasta)
(copias / "anotacoes.txt").rename(copias / "anotacoes_copia.txt")

# Mover (para outra pasta)
shutil.move(copias / "anotacoes_copia.txt", base / "anotacoes_copia.txt")

print(sorted(p.name for p in base.iterdir()))
```

```text
['Copias', 'Downloads', 'Fotos', 'anotacoes_copia.txt']
```

| Comando | Faz | Se o destino **já existe**... |
|---|---|---|
| `pasta.mkdir(parents=True, exist_ok=True)` | Cria a pasta (e as do meio) | Não faz nada (com `exist_ok=True`) |
| `shutil.copy2(origem, destino)` | Copia, mantendo a data | ⚠️ **Sobrescreve** o arquivo que estava lá |
| `shutil.move(origem, destino)` | Move (ou renomeia, até entre discos) | ⚠️ **Sobrescreve** o arquivo que estava lá |
| `origem.rename(destino)` | Renomeia / move no mesmo disco | No Windows, dá erro `FileExistsError` |

!!! danger "Sobrescrever é apagar sem avisar"
    Testamos aqui: com um arquivo `x_b.txt` já existente, `shutil.move("x_a.txt", "x_b.txt")` **trocou o conteúdo** do `x_b.txt` pelo do `x_a.txt`, sem nenhuma mensagem. O arquivo antigo sumiu. Em pastas como Downloads, nomes repetidos (`documento.pdf`, `foto.jpg`) são muito comuns. Por isso, **antes de mover ou copiar, confira se o destino está livre**.

## `destino_livre()`: nunca apagar por acidente

A ideia é a mesma do Windows quando você baixa um arquivo duas vezes: `arquivo.pdf`, `arquivo (2).pdf`, `arquivo (3).pdf`...

```python title="destino_livre.py"
from pathlib import Path


def destino_livre(destino: Path) -> Path:
    """Devolve um caminho que ainda não existe: arquivo.pdf, arquivo (2).pdf, arquivo (3).pdf..."""
    if not destino.exists():
        return destino
    n = 2
    while True:
        candidato = destino.with_name(f"{destino.stem} ({n}){destino.suffix}")
        if not candidato.exists():
            return candidato
        n += 1


teste = Path("treino") / "Downloads" / "anotacoes.txt"
print(destino_livre(teste).name)
print(destino_livre(teste.with_name("novo.txt")).name)
```

```text
anotacoes (2).txt
novo.txt
```

- `with_name()` troca só o nome, mantendo a pasta.
- O `while True` testa `(2)`, `(3)`, `(4)`... até achar um nome que não existe.

## O modo de simulação

Todo script que mexe em arquivos começa com uma constante `SIMULAR`. Com `True`, ele só **mostra** o que faria. Você confere a lista, muda para `False` e roda de novo.

```python title="mover_pdfs.py"
import shutil
from pathlib import Path

SIMULAR = True  # True: só mostra o que faria. False: faz de verdade.

origem = Path("treino") / "Downloads"
destino = Path("treino") / "PDFs"


def destino_livre(caminho: Path) -> Path:
    if not caminho.exists():
        return caminho
    n = 2
    while (candidato := caminho.with_name(f"{caminho.stem} ({n}){caminho.suffix}")).exists():
        n += 1
    return candidato


for arquivo in sorted(origem.glob("*.pdf")):
    alvo = destino_livre(destino / arquivo.name)
    if SIMULAR:
        print(f"[simulação] {arquivo} -> {alvo}")
    else:
        destino.mkdir(exist_ok=True)
        shutil.move(arquivo, alvo)
        print(f"movido: {arquivo.name} -> {alvo}")
```

Com `SIMULAR = True`:

```text
[simulação] treino\Downloads\boletim_2026_1bim.pdf -> treino\PDFs\boletim_2026_1bim.pdf
[simulação] treino\Downloads\certificado_canva.pdf -> treino\PDFs\certificado_canva.pdf
[simulação] treino\Downloads\contrato_estagio.pdf -> treino\PDFs\contrato_estagio.pdf
```

Com `SIMULAR = False`:

```text
movido: boletim_2026_1bim.pdf -> treino\PDFs\boletim_2026_1bim.pdf
movido: certificado_canva.pdf -> treino\PDFs\certificado_canva.pdf
movido: contrato_estagio.pdf -> treino\PDFs\contrato_estagio.pdf
```

!!! info "O operador `:=` (morsa)"
    `while (candidato := ...).exists():` **calcula** o candidato, **guarda** na variável e **testa**, tudo na mesma linha. É uma versão curta do `while True` da função anterior. As duas formas funcionam; use a que achar mais clara.

!!! tip "Repare: a pasta só é criada quando é de verdade"
    O `destino.mkdir()` fica dentro do `else`. Na simulação, nada é criado, nem a pasta.

## E apagar?

Este curso **não apaga** arquivos ([regra 3](01_o_que_vale_automatizar.md#as-regras-de-seguranca)). Quando quiser "limpar" algo, **mova** para uma pasta `_revisar` e apague você mesmo, depois de conferir. Comandos como `Path.unlink()` e `shutil.rmtree()` apagam **sem passar pela Lixeira**: não há como recuperar.

---

## ⚠️ Erros comuns

- **`FileNotFoundError` no `copy2` ou no `move`**: a pasta de **destino** não existe. Crie antes com `mkdir(parents=True, exist_ok=True)`.
- **`FileExistsError` no `rename`**: já existe um arquivo com o nome novo. Use `destino_livre()`.
- **Mover sem conferir e sobrescrever arquivos**: `shutil.move` e `copy2` não avisam.
- **Esquecer de voltar `SIMULAR = True`** depois de testar. Deixe o padrão sempre em simulação.
- **Rodar o script duas vezes** e mover o que já tinha sido movido: pense no que acontece na segunda vez (a [aula 04](04_renomear_fotos_pela_data.md) trata disso).

---

## Exercícios

### Básico (fixação)

Crie a pasta `treino/Backup` e **copie** para ela todos os arquivos `.docx` e `.xlsx` da `treino/Downloads` (os originais continuam onde estão).

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```python
    import shutil
    from pathlib import Path

    origem = Path("treino") / "Downloads"
    backup = Path("treino") / "Backup"
    backup.mkdir(exist_ok=True)

    for arquivo in origem.iterdir():
        if arquivo.suffix.lower() in {".docx", ".xlsx"}:
            shutil.copy2(arquivo, backup / arquivo.name)
            print(f"copiado: {arquivo.name}")
    ```

    Saída: `copiado: planilha_gastos.xlsx` e `copiado: trabalho_historia.docx` (a ordem pode variar). Como a `Backup` estava vazia, não havia risco de sobrescrever; numa pasta com arquivos, use `destino_livre()`.

### Intermediário (aplicação)

Faça um script com `SIMULAR` que **mova** todas as imagens (`.jpg`, `.jpeg`, `.png`, maiúsculas ou minúsculas) da `treino/Downloads` para `treino/Imagens`, sem nunca sobrescrever. Rode primeiro simulando e depois de verdade.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```python
    import shutil
    from pathlib import Path

    SIMULAR = True
    IMAGENS = {".jpg", ".jpeg", ".png"}

    origem = Path("treino") / "Downloads"
    destino = Path("treino") / "Imagens"


    def destino_livre(caminho: Path) -> Path:
        if not caminho.exists():
            return caminho
        n = 2
        while (candidato := caminho.with_name(f"{caminho.stem} ({n}){caminho.suffix}")).exists():
            n += 1
        return candidato


    for arquivo in sorted(origem.iterdir()):
        if arquivo.is_file() and arquivo.suffix.lower() in IMAGENS:
            alvo = destino_livre(destino / arquivo.name)
            if SIMULAR:
                print(f"[simulação] {arquivo.name} -> {alvo}")
            else:
                destino.mkdir(exist_ok=True)
                shutil.move(arquivo, alvo)
                print(f"movido: {arquivo.name} -> {alvo}")
    ```

    Vão para `Imagens`: `foto_festa.jpg`, `IMG_0042.JPG` e `meme.png`. O `.lower()` garante que o `.JPG` maiúsculo também entre.

### Avançado (desafio)

Escreva a função `mandar_para_revisar(arquivo)`, que **move** o arquivo para `treino/_revisar/AAAA-MM-DD/` (a data de **hoje**), sem sobrescrever, e devolve o caminho novo. Use-a para "limpar" os instaladores (`.exe`) da `treino/Downloads`.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```python
    import shutil
    from datetime import date
    from pathlib import Path

    REVISAR = Path("treino") / "_revisar"


    def destino_livre(caminho: Path) -> Path:
        if not caminho.exists():
            return caminho
        n = 2
        while (candidato := caminho.with_name(f"{caminho.stem} ({n}){caminho.suffix}")).exists():
            n += 1
        return candidato


    def mandar_para_revisar(arquivo: Path) -> Path:
        pasta = REVISAR / f"{date.today():%Y-%m-%d}"
        pasta.mkdir(parents=True, exist_ok=True)
        alvo = destino_livre(pasta / arquivo.name)
        shutil.move(arquivo, alvo)
        return alvo


    for exe in Path("treino", "Downloads").glob("*.exe"):
        print(f"para revisar: {mandar_para_revisar(exe)}")
    ```

    A pasta do dia guarda o que foi "limpo" em cada data. Depois de alguns dias sem sentir falta de nada, você apaga a pasta à mão. Para a versão final, acrescente o `SIMULAR`, como no intermediário.

---

## 💡 Resumo

- `mkdir(parents=True, exist_ok=True)` cria pastas; `copy2` copia; `move` move; `rename` renomeia.
- `copy2` e `move` **sobrescrevem sem avisar**; `rename` dá erro no Windows. Use **`destino_livre()`**.
- Comece todo script com **`SIMULAR = True`**, confira a lista e só então rode de verdade.
- Não apague: **mova** para `_revisar`.

## ➡️ Próximo passo

**[04 — Renomear fotos em lote pela data](04_renomear_fotos_pela_data.md)**: um script completo, e o que o teste dele revelou.
