# 04 — Renomear fotos em lote pela data

> **Curso:** Automação com Python  
> **Módulo:** 01 — Arquivos e pastas  
> **Tempo estimado:** 1 h 30 min  

---

## 🎯 Objetivos

Ao final desta aula, você será capaz de:

- Renomear dezenas de fotos com um padrão que **ordena por data**: `2026-03-14_091205.jpg`.
- Tratar **fotos com a mesma data e hora** sem perder nenhuma.
- Fazer uma simulação que mostra **exatamente** o que vai acontecer.
- Escrever um script que pode ser rodado **duas vezes** sem estragar nada.

## Pré-requisitos

- [Aula 03](03_mover_copiar_com_seguranca.md): `rename()`, `destino_livre()` e `SIMULAR`.

---

## Por que renomear pela data

Fotos chegam com nomes que não dizem nada e não se misturam bem: `IMG_0001.jpg` (celular), `DSC_1234.JPG` (câmera), `WhatsApp Image 2026-04-02.jpeg`. Com o nome no formato **ano-mês-dia_horaminutosegundo**, qualquer pasta fica em **ordem cronológica** só por ordenar pelo nome:

```text
2026-03-14_091205.jpg
2026-03-15_174031.jpg
2026-04-02_200344.jpeg
```

!!! info "Por que ano primeiro?"
    `14-03-2026` e `02-04-2026`, em ordem alfabética, ficam na ordem errada (o `02` vem antes do `14`, mesmo sendo um mês depois). Com o ano na frente, a ordem alfabética **é** a ordem do tempo. É o formato internacional **ISO 8601**.

## A primeira versão (e o que o teste mostrou)

A primeira versão deste script fazia o óbvio: para cada foto, calcular o nome pela data e usar `destino_livre()` da aula 03 para não sobrescrever. Testando na pasta de treino, apareceram **dois problemas**:

**Problema 1 — A simulação mentia.** As fotos `IMG_0001.jpg` e `IMG_0002.jpg` têm a **mesma** data e hora (fotos tiradas no mesmo segundo, ou em sequência). Na simulação, o script mostrou:

```text
[simulação] IMG_0001.jpg                     -> 2026-03-14_091205.jpg
[simulação] IMG_0002.jpg                     -> 2026-03-14_091205.jpg
```

Duas fotos com o **mesmo** nome final! Na hora de verdade, o `destino_livre()` percebia que o primeiro nome já existia e usava `_2`. Mas a simulação não sabia disso, porque na simulação **nada é renomeado**, então o primeiro nome "ainda não existe". Uma simulação que mostra algo diferente do que vai acontecer não serve para conferir.

**Problema 2 — Rodar de novo estragava.** Rodando o script uma segunda vez:

```text
2026-03-14_091205_2.jpg          -> 2026-03-14_091205_3.jpg
```

A foto `_2` "não estava no padrão" (o nome não era igual a `2026-03-14_091205`), então o script renomeou de novo, para `_3`. A cada execução, o número subiria.

!!! tip "Lição: teste o caso estranho e teste duas vezes"
    Os dois problemas só apareceram porque a pasta de treino tem, **de propósito**, duas fotos com a mesma hora, e porque o script foi rodado **duas vezes**. Sempre teste: (1) o caso repetido, (2) a simulação contra o resultado real e (3) rodar de novo.

## A versão corrigida

Duas mudanças:

1. Um conjunto `ocupados` guarda os nomes que **já existem** e os que **já foram planejados**. A simulação passa a "reservar" os nomes, igual à execução real.
2. A função `ja_no_padrao()` aceita tanto `2026-03-14_091205` quanto `2026-03-14_091205_2`, com uma **expressão regular** (`re`).

```python title="renomear_fotos.py"
"""Renomeia as fotos de uma pasta pela data: 2026-03-14_091205.jpg"""
import re
from datetime import datetime
from pathlib import Path

PASTA = Path("treino") / "Fotos"
EXTENSOES = {".jpg", ".jpeg", ".png", ".heic"}
SIMULAR = True


def nome_pela_data(foto: Path) -> str:
    """A data e a hora da foto no formato 2026-03-14_091205 (sem a extensão)."""
    momento = datetime.fromtimestamp(foto.stat().st_mtime)
    return f"{momento:%Y-%m-%d_%H%M%S}"


def ja_no_padrao(foto: Path) -> bool:
    """True para 2026-03-14_091205.jpg e também para 2026-03-14_091205_2.jpg."""
    return re.fullmatch(re.escape(nome_pela_data(foto)) + r"(_\d+)?", foto.stem) is not None


def main() -> None:
    fotos = sorted(f for f in PASTA.iterdir() if f.is_file() and f.suffix.lower() in EXTENSOES)
    ocupados = {f.name.lower() for f in PASTA.iterdir()}  # nomes que já existem ou já foram planejados
    renomeadas = 0
    for foto in fotos:
        if ja_no_padrao(foto):
            continue
        base, extensao = nome_pela_data(foto), foto.suffix.lower()
        novo, n = f"{base}{extensao}", 2
        while novo.lower() in ocupados:
            novo, n = f"{base}_{n}{extensao}", n + 1
        ocupados.add(novo.lower())
        if SIMULAR:
            print(f"[simulação] {foto.name:32} -> {novo}")
        else:
            foto.rename(foto.with_name(novo))
            print(f"{foto.name:32} -> {novo}")
        renomeadas += 1
    acao = "seriam renomeadas" if SIMULAR else "renomeadas"
    print(f"\n{renomeadas} de {len(fotos)} fotos {acao}.")


if __name__ == "__main__":
    main()
```

Simulando (`SIMULAR = True`):

```text
[simulação] DSC_1234.JPG                     -> 2026-05-20_080000.jpg
[simulação] foto.png                         -> 2026-06-01_123000.png
[simulação] IMG_0001.jpg                     -> 2026-03-14_091205.jpg
[simulação] IMG_0002.jpg                     -> 2026-03-14_091205_2.jpg
[simulação] IMG_0003.jpg                     -> 2026-03-15_174031.jpg
[simulação] WhatsApp Image 2026-04-02.jpeg   -> 2026-04-02_200344.jpeg

6 de 6 fotos seriam renomeadas.
```

Agora a simulação mostra o `_2`. Com `SIMULAR = False`, o resultado real é **igual** ao simulado. E rodando de novo:

```text
0 de 6 fotos renomeadas.
```

### Entendendo as partes novas

- **`{momento:%Y-%m-%d_%H%M%S}`**: `%Y` ano com 4 dígitos, `%m` mês, `%d` dia, `%H` hora (0–23), `%M` minuto, `%S` segundo.
- **`.lower()` nos nomes:** no Windows, `Foto.JPG` e `foto.jpg` são o mesmo arquivo. Comparar em minúsculas evita "achar" que um nome está livre quando não está. A extensão nova também fica minúscula (`.JPG` vira `.jpg`).
- **`re.fullmatch(padrão, texto)`:** confere se o texto **inteiro** segue o padrão. `re.escape()` protege os caracteres do nome; `(_\d+)?` quer dizer "opcionalmente, um `_` seguido de um ou mais dígitos".
- **`novo, n = f"{base}_{n}{extensao}", n + 1`:** atualiza as duas variáveis na mesma linha.

!!! warning "Não use dois-pontos no nome"
    `09:12:05` não pode ser nome de arquivo no Windows: os caracteres `\ / : * ? " < > |` são proibidos. Por isso a hora fica `091205`.

---

## ⚠️ Erros comuns

- **Simulação que não "reserva" os nomes**: mostra uma coisa e faz outra (problema 1).
- **Script que não reconhece o próprio resultado**: renomeia de novo a cada execução (problema 2).
- **`OSError: [WinError 123] A sintaxe do nome do arquivo... está incorreta`**: há um caractere proibido no nome novo (geralmente `:` da hora).
- **Confiar na data de modificação** de fotos copiadas ou baixadas: ela pode ser a data da cópia. Para fotos de câmera e celular, o Módulo 03 lê a data verdadeira (EXIF).

---

## Exercícios

### Básico (fixação)

Escreva um script **só de simulação** que mostre como ficariam os nomes das fotos da `treino/Fotos` no formato `2026-03-14 09h12.jpg` (data, espaço, hora com `h`). Não precisa tratar repetidos.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```python
    from datetime import datetime
    from pathlib import Path

    for foto in sorted(Path("treino", "Fotos").iterdir()):
        momento = datetime.fromtimestamp(foto.stat().st_mtime)
        novo = f"{momento:%Y-%m-%d %Hh%M}{foto.suffix.lower()}"
        print(f"{foto.name:32} -> {novo}")
    ```

    Saída, por exemplo: `IMG_0003.jpg -> 2026-03-15 17h40.jpg`. Repare que `IMG_0001` e `IMG_0002` dariam o **mesmo** nome: para renomear de verdade, seria preciso o tratamento de repetidos da aula.

### Intermediário (aplicação)

Sem renomear nada, mostre **quantas fotos há em cada mês** na `treino/Fotos`, no formato `2026-03: 3 fotos`, em ordem.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```python
    from collections import Counter
    from datetime import datetime
    from pathlib import Path

    meses = Counter()
    for foto in Path("treino", "Fotos").iterdir():
        if foto.is_file():
            meses[f"{datetime.fromtimestamp(foto.stat().st_mtime):%Y-%m}"] += 1

    for mes, quantidade in sorted(meses.items()):
        print(f"{mes}: {quantidade} fotos")
    ```

    Saída: `2026-03: 3 fotos`, `2026-04: 1 fotos`, `2026-05: 1 fotos`, `2026-06: 1 fotos`. (Para escrever "1 foto" no singular, use `"foto" if quantidade == 1 else "fotos"`.)

### Avançado (desafio)

Em vez de renomear, **organize** as fotos em subpastas por **ano** e **mês**: `treino/Fotos/2026/03/IMG_0001.jpg`. Use `SIMULAR`, não sobrescreva nada e garanta que rodar duas vezes não muda nada.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```python
    import shutil
    from datetime import datetime
    from pathlib import Path

    PASTA = Path("treino") / "Fotos"
    EXTENSOES = {".jpg", ".jpeg", ".png", ".heic"}
    SIMULAR = True


    def destino_livre(caminho: Path, ocupados: set[str]) -> Path:
        candidato, n = caminho, 2
        while candidato.exists() or str(candidato).lower() in ocupados:
            candidato = caminho.with_name(f"{caminho.stem} ({n}){caminho.suffix}")
            n += 1
        return candidato


    ocupados = set()
    # Só as fotos soltas na pasta principal: as que já estão em 2026/03 não são tocadas
    for foto in sorted(PASTA.iterdir()):
        if not (foto.is_file() and foto.suffix.lower() in EXTENSOES):
            continue
        momento = datetime.fromtimestamp(foto.stat().st_mtime)
        alvo = destino_livre(PASTA / f"{momento:%Y}" / f"{momento:%m}" / foto.name, ocupados)
        ocupados.add(str(alvo).lower())
        if SIMULAR:
            print(f"[simulação] {foto.name} -> {alvo.relative_to(PASTA)}")
        else:
            alvo.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(foto, alvo)
            print(f"{foto.name} -> {alvo.relative_to(PASTA)}")
    ```

    Rodar duas vezes não muda nada porque o `iterdir()` só olha a pasta principal: as fotos que já foram para `2026/03` não aparecem mais. O `relative_to(PASTA)` mostra só a parte final do caminho (`2026\03\IMG_0001.jpg`).

---

## 💡 Resumo

- Nome no formato **`AAAA-MM-DD_HHMMSS`** deixa as fotos em ordem cronológica.
- Fotos com a mesma hora ganham `_2`, `_3`... A simulação precisa **reservar** os nomes (`ocupados`) para mostrar a verdade.
- Um script bom **reconhece o próprio resultado** e pode rodar de novo sem estragar nada.
- Teste sempre o caso repetido, a simulação contra o real e a segunda execução.

## ➡️ Próximo passo

**[05 — Projeto do módulo: organizador de pastas com relatório](05_projeto_organizador.md)**.
