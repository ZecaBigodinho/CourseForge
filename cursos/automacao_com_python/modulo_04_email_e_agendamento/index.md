# Módulo 04 — E-mail, agendamento e boas práticas

> **Curso:** Automação com Python  
> **Módulo:** 04 · E-mail, agendamento e boas práticas  
> **Descrição:** Montar e enviar e-mails com segurança (servidor de teste, um por pessoa), guardar senhas no `.env`, registrar logs e agendar scripts no Windows.

---

## 📋 Visão Geral do Módulo

E-mail automático é útil e perigoso: uma mensagem errada vai para a turma inteira e não volta. Por isso o módulo começa pelas **regras** (só para quem espera, um por pessoa, devagar) e só envia para um **servidor de teste** que roda no seu computador e mostra os e-mails na tela. Você monta e-mails com texto, HTML e anexo, salva **rascunhos `.eml`** para conferir, guarda a configuração e as senhas num **`.env`**, registra tudo num **log** e agenda o script no **Agendador de Tarefas** do Windows. No projeto, o **lembrete semanal** avisa cada aluno dos trabalhos pendentes, com simulação, envio, log e tratamento de erros.

---

## 📚 Capítulos

- [01. Montando e-mails com o Python](01_montar_emails.md)
- [02. Enviando para um servidor de teste](02_servidor_de_teste.md)
- [03. Senhas no `.env` e configuração](03_env_e_configuracao.md)
- [04. Logs, erros e agendamento](04_logs_e_agendamento.md)
- [05. Projeto do módulo: lembrete semanal](05_projeto_lembrete.md)

---

## 🎯 Objetivos do Módulo

Ao final deste módulo, você será capaz de:

- Seguir as regras de e-mail automático: consentimento, um por pessoa, poucos e devagar.
- Montar e-mails com `EmailMessage` e conferir como rascunho `.eml`.
- Enviar com `smtplib` para um servidor de teste e tratar erros de conexão.
- Separar segredos no `.env` e validar a configuração.
- Registrar logs, devolver código de saída e agendar scripts no Windows.

---

## 🧭 Antes de começar

- **Pré-requisitos:** [Módulo 02](../modulo_02_planilhas/index.md) (ambiente virtual e planilhas). O [curso de Segurança digital](../../seguranca_digital/docs/index.md) ajuda a entender senhas de app e verificação em duas etapas.
- **Tempo estimado:** ~7 h (estimativa, ajuste ao ritmo da turma)
- **Ao final você terá:** um lembrete semanal testado, que pode ser agendado para rodar sozinho.

## ✅ Checklist do módulo

- [ ] Instalei `aiosmtpd==1.4.6` e `python-dotenv==1.2.1` no ambiente virtual.
- [ ] Montei um e-mail com texto, HTML e anexo e conferi o `.eml`.
- [ ] Enviei para o servidor de teste e vi a mensagem no outro terminal.
- [ ] Tenho um `.env` (fora do Git) e um `.env.example`.
- [ ] Rodei o lembrete em simulação e em envio de teste, e li o log.

## ➡️ Próximo passo

Comece pela **[aula 01 — Montando e-mails com o Python](01_montar_emails.md)**.
