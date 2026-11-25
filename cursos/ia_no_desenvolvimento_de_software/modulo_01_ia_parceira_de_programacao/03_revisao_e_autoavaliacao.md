# 03 — Revisão, registro e autoavaliação

> **Curso:** IA no desenvolvimento de software  
> **Módulo:** 01 — IA como parceira de programação  
> **Tempo estimado:** 3 min em aula · 20 min de estudo  

---

## 🎯 Objetivos

Ao final desta aula, você será capaz de:

- Revisar código gerado por IA com um checklist.
- Registrar o resultado dos testes numa tabela.
- Avaliar o próprio trabalho pelos indicadores da competência.

---

## Checklist de revisão de código gerado por IA

Use antes de **todo** commit com código sugerido pela IA:

- [ ] **Entendo cada linha** e consigo explicar com as minhas palavras.
- [ ] O código cumpre **cada item do requisito** (não só o caso que foi reclamado).
- [ ] Os testes cobrem o **caminho feliz**, os **limites** e os **dados inválidos**, e **todos passam**.
- [ ] Rodei **todos** os testes do projeto, não só os novos (a correção não quebrou outra coisa).
- [ ] Nenhuma biblioteca, função ou parâmetro **inventado**: conferi na documentação o que eu não conhecia.
- [ ] Nada de **dado sensível** no código: senha, chave de API, dados de pessoas reais.
- [ ] Nenhum texto do usuário entra **direto** em SQL, comando do sistema ou caminho de arquivo.
- [ ] Nomes claros e valores fixos em **constantes**.
- [ ] A mensagem de commit diz **o que** mudou e **por quê** (e cita o chamado).

## Registro dos testes

Registrar o resultado mostra o que foi testado, o que falhou e o que foi feito. Modelo preenchido com a prática da [aula 02](02_pratica_testes_com_ia.md):

| Nº | Caso de teste | Item do RF-07 | Esperado | Antes da correção | Depois |
|---|---|---|---|---|---|
| 1 | D em tudo, 90% | 1 | AP | ✅ passou | ✅ |
| 2 | D em tudo, **75%** (limite) | 1 | AP | ❌ deu RP | ✅ |
| 3 | D em tudo, 74,9% | 2 | RP | ✅ passou | ✅ |
| 4 | Uma ND, 100% | 2 | RP | ✅ passou | ✅ |
| 5 | ND e 50% | 2 | RP | ✅ passou | ✅ |
| 6 | Sem menções | 4 | ValueError | ❌ deu AP | ✅ |
| 7 | Menção "X" | 3 | ValueError | ❌ deu AP | ✅ |
| 8 | Frequência 120 | 5 | ValueError | ❌ deu AP | ✅ |
| 9 | Frequência −5 | 5 | ValueError | ❌ deu RP | ✅ |

**Resumo:** 9 casos; 5 falhas antes da correção (1 do chamado #142 e 4 encontradas pelos testes); 9 de 9 depois. **Ação corretiva:** `>=` no limite e validação das entradas.

!!! tip "Planilha ou README"
    No trabalho, a tabela pode ficar numa planilha, no chamado ou no README do projeto. O importante é ligar cada caso a um **item do requisito**.

## Meu caderno de prompts de desenvolvimento

Guarde os pedidos que funcionam. Estes servem para quase todo trabalho de manutenção:

```text title="Explicar"
Você é um programador [linguagem] experiente ajudando um colega iniciante.
Explique em até 5 linhas o que este código faz. Não corrija nada ainda.
[código]
```

```text title="Testes a partir do requisito"
Você é um testador de software experiente. Contexto: [linguagem, framework de teste].
Requisito: [regras numeradas]
Escreva testes para cada item, com os limites e os dados inválidos.
Formato: só o arquivo de testes, um comentário curto por caso.
```

```text title="Corrigir"
Este código não cumpre o requisito; os testes mostram as falhas.
Corrija para cumprir todos os itens. Formato: arquivo completo + lista do que mudou e por quê.
Requisito: [...]  Código: [...]  Falhas: [saída completa dos testes]
```

```text title="Revisão de segurança"
Você é um revisor de segurança. Aponte riscos neste código (injeção, dados sensíveis,
entradas sem validação), do mais grave para o menos grave, com a correção de cada um.
[código]
```

## Autoavaliação

Marque **D** (desenvolvido) ou **ND** (não desenvolvido) em cada indicador. Um ND indica o que rever: volte ao passo correspondente da [aula 02](02_pratica_testes_com_ia.md).

| Indicador | Evidência nesta prática | D / ND |
|---|---|---|
| Utiliza metodologias de teste de acordo com a funcionalidade | Testes de caminho feliz, de limite e de dados inválidos, ligados ao RF-07. | |
| Tabula o resultado dos testes | Tabela de registro preenchida, antes e depois. | |
| Realiza ajustes e ações corretivas conforme o resultado | `situacao.py` corrigido, 9 de 9 testes passando, checklist cumprido. | |
| Sigilo no tratamento de dados | Nenhum dado real colado no assistente de IA. | |

## ✅ Pergunta de verificação

> Você pede à IA testes para uma função de desconto, colando **só o código**. Todos os testes passam. Isso prova que a função está certa?

??? success "Resposta"
    **Não.** Testes escritos a partir do código descrevem o que o código **faz**, inclusive os defeitos. Para saber se ele está **certo**, os testes precisam vir do **requisito** (a regra do desconto) e incluir os limites. Por isso, na prática, o pedido 2 levava o RF-07, e não o código.

---

## 💡 Resumo

- O checklist transforma "parece certo" em "foi conferido".
- Cada caso de teste aponta para um **item do requisito** e tem o resultado **antes e depois** registrado.
- Guarde os pedidos que funcionam: eles valem em qualquer assistente.

## ➡️ Próximo passo

Continue praticando no curso **[IA na prática com Python](../../ia_na_pratica_com_python/docs/index.md)**, que usa a IA **dentro** dos programas, com testes automáticos, ou volte ao **[Catálogo de cursos](../../catalogo.md)**.
