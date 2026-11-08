# 02 — O pacote e as regras da escola

> **Curso:** Automação com Python  
> **Módulo:** 05 — Projeto final  
> **Tempo estimado:** 1 h 30 min  

---

## 🎯 Objetivos

Ao final desta aula, você terá:

- Entendido o que é um **pacote**, o `__init__.py`, o `__main__.py` e os **imports relativos**.
- Representado cada aluno com uma **`dataclass`**, com uma **propriedade** calculada.
- Escrito o `dados.py`: ler a planilha, limpar as notas e aplicar as regras de aprovação.

## Pré-requisitos

- [Aula 01](01_planejando_a_secretaria.md): estrutura do projeto e planilha de treino.

---

## O pacote

```python title="secretaria/__init__.py"
"""Secretaria automática: boletim, certificados e e-mails a partir da planilha da turma."""
```

```python title="secretaria/__main__.py"
"""Permite rodar com: python -m secretaria ..."""
import sys

from .cli import main

sys.exit(main())
```

- **`__init__.py`** diz ao Python que a pasta `secretaria` é um **pacote**. Pode ficar só com uma descrição.
- **`__main__.py`** é o que roda quando você digita **`python -m secretaria`**: ele chama o `main()` da linha de comando ([aula 04](04_linha_de_comando_e_testes.md)) e termina com o código de saída dele.
- **Import relativo:** dentro do pacote, `from .dados import ler_turma` (com o **ponto**) quer dizer "do arquivo `dados.py` **deste** pacote". Assim, os arquivos se encontram mesmo que a pasta mude de lugar.

!!! warning "Rode de fora da pasta do pacote"
    O comando `python -m secretaria ...` funciona a partir da pasta **que contém** a pasta `secretaria` (a `C:\Automacao`). Rodar `python cli.py` de dentro da pasta `secretaria` dá `ImportError: attempted relative import with no known parent package`.

## As regras: `dados.py`

```python title="secretaria/dados.py"
"""Leitura da planilha da turma e as regras da escola (sem gravar nenhum arquivo)."""
import re
from dataclasses import dataclass, field
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

from openpyxl import load_workbook

MEDIA_APROVACAO = 6.0
MEDIA_RECUPERACAO = 4.0
FREQUENCIA_MINIMA = 0.75
EMAIL_VALIDO = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@dataclass
class Aluno:
    matricula: int
    nome: str
    email: str
    notas: list[float | None]
    faltas: int
    media: float | None = None
    frequencia: float = 0.0
    situacao: str = ""
    problemas: list[str] = field(default_factory=list)

    @property
    def email_valido(self) -> bool:
        return bool(EMAIL_VALIDO.match(self.email))


def converter_nota(valor) -> tuple[float | None, str]:
    """(nota, problema); problema vazio = tudo certo. Veja o Módulo 02, aula 04."""
    if valor is None or str(valor).strip() == "":
        return None, "nota não lançada"
    if isinstance(valor, str):
        try:
            valor = float(valor.strip().replace(",", "."))
        except ValueError:
            return None, f"valor inválido: {valor!r}"
    if not 0 <= valor <= 10:
        return None, f"fora de 0 a 10: {valor}"
    return float(valor), ""


def arredondar(valor: float) -> float:
    """Arredonda como a escola: 4,25 vira 4,3. Veja o Módulo 02, aula 05."""
    return float(Decimal(str(valor)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))


def calcular_situacao(media: float | None, frequencia: float) -> str:
    if media is None:
        return "Pendente"
    if frequencia < FREQUENCIA_MINIMA:
        return "Reprovado"
    if media >= MEDIA_APROVACAO:
        return "Aprovado"
    if media >= MEDIA_RECUPERACAO:
        return "Recuperação"
    return "Reprovado"


def ler_turma(caminho: Path) -> tuple[dict, list[Aluno]]:
    """Lê a aba Info e a aba Alunos e já calcula média, frequência e situação."""
    livro = load_workbook(caminho, read_only=True)
    info = {chave: valor for chave, valor in livro["Info"].iter_rows(values_only=True) if chave}
    alunos = []
    for matricula, nome, email, *bimestres, faltas in livro["Alunos"].iter_rows(min_row=2, values_only=True):
        if matricula is None:
            continue
        aluno = Aluno(matricula, nome, (email or "").strip(), [], faltas or 0)
        for numero, valor in enumerate(bimestres, start=1):
            nota, problema = converter_nota(valor)
            aluno.notas.append(nota)
            if problema:
                aluno.problemas.append(f"{numero}º bim: {problema}")
        if not aluno.email_valido:
            aluno.problemas.append(f"e-mail inválido: {aluno.email or 'vazio'}")
        aluno.media = None if None in aluno.notas else arredondar(sum(aluno.notas) / len(aluno.notas))
        aluno.frequencia = (info["Aulas dadas"] - aluno.faltas) / info["Aulas dadas"]
        aluno.situacao = calcular_situacao(aluno.media, aluno.frequencia)
        alunos.append(aluno)
    livro.close()
    return info, alunos
```

### `@dataclass` e `@property`

A classe `Aluno` guarda os dados de um aluno com **nome** (`aluno.media`, `aluno.situacao`), em vez de posições numa lista (`linha[6]`). A `@dataclass` cria o `__init__` sozinha; `field(default_factory=list)` dá a **cada** aluno a sua própria lista de problemas (com `= []`, todos os alunos dividiriam a **mesma** lista, um erro clássico do Python).

`email_valido` é uma **propriedade** (`@property`): parece um atributo (`aluno.email_valido`, sem parênteses), mas é calculada na hora, a partir do e-mail. Se o e-mail mudar, a resposta muda junto.

### O que veio dos módulos anteriores

- **`converter_nota()`** e **`arredondar()`** são as mesmas do [Módulo 02](../modulo_02_planilhas/05_projeto_boletim.md#o-arredondamento-um-bug-que-o-teste-achou).
- **`calcular_situacao()`** é a `situacao()` do boletim, com as regras em **constantes** no topo do arquivo.
- **`ler_turma()`** junta tudo e devolve os alunos **já calculados**: quem usa o `dados.py` não precisa saber como a média é feita.

!!! info "Nenhum arquivo é gravado aqui"
    O `dados.py` só **lê** e **calcula**. É por isso que ele é o mais fácil de testar ([aula 04](04_linha_de_comando_e_testes.md#testes-com-pytest)): os testes não precisam limpar arquivos depois.

## Experimentando

Na pasta do projeto, abra o Python interativo (`python` no terminal) e teste:

```python
from pathlib import Path

from secretaria.dados import ler_turma

info, alunos = ler_turma(Path("treino_secretaria") / "turma_1A.xlsx")
for aluno in alunos:
    print(f"{aluno.nome:16} {aluno.media!s:>4} {aluno.frequencia:4.0%} {aluno.situacao:12} {aluno.problemas}")
```

```text
Ana Souza         8.1  95% Aprovado     []
Bruno Lima        5.5  88% Recuperação  []
Carla Mendes      9.5 100% Aprovado     []
Diego Rocha       4.3  85% Recuperação  ['e-mail inválido: vazio']
Elisa Prado       7.3  98% Aprovado     []
Felipe Torres    None  92% Pendente     ['4º bim: nota não lançada']
Gabriela Nunes    3.3  69% Reprovado    []
Heitor Alves      8.3  99% Aprovado     ['e-mail inválido: heitor.alves@example']
```

`{aluno.media!s:>4}` usa `!s` para transformar o valor em texto antes de alinhar, porque `None` não aceita o formato de número.

---

## ⚠️ Erros comuns

- **`ImportError: attempted relative import...`**: rodou um arquivo do pacote direto. Use `python -m secretaria` de fora da pasta.
- **`ModuleNotFoundError: No module named 'secretaria'`**: o terminal não está na pasta que contém `secretaria`.
- **`problemas: list = []` na dataclass**: o Python recusa (`ValueError: mutable default`), justamente para evitar a lista compartilhada. Use `field(default_factory=list)`.
- **Colunas fora de ordem na planilha**: o `for matricula, nome, email, *bimestres, faltas in ...` depende da ordem combinada.

---

## Exercícios

### Básico (fixação)

Acrescente à classe `Aluno` a propriedade `aprovado`, que devolve `True` quando a situação é `"Aprovado"`. Teste com dois alunos criados à mão.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```python
    from dataclasses import dataclass, field


    @dataclass
    class Aluno:
        matricula: int
        nome: str
        email: str
        notas: list
        faltas: int
        media: float | None = None
        frequencia: float = 0.0
        situacao: str = ""
        problemas: list[str] = field(default_factory=list)

        @property
        def aprovado(self) -> bool:
            return self.situacao == "Aprovado"


    ana = Aluno(1, "Ana Souza", "ana.souza@example.com", [8.0] * 4, 0, situacao="Aprovado")
    bruno = Aluno(2, "Bruno Lima", "bruno.lima@example.com", [5.0] * 4, 0, situacao="Recuperação")
    print(ana.aprovado, bruno.aprovado)
    ```

    Saída: `True False`. No `dados.py`, basta acrescentar o método com `@property` dentro da classe que já existe. Depois, o `documentos.py` pode usar `if aluno.aprovado:` em vez de comparar o texto.

### Intermediário (aplicação)

Escreva a função `resumo(alunos)` que devolve um dicionário com quantos alunos há em cada situação, e a **média da turma** (só com quem tem média), arredondada com `arredondar()`.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```python
    from collections import Counter
    from pathlib import Path

    from secretaria.dados import arredondar, ler_turma


    def resumo(alunos) -> dict:
        medias = [a.media for a in alunos if a.media is not None]
        resultado = dict(Counter(a.situacao for a in alunos))
        resultado["Média da turma"] = arredondar(sum(medias) / len(medias)) if medias else None
        return resultado


    info, alunos = ler_turma(Path("treino_secretaria") / "turma_1A.xlsx")
    dados = resumo(alunos)
    print(dados)
    ```

    Na turma de treino: 4 aprovados, 2 em recuperação, 1 reprovado, 1 pendente; média da turma **6,6** (a média das 7 médias, sem o Felipe).

### Avançado (desafio)

A escola criou a **menção honrosa**: alunos aprovados com média **9,0 ou mais** e **frequência de 90% ou mais**. Acrescente a regra **sem mudar** a `calcular_situacao()`: crie a função `mencao_honrosa(aluno)` e liste quem a recebe.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```python
    from pathlib import Path

    from secretaria.dados import ler_turma

    MEDIA_MENCAO = 9.0
    FREQUENCIA_MENCAO = 0.90


    def mencao_honrosa(aluno) -> bool:
        return (aluno.situacao == "Aprovado" and aluno.media is not None
                and aluno.media >= MEDIA_MENCAO and aluno.frequencia >= FREQUENCIA_MENCAO)


    info, alunos = ler_turma(Path("treino_secretaria") / "turma_1A.xlsx")
    homenageados = [a.nome for a in alunos if mencao_honrosa(a)]
    print(homenageados)
    ```

    Só a **Carla Mendes** (9,5 e 100%). Uma regra nova numa função nova, sem mexer na regra antiga, é mais segura: os testes da `calcular_situacao()` continuam valendo.

---

## 💡 Resumo

- **Pacote** = pasta com `__init__.py`; **`__main__.py`** permite `python -m secretaria`; dentro do pacote, **import relativo** (`from .dados import ...`).
- **`@dataclass`** guarda os dados com nome; **`field(default_factory=list)`** evita a lista compartilhada; **`@property`** calcula na hora.
- `dados.py` só **lê e calcula**: é o coração das regras, e o mais fácil de testar.

## ➡️ Próximo passo

**[03 — Documentos e e-mails](03_documentos_e_emails.md)**.
