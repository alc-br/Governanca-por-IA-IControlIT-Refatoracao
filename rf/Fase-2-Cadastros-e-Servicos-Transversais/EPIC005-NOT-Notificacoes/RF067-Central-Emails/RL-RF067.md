# RL-RF067 — Referência ao Legado

**Versão:** 1.0
**Data:** 2025-12-30
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF067 - Central de E-mails
**Sistema Legado:** ASP.NET Web Forms + VB.NET
**Objetivo:** Documentar o comportamento do legado relacionado a envio de e-mails, garantindo rastreabilidade, entendimento histórico e mitigação de riscos.

---

## 1. CONTEXTO DO LEGADO

### Sistema Legado

- **Arquitetura:** Monolítica WebForms com WebServices SOAP
- **Linguagem / Stack:** VB.NET, ASP.NET Web Forms (.NET Framework 4.7.2)
- **Banco de Dados:** SQL Server
- **Multi-tenant:** Sim (segregação por banco de dados, não por EmpresaId)
- **Auditoria:** Parcial (apenas logs de erro em arquivos texto)
- **Configurações:** web.config com credenciais SMTP em texto claro ou criptografia proprietária

### Observações Gerais

O sistema legado **não possui uma Central de E-mails** dedicada. O envio de e-mails era feito de forma descentralizada em diversas telas e módulos, sem controle centralizado de fila, retry, rastreamento ou deliverability.

Principais problemas identificados:
- Envio direto de e-mail sem fila (bloqueante)
- Sem retry em caso de falha
- Sem rastreamento de entrega/abertura/cliques
- Sem blacklist
- Sem rate limiting
- Configuração SMTP em web.config (não multi-tenant)
- Logs de erro gravados em `C:\Temp\Log*.txt`

---

## 2. TELAS DO LEGADO

### Tela: Default.aspx (Login e Reset de Senha)

- **Caminho:** `ic1_legado/IControlIT/IControlIT/Default.aspx`
- **Responsabilidade:** Autenticação de usuários e envio de e-mail para reset de senha

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|------|------|-------------|-------------|
| E-mail | TextBox | Sim | E-mail do usuário para envio de token |

#### Comportamentos Implícitos

- Envio de e-mail para reset de senha usando credenciais SMTP configuradas em stored procedure
- E-mail enviado de forma síncrona (bloqueia UI se SMTP falhar)
- Sem retry em caso de falha
- Sem validação de MX record
- Sem rastreamento de entrega

---

### Tela: Termo\Correio.aspx (Envio de Termo por E-mail)

- **Caminho:** `ic1_legado/IControlIT/IControlIT/Termo/Correio.aspx`
- **Responsabilidade:** Enviar termo de responsabilidade/devolução por e-mail

#### Comportamentos Implícitos

- Anexos gravados em `C:\Temp\mail\att\`
- Envio usando configuração SMTP de stored procedure
- Sem retry
- Sem rastreamento
- Sem validação de destinatário

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

| Método | Local | Responsabilidade | Observações |
|------|-------|------------------|-------------|
| Nenhum método específico | N/A | Não há WebService dedicado a e-mails | Envio feito inline nas páginas |

**Observação:** O sistema legado não possui WebService dedicado para envio de e-mails. Cada tela que precisa enviar e-mail implementa a lógica localmente usando `System.Net.Mail.SmtpClient`.

---

## 4. TABELAS LEGADAS

| Tabela | Finalidade | Problemas Identificados |
|-------|------------|-------------------------|
| Nenhuma tabela específica | N/A | Não há tabela para armazenar histórico de e-mails enviados |

**Observação:** O sistema legado não armazena histórico de e-mails enviados. Não há rastreamento de entregas, aberturas ou cliques.

---

## 5. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

### RL-RN-001: Configuração SMTP via Stored Procedure

**Descrição:** Credenciais SMTP (host, porta, usuário, senha) eram armazenadas em stored procedures ou web.config, não em tabela multi-tenant.

**Fonte:** Análise de `web.config` e documentação do README legado

**Problema:** Configuração não isolada por tenant, dificultando uso de servidores SMTP diferentes por cliente.

---

### RL-RN-002: Envio Síncrono sem Fila

**Descrição:** E-mails eram enviados de forma síncrona durante processamento de requisição HTTP, bloqueando UI em caso de falha SMTP.

**Fonte:** Padrão observado em módulos de reset de senha e envio de termos

**Problema:** Latência alta e experiência ruim em caso de falha SMTP.

---

### RL-RN-003: Sem Retry em Falha

**Descrição:** Se envio falhasse, erro era exibido para usuário ou logado em arquivo, mas não havia retry automático.

**Fonte:** Ausência de mecanismo de fila ou background job

**Problema:** E-mails críticos podiam ser perdidos por falha temporária.

---

### RL-RN-004: Anexos em Pasta Local

**Descrição:** Anexos de e-mail eram salvos em `C:\Temp\mail\att\` no servidor.

**Fonte:** `ic1_legado/README.md` linha 66

**Problema:** Não escalável, risco de saturação de disco, sem limpeza automática.

---

### RL-RN-005: Logs em Arquivo Texto

**Descrição:** Erros de envio eram gravados em `C:\Temp\Log*.txt`.

**Fonte:** `ic1_legado/README.md` linha 22

**Problema:** Sem estruturação, difícil consulta, sem retenção controlada.

---

### RL-RN-006: Sem Rastreamento de Entrega

**Descrição:** Sistema não rastreava se e-mail foi entregue, aberto ou clicado.

**Fonte:** Ausência de tabela de histórico de e-mails

**Problema:** Impossível diagnosticar problemas de deliverability ou medir engajamento.

---

### RL-RN-007: Sem Blacklist

**Descrição:** Sistema não mantinha blacklist de e-mails com hard bounce ou spam complaints.

**Fonte:** Ausência de tabela de blacklist

**Problema:** Desperdício de recursos tentando enviar para e-mails inexistentes repetidamente.

---

### RL-RN-008: Sem Rate Limiting

**Descrição:** Nenhum controle de limite de envios por domínio ou período.

**Fonte:** Ausência de controle de fila

**Problema:** Risco de ser marcado como spam por provedores.

---

### RL-RN-009: Sem Validação de MX Record

**Descrição:** Sistema não verificava se domínio do e-mail tinha MX record válido antes de tentar enviar.

**Fonte:** Padrão de envio direto

**Problema:** Tentativas de envio para domínios inexistentes.

---

### RL-RN-010: Sem Conformidade LGPD para Unsubscribe

**Descrição:** Não havia mecanismo de unsubscribe com um clique.

**Fonte:** Ausência de funcionalidade

**Problema:** Não-conformidade com LGPD e melhores práticas anti-spam.

---

## 6. GAP ANALYSIS (LEGADO x RF MODERNO)

| Item | Legado | RF067 Moderno | Observação |
|-----|--------|---------------|------------|
| Fila de envio | ❌ Não existia | ✅ Fila com priorização | CRÍTICO - E-mails críticos podiam ser atrasados |
| Retry automático | ❌ Não existia | ✅ Até 5x com backoff | CRÍTICO - E-mails perdidos em falhas temporárias |
| Rastreamento | ❌ Não existia | ✅ Entrega, abertura, cliques | IMPORTANTE - Sem métricas de engajamento |
| Blacklist | ❌ Não existia | ✅ Automática e manual | IMPORTANTE - Desperdício de recursos |
| Rate limiting | ❌ Não existia | ✅ 100/hora por domínio | IMPORTANTE - Risco de spam flags |
| Warmup de IP | ❌ Não existia | ✅ 15 dias graduais | IMPORTANTE - Reputação de envio |
| Validação MX | ❌ Não existia | ✅ Antes de enfileirar | MÉDIA - Economia de recursos |
| Unsubscribe | ❌ Não existia | ✅ Um clique (LGPD) | CRÍTICO - Conformidade legal |
| Health check SMTP | ❌ Não existia | ✅ A cada 5 minutos | IMPORTANTE - Detecção proativa de falhas |
| SPF/DKIM/DMARC | ❌ Não configurado | ✅ Configuração validada | IMPORTANTE - Deliverability |
| Templates | ❌ Inline nas telas | ✅ RF064 integrado | IMPORTANTE - Padronização |
| Supressão duplicatas | ❌ Não existia | ✅ 24h | MÉDIA - Experiência do usuário |
| Relatórios | ❌ Não existia | ✅ Deliverability completo | IMPORTANTE - Análise de desempenho |
| Multi-provedor | ❌ Apenas SMTP | ✅ SendGrid, Mailgun, SES | IMPORTANTE - Flexibilidade |
| Multi-tenant SMTP | ❌ Configuração global | ✅ Por tenant | CRÍTICO - Isolamento |
| Auditoria | ❌ Log em arquivo | ✅ Auditoria estruturada | IMPORTANTE - Rastreabilidade |
| Envio assíncrono | ❌ Síncrono | ✅ Assíncrono com fila | CRÍTICO - Performance |

---

## 7. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Criar Central de E-mails do Zero

**Motivo:** Sistema legado não possui funcionalidade equivalente. Toda a lógica de envio de e-mail será modernizada com arquitetura de fila, retry e rastreamento.

**Impacto:** Alto - Migração de todos os pontos de envio para usar nova Central.

**Data:** 2025-12-30

---

### Decisão 2: Usar Hangfire para Fila e Retry

**Motivo:** Hangfire suporta filas priorizadas, retry automático e monitoramento.

**Impacto:** Médio - Dependência adicional no backend.

**Data:** 2025-12-30

---

### Decisão 3: Rastreamento com Pixel e URL Redirecionada

**Motivo:** Padrão de mercado para rastreamento de abertura (pixel 1x1) e cliques (URL redirecionada).

**Impacto:** Baixo - Funcionalidade padrão.

**Data:** 2025-12-30

---

### Decisão 4: Blacklist Automática para Hard Bounce

**Motivo:** Evitar desperdício de recursos e manter boa reputação de envio.

**Impacto:** Médio - Requer integração com webhooks de provedores (SendGrid, Mailgun).

**Data:** 2025-12-30

---

### Decisão 5: Suporte a Múltiplos Provedores

**Motivo:** Flexibilidade para usar SendGrid, Mailgun, Amazon SES ou SMTP próprio conforme necessidade do tenant.

**Impacto:** Alto - Abstração de provedor necessária.

**Data:** 2025-12-30

---

## 8. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Mitigação |
|------|---------|-----------|
| Migração de pontos de envio | Alto | Identificar todos os pontos de envio no legado e migrar para usar nova Central |
| Configuração SMTP por tenant | Alto | Criar migração de configurações SMTP do web.config para tabela multi-tenant |
| Anexos em C:\Temp | Médio | Migrar anexos para storage cloud (Azure Blob Storage) |
| Logs em arquivo texto | Baixo | Substituir por auditoria estruturada no banco |
| E-mails em fila durante migração | Médio | Garantir que e-mails não sejam perdidos durante transição |

---

## 9. RASTREABILIDADE

| Elemento Legado | Referência RF |
|----------------|---------------|
| Default.aspx (reset senha) | RN-RF067-01 (Fila de prioridades - e-mail crítico) |
| Termo\Correio.aspx | RN-RF067-04 (Rastreamento), RN-RF067-12 (Templates) |
| Configuração SMTP web.config | RN-RF067-02 (SMTP Pools), RN-RF067-16 (Multi-tenant) |
| Logs em C:\Temp | RN-RF067-17 (Auditoria estruturada) |
| Anexos em C:\Temp\mail\att | RN-RF067-12 (Templates com anexos) |
| Envio síncrono | RN-RF067-03 (Retry assíncrono) |
| Sem rastreamento | RN-RF067-04 (Rastreamento completo) |
| Sem blacklist | RN-RF067-05 (Blacklist automática) |
| Sem validação MX | RN-RF067-08 (Validação de e-mail) |
| Sem unsubscribe | RN-RF067-09 (Unsubscribe LGPD) |

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|------|------|----------|------|
| 1.0 | 2025-12-30 | Documentação completa de referência ao legado (sistema não possuía Central de E-mails) | Agência ALC - alc.dev.br |
