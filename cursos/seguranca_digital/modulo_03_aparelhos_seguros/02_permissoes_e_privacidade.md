# 02 — Permissões e privacidade no celular

> **Curso:** Segurança digital e cidadania online  
> **Módulo:** 03 — Celular e computador seguros  
> **Tempo estimado:** 45 min  

---

## 🎯 Objetivos

Ao final desta aula, você será capaz de:

- Explicar o que são as **permissões** dos aplicativos e por que elas importam.
- Revisar quais apps podem usar **localização, câmera, microfone, contatos e fotos**.
- Reconhecer a permissão mais perigosa do Android: a de **Acessibilidade**.
- Esconder o conteúdo das **notificações** na tela bloqueada.
- Conferir quem está vendo a sua **localização** em tempo real.

## Pré-requisitos

- [Aula 01](01_atualizacoes_e_apps_oficiais.md): apps só das lojas oficiais.

---

## Permissão é uma chave que você entrega

Quando um aplicativo pede *"Permitir acesso à sua localização?"*, ele está pedindo uma **chave**. Algumas chaves fazem sentido: o aplicativo de mapas precisa da localização; o de vídeo precisa da câmera. Outras não: um jogo não precisa dos seus contatos; uma lanterna não precisa do microfone.

**Pergunta para cada permissão:** *esse aplicativo precisa disso para fazer o que eu quero?* Se a resposta for não, **negue**. O aplicativo continua funcionando (se não funcionar, desconfie dele).

| Permissão | Quem precisa de verdade | Sinal de alerta |
|---|---|---|
| 📍 **Localização** | Mapas, transporte, entregas, clima | Jogo, lanterna, editor de foto |
| 📷 **Câmera** | Câmera, chamadas de vídeo, leitor de QR code, banco (para foto de documento) | App que não tira fotos |
| 🎤 **Microfone** | Chamadas, áudio, gravador | App sem nenhuma função de voz |
| 👥 **Contatos** | Mensagens, telefone | Jogos, lojas, "limpadores de celular" |
| 🖼️ **Fotos e arquivos** | Galeria, redes sociais, editor | App que não precisa de imagens |
| 💬 **SMS** | O app de mensagens que você usa | Qualquer outro (o SMS recebe os **códigos** das suas contas) |

!!! tip "Escolha a opção mais curta"
    Quando aparecer, prefira **"Permitir somente durante o uso do app"** (e não "Sempre"), **"Somente desta vez"** e, para fotos, **"Selecionar fotos"** em vez de liberar a galeria inteira. Para localização, muitos apps funcionam bem com a **localização aproximada** em vez da precisa.

## Revisando as permissões que você já deu

| Onde | Caminho (pode variar um pouco) |
|---|---|
| **Android** | *Configurações* ➔ *Segurança e privacidade* (ou *Privacidade*) ➔ **Gerenciador de permissões**: escolha uma permissão (por exemplo, *Microfone*) e veja a lista de apps. |
| **Android** (painel) | *Configurações* ➔ *Segurança e privacidade* ➔ **Painel de privacidade**: mostra quais apps usaram localização, câmera e microfone nas últimas horas. |
| **iPhone** | *Ajustes* ➔ **Privacidade e Segurança**: cada item (*Serviços de Localização*, *Câmera*, *Microfone*, *Contatos*, *Fotos*) mostra os apps com acesso. |

!!! info "Os indicadores na tela"
    Android e iPhone mostram um **pontinho** (ou ícone) no canto da tela quando a **câmera** ou o **microfone** estão em uso. Se ele aparecer sem você estar usando nada que precise disso, abra o painel de privacidade e descubra qual app foi.

## A permissão mais perigosa: Acessibilidade

No Android, a permissão de **Acessibilidade** existe para ajudar pessoas com deficiência: ler a tela em voz alta, tocar em botões por comando. Por isso ela é poderosa: um app com essa permissão **vê tudo o que aparece na tela e toca nos botões por você**.

Aplicativos maliciosos (como os do golpe do APK, da [aula 01](01_atualizacoes_e_apps_oficiais.md)) insistem para você ligar a Acessibilidade, às vezes com telas falsas de "ative para continuar". Com ela, conseguem ler senhas, códigos e até fazer um Pix.

!!! danger "Só ligue Acessibilidade para quem você conhece"
    Leitores de tela, teclados e apps de acessibilidade que **você** escolheu, sim. Um app recém-instalado que **insiste** nessa permissão, não: desinstale. Confira em *Configurações* ➔ *Acessibilidade* ➔ *Apps instalados* / *Serviços instalados*: tudo o que estiver ligado ali precisa ser reconhecido por você.

## Notificações na tela bloqueada

Os códigos de verificação chegam por SMS e por notificação. Se o conteúdo aparece **na tela bloqueada**, qualquer pessoa com o seu celular na mão (ou olhando por cima do seu ombro) lê o código.

- **Android:** *Configurações* ➔ *Notificações* ➔ *Notificações na tela de bloqueio* ➔ **Ocultar conteúdo confidencial** (ou mostrar só "conversas, sem conteúdo").
- **iPhone:** *Ajustes* ➔ *Notificações* ➔ *Mostrar Pré-visualizações* ➔ **Quando Desbloqueado**.

## Quem vê a sua localização

Compartilhar a localização com a família pode ser útil. Mas vale conferir **com quem** você compartilha e se isso ainda faz sentido.

- **Google Maps:** foto do perfil ➔ **Compartilhamento de localização**.
- **iPhone:** app **Buscar** ➔ *Pessoas*.
- **WhatsApp:** localização em tempo real enviada numa conversa (pare em *Configurações* ➔ *Privacidade* ➔ *Localização em tempo real*).

!!! warning "Controle em relacionamentos"
    Ninguém tem o direito de exigir a sua senha ou de acompanhar a sua localização o tempo todo, nem namorado(a) ou parceiro(a). Isso pode ser uma forma de **controle abusivo**. No iPhone, a **Verificação de Segurança** (*Ajustes* ➔ *Privacidade e Segurança* ➔ *Verificação de Segurança*) mostra e permite parar, de uma vez, o que você compartilha. Se você se sentir em risco, procure alguém de confiança, a escola ou a rede de proteção (o Módulo 04 traz os canais).

---

## ⚠️ Erros comuns

- **Tocar em "Permitir" em tudo** para o aplicativo abrir logo.
- **Liberar a galeria inteira** quando bastava escolher uma foto.
- **Ligar a Acessibilidade** porque um app "pediu para funcionar".
- **Código aparecendo na tela bloqueada.**
- **Esquecer um compartilhamento de localização** ligado com alguém que já não faz parte da sua vida.

---

## Exercícios

### Básico (fixação)

1. Faz sentido? Responda sim ou não e explique: (a) app de mapas pedindo localização; (b) jogo de cartas pedindo contatos; (c) app de chamadas de vídeo pedindo câmera; (d) lanterna pedindo microfone.
2. Por que a permissão de Acessibilidade é tão perigosa nas mãos de um app malicioso?

<!-- gabarito -->
??? success "Gabarito — Básico"
    1. (a) Sim, é a função dele. (b) Não, um jogo não precisa dos seus contatos. (c) Sim. (d) Não: lanterna não usa microfone; desconfie do app.
    2. Porque ela deixa o app **ver tudo o que aparece na tela** e **tocar nos botões por você**: dá para ler senhas e códigos e até fazer transações.

### Intermediário (aplicação)

1. No **Gerenciador de permissões** (Android) ou em **Privacidade e Segurança** (iPhone), revise **Localização**, **Microfone** e **Contatos**. Retire pelo menos uma permissão que não faz sentido.
2. Esconda o conteúdo das notificações na **tela bloqueada**.
3. (Android) Confira a lista de **Acessibilidade**: há algo ligado que você não reconhece?

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    1. Use os caminhos da tabela "Revisando as permissões". Para cada app, escolha **Não permitir** ou **Permitir só durante o uso**.
    2. Android: *Notificações* ➔ *Notificações na tela de bloqueio* ➔ *Ocultar conteúdo confidencial*. iPhone: *Notificações* ➔ *Mostrar Pré-visualizações* ➔ *Quando Desbloqueado*. Teste mandando uma mensagem para você mesmo com o celular bloqueado.
    3. *Configurações* ➔ *Acessibilidade*. Tudo o que estiver **ativado** precisa ser algo que você (ou quem configurou o celular para você) escolheu. App desconhecido com Acessibilidade ligada: desligue e desinstale, e troque as senhas usando **outro** aparelho.

### Avançado (desafio)

1. Depois de instalar um app de "cupons de desconto" pelo link de um anúncio, o celular da Ana mostra uma tela: *"Para receber os cupons, ative o serviço Cupons+ em Acessibilidade"*. O que está acontecendo e o que ela deve fazer?
2. O namorado da Bia pede a senha do celular dela "como prova de confiança" e quer que ela compartilhe a localização o tempo todo. Escreva uma resposta curta que a Bia pode dar e diga onde ela pode procurar ajuda se ele insistir ou ameaçar.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    1. É o padrão dos apps maliciosos: instalado fora da loja (ou por anúncio) e insistindo na Acessibilidade para controlar a tela. Ela **não** deve ativar; deve desinstalar o app (se ele dificultar, iniciar o celular em modo de segurança ou procurar ajuda técnica), rodar o **Play Protect** e, se já tiver ativado, trocar as senhas importantes **em outro aparelho** e avisar o banco.
    2. Exemplo: *"Confiança não é ter a minha senha. Eu não peço a sua e não vou passar a minha nem compartilhar minha localização o tempo todo."* Se ele insistir, ameaçar ou controlar, ela deve conversar com alguém de confiança (família, professor, orientação da escola) e conhecer os canais de ajuda do Módulo 04. Controle da senha e da localização pode ser sinal de relacionamento abusivo.

---

## 💡 Resumo

- Permissão é uma **chave**: dê só o que o app precisa, de preferência **"só durante o uso"**.
- Revise de tempos em tempos no **Gerenciador de permissões** (Android) ou em **Privacidade e Segurança** (iPhone).
- **Acessibilidade** é a permissão mais perigosa: só para apps que você escolheu.
- Esconda o conteúdo das **notificações** na tela bloqueada.
- Confira **com quem** você compartilha a localização. Ninguém tem o direito de exigir a sua senha.

## ➡️ Próximo passo

**[03 — Bloqueio de tela, roubo e backup](03_bloqueio_roubo_e_backup.md)**: o que fazer **antes** e **depois** de perder o celular.
