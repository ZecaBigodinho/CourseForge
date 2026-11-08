# 02 — Senha forte e frase-senha

> **Curso:** Segurança digital e cidadania online  
> **Módulo:** 01 — Senhas e contas  
> **Tempo estimado:** 50 min  

---

## 🎯 Objetivos

Ao final desta aula, você será capaz de:

- Explicar por que o **tamanho** da senha importa mais que os símbolos.
- Reconhecer senhas fracas, mesmo as que "parecem" fortes.
- Criar uma **frase-senha** longa e fácil de lembrar.
- Saber quando trocar uma senha (e quando não precisa).
- Responder às "perguntas de segurança" sem facilitar a vida de golpistas.

## Pré-requisitos

- [Aula 01](01_por_que_as_contas_sao_o_alvo.md): o mapa das suas contas.

---

## Como uma senha é "quebrada"

Quando um site é invadido, as senhas em geral não vazam escritas: vazam **embaralhadas** (um código que não dá para desfazer). Para descobrir a senha, o golpista põe um programa para **testar combinações**: embaralha cada tentativa do mesmo jeito e compara. Um computador com boas placas de vídeo testa **bilhões de tentativas por segundo**.

E ele não começa pelo `aaaa`. Começa pelas senhas mais comuns, por palavras do dicionário, nomes, datas e as "trocas espertas" que todo mundo faz: `a` por `@`, `o` por `0`, `!` no final.

!!! danger "Estas senhas caem em segundos"
    `123456` · `senha123` · `brasil2026` · `flamengo10` · `Ana2008!` · `P@ssw0rd` · `qwerty` · nome do filho + ano · data de nascimento.

    `P@ssw0rd` parece complicada, mas é a palavra *password* com trocas que os programas já conhecem. `Ana2008!` é nome + ano + exclamação, o modelo mais usado no Brasil.

## Tamanho é o que mais importa

Cada caractere a mais **multiplica** o número de combinações. Veja quanto tempo um computador levaria para testar **todas** as combinações de cada tipo de senha, fazendo 10 bilhões de tentativas por segundo:

| Tipo de senha | Exemplo do formato | Tempo para testar tudo |
|---|---|---|
| 8 letras minúsculas | `kbxtqrma` | **21 segundos** |
| 8 caracteres misturando tudo (A-z, 0-9, símbolos) | `k#8Tq!r2` | cerca de **7 dias** |
| 12 letras minúsculas | `kbxtqrmavlez` | cerca de **110 dias** |
| 4 palavras sorteadas | `girafa-pastel-trilho-nuvem` | cerca de **4 dias** |
| 5 palavras sorteadas | `girafa-pastel-trilho-nuvem-sabonete` | cerca de **90 anos** |
| 16 letras minúsculas | `kbxtqrmavlezpowd` | cerca de **140 mil anos** |
| 6 palavras sorteadas | `girafa-pastel-trilho-nuvem-sabonete-viola` | cerca de **700 mil anos** |

!!! info "Como esses números foram calculados"
    Combinações possíveis ÷ 10 bilhões por segundo. Exemplos: 8 minúsculas = 26⁸ ≈ 209 bilhões de combinações (21 s); palavras sorteadas de uma lista de 7.776 palavras: 5 palavras = 7.776⁵ ≈ 28 quintilhões (≈ 90 anos). Vale **só para senhas sorteadas de verdade**. Uma senha "inventada de cabeça" costuma seguir um padrão e cai bem antes.

**Conclusão:** uma senha **longa** só com palavras simples ganha de uma senha **curta** cheia de símbolos, e ainda é mais fácil de lembrar.

## A técnica da frase-senha

Uma **frase-senha** é uma sequência de palavras **sem relação entre si**. Para ser forte:

1. **Pelo menos 5 palavras**, sorteadas, sem formar uma frase conhecida.
2. **Nada sobre você:** nem nomes da família, nem time, nem datas, nem cidade.
3. Separe as palavras com um caractere (`-`, `.` ou espaço, se o site aceitar).

**Como sortear de verdade:** abra um livro ou dicionário numa página qualquer, aponte uma palavra sem olhar e repita cinco vezes. Ou peça ao **gerenciador de senhas** ([aula 03](03_gerenciador_de_senhas.md)): quase todos têm a opção de gerar frase-senha.

!!! example "Exemplo (não use esta: ela está publicada aqui)"
    Palavras sorteadas: **girafa**, **pastel**, **trilho**, **nuvem**, **sabonete**.

    Frase-senha: `girafa-pastel-trilho-nuvem-sabonete`

    Para lembrar, invente uma cena absurda: *uma girafa comendo pastel em cima do trilho, numa nuvem de sabonete*. Cenas estranhas grudam na memória.

**E quando o site exige maiúscula, número e símbolo?** Acrescente sem complicar: `Girafa-pastel-trilho-nuvem-sabonete-7`. A força continua vindo do tamanho.

!!! warning "Frase famosa não serve"
    `ordem-e-progresso`, `o-rato-roeu-a-roupa-do-rei-de-roma`, versos de música e ditados estão nas listas dos programas de ataque. As palavras precisam ser **sorteadas**, não lembradas.

## Uma senha diferente para cada conta

A frase-senha resolve a força. Mas, se ela for repetida em vários sites, **um único vazamento** abre todas as contas (como no desafio da [aula 01](01_por_que_as_contas_sao_o_alvo.md)).

Ninguém consegue decorar 50 frases-senha. A solução realista:

- **Decore só duas ou três:** a do **e-mail principal**, a do **celular/computador** e a do **gerenciador de senhas**.
- Para todo o resto, o **gerenciador** cria e guarda uma senha diferente ([aula 03](03_gerenciador_de_senhas.md)).

!!! danger "Variações não contam como senhas diferentes"
    `girafa-pastel-trilho-nuvem-insta` e `girafa-pastel-trilho-nuvem-face` são, para um golpista, **a mesma senha**: ao ver uma, ele testa as variações nos outros sites.

## Quando trocar a senha

Trocar a senha "todo mês" não é mais recomendado: as pessoas acabam criando senhas fracas e previsíveis (`Senha01`, `Senha02`...). Troque **na hora** quando:

- o site avisar de um vazamento, ou o seu e-mail aparecer em um (verificação na [aula 05](05_projeto_plano_de_protecao.md));
- você digitou a senha numa página suspeita ou clicou num link estranho;
- você usou a senha num computador público ou de outra pessoa;
- você contou a senha para alguém (mesmo de confiança);
- a conta mostrou um acesso que não foi você.

## Perguntas de segurança

"Qual o nome do seu primeiro animal de estimação?", "Em que cidade sua mãe nasceu?". As respostas verdadeiras costumam estar nas suas redes sociais. Duas saídas seguras:

- Se o site deixar, **não use** pergunta de segurança: prefira e-mail ou celular de recuperação.
- Se for obrigatório, **invente** uma resposta (por exemplo, outra frase-senha) e guarde no gerenciador de senhas.

---

## ⚠️ Erros comuns

- **Trocar letras por símbolos achando que fica forte** (`p@ssw0rd`, `S3nh@`): os programas testam essas trocas primeiro.
- **Senha com dados pessoais:** nome, apelido, data, placa do carro, telefone, time.
- **A mesma senha em tudo, "só mudando o final".**
- **Senha anotada no celular, num bloco de notas sem proteção**, ou num papel colado no monitor.
- **Contar a senha para "alguém do suporte".** Nenhum banco, loja, escola ou empresa séria pede a sua senha, nem por telefone nem por mensagem.

---

## Exercícios

### Básico (fixação)

1. Ordene da mais fraca para a mais forte: `Flamengo2026!`, `kbxtqrma`, `vela-tucano-bigorna-chuva-mate`, `P@ssw0rd`.
2. Por que `P@ssw0rd` é fraca, mesmo tendo maiúscula, número e símbolo?

<!-- gabarito -->
??? success "Gabarito — Básico"
    1. `P@ssw0rd` e `Flamengo2026!` (as duas caem quase na hora: estão em listas ou seguem o padrão "palavra conhecida + ano + símbolo") ➔ `kbxtqrma` (sorteada, mas curta: cerca de 21 segundos) ➔ `vela-tucano-bigorna-chuva-mate` (5 palavras sorteadas: dezenas de anos).
    2. É a palavra *password* com as trocas mais comuns (`a`➔`@`, `o`➔`0`). Os programas de ataque testam essas trocas logo no começo.

### Intermediário (aplicação)

1. Sorteie 5 palavras num livro ou dicionário e monte uma frase-senha. **Não mostre para ninguém.**
2. Invente uma cena absurda para lembrar dela e teste a memória no fim da aula, escrevendo-a de cabeça num papel e depois **rasgando** o papel.
3. Responda: em qual conta do seu mapa (aula 01) essa frase-senha deve ser usada?

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    1. Resposta pessoal. Confira: 5 palavras ou mais, sorteadas, sem nomes, datas ou frases conhecidas.
    2. Se você não lembrou, sorteie de novo ou use uma cena mais exagerada. É melhor descobrir agora do que depois de trocar a senha.
    3. Numa conta 🔴 crítica que você precisa digitar de cabeça: o **e-mail principal** é a melhor escolha. (O gerenciador de senhas, da aula 03, também vai precisar de uma.)

### Avançado (desafio)

1. Um site exige "de 8 a 12 caracteres, com maiúscula, número e símbolo". Por que esse limite de 12 atrapalha a segurança? Crie um formato de senha que cumpra a regra e seja o mais forte possível.
2. A Ana troca a senha do e-mail todo mês: `Escola@01`, `Escola@02`, `Escola@03`... Explique o problema e proponha um jeito melhor.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    1. O limite impede senhas longas, que são a principal defesa. O melhor é usar os 12 caracteres **sorteados** pelo gerenciador de senhas, misturando tudo (por exemplo, no formato `k#8Tq!r2Vx9m`): com 12 caracteres sorteados de 94 possíveis, testar todas as combinações levaria mais de um milhão de anos. Sem gerenciador, sorteie 3 palavras curtas e acrescente número e símbolo, aproveitando os 12 caracteres.
    2. As senhas seguem um padrão óbvio: quem descobrir uma adivinha as próximas. E "Escola" + símbolo + número é um formato muito comum. Melhor: uma frase-senha longa e única, trocada **só** quando houver motivo (vazamento, acesso estranho, senha digitada em lugar suspeito), e a verificação em duas etapas ligada ([aula 04](04_verificacao_em_duas_etapas.md)).

---

## 💡 Resumo

- Senhas são quebradas testando bilhões de combinações por segundo, começando pelas mais comuns e pelas "trocas espertas".
- **Tamanho** vale mais que símbolo: 5 palavras sorteadas aguentam dezenas de anos; 8 caracteres misturados, poucos dias.
- **Frase-senha** = 5 ou mais palavras sorteadas, sem nada pessoal, lembradas com uma cena absurda.
- Decore só 2 ou 3 frases-senha; o resto fica com o **gerenciador de senhas**, uma senha diferente para cada conta.
- Troque a senha quando houver **motivo**, não por calendário. Perguntas de segurança: evite ou invente a resposta.

## ➡️ Próximo passo

**[03 — Gerenciador de senhas](03_gerenciador_de_senhas.md)**: como ter uma senha diferente em cada conta sem precisar decorar nenhuma delas.
