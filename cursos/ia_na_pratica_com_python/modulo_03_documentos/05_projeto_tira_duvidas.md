# 05 — Projeto do módulo: tira-dúvidas do regulamento

> **Curso:** IA na prática com Python  
> **Módulo:** 03 — IA com os seus documentos  
> **Tempo estimado:** 2 h  

---

## 🎯 Objetivos

Ao final desta aula, você terá um programa que:

- Lê um regulamento em **PDF ou TXT**, divide em trechos e responde dúvidas **no terminal**, sempre com a **fonte**.
- Funciona com o **Gemini** ou **sem IA** (modo simulado).
- **Registra** as perguntas (sem identificar quem perguntou), para a escola ver o que o regulamento não responde.
- **Avalia a busca** com um arquivo de perguntas de teste, antes de colocar em uso.

## Pré-requisitos

- Aulas [01](01_ler_documentos.md) a [04](04_responder_com_fonte.md) deste módulo, com `ler_documento.py`, `trechos.py`, `buscar.py`, `responder.py` e `erros_ia.py` na pasta.

---

## O programa

```python title="tira_duvidas.py"
"""Tira-dúvidas do regulamento: responde só com base no documento e cita a fonte.

    python tira_duvidas.py treino_docs/regulamento_escola.pdf             # perguntas no terminal
    python tira_duvidas.py treino_docs/regulamento_escola.pdf --avaliar perguntas_teste.csv
"""
import argparse
import csv
import os
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

from buscar import buscar
from erros_ia import explicar_erro
from ler_documento import ler_paginas
from responder import responder, responder_simulado
from trechos import dividir

REGISTRO = Path("perguntas_registradas.csv")


def escolher_resposta(simulado: bool):
    load_dotenv()
    if simulado or not os.getenv("GEMINI_API_KEY"):
        return responder_simulado, "simulado"
    from google import genai
    cliente, modelo = genai.Client(), os.getenv("GEMINI_MODELO", "gemini-3.8-flash")
    return (lambda pergunta, trechos: responder(cliente, modelo, pergunta, trechos)), "Gemini"


def registrar(pergunta: str, resultado: dict) -> None:
    """Guarda pergunta e resultado (sem nada de quem perguntou): mostra o que o regulamento não responde."""
    novo = not REGISTRO.exists()
    with open(REGISTRO, "a", newline="", encoding="utf-8-sig") as arq:
        escritor = csv.writer(arq, delimiter=";")
        if novo:
            escritor.writerow(["Quando", "Pergunta", "Encontrou", "Fonte"])
        escritor.writerow([f"{datetime.now():%d/%m/%Y %H:%M}", pergunta,
                           "sim" if resultado["encontrou"] else "não", resultado["fonte"]])


def avaliar(trechos: list, caminho: Path) -> int:
    """Confere a BUSCA (sem IA): a seção certa aparece entre os 3 primeiros trechos?"""
    with open(caminho, newline="", encoding="utf-8-sig") as arq:
        casos = list(csv.DictReader(arq, delimiter=";"))
    acertos = avaliados = 0
    for caso in casos:
        titulos = [t.titulo for _, t in buscar(caso["pergunta"], trechos)]
        esperado = caso["secao_esperada"].strip()
        if not esperado:  # pergunta fora do regulamento: quem deve recusar é a etapa da resposta
            print(f"--   {caso['pergunta']:48} -> fora do regulamento (confira a resposta)")
            continue
        avaliados += 1
        ok = esperado in titulos
        acertos += ok
        print(f"{'OK ' if ok else 'ERRO'} {caso['pergunta']:48} -> {titulos[:1] or ['(nada)']}")
    print(f"\nBusca: {acertos} de {avaliados} perguntas com a seção certa entre os 3 primeiros trechos.")
    return 0 if acertos == avaliados else 1


def main(argumentos: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Tira-dúvidas de um documento (PDF ou TXT).")
    parser.add_argument("documento", type=Path)
    parser.add_argument("--simulado", action="store_true", help="sem IA")
    parser.add_argument("--avaliar", type=Path, help="CSV pergunta;secao_esperada para conferir a busca")
    args = parser.parse_args(argumentos)
    if not args.documento.exists():
        print(f"Documento não encontrado: {args.documento}")
        return 2
    trechos = dividir(ler_paginas(args.documento))
    if not trechos:
        print("Não achei texto no documento (é um PDF escaneado?).")
        return 2
    if args.avaliar:
        return avaliar(trechos, args.avaliar)

    resposta_para, nome = escolher_resposta(args.simulado)
    print(f"Tira-dúvidas ({nome}) — {len(trechos)} trechos de {args.documento.name}. Digite /sair para terminar.")
    while True:
        pergunta = input("\nSua dúvida: ").strip()
        if pergunta in ("/sair", ""):
            if pergunta == "/sair":
                break
            continue
        try:
            resultado = resposta_para(pergunta, trechos)
        except Exception as erro:
            print(f"(A API não respondeu: {explicar_erro(erro)})")
            continue
        print(resultado["resposta"])
        if resultado["fonte"]:
            print(f"  Fonte: {resultado['fonte']}")
        registrar(pergunta, resultado)
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

## Usando

```text
> python tira_duvidas.py treino_docs/regulamento_escola.pdf --simulado
Tira-dúvidas (simulado) — 9 trechos de regulamento_escola.pdf. Digite /sair para terminar.

Sua dúvida: Quantos livros posso pegar na biblioteca?
O aluno pode pegar até 2 livros por vez, pelo prazo de 7 dias. O empréstimo pode ser renovado uma vez, por mais 7 dias, se ninguém tiver reservado o livro.
  Fonte: 8. Biblioteca, página 3

Sua dúvida: Tem cantina na escola?
Não encontrei essa informação no regulamento. Procure a secretaria.
```

Com chave, a resposta vem escrita pela IA, curta, e com a mesma fonte. O arquivo `perguntas_registradas.csv` guarda cada pergunta e se ela foi respondida:

```text
Quando;Pergunta;Encontrou;Fonte
08/11/2026 20:00;Quantos livros posso pegar na biblioteca?;sim;8. Biblioteca, página 3
08/11/2026 20:00;Tem cantina na escola?;não;
```

!!! tip "O registro melhora o regulamento"
    Muitas perguntas "não encontrei" sobre o mesmo assunto (cantina, Wi-Fi, armários) mostram o que **falta** no regulamento ou num FAQ. O registro guarda só a pergunta e a hora, sem nome nem matrícula de quem perguntou.

## Medindo antes de confiar: a avaliação

As perguntas de teste ficam num CSV, com a seção que **deveria** ser encontrada (vazia = a pergunta não é respondida pelo regulamento):

```text
pergunta;secao_esperada
Quantos livros posso pegar na biblioteca?;8. Biblioteca
Posso renovar o empréstimo do livro?;8. Biblioteca
Que horas começam as aulas da tarde?;1. Horários
A que horas fecha o portão?;1. Horários
Cheguei atrasado, o que acontece?;2. Atrasos
Qual a frequência mínima?;3. Frequência
Faltei à prova, como faço a segunda chamada?;5. Segunda chamada
Posso usar o celular na sala?;6. Celular
Preciso ir de uniforme?;7. Uniforme
Posso usar o laboratório depois da aula?;9. Laboratório de informática
Qual a nota para passar de ano?;4. Avaliação
Tem cantina na escola?;
```

```text
> python tira_duvidas.py treino_docs/regulamento_escola.pdf --avaliar perguntas_teste.csv
OK  Quantos livros posso pegar na biblioteca?        -> ['8. Biblioteca']
...
ERRO Cheguei atrasado, o que acontece?                -> ['(nada)']
...
ERRO Qual a nota para passar de ano?                  -> ['(nada)']
--   Tem cantina na escola?                           -> fora do regulamento (confira a resposta)

Busca: 9 de 11 perguntas com a seção certa entre os 3 primeiros trechos.
```

A avaliação mede a **busca**, a parte sem IA e de graça. Os dois erros são de **vocabulário**: "atras**ado**" × "atras**o**"; "nota para passar" × "média para aprovação" ([aula 03](03_buscar_trechos.md#os-dois-limites)). O desafio desta aula resolve os dois.

!!! info "Por que avaliar a busca, e não a resposta?"
    Se a busca não acha o trecho certo, a IA **nunca** vai responder certo, por melhor que seja. E a busca pode ser testada sem gastar nada, quantas vezes quiser. Toda vez que mudar a busca (sinônimos, tamanho dos trechos), rode a avaliação de novo.

---

## ⚠️ Erros comuns

- **Pôr em uso sem avaliar**: os alunos descobrem os erros por você.
- **Registrar quem perguntou**: o registro precisa só das perguntas.
- **Regulamento desatualizado**: o tira-dúvidas repete o que está no documento. Mudou o regulamento, troque o PDF.
- **Usar com documentos sigilosos** no plano gratuito.

---

## Exercícios

### Básico (fixação)

Rode a avaliação pelo Python (`main([...])`) e mostre o código de saída. Por que ele é 1?

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```python
    from tira_duvidas import main

    codigo = main(["treino_docs/regulamento_escola.pdf", "--avaliar", "perguntas_teste.csv"])
    print("código de saída:", codigo)
    ```

    Código **1**: nem todas as perguntas avaliadas acharam a seção certa (9 de 11). Um código diferente de zero permite usar a avaliação num **teste automático**: se alguém piorar a busca, o teste avisa.

### Intermediário (aplicação)

Simule uma sessão com o `input` trocado por uma lista de perguntas (no modo simulado) e confira o `perguntas_registradas.csv`: quantas foram respondidas?

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```python
    import builtins
    import csv
    from pathlib import Path

    from tira_duvidas import main

    Path("perguntas_registradas.csv").unlink(missing_ok=True)
    entradas = iter(["Quantos livros posso pegar na biblioteca?", "Posso usar o celular na sala de aula?",
                     "Tem cantina na escola?", "/sair"])
    builtins.input = lambda _prompt="": next(entradas)
    main(["treino_docs/regulamento_escola.pdf", "--simulado"])

    with open("perguntas_registradas.csv", encoding="utf-8-sig") as arq:
        registro = list(csv.DictReader(arq, delimiter=";"))
    respondidas = sum(1 for r in registro if r["Encontrou"] == "sim")
    print(f"{respondidas} de {len(registro)} respondidas")
    ```

    2 de 3: biblioteca e celular, sim; cantina, não. (No modo simulado, "Preciso ir de uniforme?" ficaria sem resposta: só uma palavra em comum, abaixo do limite mais exigente da [aula 04](04_responder_com_fonte.md#dois-limites-de-pontos).) O `missing_ok=True` evita erro se o registro ainda não existir.

### Avançado (desafio)

Acrescente à busca um dicionário de **sinônimos** do assunto escolar (`atrasado` ➔ `atraso`, `passar` ➔ `aprovacao`, `nota` ➔ `media`) e rode a avaliação de novo. Quantas acertam agora?

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```python
    from pathlib import Path

    import buscar
    from ler_documento import ler_paginas
    from tira_duvidas import avaliar
    from trechos import dividir

    SINONIMOS = {"atrasado": "atraso", "passar": "aprovacao", "nota": "media", "aprovado": "aprovacao"}
    palavras_original = buscar.palavras


    def palavras_com_sinonimos(texto: str) -> list[str]:
        return [SINONIMOS.get(p, p) for p in palavras_original(texto)]


    buscar.palavras = palavras_com_sinonimos   # a busca passa a usar a versão nova
    trechos = dividir(ler_paginas(Path("treino_docs") / "regulamento_escola.pdf"))
    codigo = avaliar(trechos, Path("perguntas_teste.csv"))
    print("código:", codigo)
    ```

    **11 de 11**, código 0. A troca vale nos dois lados (pergunta e trecho), porque a busca usa a mesma `palavras()` para os dois. Um dicionário pequeno, feito com as perguntas que **realmente** falharam (o registro e a avaliação mostram quais), resolve muito: é melhorar com base em dados, e não no chute.

---

## 💡 Resumo

- O tira-dúvidas junta **ler ➔ dividir ➔ buscar ➔ responder com fonte**, com IA ou sem.
- **Registre** as perguntas (sem identificar ninguém) para ver o que o documento não responde.
- **Avalie a busca** com perguntas de teste antes de usar, e de novo a cada mudança.
- Sinônimos do assunto, escolhidos pelos erros medidos, resolvem a maior parte dos problemas de vocabulário.

## ➡️ Próximo passo

**[Módulo 04 — Segurança, custos e testes](../modulo_04_seguranca_custos_testes/index.md)**: dados pessoais e LGPD, *prompt injection*, limites e erros da API e a bateria de testes do atendente.
