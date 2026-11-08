# 05 — Projeto do módulo: resumidor de textos

> **Curso:** IA na prática com Python  
> **Módulo:** 01 — Conversando com um modelo por API  
> **Tempo estimado:** 2 h  

---

## 🎯 Objetivos

Ao final desta aula, você terá um programa de terminal que:

- Lê um arquivo **`.txt`** e gera um **resumo** com o tamanho pedido (em frases).
- Usa o **Gemini** quando há chave, ou o **motor simulado** quando não há (ou quando você pedir).
- Confere o arquivo antes (existe? está vazio? é grande demais?) para não gastar a cota à toa.
- **Grava** o resumo num arquivo ao lado do original e mostra palavras e tokens.

## Pré-requisitos

- Aulas [01](01_o_que_e_uma_api_de_ia.md) a [04](04_conversa_e_motores.md) deste módulo, com `motores.py` e `erros_ia.py` na pasta.

---

## O texto de exemplo

Salve como `texto_exemplo.txt` (texto inventado):

```text
A Padaria Pão Quente abriu em 2019 no centro da cidade. No começo, vendia só pão francês e bolo de fubá. Com o tempo, a padaria passou a fazer salgados, tortas e encomendas para festas. Em 2024, a dona, Ana Souza, criou um perfil nas redes sociais para divulgar os produtos. As encomendas pela internet cresceram rápido e hoje representam metade das vendas da padaria. Para dar conta, a padaria contratou dois funcionários e comprou um forno novo. Ana diz que o próximo passo é aceitar pedidos pelo WhatsApp com um catálogo de produtos.
```

## O resumidor

```python title="resumidor.py"
"""Resumidor de textos: lê um .txt e grava o resumo ao lado.

    python resumidor.py texto.txt            # resumo de 2 frases
    python resumidor.py texto.txt --frases 4
"""
import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from erros_ia import explicar_erro
from motores import MotorGemini, MotorSimulado

INSTRUCOES = ("Você resume textos em português do Brasil. Use só informações que estão no texto, "
              "sem acrescentar opiniões nem fatos novos. Responda apenas com o resumo.")
LIMITE_CARACTERES = 20_000  # textos maiores gastam muitos tokens: divida antes


def escolher_motor(simulado: bool):
    load_dotenv()
    if simulado or not os.getenv("GEMINI_API_KEY"):
        return MotorSimulado(), "simulado"
    return MotorGemini(INSTRUCOES, os.getenv("GEMINI_MODELO", "gemini-3.8-flash")), "Gemini"


def main(argumentos: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Resume um arquivo de texto.")
    parser.add_argument("arquivo", type=Path, help="arquivo .txt com o texto")
    parser.add_argument("--frases", type=int, default=2, help="tamanho do resumo, em frases (padrão: 2)")
    parser.add_argument("--simulado", action="store_true", help="usa o motor simulado, mesmo com chave")
    args = parser.parse_args(argumentos)

    if not args.arquivo.exists():
        print(f"Arquivo não encontrado: {args.arquivo}")
        return 2
    texto = args.arquivo.read_text(encoding="utf-8").strip()
    if not texto:
        print("O arquivo está vazio.")
        return 2
    if len(texto) > LIMITE_CARACTERES:
        print(f"O texto tem {len(texto)} caracteres; o limite deste resumidor é {LIMITE_CARACTERES}.")
        return 2

    motor, nome = escolher_motor(args.simulado)
    try:
        resumo = motor.responder(texto, frases=args.frases)
    except Exception as erro:
        print(f"A API não respondeu: {explicar_erro(erro)}")
        return 1

    destino = args.arquivo.with_name(f"{args.arquivo.stem}_resumo.txt")
    destino.write_text(resumo + "\n", encoding="utf-8")
    print(resumo)
    print(f"\n[motor: {nome} | {len(texto.split())} palavras -> {len(resumo.split())} palavras"
          f" | tokens: {motor.tokens_usados}] Resumo salvo em {destino.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

## Rodando

Sem chave (ou com `--simulado`):

```text
> python resumidor.py texto_exemplo.txt
A Padaria Pão Quente abriu em 2019 no centro da cidade. Com o tempo, a padaria passou a fazer salgados, tortas e encomendas para festas.

[motor: simulado | 94 palavras -> 25 palavras | tokens: 0] Resumo salvo em texto_exemplo_resumo.txt
```

Com chave, o resumo vem do Gemini: escrito **com outras palavras** e podendo **juntar** informações de frases diferentes (o simulado só copia frases inteiras, e por isso deixou de fora o crescimento das vendas pela internet). A linha final mostra os tokens gastos.

```powershell
python resumidor.py texto_exemplo.txt --frases 3
python resumidor.py texto_exemplo.txt --simulado
```

### Decisões do projeto

| Decisão | Por quê |
|---|---|
| **Conferir o arquivo antes** de chamar a API | Erro de digitação no nome ou arquivo vazio não devem gastar cota. |
| **`LIMITE_CARACTERES`** | Textos enormes gastam muitos tokens (e podem passar do limite do modelo). Para textos longos, divida em partes (Módulo 03 do curso). |
| **Instruções "só com o que está no texto"** | Resumo não é lugar de opinião nem de "completar" com informações que o texto não tem. |
| **`--simulado`** | Testar o programa sem gastar, mesmo com a chave configurada. |
| **Resumo gravado ao lado** (`_resumo.txt`) | O original nunca é alterado ([regra de Automação](../../automacao_com_python/modulo_01_arquivos_e_pastas/01_o_que_vale_automatizar.md#as-regras-de-seguranca)). |
| **Códigos de saída** (0, 1, 2) | 0 = deu certo; 1 = a API falhou; 2 = problema com o arquivo. Úteis se o resumidor for usado por outro programa. |

!!! warning "Confira o resumo"
    Um resumo de IA pode **omitir** algo importante ou, raramente, **afirmar** algo que não estava no texto. Para trabalhos escolares e documentos importantes, leia o original e confira. E lembre: textos com **dados pessoais** não vão para o plano gratuito ([aula 01](01_o_que_e_uma_api_de_ia.md#o-plano-gratuito-limites-privacidade-e-idade)).

---

## ⚠️ Erros comuns

- **Resumir o próprio resumo** sem querer (`texto_exemplo_resumo.txt`): o programa aceita, mas o resultado fica cada vez mais pobre.
- **Texto salvo em outra codificação** (ANSI): acentos viram `�`. Salve o `.txt` em **UTF-8** (no VS Code, canto inferior direito).
- **Pedir 1 frase para um texto de 20 páginas**: o resumo fica genérico demais. Resuma por partes.
- **Confiar no resumo sem ler** em situações importantes.

---

## Exercícios

### Básico (fixação)

Rode o resumidor pelo Python (chamando `main([...])`), no motor simulado, pedindo **3 frases**. Confira o arquivo gravado.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```python
    from pathlib import Path

    from resumidor import main

    codigo = main(["texto_exemplo.txt", "--frases", "3", "--simulado"])
    resumo = Path("texto_exemplo_resumo.txt").read_text(encoding="utf-8")
    print(codigo)
    print(resumo)
    ```

    `main()` recebe a lista de argumentos como se fossem digitados no terminal. Código 0, e o resumo com 3 frases (a terceira é a das encomendas pela internet).

### Intermediário (aplicação)

Teste o resumidor com o **motor do Gemini** usando o `ClienteFalso`, sem chave real: confira que o pedido levou as **instruções** de resumo e o texto com "Resuma em no máximo 2 frases".

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```python
    import os

    import google.genai as genai

    from cliente_falso import ClienteFalso
    from resumidor import main

    os.environ["GEMINI_API_KEY"] = "chave-falsa-para-teste"
    falso = ClienteFalso("A padaria cresceu com as encomendas pela internet.")
    genai.Client = lambda *args, **kwargs: falso

    codigo = main(["texto_exemplo.txt"])
    pedido = falso.pedidos[0]
    print(codigo, pedido["input"][:31])
    print(pedido["system_instruction"][:40])
    ```

    O resumo gravado é o do cliente falso, e o pedido começa com `Resuma em no máximo 2 frases:`. Assim se testa o caminho "com chave" inteiro, inclusive a montagem do pedido, sem chamar a API.

### Avançado (desafio)

Faça o resumidor aceitar **uma pasta**: resumir todos os `.txt` dela (menos os que já terminam em `_resumo.txt`) e mostrar, no fim, o total de arquivos e de tokens. Use o motor simulado para testar.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```python
    from pathlib import Path

    from motores import MotorSimulado

    pasta = Path("textos")
    pasta.mkdir(exist_ok=True)
    for i in (1, 2):
        (pasta / f"texto_{i}.txt").write_text(Path("texto_exemplo.txt").read_text(encoding="utf-8"), encoding="utf-8")

    motor = MotorSimulado()
    resumidos = 0
    for arquivo in sorted(pasta.glob("*.txt")):
        if arquivo.stem.endswith("_resumo"):
            continue
        resumo = motor.responder(arquivo.read_text(encoding="utf-8"), frases=2)
        arquivo.with_name(f"{arquivo.stem}_resumo.txt").write_text(resumo + "\n", encoding="utf-8")
        resumidos += 1
    print(f"{resumidos} arquivos resumidos, {motor.tokens_usados} tokens")
    ```

    Pular os `_resumo.txt` evita resumir o que já é resumo (e, rodando de novo, não gera `texto_1_resumo_resumo.txt`). Um **só** motor para todos os arquivos permite somar os tokens. Com o Gemini, acrescente uma pausa entre os pedidos para não estourar o limite por minuto ([Automação, Módulo 04](../../automacao_com_python/modulo_04_email_e_agendamento/02_servidor_de_teste.md)).

---

## 💡 Resumo

- O resumidor confere o arquivo, escolhe o motor (Gemini ou simulado), resume e **grava ao lado**.
- Instruções de resumo: **só o que está no texto**, sem opinião.
- `--simulado` e o **cliente falso** testam tudo sem gastar a cota.
- Confira resumos importantes e não mande dados pessoais no plano gratuito.

## ➡️ Próximo passo

**Módulo 02 — Tarefas úteis** *(em produção)*: classificar mensagens, extrair dados em JSON e reescrever textos com tom definido.
