# 04 — Links falsos, lojas e boletos falsos

> **Curso:** Segurança digital e cidadania online  
> **Módulo:** 02 — Golpes mais comuns  
> **Tempo estimado:** 50 min  

---

## 🎯 Objetivos

Ao final desta aula, você será capaz de:

- Reconhecer mensagens de **phishing** por SMS, e-mail e redes sociais.
- **Ler um endereço** de site e encontrar o nome verdadeiro dele.
- Identificar uma **loja falsa** antes de comprar.
- Saber o que fazer se você **clicou** num link falso ou digitou dados nele.

## Pré-requisitos

- [Aula 03](03_golpes_com_pix.md): conferir o recebedor e o beneficiário antes de pagar.

!!! note "Endereços desta aula"
    Os endereços usam nomes inventados (como `bancoexemplo.com.br`). Não digite nenhum deles: o objetivo é aprender a **ler**.

---

## Phishing: a isca

**Phishing** (lê-se "fíxin", de *fishing*, pescar) é a mensagem que joga uma **isca** para você clicar num link e entregar senha, dados do cartão ou um pagamento. Chega por SMS, e-mail, WhatsApp, anúncio ou comentário.

<div class="cf-chat" markdown>
<p class="cf-chat__topo">SMS · 29012</p>
<p class="cf-msg">ENTREGA: Sua encomenda BR92●●●●●●●● esta retida por endereço incompleto. Evite a devolução, atualize em ate 24h: rastreio-encomendas-br.top/atualizar</p>
</div>

<div class="cf-chat" markdown>
<p class="cf-chat__topo">SMS · BANCOEXEMPLO</p>
<p class="cf-msg">BancoExemplo: Compra APROVADA de R$ 1.849,90 no cartão final 4417. Não reconhece? Cancele agora: bancoexemplo-cancelamento.com/app</p>
</div>

Os dois usam os gatilhos da [aula 01](01_engenharia_social.md): **urgência** ("em até 24h", "agora") e **medo** ("devolução", "compra aprovada"). E os dois trazem um **link**.

!!! danger "Regra de ouro dos links"
    **Não resolva nada pelo link que chegou.** Encomenda: abra o site ou app da transportadora e digite o código você mesmo. Compra estranha: abra o aplicativo do banco. Se for verdade, vai aparecer lá.

## Lendo um endereço

O endereço de um site tem várias partes, mas só uma diz **de quem** ele é: o **domínio**. Para achá-lo, olhe o trecho entre `https://` e a **primeira barra** `/`. O que vale é o **final** desse trecho: o nome que vem logo antes do `.com.br`, `.com`, `.gov.br`, `.top`... Tudo o que estiver antes disso pode ser enfeite.

```text
https://www.bancoexemplo.com.br/cartoes/segunda-via
        └──────┬──────────────┘
          domínio: bancoexemplo.com.br  ✅ é o banco

https://www.bancoexemplo.com.br.atualiza-cadastro.top/login
        └─────────────────┬─────────────────────────┘
          domínio: atualiza-cadastro.top  ⛔ NÃO é o banco
          (o "bancoexemplo.com.br" no começo é só enfeite)

https://bancoexernplo.com.br/login
          domínio: bancoexernplo.com.br  ⛔ "rn" no lugar de "m"
```

**Truques comuns:**

| Truque | Exemplo | Como perceber |
|---|---|---|
| O nome verdadeiro **no começo** | `bancoexemplo.com.br.seguro-app.top` | O domínio é o que vem **no fim**, antes da primeira `/`. |
| Letras parecidas | `bancoexernplo`, `rnercadolivre`, `paypa1` | Leia devagar, letra por letra. |
| Palavras "oficiais" a mais | `bancoexemplo-cancelamento.com`, `gov-br-beneficio.site` | Hífen + palavra extra = **outro** domínio. |
| Final estranho | `.top`, `.xyz`, `.site`, `.online` para banco ou governo | Órgãos do governo brasileiro usam **`.gov.br`**. |
| Link encurtado | `bit.ly/...`, `encurtador.com/...` | Não dá para ver o destino. Não use para pagamentos ou login. |

!!! warning "O cadeado não prova nada"
    O cadeado 🔒 (ou `https`) só quer dizer que a conexão é **criptografada**. Sites falsos também têm cadeado. Ele não diz **de quem** é o site; quem diz é o domínio.

!!! tip "Cuidado com anúncios na busca"
    Ao pesquisar "segunda via banco X" ou "telefone da loja Y", os primeiros resultados podem ser **anúncios patrocinados** pagos por golpistas. Prefira o **aplicativo oficial** ou o endereço que você já conhece e salvou nos favoritos.

## Lojas falsas

Sites e perfis que **imitam** lojas conhecidas, ou que inventam uma loja com preços impossíveis. Eles recebem o Pix e não entregam nada.

| Sinal de alerta | Por quê |
|---|---|
| Preço **muito** abaixo das outras lojas ("iPhone por R$ 1.200") | A isca é o preço. |
| **Só aceita Pix** (ou dá um desconto enorme no Pix) | Pix cai na hora e é mais difícil contestar que cartão. |
| Contagem regressiva, "últimas unidades", "só hoje" | Urgência. |
| Sem **CNPJ**, endereço ou telefone; ou o CNPJ é de outra empresa | Loja séria se identifica. |
| Perfil novo, poucas postagens, **comentários desativados** | Esconde as reclamações. |
| Nome do recebedor do Pix diferente do nome da loja | Veja a [aula 03](03_golpes_com_pix.md). |

**Antes de comprar numa loja que você não conhece:**

1. Procure o nome da loja no **Reclame Aqui** e veja a reputação e as reclamações recentes.
2. Confira o **CNPJ** do rodapé do site numa consulta pública de CNPJ (a da Receita Federal é gratuita): a empresa existe, está ativa e o nome bate com o da loja?
3. Prefira pagar com **cartão de crédito** (dá para contestar) ou por uma plataforma com garantia de compra.
4. Desconfie de "loja" que só atende pelo WhatsApp e manda o Pix para uma pessoa física.

## Boletos e cobranças falsas

Além do boleto adulterado da aula 03, há o boleto **inventado**: cobrança de uma "dívida" que você não tem, de uma "renovação" de domínio, de um "protesto em cartório", de uma "taxa do benefício".

- Não reconhece a cobrança? **Não pague.** Procure a empresa ou o órgão pelo canal oficial.
- Pague contas da casa pelo **site ou app oficial** (ou pelo **DDA**, a lista de boletos registrados no seu CPF dentro do aplicativo do banco).
- Na tela de pagamento, confira sempre o **beneficiário**.

## Cliquei. E agora?

| O que você fez | O que fazer agora |
|---|---|
| Só **abriu** o link e fechou | Em geral, nada aconteceu. Não volte ao site e apague a mensagem. Mantenha o celular atualizado (Módulo 03). |
| **Digitou uma senha** | Troque essa senha **imediatamente** (e em qualquer lugar onde ela se repita). Confira a verificação em duas etapas e os aparelhos conectados ([Módulo 01](../modulo_01_senhas_e_contas/05_projeto_plano_de_protecao.md#passo-3-se-uma-conta-for-invadida)). |
| **Digitou dados do cartão** | Ligue para o banco (número atrás do cartão) ou use o app para **bloquear** o cartão e pedir um novo. Acompanhe a fatura. |
| **Pagou** (Pix ou boleto) | Procure o banco **na hora** e peça o **MED** ([aula 03](03_golpes_com_pix.md#cai-num-golpe-com-pix-o-med)). Registre boletim de ocorrência. |
| **Instalou um aplicativo** que o link pediu | Desligue os dados móveis e o Wi-Fi, desinstale o app e procure ajuda (o Módulo 03 detalha). Troque as senhas usando **outro** aparelho. |

!!! tip "Denuncie"
    Encaminhe e-mails falsos com o botão **Denunciar phishing** do seu e-mail. No WhatsApp e nas redes sociais, use **Denunciar**. Cada denúncia ajuda a derrubar o golpe antes que ele chegue a outra pessoa.

---

## ⚠️ Erros comuns

- **Confiar no cadeado** ou no "visual igualzinho" do site.
- **Ler o endereço só no começo.** O domínio está no fim, antes da primeira `/`.
- **Clicar no anúncio patrocinado** em vez de usar o app ou o endereço salvo.
- **Comprar pelo preço**, sem pesquisar a loja.
- **Ter vergonha e não fazer nada** depois de clicar. O que você faz nos primeiros minutos é o que mais protege.

---

## Exercícios

### Básico (fixação)

1. Qual é o domínio de cada endereço? É o do `bancoexemplo.com.br`?
    - `https://app.bancoexemplo.com.br/pix`
    - `https://bancoexemplo.com.br.validacao.xyz/entrar`
    - `https://www.bancoexemplo-seguranca.com/token`
2. O site tem cadeado. Isso prova que é verdadeiro? Por quê?

<!-- gabarito -->
??? success "Gabarito — Básico"
    1. `bancoexemplo.com.br` ✅ (o `app.` é só uma parte do próprio site do banco); `validacao.xyz` ⛔; `bancoexemplo-seguranca.com` ⛔ (o hífen cria **outro** domínio).
    2. Não. O cadeado só mostra que a conexão é criptografada; qualquer site, inclusive falso, pode ter cadeado. Quem diz de quem é o site é o **domínio**.

### Intermediário (aplicação)

1. Procure no seu celular uma mensagem (SMS, e-mail ou WhatsApp) que tenha um link de cobrança, entrega ou prêmio. **Sem clicar**, aponte os gatilhos e o domínio do link. Se for golpe, denuncie e apague.
2. Escolha uma loja on-line que você nunca usou e faça as verificações da aula: Reclame Aqui, CNPJ e formas de pagamento. Você compraria?

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    1. Resposta pessoal. Para ver o link sem abrir: no computador, passe o mouse por cima; no celular, toque e **segure** e leia o endereço (sem tocar em *Abrir*). Procure urgência, medo, prêmio e domínios estranhos.
    2. Resposta pessoal. Sinais bons: reputação boa e reclamações respondidas no Reclame Aqui; CNPJ ativo com nome compatível; pagamento por cartão ou plataforma com garantia; contato e endereço reais.

### Avançado (desafio)

1. A mãe da Ana recebeu um SMS de "taxa de importação" de R$ 39,90 de uma encomenda que ela realmente está esperando, com link para pagar via Pix. Por que o fato de ela esperar uma encomenda torna o golpe mais perigoso? Como ela deve conferir?
2. O Bruno digitou a senha do e-mail num site falso há 10 minutos. Escreva a lista do que ele deve fazer, em ordem.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    1. Porque a mensagem "combina" com a realidade dela, e a chance de acreditar sem conferir é maior. Os golpistas mandam o mesmo SMS para milhares de pessoas, e muitas estão esperando encomendas. Ela deve ignorar o link e conferir o rastreio pelo **site ou app oficial** da transportadora, digitando o código ela mesma; se houver uma taxa de verdade, ela vai aparecer lá, com pagamento pelo canal oficial.
    2. (1) Trocar a senha do e-mail **agora**, por uma frase-senha nova; (2) ligar ou conferir a verificação em duas etapas; (3) ver os aparelhos conectados e encerrar os desconhecidos; (4) conferir o e-mail e o telefone de recuperação; (5) trocar a senha em qualquer outro site em que ela se repetia; (6) denunciar o site falso (no navegador ou no e-mail); (7) ficar de olho em avisos de login e de troca de senha nos próximos dias.

---

## 💡 Resumo

- **Phishing** é a isca: mensagem com urgência ou medo e um **link**. Não resolva nada pelo link; abra o app ou o site oficial.
- O **domínio** (logo antes da primeira `/`, lido do fim para o começo) diz de quem é o site. Cadeado não prova nada.
- **Loja falsa:** preço impossível, só Pix, sem CNPJ, comentários desativados. Pesquise no Reclame Aqui e confira o CNPJ.
- **Boleto:** pague contas pelo site/app oficial ou pelo DDA e confira o beneficiário.
- **Cliquei:** troque a senha, bloqueie o cartão ou peça o MED, conforme o que aconteceu. Rapidez é tudo.

## ➡️ Próximo passo

**[05 — Projeto do módulo: golpe ou não?](05_projeto_golpe_ou_nao.md)**: analise casos simulados e crie um alerta para a sua família.
