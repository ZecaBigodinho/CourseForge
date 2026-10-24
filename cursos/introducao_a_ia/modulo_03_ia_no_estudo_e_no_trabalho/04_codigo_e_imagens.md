# 04 — Código e imagens com IA

> **Curso:** Introdução à IA  
> **Módulo:** 03 — IA no estudo e no trabalho  
> **Tempo estimado:** 1 h 30 min  

---

## Objetivos

Ao final desta aula, você será capaz de:

- Pedir à IA para **explicar** um código linha por linha e **encontrar** um erro.
- Pedir um trecho de código **e testá-lo** antes de usar.
- Reconhecer os riscos do código gerado: erros escondidos, **bibliotecas que não existem** e **segredos** no código.
- Escrever um bom **pedido de imagem** e refinar o resultado.
- Reconhecer os limites e os cuidados das imagens geradas: **texto errado**, **estereótipos**, **direitos** e **rotulagem**.

## Pré-requisitos

- [Aula 03](03_planilhas_e_dados.md) (testar o que a IA gera).
- Para a parte de código: ter visto o começo do [curso de Python](../../python_para_desktop/docs/index.md) ajuda, mas não é obrigatório — os exemplos são curtos e explicados.

---

## Parte 1 — Código

### Explicar e depurar

Os usos mais seguros para quem está aprendendo a programar:

| Pedido | Exemplo |
|---|---|
| **Explicar** | “Explique este código Python linha por linha, para um iniciante.” |
| **Encontrar o erro** | “Este código deveria somar os preços, mas mostra só o último. Onde está o erro? Explique antes de corrigir.” |
| **Entender a mensagem de erro** | “O Python mostrou `NameError: name 'totl' is not defined`. O que significa?” |
| **Tutor** | “Não me dê o código; me dê uma dica de cada vez.” (Módulo 02, aula 03) |

### Pedir código

```text
Escreva uma função em Python chamada situacao(nota1, nota2) que calcule a média das duas notas
e devolva "Aprovado" se a média for 6 ou mais, e "Reprovado" se for menor.
Inclua 3 testes com assert, inclusive o caso da média exatamente 6.
Explique o código em 3 linhas.
```

Repare no pedido: **nome da função**, **entradas e saída**, a **regra** e **testes** — inclusive o caso de limite (média 6), onde os erros costumam se esconder (lembra do `>` × `>=` no Excel?).

### Os riscos do código gerado

- **Parece certo e está errado:** o código roda, mas o resultado está errado em alguns casos. Por isso, **teste** com casos que você sabe a resposta.
- **Bibliotecas que não existem:** a IA pode sugerir instalar um pacote com nome inventado — e há golpistas que publicam pacotes com esses nomes. Antes de instalar, confira se o pacote existe e é conhecido (página oficial, número de downloads, documentação).
- **Segredos no código:** nunca cole **senhas** ou **chaves de API** no prompt nem deixe no código; use o arquivo `.env` (curso de Python e Módulo 05 deste curso).
- **Você precisa entender:** se não entende o que o código faz, não consegue consertar quando quebrar — e não deve entregar como seu.

!!! warning "Na escola, siga a regra do professor"
    Em exercícios de programação, pedir o código pronto pode ser **proibido** — e quase sempre atrapalha o aprendizado. Use explicação, dicas e depuração.

---

## Parte 2 — Imagens

Muitos assistentes (e editores como o Canva) geram imagens a partir de um texto. O pedido de imagem também tem receita:

| Elemento | Exemplo |
|---|---|
| **Assunto** | “uma banca de feira com frutas tropicais” |
| **Estilo** | “ilustração plana, cores vivas” · “foto realista” · “aquarela” |
| **Composição** | “vista de frente, com espaço vazio no topo para um título” |
| **Cores e luz** | “tons de laranja e verde, luz da manhã” |
| **Formato** | “horizontal, para um banner” · “quadrado, para post” |
| **Evitar** | “sem texto na imagem, sem pessoas” |

### Os limites

- **Texto dentro da imagem** costuma sair com letras erradas. Gere a imagem **sem texto** e escreva o título no PowerPoint, no Canva ou no Word.
- **Detalhes** (mãos, objetos pequenos, placas) podem sair estranhos. Olhe a imagem com atenção antes de usar.
- **Estereótipos:** pedir “um médico” ou “uma pessoa cientista” pode gerar sempre o mesmo tipo de pessoa — o **viés dos dados** do Módulo 01. Descreva a diversidade que você quer.

### Os cuidados

!!! danger "Pessoas reais, marcas e enganos"
    **Não** gere imagens de **pessoas reais** (colegas, professores, famosos) — muito menos em situações falsas ou constrangedoras. Isso pode violar direitos de imagem e configurar crime. Evite também **logotipos** e **personagens** protegidos. E **rotule**: “Imagem gerada por IA” quando a imagem puder ser confundida com uma foto real.

- **Direitos autorais** das imagens geradas são um assunto ainda em discussão nos tribunais e nas leis — o Módulo 04 trata disso. Para trabalhos e materiais da empresa, siga as regras da escola ou da empresa.
- Pedir “no estilo de [artista vivo]” é questionado por muitos artistas. Prefira descrever o **estilo** (“traço de nanquim, cores chapadas”).

---

??? note "Equivalentes e alternativas"
    | Tarefa | Com qualquer assistente | Outras ferramentas gratuitas |
    |---|---|---|
    | Explicar e depurar código | Prompt de explicação ou tutor | O próprio VS Code mostra os erros (Módulo 00 do curso de Python) |
    | Testar código | Rodar no seu computador ou em um ambiente on-line | — |
    | Gerar imagens | Assistentes com geração de imagem | Editores como o Canva (recursos de IA conforme o plano) |
    | Imagens sem IA | — | Bancos de imagens com licença livre e as imagens de banco do Office (Módulo 03 do curso de Office) |

---

## ⚠️ Erros comuns

- **Usar o código sem testar.** Teste com casos conhecidos e com o caso de limite.
- **Instalar o pacote que a IA mandou** sem conferir se ele existe.
- **Colar senha ou chave de API** no prompt.
- **Pedir texto dentro da imagem** e publicar com erro de ortografia.
- **Gerar imagem de pessoa real** ou usar sem rotular uma imagem que parece foto.

---

## Exercícios

### Básico (fixação)

Este código deveria mostrar o **total** dos preços (40,50), mas mostra 20,0. Peça à IA para **explicar o erro antes de corrigir**, e depois corrija você mesmo.

```python
precos = [12.5, 8.0, 20.0]
total = 0
for p in precos:
    total = p
print("Total:", total)
```

<!-- gabarito -->
??? success "Gabarito — Básico"
    **O erro:** dentro do `for`, `total = p` **troca** o valor do total pelo preço da vez, em vez de **somar**. No fim, sobra só o último preço (20,0).

    **Correção:**

    ```python
    precos = [12.5, 8.0, 20.0]
    total = 0
    for p in precos:
        total += p
    print("Total:", total)
    ```

    Saída: `Total: 40.5`. (`total += p` é o mesmo que `total = total + p`.) Também daria para usar `print("Total:", sum(precos))`.

### Intermediário (aplicação)

Use o prompt da aula para pedir a função `situacao(nota1, nota2)` com os testes. **Rode** o código (no VS Code, no terminal ou em um ambiente on-line) e confira os testes. Acrescente **um teste seu** que a IA não fez.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    Uma resposta correta:

    ```python
    def situacao(nota1, nota2):
        media = (nota1 + nota2) / 2
        if media >= 6:
            return "Aprovado"
        return "Reprovado"

    assert situacao(7, 5) == "Aprovado"     # média 6,0
    assert situacao(5, 6.5) == "Reprovado"  # média 5,75
    assert situacao(6, 6) == "Aprovado"     # média 6,0 (limite)
    assert situacao(10, 1) == "Reprovado"   # média 5,5 (teste a mais)
    print("todos os testes passaram")
    ```

    Saída: `todos os testes passaram`. **Confira no código da IA:** se usou `>` em vez de `>=`, o teste da média exatamente 6 **falha** (`AssertionError`) — é para isso que serve o caso de limite.

### Avançado (desafio)

1. Peça uma imagem para o **cartaz da promoção de Dia das Crianças** da aula 02, usando a receita de imagem, **sem texto** e com espaço para o título. Faça **dois refinamentos** e monte o cartaz com o título no PowerPoint ou no Canva, rotulando a imagem.
2. Peça **quatro imagens** de “uma pessoa trabalhando como engenheira” sem dar outras características. Observe quem aparece. Depois, reescreva o pedido para obter **diversidade** e compare.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    1. Um pedido possível: “Ilustração plana, cores vivas, brinquedos coloridos (pipa, bola, carrinho, boneca) espalhados em um fundo amarelo, vista de cima, **espaço vazio na parte de cima** para um título, formato vertical, **sem texto e sem pessoas**.” Refinamentos típicos: “menos objetos, mais espaço vazio”; “cores mais suaves”. No cartaz: título e datas digitados por você (6 a 12 de outubro) e, no rodapé, “Imagem gerada por IA”.
    2. O que costuma acontecer: as quatro imagens mostram pessoas **muito parecidas** (mesmo gênero, idade e tom de pele) — é o **viés** dos dados de treino. Um pedido melhor: “quatro pessoas diferentes trabalhando como engenheiras — mulheres e homens, de idades e tons de pele variados, em uma obra e em um laboratório”. **Registre** a comparação: o que mudou e por que isso importa em um material que vai ser visto por muita gente.

---

## 💡 Resumo

- Código: **explicar**, **depurar** e pedir com **regra e testes**; **teste** sempre, inclusive o caso de limite.
- Riscos: erro escondido, **pacote inventado**, **segredo no código**, usar o que não entende.
- Imagem: **assunto, estilo, composição, cores, formato e o que evitar**; título fora da imagem.
- Cuidados: **estereótipos**, **pessoas reais**, marcas, direitos e **rótulo** de imagem gerada por IA.

## ➡️ Próximo passo

**[05 — Projeto do módulo: uma tarefa real com IA](05_projeto_tarefa_real_com_ia.md)**: escolher uma tarefa sua, fazer com IA do começo ao fim e avaliar se valeu a pena.
