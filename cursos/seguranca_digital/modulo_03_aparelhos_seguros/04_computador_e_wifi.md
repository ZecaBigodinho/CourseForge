# 04 — Computador, Wi-Fi e o computador da escola

> **Curso:** Segurança digital e cidadania online  
> **Módulo:** 03 — Celular e computador seguros  
> **Tempo estimado:** 50 min  

---

## 🎯 Objetivos

Ao final desta aula, você será capaz de:

- Deixar o **Windows** atualizado e com o **antivírus** que já vem nele funcionando.
- Escolher **extensões** de navegador e programas com segurança.
- Usar **Wi-Fi público** sem expor as suas contas.
- Proteger o **roteador** de casa.
- Usar o **computador da escola** (ou de uma lan house) sem deixar contas abertas.
- Reconhecer sinais de que um aparelho pode estar **infectado** e o que fazer.

## Pré-requisitos

- [Aula 01](01_atualizacoes_e_apps_oficiais.md): atualizações e apps oficiais.

---

## Windows: atualização e antivírus

O Windows 10 e o 11 já vêm com o **Segurança do Windows** (o antigo *Windows Defender*), um antivírus **gratuito** que, para o uso de casa e da escola, é suficiente. Não é preciso instalar outro, e **dois antivírus juntos** atrapalham um ao outro.

1. *Configurações* ➔ **Windows Update**: deixe as atualizações ligadas e **reinicie** quando ele pedir.
2. Abra o app **Segurança do Windows** (procure no menu Iniciar). Os itens precisam estar com o **✓ verde**: *Proteção contra vírus e ameaças*, *Firewall*, *Controle de aplicativos e do navegador*.

!!! warning "Windows 10: fim do suporte"
    A Microsoft encerrou o suporte normal ao **Windows 10** em outubro de 2025: computadores com ele deixam de receber correções de segurança, a não ser os inscritos no programa de atualizações estendidas. Se o seu computador aceita o Windows 11, vale atualizar; se não aceita, redobre os cuidados desta aula e evite usar o banco nele.

!!! danger "\"Seu computador está infectado! Ligue para o suporte\""
    Uma página que de repente ocupa a tela toda, apita e mostra um número de "suporte da Microsoft" é **golpe**. A Microsoft não mostra telefone em alerta de vírus. Feche o navegador (se não fechar, *Ctrl+Shift+Esc* ➔ *Gerenciador de Tarefas* ➔ finalizar o navegador) e **não ligue** para o número.

## Programas e extensões

- Baixe programas **só do site oficial** do fabricante ou da **Microsoft Store**. Cuidado com os anúncios no topo da busca, que levam a cópias com vírus ([Módulo 02](../modulo_02_golpes/04_links_lojas_e_boletos_falsos.md#lendo-um-endereco)).
- Na instalação, leia as telas: desmarque "instalar também" barras, antivírus ou programas extras.
- **Extensões** do navegador (as "pecinhas" do Chrome ou do Edge) podem ler tudo o que você faz nos sites. Instale poucas, só da loja oficial do navegador, e remova as que você não usa: menu ➔ *Extensões* ➔ *Gerenciar extensões*.

## Wi-Fi público

Wi-Fi de shopping, rodoviária, praça ou lanchonete é **compartilhado com desconhecidos**. Riscos:

- **Rede falsa:** alguém cria uma rede chamada `Shopping_WiFi_Gratis` para ver o que passa por ela.
- **Página de login falsa:** a rede pede "entre com o seu e-mail e senha" para liberar a internet.

**Como usar com segurança:**

| ✅ Pode | ⛔ Evite |
|---|---|
| Ver notícias, vídeos, mapas | Abrir o **banco** e fazer **Pix** (use os **dados móveis** do celular) |
| Sites com `https` e apps atualizados | Digitar a senha do e-mail numa página que **a rede** abriu |
| Redes cujo nome você confirmou com o estabelecimento | Conectar em rede aberta "grátis" sem saber de quem é |

!!! tip "Esqueça a rede depois"
    Ao sair, use *Esquecer esta rede* nas configurações de Wi-Fi. Assim o celular não se conecta sozinho a uma rede falsa com o mesmo nome em outro lugar. E deixe o Wi-Fi do celular configurado para **não conectar automaticamente** em redes abertas.

## O roteador de casa

O roteador é a "porta" da internet da sua casa. Peça ajuda a quem cuida da internet aí (ou ao técnico da operadora) para conferir:

1. **Senha do Wi-Fi** longa (uma frase-senha serve) e segurança **WPA2** ou **WPA3** (nunca rede aberta ou WEP).
2. **Senha de administrador** do roteador trocada (a que vem de fábrica, como `admin`, está na internet).
3. **Rede de visitantes** (se o roteador tiver) para quem vem de fora, separada dos seus aparelhos.

## Computador da escola, do trabalho ou da lan house

Você já viu parte disso no [Módulo 01](../modulo_01_senhas_e_contas/03_gerenciador_de_senhas.md#computador-da-escola-ou-emprestado). O roteiro completo:

1. Use uma **janela anônima** (*Ctrl+Shift+N* no Chrome e no Edge).
2. Quando o navegador oferecer **salvar a senha**, escolha **Nunca**.
3. **Não** marque "manter conectado" / "lembrar de mim".
4. No fim: **saia** de cada conta (*Sair*), feche **todas** as janelas do navegador e, se baixou arquivos, apague-os da pasta *Downloads*.
5. Se esqueceu uma conta aberta: no Google, *Gerenciar sua conta* ➔ *Segurança* ➔ *Seus dispositivos* ➔ sair do computador esquecido.

!!! warning "Pendrive: nos dois sentidos"
    Um pendrive que passa por muitos computadores pode levar vírus. E um pendrive **achado** nunca deve ser conectado "para ver de quem é": é um truque conhecido para infectar computadores. Para levar trabalhos, prefira o e-mail ou um serviço de nuvem.

## Sinais de aparelho infectado

| Sinal | Pode ser |
|---|---|
| Anúncios aparecendo fora de qualquer app, em tela cheia | App com propaganda maliciosa (*adware*) |
| Bateria e internet acabando rápido, aparelho quente sem uso | Algo rodando escondido |
| Apps que você não instalou; ícone que sumiu depois de instalar | App malicioso escondido |
| Página inicial do navegador mudou sozinha, buscas indo para um site estranho | Extensão ou programa malicioso |
| Amigos recebendo mensagens suas que você não mandou | Conta invadida (Módulo 01) ou aparelho comprometido |

**O que fazer:**

1. **Desinstale** apps e extensões que você não reconhece ou instalou recentemente.
2. Faça uma verificação: **Play Protect** (Android) ou **Segurança do Windows** ➔ *Verificação completa*.
3. Revise a **Acessibilidade** e as permissões ([aula 02](02_permissoes_e_privacidade.md)).
4. Troque as senhas importantes **usando outro aparelho** que esteja confiável.
5. Se nada resolver: com o **backup em dia**, restaure o aparelho para as **configurações de fábrica**, ou procure uma assistência de confiança.

---

## ⚠️ Erros comuns

- **Instalar um segundo antivírus "grátis"** baixado de anúncio (muitos são o próprio vírus).
- **Ligar para o número** do falso alerta de vírus.
- **Fazer Pix no Wi-Fi do shopping** em vez de usar os dados móveis.
- **Senha de fábrica** no roteador.
- **Sair do computador da escola sem fazer logout.**
- **Conectar o pendrive achado** no corredor.

---

## Exercícios

### Básico (fixação)

1. É preciso instalar outro antivírus no Windows 11? Por quê?
2. Cite duas coisas que você **não** deve fazer num Wi-Fi público.

<!-- gabarito -->
??? success "Gabarito — Básico"
    1. Para o uso comum, não: o **Segurança do Windows** já vem incluído, é gratuito e atualizado pelo Windows Update. Dois antivírus juntos atrapalham um ao outro.
    2. Abrir o banco ou fazer Pix (use os dados móveis); digitar a senha do e-mail numa página aberta pela rede; conectar em rede aberta sem saber de quem é.

### Intermediário (aplicação)

1. No computador que você usa, abra o **Segurança do Windows** e confira se os itens estão com ✓ verde. Anote o que não estiver.
2. No navegador, abra **Gerenciar extensões** e remova as que você não usa.
3. No celular, "esqueça" as redes Wi-Fi públicas salvas.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    1. Menu Iniciar ➔ *Segurança do Windows*. Item com ⚠️ ou ❌: clique nele e siga a ação sugerida (geralmente *Ativar* ou *Atualizar*). Se o computador for da escola, avise o professor ou o responsável pela sala.
    2. Chrome: menu ⋮ ➔ *Extensões* ➔ *Gerenciar extensões*. Edge: menu ⋯ ➔ *Extensões*. Remova o que você não reconhece ou não usa.
    3. *Configurações* ➔ *Wi-Fi* ➔ *Redes salvas* (Android) ou *Ajustes* ➔ *Wi-Fi* ➔ *Editar* (iPhone) ➔ apagar as redes de shopping, rodoviária etc.

### Avançado (desafio)

1. A tia da Ana estava navegando e apareceu uma tela vermelha, com sirene: *"VÍRUS DETECTADO! Ligue para o Suporte Microsoft 0800-●●●-●●●●"*. Ela ligou, e o "técnico" pediu para instalar um programa de acesso remoto. O que está acontecendo e o que ela deve fazer agora?
2. O Bruno quer fazer um Pix urgente e está no shopping. Ele tem pouco crédito de dados. Qual é a forma mais segura?

<!-- gabarito -->
??? success "Gabarito — Avançado"
    1. É o golpe do **falso suporte técnico**: a página é um anúncio malicioso e o "técnico" quer controlar o computador (e chegar ao banco). Ela deve **desligar** a ligação, **desconectar o computador da internet**, desinstalar o programa de acesso remoto (*Configurações* ➔ *Aplicativos*), rodar a verificação completa do Segurança do Windows e trocar as senhas usadas nesse computador **de outro aparelho**. Se informou dados do banco ou do cartão, ligar para o banco pelo número do cartão.
    2. Usar os **dados móveis** (um Pix gasta pouquíssima internet), no **aplicativo** do banco, conferindo o nome do recebedor. Se não tiver dados, é melhor esperar chegar a uma rede confiável do que usar o Wi-Fi público.

---

## 💡 Resumo

- Windows com **Windows Update** ligado e **Segurança do Windows** com ✓ verde. Falso alerta de vírus com telefone é golpe.
- Programas **só do site oficial** ou da loja; poucas **extensões**.
- **Wi-Fi público:** nada de banco e senhas; use os **dados móveis** e esqueça a rede depois.
- **Roteador:** frase-senha no Wi-Fi, WPA2/WPA3, senha de administrador trocada.
- **Computador da escola:** janela anônima, não salvar senha, sair das contas.
- Sinais de infecção: desinstale o suspeito, verifique, troque senhas de outro aparelho e, se preciso, restaure.

## ➡️ Próximo passo

**[05 — Projeto do módulo: checkup de segurança](05_projeto_checkup.md)**: revisar o seu celular e ajudar alguém da família a revisar o dele.
