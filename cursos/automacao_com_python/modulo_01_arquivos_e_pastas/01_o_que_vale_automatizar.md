# 01 — O que vale automatizar e a pasta de treino

> **Curso:** Automação com Python  
> **Módulo:** 01 — Arquivos e pastas  
> **Tempo estimado:** 1 h  

---

## 🎯 Objetivos

Ao final desta aula, você será capaz de:

- Reconhecer **tarefas que valem a pena automatizar** (e as que não valem).
- Seguir as **regras de segurança** de quem automatiza: treinar numa cópia, simular antes, nunca apagar.
- Preparar a pasta do curso no **VS Code** e rodar um script pelo terminal.
- Criar a **pasta de treino**, com arquivos de mentira, para praticar sem medo.

## Pré-requisitos

- Python instalado e o básico da linguagem: variáveis, `if`, `for`, listas, dicionários e funções. É o que o [Módulo 01 do curso Python para Desktop](../../python_para_desktop/modulo_01_fundamentos/index.md) ensina.
- VS Code com a extensão Python (veja o [Módulo 00 do curso de Python](../../python_para_desktop/modulo_06_vscode_config/index.md), se precisar).

!!! info "Versão do Python"
    Os exemplos foram testados com o **Python 3.13** e funcionam do **3.11** em diante. Confira a sua com `python --version` no terminal.

---

## O que é automatizar

**Automatizar** é ensinar o computador a fazer uma tarefa **repetitiva** que hoje você faz com o mouse: renomear 200 fotos, separar os arquivos da pasta Downloads, gerar 40 certificados, montar o mesmo relatório toda semana.

Um script de automação é um programa Python comum. A diferença é o assunto: em vez de calcular médias na tela, ele mexe em **arquivos**, **planilhas**, **documentos** e **e-mails**.

### Vale a pena automatizar quando...

| ✅ Vale | ❌ Não vale (ainda) |
|---|---|
| A tarefa se **repete** (todo dia, toda semana, todo bimestre) | Acontece uma vez só e leva 2 minutos |
| São **muitos itens** iguais (200 fotos, 40 alunos) | Cada caso é diferente e exige decisão humana |
| As **regras são claras** ("PDF vai para Documentos") | As regras mudam toda hora ou ninguém sabe explicar |
| **Erro humano** é comum (digitar nome errado, esquecer um) | O custo de um erro do script seria muito alto e não dá para conferir |

!!! example "Tarefas que este curso vai automatizar"
    - Módulo 01: organizar a pasta Downloads e renomear fotos pela data.
    - Módulo 02: transformar a planilha de notas em boletim com médias e cores.
    - Módulo 03: gerar certificados e crachás da turma a partir da planilha.
    - Módulo 04: preparar e-mails de lembrete e agendar o script para rodar sozinho.
    - Módulo 05: juntar tudo na **Secretaria automática**.

## As regras de segurança

Um script faz em 1 segundo o que você faria em 1 hora, **inclusive o erro**. Por isso, quem automatiza segue quatro regras:

1. **Treine numa cópia.** Nunca rode um script novo na sua pasta de verdade. Use a **pasta de treino** desta aula ou uma cópia da pasta real.
2. **Simule antes.** Todo script que move, renomeia ou altera arquivos deste curso tem um **modo de simulação**: ele mostra o que **faria**, sem fazer. Você confere e só então roda de verdade.
3. **Nunca apague.** Em vez de apagar, **mova** para uma pasta (por exemplo, `_revisar`). Apagar é a única coisa que não tem volta.
4. **Guarde o que mudou.** Um bom script deixa um **relatório** (o que estava onde, para onde foi). Com ele, dá para desfazer.

!!! danger "Arquivos dos outros e dados pessoais"
    Automatize só pastas **suas** ou com **autorização** de quem é dono. Planilhas com dados de alunos, clientes ou funcionários têm **dados pessoais**: trate com o cuidado da LGPD (veja o curso de [Segurança digital](../../seguranca_digital/modulo_04_cidadania_e_direitos/03_lgpd_no_dia_a_dia.md)). Neste curso, todos os dados são **inventados**.

## Preparando a pasta do curso

1. Crie uma pasta para o curso, por exemplo `C:\Automacao` (fora de *Documentos* e da área de trabalho, para não misturar com os seus arquivos).
2. No VS Code: **Arquivo** ➔ **Abrir Pasta...** ➔ escolha `C:\Automacao`.
3. Abra o terminal: **Terminal** ➔ **Novo Terminal**. Ele já abre dentro da pasta.

Todos os scripts do módulo ficam soltos nessa pasta, e todos trabalham na subpasta `treino`.

!!! tip "Rodando um script"
    Crie o arquivo no VS Code (*Arquivo* ➔ *Novo Arquivo*, salve como `nome.py`) e, no terminal, digite `python nome.py`. Também dá para usar o botão ▶ no canto superior direito do editor.

## A pasta de treino

Este script cria a pasta `treino` com **arquivos de mentira**: uma pasta `Downloads` bagunçada, com documentos, imagens, músicas e instaladores, e uma pasta `Fotos` com fotos de datas diferentes. Os arquivos são cheios de `x` (não são documentos de verdade), mas têm nome, tamanho e data como os reais.

```python title="criar_treino.py"
"""Cria a pasta de treino com arquivos de mentira para praticar com segurança."""
import os
from datetime import datetime
from pathlib import Path

TREINO = Path("treino")

DOWNLOADS = [
    "boletim_2026_1bim.pdf", "trabalho_historia.docx", "foto_festa.jpg", "IMG_0042.JPG",
    "planilha_gastos.xlsx", "musica_aula.mp3", "video_formatura.mp4", "instalador_vscode.exe",
    "contrato_estagio.pdf", "lista_compras.txt", "apresentacao_ciencias.pptx", "meme.png",
    "projeto_final.zip", "anotacoes.txt", "certificado_canva.pdf", "sem_extensao",
]

FOTOS = {  # nome: data e hora em que a "foto" foi tirada
    "IMG_0001.jpg": "2026-03-14 09:12:05",
    "IMG_0002.jpg": "2026-03-14 09:12:05",   # mesma hora da anterior (de propósito)
    "IMG_0003.jpg": "2026-03-15 17:40:31",
    "WhatsApp Image 2026-04-02.jpeg": "2026-04-02 20:03:44",
    "DSC_1234.JPG": "2026-05-20 08:00:00",
    "foto.png": "2026-06-01 12:30:00",
}


def criar(caminho: Path, tamanho: int, data: str | None = None) -> None:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_bytes(b"x" * tamanho)
    if data:
        momento = datetime.strptime(data, "%Y-%m-%d %H:%M:%S").timestamp()
        os.utime(caminho, (momento, momento))


def main() -> None:
    if TREINO.exists():
        print("A pasta 'treino' já existe. Apague-a se quiser começar do zero.")
        return
    for i, nome in enumerate(DOWNLOADS):
        criar(TREINO / "Downloads" / nome, 1_000 * (i + 1) ** 2)
    for nome, data in FOTOS.items():
        criar(TREINO / "Fotos" / nome, 50_000, data)
    print(f"Pasta de treino criada em: {TREINO.resolve()}")


if __name__ == "__main__":
    main()
```

Rode no terminal:

```text
> python criar_treino.py
Pasta de treino criada em: C:\Automacao\treino
```

Abra a pasta `treino` no Explorador de Arquivos e veja o que foi criado. Repare que as fotos têm **datas de modificação** diferentes: elas vão ser usadas na [aula 04](04_renomear_fotos_pela_data.md).

!!! info "O que há de novo no código"
    - `Path("treino")` representa um **caminho** de pasta ou arquivo; o operador `/` junta partes: `TREINO / "Downloads" / nome`. A [aula 02](02_pathlib.md) explica tudo isso.
    - `os.utime` muda a **data de modificação** do arquivo. Aqui serve só para as fotos de mentira parecerem tiradas em dias diferentes.
    - `if __name__ == "__main__":` faz o `main()` rodar quando você executa o arquivo, mas não quando outro script o importa.

!!! tip "Bagunçou tudo? Comece de novo"
    A pasta de treino existe para isso. Apague a pasta `treino` (pelo Explorador de Arquivos) e rode `python criar_treino.py` outra vez. Em segundos ela volta ao estado original.

---

## ⚠️ Erros comuns

- **`python: can't open file 'criar_treino.py'`**: o terminal não está na pasta do script. Abra a pasta no VS Code (*Abrir Pasta*) e abra um terminal novo.
- **`'python' não é reconhecido como um comando`**: o Python não está instalado ou não está no PATH. Veja a instalação no [curso de Python](../../python_para_desktop/modulo_06_vscode_config/index.md).
- **Rodar um script novo direto na pasta Downloads de verdade.** Sempre na `treino` primeiro.
- **A pasta `treino` foi criada em outro lugar**: o script cria a pasta onde o **terminal** está. Confira o caminho que ele imprime.

---

## Exercícios

### Básico (fixação)

Classifique: vale automatizar ou não? Explique em uma frase. (a) Renomear as 300 fotos da excursão. (b) Escrever uma carta de agradecimento para a diretora. (c) Gerar o boletim de 35 alunos todo bimestre. (d) Escolher qual foto vai para a capa do álbum.

<!-- gabarito -->
??? success "Gabarito — Básico"
    (a) **Vale:** muitos itens, regra clara (nome pela data). (b) **Não vale:** acontece uma vez e é um texto pessoal. (c) **Vale:** se repete todo bimestre, com regras claras (médias, situação). (d) **Não vale:** é uma decisão de gosto, humana.

### Intermediário (aplicação)

Acrescente à lista `DOWNLOADS` do `criar_treino.py` três arquivos: `curriculo.pdf`, `figurinha.webp` e `backup_celular.rar`. Apague a pasta `treino`, rode de novo e confira se eles apareceram.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    Basta acrescentar os nomes no fim da lista (antes do `]`):

    ```python
    DOWNLOADS = [
        "boletim_2026_1bim.pdf", "trabalho_historia.docx", "foto_festa.jpg", "IMG_0042.JPG",
        "planilha_gastos.xlsx", "musica_aula.mp3", "video_formatura.mp4", "instalador_vscode.exe",
        "contrato_estagio.pdf", "lista_compras.txt", "apresentacao_ciencias.pptx", "meme.png",
        "projeto_final.zip", "anotacoes.txt", "certificado_canva.pdf", "sem_extensao",
        "curriculo.pdf", "figurinha.webp", "backup_celular.rar",
    ]
    ```

    Como a pasta `treino` já existia, o script avisa e não faz nada: é preciso **apagá-la** antes de rodar de novo. Agora a `Downloads` tem 19 arquivos.

### Avançado (desafio)

A Ana quer um script que "apague todos os arquivos com mais de 1 ano da pasta Downloads". Usando as quatro regras de segurança, reescreva o pedido dela de um jeito mais seguro.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    Uma versão segura: *"Um script que, primeiro, **lista** (simulação) os arquivos da Downloads com mais de 1 ano e o espaço que eles ocupam; depois de eu conferir, **move** esses arquivos para uma pasta `_revisar` (em vez de apagar) e grava um **relatório** com o que foi movido. Vou testar antes na pasta de treino."* Assim: treina numa cópia (regra 1), simula antes (regra 2), não apaga (regra 3) e guarda o que mudou (regra 4). Depois de alguns dias, se nada fez falta, a própria Ana apaga a `_revisar`.

---

## 💡 Resumo

- Automatize tarefas **repetitivas**, com **muitos itens** e **regras claras**.
- As quatro regras: **treine numa cópia**, **simule antes**, **nunca apague** (mova) e **guarde o que mudou**.
- A pasta do curso fica aberta no VS Code; scripts rodam com `python nome.py` no terminal.
- O `criar_treino.py` recria a pasta de treino sempre que você precisar começar do zero.

## ➡️ Próximo passo

**[02 — Caminhos e listas de arquivos com `pathlib`](02_pathlib.md)**: como o Python enxerga pastas e arquivos.
