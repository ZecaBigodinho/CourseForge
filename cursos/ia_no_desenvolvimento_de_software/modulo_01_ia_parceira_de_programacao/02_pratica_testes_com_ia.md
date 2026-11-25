# 02 — Prática: testes e correção com IA

> **Curso:** IA no desenvolvimento de software  
> **Módulo:** 01 — IA como parceira de programação  
> **Tempo estimado:** 10 min em aula · 1 h com os exercícios  

---

## 🎯 Objetivos

Ao final desta aula, você será capaz de:

- Pedir à IA que explique um código e comparar a explicação com o requisito.
- Gerar testes **a partir do requisito** e rodá-los com o pytest.
- Interpretar as falhas, corrigir o defeito com ajuda da IA e confirmar com os testes.

## Pré-requisitos

- [Aula 01 — Onde a IA entra no desenvolvimento](01_onde_a_ia_entra.md).
- Python 3.11 ou mais novo e o pytest: `pip install pytest`.
- Um assistente de IA gratuito aberto no navegador. **Sem internet?** Use as respostas de exemplo de cada passo.

---

## A situação

Você entrou na equipe que mantém o **sistema acadêmico** de uma escola técnica. Um coordenador abriu um chamado:

!!! bug "Chamado #142"
    "A aluna Ana teve menção D em todas as unidades e **exatamente 75%** de frequência, mas o sistema mostrou **RP**. Pelo plano de curso, ela está aprovada."

O requisito, como está na documentação do sistema:

```text title="RF-07 — Situação final do aluno"
1. O aluno é AP (aprovado) quando TODAS as menções são "D" e a frequência é de
   pelo menos 75%.
2. Nos demais casos, o aluno é RP (reprovado).
3. As menções válidas são "D" (desenvolvida) e "ND" (não desenvolvida).
   Qualquer outro valor é erro de digitação: o sistema deve recusar (ValueError).
4. Sem nenhuma menção lançada, não há como decidir: o sistema deve recusar (ValueError).
5. A frequência vai de 0 a 100. Fora disso, o sistema deve recusar (ValueError).
```

E o código atual:

```python title="situacao.py"
"""Situação final do aluno no curso.

Regra (plano de curso): o aluno é AP (aprovado) quando tem menção D
em todas as unidades curriculares e frequência mínima de 75%.
Caso contrário, é RP (reprovado).
"""


def situacao_final(mencoes, frequencia):
    if frequencia > 75 and "ND" not in mencoes:
        return "AP"
    return "RP"
```

Crie uma pasta `chamado_142`, salve o arquivo `situacao.py` nela e abra a pasta no VS Code.

!!! danger "Dados inventados"
    A "Ana" do chamado é fictícia. No trabalho real, **não** cole nomes, matrículas ou notas de alunos no chat da IA: o código e o requisito bastam.

---

## Passo 1 — Pedir uma explicação

Antes de mexer, entenda. Copie o código e mande este pedido:

```text title="Pedido 1"
Você é um programador Python experiente ajudando um colega iniciante.
Explique, em português e em até 5 linhas, o que esta função faz.
Não corrija nada ainda.

[cole aqui o código de situacao.py]
```

Leia a resposta e **compare com o requisito RF-07**. Em que ponto o código e o requisito discordam?

??? example "Resposta de exemplo (se estiver sem IA)"
    <div class="cf-chat" markdown>
    <p class="cf-chat__topo">Assistente de IA</p>
    <p class="cf-msg">A função recebe uma lista de menções e a frequência do aluno. Ela devolve "AP" quando a frequência é <strong>maior que 75</strong> e nenhuma menção é "ND". Em qualquer outro caso, devolve "RP". Ela não confere se a lista está vazia nem se as menções e a frequência têm valores válidos.</p>
    </div>

    Repare: a explicação está **certa sobre o código**, mas o requisito diz "**pelo menos** 75%". Maior que 75 deixa de fora exatamente o caso da Ana.

## Passo 2 — Gerar testes a partir do requisito

Este é o passo mais importante da aula. Você vai dar à IA **o requisito**, e não o código.

```text title="Pedido 2"
Você é um testador de software experiente.
Contexto: Python 3.11 e pytest, sistema acadêmico de uma escola técnica.
A função situacao_final(mencoes, frequencia), do módulo situacao, deve seguir
este requisito:

[cole aqui o RF-07 inteiro]

Escreva testes que cubram cada item do requisito, incluindo os valores de limite
(75 e logo abaixo de 75) e os dados inválidos.
Formato: só o arquivo test_situacao.py, usando pytest.mark.parametrize, com um
comentário curto em cada caso.
```

Salve a resposta como `test_situacao.py`, na mesma pasta.

??? example "Resposta de exemplo (se estiver sem IA)"
    ```python title="test_situacao.py"
    import pytest

    from situacao import situacao_final


    @pytest.mark.parametrize("mencoes, frequencia, esperado", [
        (["D", "D", "D", "D"], 90, "AP"),     # caminho feliz
        (["D", "D", "D", "D"], 75, "AP"),     # limite exato: 75% já aprova
        (["D", "D", "D", "D"], 74.9, "RP"),   # logo abaixo do limite
        (["D", "ND", "D", "D"], 100, "RP"),   # uma UC não desenvolvida
        (["ND"], 50, "RP"),                   # os dois motivos juntos
    ])
    def test_situacao(mencoes, frequencia, esperado):
        assert situacao_final(mencoes, frequencia) == esperado


    @pytest.mark.parametrize("mencoes, frequencia", [
        ([], 90),            # nenhuma menção lançada
        (["D", "X"], 90),    # menção que não existe
        (["D"], 120),        # frequência impossível
        (["D"], -5),
    ])
    def test_dados_invalidos(mencoes, frequencia):
        with pytest.raises(ValueError):
            situacao_final(mencoes, frequencia)
    ```

!!! warning "Confira os testes antes de rodar"
    A IA também erra nos testes. Leia cada caso e pergunte: **"este resultado esperado bate com o RF-07?"** Um teste errado é tão ruim quanto um código errado.

## Passo 3 — Rodar e ver falhar

No terminal do VS Code, dentro da pasta `chamado_142`:

```bash
python -m pytest -q
```

```text title="Saída (resumida)"
FAILED test_situacao.py::test_situacao[mencoes1-75-AP] - AssertionError
FAILED test_situacao.py::test_dados_invalidos[mencoes0-90] - Failed: DID NOT RAISE
FAILED test_situacao.py::test_dados_invalidos[mencoes1-90] - Failed: DID NOT RAISE
FAILED test_situacao.py::test_dados_invalidos[mencoes2-120] - Failed: DID NOT RAISE
FAILED test_situacao.py::test_dados_invalidos[mencoes3--5] - Failed: DID NOT RAISE
5 failed, 4 passed
```

Os testes acharam **o defeito do chamado** (o limite de 75%) e **mais quatro** que ninguém tinha reclamado ainda: lista vazia, menção digitada errada e frequências impossíveis. Teste que falha aqui é **boa notícia**: o problema apareceu antes de chegar ao aluno.

!!! note "E se você tivesse mostrado só o código?"
    Peça à IA, em outra conversa, "escreva testes para esta função" colando só o código. É comum ela escrever algo como `assert situacao_final(["D"], 75) == "RP"`: um teste que **passa** e **confirma o defeito**. A IA descreve o que o código faz; só o requisito diz o que ele **deveria** fazer.

## Passo 4 — Corrigir com ajuda da IA

```text title="Pedido 3"
Você é um programador Python experiente.
Esta função não cumpre o requisito abaixo; os testes do pytest mostram as falhas.
Corrija a função para cumprir TODOS os itens do requisito.
Use nomes claros, type hints e constantes para os valores fixos (como o 75).
Formato: o arquivo situacao.py completo e, depois, uma lista curta com o que
mudou e por quê.

Requisito: [cole o RF-07]
Código: [cole situacao.py]
Falhas: [cole a saída do pytest]
```

??? example "Resposta de exemplo (se estiver sem IA)"
    ```python title="situacao.py"
    """Situação final do aluno no curso.

    Regra (plano de curso): o aluno é AP (aprovado) quando tem menção D
    em todas as unidades curriculares e frequência mínima de 75%.
    Caso contrário, é RP (reprovado).
    """

    MENCOES_VALIDAS = {"D", "ND"}
    FREQUENCIA_MINIMA = 75


    def situacao_final(mencoes: list[str], frequencia: float) -> str:
        if not mencoes:
            raise ValueError("Nenhuma menção lançada.")
        for mencao in mencoes:
            if mencao not in MENCOES_VALIDAS:
                raise ValueError(f"Menção inválida: {mencao!r}. Use 'D' ou 'ND'.")
        if not 0 <= frequencia <= 100:
            raise ValueError("A frequência deve estar entre 0 e 100.")

        if frequencia >= FREQUENCIA_MINIMA and all(m == "D" for m in mencoes):
            return "AP"
        return "RP"
    ```

    **O que mudou:**

    - `>` virou `>=`: 75% agora aprova (item 1, o chamado #142).
    - Lista vazia, menção desconhecida e frequência fora de 0–100 geram `ValueError` (itens 3, 4 e 5).
    - `all(m == "D" ...)` diz a regra do jeito que ela está escrita: **todas** as menções são D.
    - Os valores fixos viraram constantes, fáceis de achar se a regra mudar.

Substitua o `situacao.py` pela versão corrigida, **leia cada linha** e rode de novo:

```bash
python -m pytest -q
```

```text title="Saída"
.........                                                       [100%]
9 passed
```

## Passo 5 — Revisar antes de entregar

Testes passando não encerram o trabalho. Antes do commit, passe a correção pelo **checklist de revisão** da [aula 03](03_revisao_e_autoavaliacao.md) e registre os resultados na tabela de testes. Na mensagem de commit, cite o chamado:

```bash
git commit -m "fix: 75% de frequência aprova (chamado #142) e dados inválidos são recusados"
```

---

## ⚠️ Erros comuns

- **`ModuleNotFoundError: No module named 'situacao'`**: rode o pytest **dentro** da pasta `chamado_142`, onde estão os dois arquivos.
- **Mudar o teste para "passar"**: se o teste segue o requisito, quem muda é o código. Só mude o teste se ele contrariar o requisito.
- **Colar só a parte "interessante" do erro**: mande à IA a saída inteira do pytest; o nome do caso que falhou é a pista principal.

## Exercícios

### Básico (fixação)

Sem rodar nada: qual dos 9 testes pegaria o defeito do chamado #142 e por que nenhum teste com frequência 90 ou 50 conseguiria pegá-lo?

??? success "Gabarito — Básico"
    O teste `(["D", "D", "D", "D"], 75, "AP")`, o **valor de limite**. O defeito está em `>` no lugar de `>=`, e os dois só dão resultados diferentes **exatamente em 75**. Com 90, os dois aprovam; com 50, os dois reprovam. Por isso testes de limite são obrigatórios em regras com "pelo menos", "no máximo", "a partir de".

### Intermediário (aplicação)

A coordenação pediu um requisito novo:

```text title="RF-08 — Motivos da reprovação"
A função motivos_reprovacao(mencoes, frequencia) devolve uma lista de textos:
- "frequência abaixo de 75%" quando a frequência for menor que 75;
- "UC não desenvolvida" quando houver pelo menos uma menção "ND".
Aluno aprovado: lista vazia.
```

Faça na ordem: (1) peça à IA os **testes** a partir do RF-08, (2) rode e veja falhar (a função ainda não existe), (3) peça o código, (4) rode até passar. Coloque a função em `situacao.py`, aproveitando as constantes.

??? success "Gabarito — Intermediário"
    ```python title="situacao.py — acrescentar no fim"
    def motivos_reprovacao(mencoes: list[str], frequencia: float) -> list[str]:
        situacao_final(mencoes, frequencia)  # reaproveita as validações do RF-07
        motivos = []
        if frequencia < FREQUENCIA_MINIMA:
            motivos.append("frequência abaixo de 75%")
        if "ND" in mencoes:
            motivos.append("UC não desenvolvida")
        return motivos
    ```

    ```python title="test_motivos.py"
    import pytest

    from situacao import motivos_reprovacao


    @pytest.mark.parametrize("mencoes, frequencia, esperado", [
        (["D", "D"], 75, []),                                    # aprovado
        (["D", "D"], 60, ["frequência abaixo de 75%"]),
        (["D", "ND"], 80, ["UC não desenvolvida"]),
        (["ND"], 10, ["frequência abaixo de 75%", "UC não desenvolvida"]),
    ])
    def test_motivos(mencoes, frequencia, esperado):
        assert motivos_reprovacao(mencoes, frequencia) == esperado
    ```

    Chamar `situacao_final` no começo faz a função recusar os mesmos dados inválidos, sem repetir as validações. Escrever os testes **antes** do código (TDD) é o jeito mais seguro de trabalhar com IA: o teste é a sua definição de "pronto".

### Avançado (desafio)

Um colega pediu à IA uma busca de alunos por turma, e ela sugeriu este código:

```python title="busca.py"
import sqlite3


def alunos_da_turma(conexao: sqlite3.Connection, turma: str) -> list[str]:
    sql = f"SELECT nome FROM alunos WHERE turma = '{turma}'"
    return [linha[0] for linha in conexao.execute(sql)]
```

Peça à IA uma **revisão de segurança** do código. Depois, escreva um teste que prove o problema (dica: o que acontece com a turma `x' OR '1'='1`?) e corrija.

??? success "Gabarito — Avançado"
    O problema é **injeção de SQL**: o texto da turma entra direto no comando. Com `x' OR '1'='1`, a condição vira sempre verdadeira e a função devolve **todos** os alunos de todas as turmas. A correção é a **consulta parametrizada**: o banco recebe o valor separado do comando.

    ```python title="busca.py"
    import sqlite3


    def alunos_da_turma(conexao: sqlite3.Connection, turma: str) -> list[str]:
        sql = "SELECT nome FROM alunos WHERE turma = ?"
        return [linha[0] for linha in conexao.execute(sql, (turma,))]
    ```

    ```python title="test_busca.py"
    import sqlite3

    import pytest

    from busca import alunos_da_turma


    @pytest.fixture
    def conexao():
        con = sqlite3.connect(":memory:")
        con.execute("CREATE TABLE alunos (nome TEXT, turma TEXT)")
        con.executemany("INSERT INTO alunos VALUES (?, ?)",
                        [("Ana", "PS-01"), ("Bruno", "PS-01"), ("Carla", "PS-02")])
        yield con
        con.close()


    def test_busca_normal(conexao):
        assert alunos_da_turma(conexao, "PS-01") == ["Ana", "Bruno"]


    def test_injecao_nao_devolve_todos(conexao):
        assert alunos_da_turma(conexao, "x' OR '1'='1") == []
    ```

    Com o código original, `test_injecao_nao_devolve_todos` **falha** (vêm os três alunos); com o corrigido, passa. Código de banco gerado por IA deve sempre passar por esta pergunta: **algum texto do usuário entra direto no SQL?**

## 💡 Resumo

- Explicação da IA descreve o **código**; o **requisito** diz o que é certo.
- Gere testes **a partir do requisito**, incluindo **limites** e **dados inválidos**.
- Teste falhando antes da correção é sinal de que o teste funciona.
- Correção da IA só entra depois de **ler**, **rodar os testes** e **revisar**.

## ➡️ Próximo passo

**[03 — Revisão, registro e autoavaliação](03_revisao_e_autoavaliacao.md)**.
