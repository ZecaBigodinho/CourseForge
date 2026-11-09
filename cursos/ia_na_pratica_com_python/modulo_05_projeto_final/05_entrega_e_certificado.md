# 05 — Entrega e certificado

> **Curso:** IA na prática com Python  
> **Módulo:** 05 — Projeto final  
> **Tempo estimado:** 1 h 30 min (mais a demonstração)  

---

## 🎯 Objetivos

Ao final desta aula, você terá:

- A **bateria de testes** final do atendente, com os casos de encomenda, e o **relatório** para a entrega.
- O **README** do projeto e o `.env.example`.
- O **roteiro da demonstração**, o **checklist** e a **rubrica** de avaliação.
- O **certificado** do curso.

## Pré-requisitos

- Aulas [01](01_planejando_o_atendente.md) a [04](04_a_janela.md), com o atendente funcionando no lote, no terminal e na janela.

---

## A bateria final

A bateria do Módulo 04 testava respostas; agora ela testa também as **encomendas**. Acrescente três casos ao `casos_atendente.csv`:

```text
14;Quero 20 coxinhas para amanhã;pedido;R$ 140,00;
15;Quero 3 pizzas para amanhã;pedido;precisamos;Anotamos
16;Preciso de 150 pães de queijo para amanhã;pedido;precisamos;Anotamos
```

- **14:** encomenda válida, com o total **do cardápio**.
- **15 e 16:** pedidos que **não podem** ser anotados (produto fora do cardápio, quantidade acima do limite): a resposta pede os dados e **não** diz "Anotamos".

```text
> python bateria.py casos_atendente.csv
  caso 13 FALHOU: categoria 'outro', esperava 'dúvida'; faltou 'R$ 7,00'
09/11/2026 19:12 · 15 de 16 casos aprovados
Relatório: relatorio_testes.md
```

O caso 13 ("Tem coxinha hoje", sem "?") continua mostrando o limite das regras. Com a IA (`--com-ia`), ele passa. Sem chave, ele é o assunto do exercício avançado: uma **melhoria** sua.

O **`relatorio_testes.md`** entra na entrega: ele mostra, caso a caso, o que o atendente faz, inclusive o que ele **recusa**.

## O README

Todo projeto que outra pessoa vai usar precisa de um **README.md** na pasta principal. Modelo:

```markdown
# Atendente da Padaria Pão Quente

Responde as mensagens dos clientes com os dados reais da padaria (cardápio e horário),
anota encomendas com o total calculado pelo cardápio e passa para a equipe o que precisa
de uma pessoa. Registra tudo em atendimentos.xlsx. Funciona com o Gemini ou sem IA.

## Instalação

    python -m venv .venv
    .venv\Scripts\activate
    python -m pip install google-genai==2.34.0 python-dotenv==1.2.1 openpyxl==3.1.5 customtkinter==5.2.2 pytest==8.4.2
    copy .env.example .env      (só para usar a IA: coloque a sua chave no .env)

## Uso

    python pao_quente.py lote mensagens_padaria.csv     (um arquivo de mensagens)
    python pao_quente.py conversa                       (no terminal)
    python pao_quente.py janela                         (na janela)

Acrescente --simulado (antes do comando) para usar só as regras, sem IA.

## Segurança

- Dados pessoais (e-mail, CPF, telefone, cartão, CEP) são mascarados antes de qualquer
  envio e na planilha. Mensagens com dados de saúde ou segredos vão para a equipe.
- Tentativas de dar ordens ao atendente vão para a equipe. As respostas da IA são
  conferidas (preço, promessas, dados pessoais) antes de sair.
- Valores de encomendas são calculados pelo programa, nunca pela IA.
- Limite de 200 chamadas à API por execução.

## Testes

    python -m pytest testes                 (nenhum teste chama a API)
    python bateria.py casos_atendente.csv   (gera relatorio_testes.md)
```

E o **`.env.example`**, que vai junto (sem a chave de verdade):

```text
GEMINI_API_KEY=coloque-a-sua-chave-aqui
GEMINI_MODELO=gemini-3.8-flash
```

!!! danger "O `.env` não vai na entrega"
    Se o projeto for para o GitHub, o `.env` fica no `.gitignore` (veja o [Módulo 01](../modulo_01_api_de_ia/01_o_que_e_uma_api_de_ia.md#com-chave-o-env)). A planilha `atendimentos.xlsx` também não precisa ir: ela é gerada pelo programa.

## O roteiro da demonstração (5 a 8 minutos)

| Tempo | Mostre |
|---|---|
| 1 min | **O problema:** quantas mensagens a padaria recebe e o que o atendente faz (e não faz) |
| 2 min | **`python pao_quente.py lote mensagens_padaria.csv`** e a planilha: as três abas, as encomendas com o total, o motivo de cada caso para revisar e o telefone mascarado |
| 1 min | **A janela:** uma dúvida de preço, uma encomenda e um caso para revisar, com o motivo na barra de status |
| 1 min | **Segurança ao vivo:** uma tentativa de injeção e uma mensagem com CPF |
| 1 min | **Os testes:** `python -m pytest testes` e a bateria com o relatório |
| 1 min | **A sua melhoria**, com o caso novo na bateria que prova que ela funciona |

!!! warning "Só mensagens de treino"
    A demonstração usa mensagens **inventadas**. Mensagens de clientes de verdade são dados pessoais e, no plano gratuito, não podem ir para a API.

Quem tem chave pode mostrar o modo com IA; quem não tem (ou tem menos de 18 anos) demonstra **tudo sem IA**, e a avaliação é a mesma.

## Checklist final

- [ ] `python pao_quente.py --simulado lote mensagens_padaria.csv` roda e gera a planilha com as três abas.
- [ ] A conversa no terminal e a janela funcionam e registram o canal certo.
- [ ] `python -m pytest testes` passa (pelo menos os 42 testes do curso).
- [ ] A bateria roda e o `relatorio_testes.md` está na entrega, com os casos que falham **explicados**.
- [ ] O `.env` está fora da entrega e existe um `.env.example`.
- [ ] O README explica instalação, uso, segurança e testes.
- [ ] Você fez **pelo menos uma melhoria** própria, com **um caso novo na bateria** ou **um teste novo**. Ideias: o horário ou o botão Limpar na janela ([aula 04](04_a_janela.md)); o prazo especial da torta ([aula 02](02_encomendas_com_regras.md)); o resumo do dia como subcomando ([aula 03](03_registro_e_linha_de_comando.md)); um produto novo no cardápio; a regra do caso 13 (exercício avançado abaixo).

## Rubrica de avaliação

| Critério | Precisa melhorar | Bom | Excelente |
|---|---|---|---|
| **Funciona** | Algum comando quebra com as mensagens de treino | Lote, conversa e janela funcionam | Funciona também com mensagens novas criadas pelo aluno |
| **Respostas corretas** | Inventa preço ou anota encomenda inválida | Respostas e encomendas corretas, total pelo cardápio | Tudo isso, mais regras novas da padaria com testes |
| **Segurança** | Dados pessoais na API ou na planilha; IA decidindo valores | Máscaras, casos sensíveis e injeção para a equipe, conferência das respostas | Tudo isso, explicado com clareza na demonstração |
| **Testes** | Sem testes ou testes falhando | Pytest e bateria passando (com o caso 13 explicado) | Testes e casos novos para a melhoria feita |
| **Organização** | Regras dentro da janela, código repetido | Cada arquivo com uma função clara | Funções pequenas, nomes claros, README que um colega seguiu sozinho |
| **Demonstração** | Confusa ou com dados reais | Completa, no tempo | Responde com segurança "e se..." do professor |

!!! success "O que libera o certificado"
    O certificado do curso é liberado com a **entrega e a demonstração do Atendente da Padaria Pão Quente**: funcionando com as mensagens de treino, com o pytest e a bateria (com o relatório), o README e pelo menos uma melhoria própria.

!!! note "Para o professor"
    Na demonstração, peça ao aluno para digitar na janela uma mensagem que **você** inventar na hora (uma injeção diferente, um CPF sem pontos, uma encomenda para "depois de amanhã"). Boa pergunta final: *"O que precisaria mudar antes de usar isto com clientes de verdade?"* (Resposta esperada: plano pago com termos de privacidade adequados ou nenhum dado pessoal na API; combinar com a dona da padaria quem revisa as respostas; testar com mais mensagens reais anonimizadas; manter uma pessoa enviando as respostas.)

---

## Exercícios

### Básico (fixação)

Acrescente os três casos de encomenda ao `casos_atendente.csv` (pelo Python) e rode a bateria.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```python
    from pathlib import Path

    from bateria import main

    casos = Path("casos_atendente.csv")
    novos = ("14;Quero 20 coxinhas para amanhã;pedido;R$ 140,00;\n"
             "15;Quero 3 pizzas para amanhã;pedido;precisamos;Anotamos\n"
             "16;Preciso de 150 pães de queijo para amanhã;pedido;precisamos;Anotamos\n")
    casos.write_text(casos.read_text(encoding="utf-8") + novos, encoding="utf-8")
    codigo = main([str(casos)])
    ```

    `15 de 16 casos aprovados`: os três novos passam; só o 13 falha.

### Intermediário (aplicação)

Escreva `conferir_entrega.py`: roda o pytest e a bateria e diz se o projeto está pronto para entregar. Falhas **conhecidas e explicadas** (como o caso 13 sem IA) ficam numa lista e não impedem a entrega; qualquer outra, sim.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```python title="conferir_entrega.py"
    """Confere o projeto antes da entrega: pytest + bateria (com as falhas conhecidas explicadas)."""
    import subprocess
    import sys
    from pathlib import Path

    import bateria

    CONHECIDAS = {"13": "sem IA, as regras só reconhecem dúvida com '?' (com IA, passa)"}


    def main() -> int:
        pytest = subprocess.run([sys.executable, "-m", "pytest", "-q", "testes"], capture_output=True, text=True)
        print("pytest:", pytest.stdout.strip().splitlines()[-1])
        resultados = bateria.rodar(bateria.ler_casos(Path("casos_atendente.csv")))
        inesperadas = [caso["id"] for caso, _, falhas in resultados if falhas and caso["id"] not in CONHECIDAS]
        for caso, _, falhas in resultados:
            if falhas and caso["id"] in CONHECIDAS:
                print(f"caso {caso['id']}: falha conhecida ({CONHECIDAS[caso['id']]})")
        if pytest.returncode != 0 or inesperadas:
            print("NÃO está pronto. Casos com falha inesperada:", ", ".join(inesperadas) or "-")
            return 1
        print("Pronto para entregar.")
        return 0


    if __name__ == "__main__":
        sys.exit(main())
    ```

    Rodando `python conferir_entrega.py`: o pytest passa, o caso 13 aparece como falha conhecida e a saída termina em `Pronto para entregar.`. Se uma mudança sua quebrar **outro** caso, o script avisa. Uma falha conhecida precisa de uma **explicação escrita**: sem ela, é só um problema escondido.

### Avançado (desafio)

Faça o caso 13 passar **sem IA**: acrescente `"tem "` às palavras de **dúvida** do `classificar.py`. Antes, acrescente à bateria o caso `17;O bolo tem gosto de queimado;reclamação;gerência;`, para garantir que a regra nova não estraga uma reclamação que também tem "tem".

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```python
    from pathlib import Path

    import classificar
    from bateria import main

    casos = Path("casos_atendente.csv")
    novos = ("14;Quero 20 coxinhas para amanhã;pedido;R$ 140,00;\n"
             "15;Quero 3 pizzas para amanhã;pedido;precisamos;Anotamos\n"
             "16;Preciso de 150 pães de queijo para amanhã;pedido;precisamos;Anotamos\n"
             "17;O bolo tem gosto de queimado;reclamação;gerência;\n")
    casos.write_text(casos.read_text(encoding="utf-8") + novos, encoding="utf-8")

    classificar.PALAVRAS["dúvida"].append("tem ")   # no arquivo: "dúvida": ["?", "tem "]
    codigo = main([str(casos)])
    ```

    `17 de 17 casos aprovados` e código **0**. O caso 17 passa porque as regras de **reclamação** vêm **antes** das de dúvida ("queimado" decide primeiro), como o [Módulo 02](../modulo_02_tarefas_uteis/01_classificar_mensagens.md) já tinha avisado: a ordem importa. Escrever o caso que poderia quebrar **antes** da mudança é o hábito que separa uma melhoria de um remendo. No projeto, faça a troca **no arquivo** `classificar.py` e atualize o `CONHECIDAS` do `conferir_entrega.py` (o 13 deixa de ser falha conhecida).

---

## Parabéns! 🎉

Você terminou o curso **IA na prática com Python**. Agora você sabe:

- chamar um modelo de IA por **API**, com a chave no `.env`, instruções de sistema, conversa com memória e tratamento de erros;
- **classificar**, **extrair dados em JSON** com validação, **reescrever** com tom definido e decidir quando **não** usar IA;
- responder **só com base em documentos**, com busca, "não encontrei" e **fonte**;
- proteger **dados pessoais** (LGPD), resistir a **prompt injection**, controlar **erros, limites e custos**;
- **testar** tudo sem gastar a cota, com o cliente falso, IAs de mentira e o pytest;
- juntar tudo num **atendente** com regras, registro, linha de comando e janela.

E, acima de tudo, a regra que atravessa o curso: **a IA escreve; o seu programa confere e decide.**

!!! tip "Continue estudando"
    - **[Segurança digital](../../seguranca_digital/docs/index.md):** os golpes e cuidados do outro lado, o de quem recebe as mensagens.
    - **[Automação com Python](../../automacao_com_python/docs/index.md):** agende o atendimento em lote e gere relatórios do dia em PDF.
    - **[Git e GitHub](../../python_para_desktop/modulo_05_git_github/index.md):** versione o projeto, com o `.env` fora do repositório, e publique o README.
    - **[Catálogo de cursos](../../catalogo.md).**
