# RL-RF064 — Referência ao Legado

**Versão:** 2.0
**Data:** 2025-01-14
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF-064 (Gestão de Templates de E-mail)
**Sistema Legado:** IControlIT v1.0 (ASP.NET Web Forms + VB.NET)
**Objetivo:** Documentar o comportamento de envio de e-mails no sistema legado, demonstrando que **NÃO existe biblioteca de templates** no legado. O RF-064 é uma funcionalidade **inteiramente nova** que expande capacidades básicas de SMTP para um sistema moderno de gestão de templates responsivos.

---

## 1. CONTEXTO DO LEGADO

O sistema legado IControlIT v1.0 possui apenas funcionalidade **básica de envio de e-mails via SMTP**.

**Características gerais:**
- **Arquitetura:** Monolítica Web Forms
- **Linguagem/Stack:** ASP.NET Web Forms + VB.NET
- **Banco de Dados:** SQL Server (schema legado sem auditoria)
- **Multi-tenant:** Não (sistema single-tenant)
- **Auditoria:** Inexistente
- **Configurações SMTP:** Web.config hardcoded

**Funcionalidade de e-mail no legado:**
- Envio de e-mails transacionais simples (notificações, alertas)
- Configuração SMTP básica (servidor, porta, credenciais)
- Templates estáticos diretamente no código VB.NET (strings concatenadas)
- **SEM biblioteca de templates**
- **SEM design responsivo**
- **SEM rastreamento de abertura/cliques**
- **SEM testes A/B**
- **SEM personalização de branding por empresa**

---

## 2. TELAS DO LEGADO

### Tela: Correio.aspx

- **Caminho:** `ic1_legado/IControlIT/Correio.aspx`
- **Responsabilidade:** Tela para envio manual de e-mails pelo usuário (formulário simples)

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|------|------|-------------|-------------|
| Para (Destinatário) | TextBox | Sim | Aceita múltiplos e-mails separados por vírgula |
| Assunto | TextBox | Sim | Texto simples, sem variáveis |
| Mensagem | TextArea | Sim | HTML básico aceito, sem validação |
| Anexos | FileUpload | Não | Upload de arquivos permitido |

#### Comportamentos Implícitos

- **Validação de e-mail ausente:** Aceita qualquer string no campo "Para", sem validação de formato
- **Sem preview:** Usuário não vê prévia do e-mail antes de enviar
- **Sem histórico:** E-mails enviados não são armazenados no banco de dados
- **Sem retry:** Falha no envio resulta em perda do e-mail (sem fila de reenvio)
- **SMTP hardcoded:** Configurações de servidor SMTP estão no Web.config, usuário não pode alterar
- **Sem rastreamento:** Impossível saber se e-mail foi aberto ou clicado

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

| Método | Local | Responsabilidade | Observações |
|------|-------|------------------|-------------|
| EnviarEmail() | Default.aspx.vb | Envio básico via System.Net.Mail.SmtpClient | Método estático usado em várias partes do sistema |
| ConfigurarSMTP() | Web.config | Configurações de servidor SMTP | Hardcoded, sem interface de gerenciamento |
| NotificarUsuario() | Termo module | Envia notificação de aceite de termo | Template de e-mail embutido no código VB.NET |

**Exemplo de código legado (Default.aspx.vb):**

```vb
' Método básico de envio de e-mail no legado
Public Shared Sub EnviarEmail(destinatario As String, assunto As String, corpo As String)
    Dim smtp As New SmtpClient(ConfigurationManager.AppSettings("SmtpHost"))
    smtp.Port = CInt(ConfigurationManager.AppSettings("SmtpPort"))
    smtp.Credentials = New NetworkCredential(
        ConfigurationManager.AppSettings("SmtpUser"),
        ConfigurationManager.AppSettings("SmtpPassword")
    )

    Dim mail As New MailMessage()
    mail.From = New MailAddress(ConfigurationManager.AppSettings("SmtpFrom"))
    mail.To.Add(destinatario)
    mail.Subject = assunto
    mail.Body = corpo
    mail.IsBodyHtml = True

    smtp.Send(mail) ' Sem tratamento de erro, sem retry
End Sub
```

**Problemas identificados:**
- ❌ Sem tratamento de exceção
- ❌ Sem fila de envio (bloqueio síncrono)
- ❌ Sem retry automático em caso de falha
- ❌ Corpo do e-mail concatenado manualmente (strings hardcoded)
- ❌ Sem validação de destinatário
- ❌ Sem logs de auditoria

---

## 4. TABELAS LEGADAS

**NENHUMA tabela relacionada a templates de e-mail existe no legado.**

O sistema legado **NÃO armazena templates** no banco de dados. Templates são strings hardcoded no código VB.NET.

| Tabela | Finalidade | Problemas Identificados |
|-------|------------|-------------------------|
| (Inexistente) | Templates de e-mail | **Não existe** — Templates embutidos no código |
| (Inexistente) | Histórico de envios | **Não existe** — Sem rastreabilidade de e-mails enviados |
| (Inexistente) | Métricas de e-mail | **Não existe** — Sem tracking de abertura/cliques |

---

## 5. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

Regras identificadas no código VB.NET que **NÃO estavam documentadas formalmente:**

- **RL-RN-001: SMTP síncrono bloqueia requisição**
  - Sistema trava durante envio de e-mail (sem fila assíncrona)
  - Timeout de 30 segundos pode causar erro HTTP 500 se SMTP demorar

- **RL-RN-002: Templates hardcoded no código VB.NET**
  - E-mails de notificação (termo aceito, alerta de vencimento) estão embutidos no código
  - Alterar template exige recompilação e deploy da aplicação

- **RL-RN-003: Configuração SMTP global (Web.config)**
  - Uma única configuração SMTP para todo o sistema
  - Impossível customizar servidor SMTP por empresa/cliente

- **RL-RN-004: Sem validação de deliverability**
  - Sistema não verifica SPF/DKIM/DMARC
  - E-mails frequentemente caem em spam

- **RL-RN-005: Sem controle de unsubscribe (CAN-SPAM/LGPD)**
  - Usuários não podem se descadastrar de e-mails automaticamente
  - Violação potencial de LGPD e CAN-SPAM Act

---

## 6. GAP ANALYSIS (LEGADO x RF MODERNO)

| Item | Legado | RF-064 Moderno | Observação |
|-----|--------|----------------|------------|
| **Templates** | ❌ Hardcoded no código VB.NET | ✅ Biblioteca gerenciável via UI | **GAP CRÍTICO** — Funcionalidade nova |
| **Design Responsivo** | ❌ HTML estático (desktop-only) | ✅ CSS media queries mobile-first | **GAP CRÍTICO** — Mobile representa 60%+ de aberturas |
| **Rastreamento de Abertura** | ❌ Inexistente | ✅ Pixel tracking + métricas | **GAP CRÍTICO** — Sem visibilidade no legado |
| **Rastreamento de Cliques** | ❌ Inexistente | ✅ URL wrapping + analytics | **GAP CRÍTICO** — Impossível medir conversão |
| **Branding Customizado** | ❌ Logo/cores fixos | ✅ Branding por empresa (multi-tenant) | **GAP IMPORTANTE** — Necessário para white-label |
| **Teste A/B** | ❌ Inexistente | ✅ Variações automáticas + winner | **GAP IMPORTANTE** — Otimização de conversão |
| **Compatibilidade Multi-Cliente** | ❌ Não testado | ✅ Validado em Gmail/Outlook/Apple/Yahoo | **GAP IMPORTANTE** — Renderização quebrada no legado |
| **Fila de Envio Assíncrona** | ❌ SMTP síncrono | ✅ Hangfire job queue | **GAP IMPORTANTE** — Timeout frequente no legado |
| **Versionamento de Templates** | ❌ Inexistente | ✅ Controle de versão (v1.0 → v2.0) | **GAP MÉDIO** — Rollback impossível no legado |
| **Preview Multi-Dispositivo** | ❌ Inexistente | ✅ Preview desktop/tablet/mobile | **GAP MÉDIO** — Melhor UX |
| **Anti-Spam Score** | ❌ Não calculado | ✅ SpamAssassin score | **GAP MÉDIO** — Deliverability ruim no legado |
| **Unsubscribe (LGPD/CAN-SPAM)** | ❌ Ausente | ✅ Link obrigatório + gestão opt-out | **GAP CRÍTICO (LEGAL)** — Violação regulatória |

**Conclusão:** O RF-064 é **95% funcionalidade nova**. Apenas 5% (envio SMTP básico) existe no legado, mas será **completamente redesenhado** com arquitetura moderna (Hangfire, tracking, branding, templates).

---

## 7. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Criar biblioteca de templates do zero

- **Descrição:** Implementar sistema completo de templates gerenciáveis (CRUD, preview, versionamento)
- **Motivo:** Legado não possui biblioteca de templates — templates hardcoded no código VB.NET são insustentáveis
- **Impacto:** **Alto** — Exige desenvolvimento de nova funcionalidade completa
- **Benefício:** Permitirá gerenciamento visual de templates sem deploy de código

### Decisão 2: Implementar rastreamento via pixel/URL wrapping

- **Descrição:** Adicionar pixel invisível (1x1) para rastreamento de abertura + URL wrapping para rastreamento de cliques
- **Motivo:** Legado não possui visibilidade de métricas de e-mail (open rate, CTR)
- **Impacto:** **Alto** — Exige infraestrutura de tracking (endpoint de pixel, serviço de redirect)
- **Benefício:** Métricas de engajamento permitirão otimizar comunicação com usuários

### Decisão 3: Migrar envio síncrono (SmtpClient) para assíncrono (Hangfire)

- **Descrição:** Substituir envio SMTP síncrono por fila assíncrona com Hangfire
- **Motivo:** Envio síncrono no legado causa timeout e bloqueia requisições HTTP
- **Impacto:** **Médio** — Exige configuração de Hangfire + jobs + retry policies
- **Benefício:** Melhor performance, retry automático, não bloqueia UI

### Decisão 4: Implementar branding customizado por empresa (multi-tenant)

- **Descrição:** Permitir que cada empresa configure logo, cores primárias/secundárias, rodapé customizado
- **Motivo:** Legado é single-tenant com logo fixo — impossível atender white-label
- **Impacto:** **Médio** — Exige tabela de branding + serviço de merge de dados
- **Benefício:** Habilita modelo white-label para clientes B2B

### Decisão 5: Adicionar validação de deliverability (SPF/DKIM/DMARC)

- **Descrição:** Validar configuração de autenticação de e-mail (SPF, DKIM, DMARC) antes de ativar template
- **Motivo:** E-mails do legado frequentemente caem em spam devido a falta de autenticação
- **Impacto:** **Baixo** — Validação via APIs externas (MXToolbox, Postmark)
- **Benefício:** Melhor deliverability (menos spam)

### Decisão 6: Implementar link de unsubscribe obrigatório (LGPD/CAN-SPAM)

- **Descrição:** Adicionar link "Cancelar inscrição" em todos os templates + gestão de opt-out
- **Motivo:** Legado não possui mecanismo de opt-out — violação de LGPD e CAN-SPAM Act
- **Impacto:** **Médio** — Exige tabela de opt-out + validação antes de envio
- **Benefício:** Conformidade legal (LGPD, CAN-SPAM)

---

## 8. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Probabilidade | Mitigação |
|------|---------|---------------|-----------|
| **Templates legados não funcionarão no novo sistema** | Alto | Certa | Criar ferramenta de conversão de strings VB.NET → templates HTML responsivos |
| **Usuários habituados a envio manual (Correio.aspx)** | Médio | Alta | Manter tela de envio manual como fallback durante transição |
| **Configuração SMTP legada (Web.config) precisa migrar** | Alto | Certa | Criar migration script para migrar Web.config → tabela ConfiguracaoSMTP |
| **E-mails em fila no momento da migração podem ser perdidos** | Alto | Média | Implementar flag de compatibilidade para processar fila legada antes de desligar sistema antigo |
| **Métricas de e-mail não existem no legado (sem baseline)** | Baixo | Certa | Aceitar que métricas começam do zero no sistema moderno |
| **Testes de compatibilidade (Gmail/Outlook) podem falhar em templates antigos** | Médio | Alta | Reprojetar templates críticos (boas-vindas, recuperação de senha) com design responsivo |

---

## 9. RASTREABILIDADE

| Elemento Legado | Referência RF-064 Moderno | Status Migração |
|----------------|---------------------------|-----------------|
| EnviarEmail() (Default.aspx.vb) | RN-RF064-001 (Design Responsivo) | **Substituído** — Novo sistema de templates |
| Correio.aspx (envio manual) | Seção 6.1 — Endpoint POST /api/templates-email/{id}/enviar | **Migrado** — UI moderna substituirá formulário legado |
| Configuração SMTP (Web.config) | Seção 5.6 — Tabela ConfiguracaoSMTP | **Migrado** — Configuração via UI em vez de arquivo |
| Templates hardcoded VB.NET | Seção 5.1 — Tabela TemplateEmail | **Substituído** — Biblioteca gerenciável |
| (Inexistente) Rastreamento | RN-RF064-003, RN-RF064-004 | **Funcionalidade Nova** — Pixel tracking + URL wrapping |
| (Inexistente) Teste A/B | RN-RF064-006 | **Funcionalidade Nova** — A/B testing automático |
| (Inexistente) Branding | RN-RF064-005 | **Funcionalidade Nova** — Branding por empresa |
| (Inexistente) Unsubscribe | RN-RF064-007 | **Funcionalidade Nova** — Conformidade LGPD/CAN-SPAM |

---

## 10. OBSERVAÇÕES FINAIS

### Funcionalidade Legada vs Nova

**O que existe no legado (5%):**
- ✅ Envio SMTP básico (System.Net.Mail.SmtpClient)
- ✅ Tela de envio manual (Correio.aspx)
- ✅ Configuração SMTP em Web.config

**O que é NOVO no RF-064 (95%):**
- ✨ Biblioteca de templates gerenciáveis
- ✨ Design responsivo (mobile-first)
- ✨ Rastreamento de abertura/cliques
- ✨ Teste A/B automático
- ✨ Branding customizado por empresa
- ✨ Compatibilidade multi-cliente (Gmail/Outlook/Apple/Yahoo)
- ✨ Fila assíncrona de envio (Hangfire)
- ✨ Versionamento de templates
- ✨ Preview multi-dispositivo
- ✨ Anti-spam score (SpamAssassin)
- ✨ Unsubscribe (LGPD/CAN-SPAM)
- ✨ Métricas de engajamento

### Conclusão

O RF-064 **NÃO é uma migração** de funcionalidade legada.
É uma **nova funcionalidade** que expande capacidades básicas de SMTP (legado) para um **sistema moderno de gestão de templates de e-mail** com rastreamento, personalização e conformidade legal.

A única parte do legado que será **migrada** é:
- Configuração SMTP (Web.config → tabela ConfiguracaoSMTP)
- Templates de e-mail críticos hardcoded no código VB.NET → converter para templates HTML responsivos

Todo o restante (biblioteca de templates, rastreamento, A/B testing, branding) é **funcionalidade inteiramente nova**.

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|------|------|-----------|-------|
| 2.0 | 2025-01-14 | Adequação para Governança v2.0 com análise completa do legado (envio SMTP básico) e identificação de que RF-064 é 95% funcionalidade nova | Agência ALC - alc.dev.br |
| 1.0 | 2025-01-14 | Análise inicial do sistema legado IControlIT v1.0 | Agência ALC - alc.dev.br |
