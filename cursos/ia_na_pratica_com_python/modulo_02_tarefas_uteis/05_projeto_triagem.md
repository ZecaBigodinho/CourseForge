# 05 — Projeto do módulo: triagem de mensagens

> **Curso:** IA na prática com Python  
> **Módulo:** 02 — Tarefas úteis  
> **Tempo estimado:** 2 h  

---

## 🎯 Objetivos

Ao final desta aula, você terá um programa que, a partir de um CSV de mensagens de clientes:

- **Tira dados pessoais** (e-mail, CPF, telefone) antes de mandar qualquer coisa para a API.
- **Classifica** cada mensagem com o classificador **híbrido** (regras + IA).
- **Extrai** os dados dos pedidos em JSON, com validação.
- Monta uma **planilha** com as abas **Mensagens**, **Pedidos** e **Revisar**.

## Pré-requisitos

- Aulas [01](01_classificar_mensagens.md) a [04](04_regras_ou_ia.md) deste módulo, com `classificar.py`, `extrair.py`, `regras_ou_ia.py` e `erros_ia.py` na pasta.
- `openpyxl` instalado no ambiente virtual (`python -m pip install openpyxl==3.1.5`).

---

## O programa

```python title="triagem.py"
"""Triagem de mensagens de clientes: classifica, extrai os pedidos e monta uma planilha.

    python triagem.py mensagens.csv              # usa o Gemini se houver chave no .env
    python triagem.py mensagens.csv --simulado   # só regras, sem IA
"""
import argparse
import csv
import os
import re
import sys
import time
from collections import Counter
from datetime import date
from pathlib import Path

from dotenv import load_dotenv
from openpyxl import Workbook
from openpyxl.styles import Font

from classificar import classificar_simulado
from erros_ia import explicar_erro
from extrair import extrair_pedido, extrair_simulado
from regras_ou_ia import classificar_hibrido

PAUSA = 1.0  # segundos entre chamadas à API (limite por minuto do plano gratuito)
DADOS_PESSOAIS = [  # tirados ANTES de mandar para a API
    (re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"), "[e-mail]"),
    (re.compile(r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b"), "[CPF]"),
    (re.compile(r"(\(?\d{2}\)?\s*)?9?\d{4}-?\d{4}\b"), "[telefone]"),
]


def mascarar(texto: str) -> str:
    for padrao, troca in DADOS_PESSOAIS:
        texto = padrao.sub(troca, texto)
    return texto


def ler_mensagens(caminho: Path) -> list[dict]:
    with open(caminho, newline="", encoding="utf-8-sig") as arq:
        return [linha for linha in csv.DictReader(arq, delimiter=";") if linha.get("mensagem", "").strip()]


class ComIA:
    def __init__(self, cliente, modelo: str):
        self.cliente, self.modelo, self.chamadas = cliente, modelo, 0

    def classificar_todas(self, textos: list[str]) -> list[str]:
        categorias, chamadas = classificar_hibrido(textos, self.cliente, self.modelo)
        self.chamadas += chamadas
        return categorias

    def extrair(self, texto: str, hoje: date):
        time.sleep(PAUSA)
        self.chamadas += 1
        return extrair_pedido(self.cliente, self.modelo, texto, hoje)


class SemIA:
    chamadas = 0

    def classificar_todas(self, textos: list[str]) -> list[str]:
        return [classificar_simulado(t) for t in textos]

    def extrair(self, texto: str, hoje: date):
        return extrair_simulado(texto, hoje)


def montar_planilha(linhas: list[dict], destino: Path) -> None:
    livro = Workbook()
    abas = {"Mensagens": ["Id", "Data", "Mensagem", "Categoria"],
            "Pedidos": ["Id", "Produto", "Quantidade", "Entrega"],
            "Revisar": ["Id", "Mensagem", "Motivo"]}
    planilhas = {}
    for i, (nome, cabecalho) in enumerate(abas.items()):
        aba = livro.active if i == 0 else livro.create_sheet()
        aba.title = nome
        aba.append(cabecalho)
        for celula in aba[1]:
            celula.font = Font(bold=True)
        planilhas[nome] = aba
    for l in linhas:
        planilhas["Mensagens"].append([l["id"], l["data"], l["mensagem"], l["categoria"]])
        if l.get("pedido"):
            p = l["pedido"]
            planilhas["Pedidos"].append([l["id"], p["produto"], p["quantidade"], p["data_entrega"]])
            planilhas["Pedidos"].cell(row=planilhas["Pedidos"].max_row, column=4).number_format = "dd/mm/yyyy"
        if l.get("revisar"):
            planilhas["Revisar"].append([l["id"], l["mensagem"], l["revisar"]])
    planilhas["Mensagens"].column_dimensions["C"].width = 60
    planilhas["Revisar"].column_dimensions["B"].width = 60
    livro.save(destino)


def main(argumentos: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Triagem de mensagens de clientes.")
    parser.add_argument("arquivo", type=Path, help="CSV com as colunas id;data;mensagem")
    parser.add_argument("--simulado", action="store_true", help="só regras, sem chamar a IA")
    args = parser.parse_args(argumentos)
    if not args.arquivo.exists():
        print(f"Arquivo não encontrado: {args.arquivo}")
        return 2

    load_dotenv()
    if args.simulado or not os.getenv("GEMINI_API_KEY"):
        motor, nome = SemIA(), "regras (sem IA)"
    else:
        from google import genai
        motor, nome = ComIA(genai.Client(), os.getenv("GEMINI_MODELO", "gemini-3.8-flash")), "Gemini + regras"

    linhas = ler_mensagens(args.arquivo)
    hoje = date.today()
    textos = [mascarar(l["mensagem"]) for l in linhas]
    try:
        categorias = motor.classificar_todas(textos)
        for linha, texto, categoria in zip(linhas, textos, categorias):
            linha["categoria"] = categoria
            if categoria == "revisar":
                linha["revisar"] = "a IA respondeu algo fora das categorias"
            elif categoria == "pedido":
                pedido, motivo = motor.extrair(texto, hoje)
                linha["pedido"] = pedido
                if not pedido:
                    linha["revisar"] = f"pedido sem dados completos: {motivo}"
    except Exception as erro:
        print(f"A API não respondeu: {explicar_erro(erro)}")
        return 1

    destino = args.arquivo.with_name(f"triagem_{hoje:%Y-%m-%d}.xlsx")
    try:
        montar_planilha(linhas, destino)
    except PermissionError:
        print(f"Não consegui salvar {destino.name}: está aberto no Excel? Feche e rode de novo.")
        return 1
    contagem = Counter(l["categoria"] for l in linhas)
    print(f"[{nome}] {len(linhas)} mensagens: " + ", ".join(f"{c} {n}" for c, n in contagem.most_common()))
    print(f"Pedidos extraídos: {sum(1 for l in linhas if l.get('pedido'))} | "
          f"para revisar: {sum(1 for l in linhas if l.get('revisar'))} | chamadas à IA: {motor.chamadas}")
    print(f"Planilha: {destino}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

## Rodando

```text
> python triagem.py mensagens_exemplo.csv --simulado
[regras (sem IA)] 10 mensagens: pedido 3, dúvida 3, reclamação 2, elogio 1, outro 1
Pedidos extraídos: 3 | para revisar: 0 | chamadas à IA: 0
Planilha: triagem_2026-11-08.xlsx
```

Com chave (sem `--simulado`), as mensagens óbvias continuam com as regras, as duvidosas vão para a IA, e cada pedido tem os dados extraídos pela IA (em JSON, validados). O número de **chamadas à IA** aparece no fim, para você acompanhar o uso da cota.

### Decisões do projeto

| Decisão | Por quê |
|---|---|
| **`mascarar()` antes de tudo** | E-mails, CPFs e telefones dos clientes **não** vão para a API (no plano gratuito, as mensagens podem ser lidas). A planilha guarda a mensagem **original**, que fica no seu computador. |
| **Classificador híbrido** | Menos chamadas, decisões fáceis previsíveis ([aula 04](04_regras_ou_ia.md)). |
| **Pedidos validados** | Pedido com dados incompletos ou estranhos vai para **Revisar**, com o motivo. |
| **Aba Revisar** | Tudo o que o programa não tem certeza vai para uma pessoa: categoria fora da lista, pedido sem dados. |
| **`PAUSA` entre chamadas** | O plano gratuito limita pedidos por minuto. |
| **`ComIA` e `SemIA` com o mesmo jeito** | O resto do programa não muda conforme o caminho (como os motores do [Módulo 01](../modulo_01_api_de_ia/04_conversa_e_motores.md#dois-motores-o-mesmo-jeito)). |

```text
>>> mascarar("Me liga no (11) 98765-4321 ou ana.souza@example.com, CPF 123.456.789-09. Quero 2 bolos dia 14/11.")
'Me liga no [telefone] ou [e-mail], CPF [CPF]. Quero 2 bolos dia 14/11.'
```

!!! warning "Mascarar não é tudo"
    Nomes e endereços escritos no meio do texto ("sou a Ana da rua tal") não são pegos por padrões simples. Para dados de clientes de verdade, o caminho seguro é um plano pago com termos de privacidade adequados, ou não usar a API. O Módulo 04 volta a esse assunto.

---

## ⚠️ Erros comuns

- **CSV com outro separador** (vírgula) ou sem a coluna `mensagem`: o programa não acha as mensagens. Use `id;data;mensagem`.
- **Planilha aberta no Excel** ao rodar de novo: o programa avisa e não grava.
- **Ignorar a aba Revisar**: ela é o que a IA e as regras não resolveram. Alguém precisa olhar.
- **Rodar com mensagens reais** no plano gratuito sem pensar nos dados pessoais.

---

## Exercícios

### Básico (fixação)

Rode a triagem pelo Python (`main([...])`) no modo simulado e confira, abrindo a planilha com o `openpyxl`, quantas linhas há em cada aba.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```python
    from datetime import date
    from pathlib import Path

    from openpyxl import load_workbook

    from triagem import main

    codigo = main(["mensagens_exemplo.csv", "--simulado"])
    livro = load_workbook(Path(f"triagem_{date.today():%Y-%m-%d}.xlsx"))
    linhas = {aba.title: aba.max_row - 1 for aba in livro}
    print(codigo, linhas)
    ```

    `0 {'Mensagens': 10, 'Pedidos': 3, 'Revisar': 0}` (o `- 1` desconta o cabeçalho).

### Intermediário (aplicação)

Teste o caminho **com IA** usando o `ClienteFalso`: quando o pedido tem `response_format`, ele devolve um JSON de pedido; senão, a categoria `"pedido"`. Quantas chamadas foram feitas?

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```python
    import json
    import os

    import google.genai as genai

    import triagem
    from cliente_falso import ClienteFalso

    os.environ["GEMINI_API_KEY"] = "chave-falsa-para-teste"
    triagem.PAUSA = 0   # sem esperar entre chamadas, no teste


    def responder(pedido: dict) -> str:
        if "response_format" in pedido:
            return json.dumps({"produto": "coxinha", "quantidade": 50, "data_entrega": ""})
        return "pedido"


    falso = ClienteFalso(responder)
    genai.Client = lambda *args, **kwargs: falso
    codigo = triagem.main(["mensagens_exemplo.csv"])
    print(codigo, len(falso.pedidos))
    ```

    **8** chamadas: 3 de classificação (as duvidosas) e 5 de extração (os 3 pedidos das regras e as 2 duvidosas que o falso classificou como pedido). A `PAUSA = 0` só existe no teste.

### Avançado (desafio)

Acrescente à `mascarar()` (numa cópia) a troca de **placas de carro** no padrão Mercosul (`ABC1D23`) e no antigo (`ABC-1234`) por `[placa]`, e teste.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```python
    import re

    import triagem

    triagem.DADOS_PESSOAIS.append((re.compile(r"\b[A-Z]{3}-?\d[A-Z0-9]\d{2}\b"), "[placa]"))

    exemplos = ["Meu carro é o ABC1D23, estacionei na frente.", "A placa é ABC-1234.", "Quero 2 bolos."]
    mascarados = [triagem.mascarar(e) for e in exemplos]
    for m in mascarados:
        print(m)
    ```

    A expressão pega as duas formas: três letras, hífen opcional, um número, uma letra **ou** número, e mais dois números. A frase sem placa não muda. Como `DADOS_PESSOAIS` é uma **lista**, acrescentar um padrão não mexe no resto do código.

---

## 💡 Resumo

- **Mascarar** dados pessoais antes da API; a planilha guarda o original no seu computador.
- **Híbrido** para classificar, **JSON validado** para os pedidos, **Revisar** para o resto.
- `ComIA`/`SemIA` com o mesmo jeito; `PAUSA` para respeitar o limite.

## ➡️ Próximo passo

**Módulo 03 — IA com os seus documentos** *(em produção)*: ler PDF e TXT, responder só com base no documento e citar a fonte.
