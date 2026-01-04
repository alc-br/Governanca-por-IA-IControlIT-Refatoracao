# RL-RF087 — Referência ao Legado (Gestão de Integrações)

**Versão:** 1.0
**Data:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF-087
**Sistema Legado:** IControlIT v1 (ASP.NET Web Forms + VB.NET)
**Objetivo:** Documentar que esta funcionalidade é NOVA e não possui equivalente no sistema legado. Qualquer integrações no legado eram hardcoded diretamente no código-fonte.

---

## 1. CONTEXTO DO SISTEMA LEGADO

### 1.1 Stack Tecnológica do Legado

- **Arquitetura:** Monolítica (ASP.NET Web Forms)
- **Linguagem:** VB.NET (code-behind .aspx.vb)
- **Frontend:** ASP.NET Web Forms (ViewState, PostBack)
- **Backend:** VB.NET + ADO.NET
- **Banco de Dados:** SQL Server (múltiplas instâncias por cliente)
- **Multi-tenant:** Parcial (bancos separados por cliente)
- **Auditoria:** Parcial (sem padrão consistente)
- **Configurações:** Web.config + AppSettings no banco

### 1.2 Problemas Arquiteturais Identificados

1. **Ausência de Gestão Centralizada de Integrações**
   - Integrações eram hardcoded diretamente no código VB.NET
   - Cada integração exigia deploy de código novo
   - Sem interface administrativa para configurar integrações
   - Sem monitoramento centralizado de execuções
   - Sem tratamento padronizado de erros

2. **Credenciais em Texto Plano**
   - Credenciais de APIs externas armazenadas em Web.config
   - Alguns casos: credenciais hardcoded no código VB.NET
   - Sem criptografia de credenciais sensíveis
   - Difícil rotação de credenciais (exigia deploy)

3. **Falta de Resiliência**
   - Sem Circuit Breaker (falhas em cascata)
   - Sem Rate Limiting (sobrecarga de APIs externas)
   - Sem Retry automático (falhas transitórias não tratadas)
   - Timeout hardcoded ou ausente

4. **Ausência de Auditoria de Integrações**
   - Não havia log centralizado de execuções
   - Difícil rastrear quando/quem executou integração
   - Sem histórico de request/response para debugging

---

## 2. TELAS ASPX DO LEGADO

### 2.1 Não Aplicável

**DESTINO:** DESCARTADO

**Justificativa:** O sistema legado **NÃO** possui telas de gestão de integrações. Toda configuração era feita via código ou Web.config.

---

## 3. WEBSERVICES E MÉTODOS LEGADOS

### 3.1 Integrações Hardcoded Encontradas

Durante a análise do código legado, foram identificadas integrações diretas (sem gestão centralizada):

| Localização | Sistema Externo | Descrição | DESTINO |
|-------------|-----------------|-----------|---------|
| `ic1_legado/IControlIT/Classes/IntegracaoERP.vb` | ERP (não especificado) | Integração hardcoded com ERP via XML | SUBSTITUÍDO |
| `ic1_legado/IControlIT/Classes/EmailService.vb` | SMTP (Gmail/Outlook) | Envio de emails sem configuração dinâmica | SUBSTITUÍDO |
| `ic1_legado/IControlIT/WebServices/ImportacaoUsuarios.asmx` | LDAP/Active Directory | Importação manual de usuários do AD | SUBSTITUÍDO |

**Justificativa de SUBSTITUÍDO:**
Todas essas integrações hardcoded serão substituídas por configurações dinâmicas no módulo de Gestão de Integrações do RF-087.

---

## 4. STORED PROCEDURES DO LEGADO

### 4.1 Não Aplicável

**DESTINO:** DESCARTADO

**Justificativa:** Não há stored procedures específicas para gestão de integrações no legado. Integrações eram código VB.NET apenas.

---

## 5. TABELAS LEGADAS

### 5.1 Configurações de Integração (Tabela AppSettings)

**Tabela:** `[dbo].[AppSettings]`
**Problemas Identificados:**
- Chave-valor genérico (não específico para integrações)
- Valores em texto plano (sem criptografia)
- Sem versionamento ou auditoria de alterações
- Sem suporte a múltiplos endpoints
- Sem separação por tenant (global para todos os clientes)

**DESTINO:** SUBSTITUÍDO

**Justificativa:** Será substituído por tabelas especializadas (Integracao, IntegracaoEndpoint, IntegracaoExecucao) com criptografia, auditoria e multi-tenancy.

---

## 6. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

### RL-RN-001: Timeout Fixo de 30 Segundos
**Localização:** `ic1_legado/IControlIT/Classes/IntegracaoERP.vb:45`
**Descrição:** Requisições HTTP tinham timeout hardcoded de 30 segundos, sem configuração.
**DESTINO:** ASSUMIDO
**Rastreabilidade:** RN-RF087-005 (Timeout Configurável com padrão de 30 segundos)

---

### RL-RN-002: Retry de 3 Tentativas
**Localização:** `ic1_legado/IControlIT/Classes/IntegracaoERP.vb:78`
**Descrição:** Lógica manual de retry com 3 tentativas e delay fixo de 1 segundo.
**DESTINO:** SUBSTITUÍDO
**Rastreabilidade:** RN-RF087-008 (Retry com Backoff Exponencial)
**Migração Moderna:** Biblioteca Polly com backoff exponencial

---

### RL-RN-003: Credenciais em Web.config
**Localização:** `ic1_legado/IControlIT/Web.config`
**Descrição:** Credenciais de APIs externas armazenadas em texto plano no Web.config.
**DESTINO:** SUBSTITUÍDO
**Rastreabilidade:** RN-RF087-004 (Credenciais Criptografadas)
**Migração Moderna:** Campo CredenciaisJson criptografado no banco de dados

---

### RL-RN-004: Logs em Arquivo TXT
**Localização:** `ic1_legado/IControlIT/Logs/`
**Descrição:** Logs de integrações salvos em arquivos .txt sem estrutura.
**DESTINO:** SUBSTITUÍDO
**Rastreabilidade:** RN-RF087-015 (Auditoria de Execuções)
**Migração Moderna:** Tabela IntegracaoExecucao com JSON estruturado

---

### RL-RN-005: Ausência de Circuit Breaker
**Localização:** Todo o código legado
**Descrição:** Não havia proteção contra falhas em cascata. Se API externa falhava, tentava infinitamente.
**DESTINO:** A_REVISAR (funcionalidade nova)
**Rastreabilidade:** RN-RF087-006 (Circuit Breaker)
**Migração Moderna:** Biblioteca Polly com padrão Circuit Breaker

---

### RL-RN-006: Ausência de Rate Limiting
**Localização:** Todo o código legado
**Descrição:** Não havia controle de quantidade de requisições. Risco de sobrecarga de APIs externas.
**DESTINO:** A_REVISAR (funcionalidade nova)
**Rastreabilidade:** RN-RF087-007 (Rate Limiting)
**Migração Moderna:** Sliding window counter implementado

---

## 7. GAP ANALYSIS (LEGADO × MODERNO)

| Item | Legado | RF-087 Moderno | Observação |
|------|--------|----------------|------------|
| **Gestão de Integrações** | Hardcoded no código VB.NET | Interface administrativa completa | Funcionalidade NOVA |
| **Credenciais** | Texto plano (Web.config) | Criptografadas (banco de dados) | Segurança crítica |
| **Resiliência** | Ausente | Circuit Breaker + Rate Limiting + Retry | Funcionalidade NOVA |
| **Monitoramento** | Logs em arquivos .txt | Dashboard com estatísticas e histórico | Funcionalidade NOVA |
| **Webhooks** | Ausente | Suporte a webhooks IN/OUT com HMAC | Funcionalidade NOVA |
| **Filas** | Ausente | Processamento assíncrono com Hangfire | Funcionalidade NOVA |
| **Multi-tenant** | Parcial (bancos separados) | Completo (Row-Level Security) | Melhoria |
| **Auditoria** | Inexistente | Completa (AuditInterceptor) | Funcionalidade NOVA |
| **Tipos de Integração** | Apenas HTTP (hardcoded) | REST, SOAP, GraphQL, Webhooks, FTP, SFTP, LDAP | Expansão significativa |
| **Autenticação** | Basic apenas | NONE, Basic, Bearer, API Key, OAuth2, mTLS | Expansão significativa |

---

## 8. DECISÕES DE MODERNIZAÇÃO

### 8.1 Decisão: Criar Módulo de Gestão de Integrações do Zero
- **Motivo:** O legado não possui funcionalidade equivalente. Integrações eram hardcoded.
- **Impacto:** ALTO (funcionalidade totalmente nova)
- **Benefício:** Permite configurar integrações sem deploy de código, aumenta flexibilidade e segurança.

---

### 8.2 Decisão: Usar Biblioteca Polly para Resiliência
- **Motivo:** Implementar Circuit Breaker, Retry e Timeout de forma padronizada e testada.
- **Impacto:** MÉDIO (nova dependência externa)
- **Benefício:** Evita reimplementar padrões complexos de resiliência. Polly é padrão da indústria.

---

### 8.3 Decisão: Usar Hangfire para Processamento Assíncrono
- **Motivo:** Executar integrações longas em background sem bloquear requisições HTTP.
- **Impacto:** MÉDIO (nova dependência externa + infraestrutura de filas)
- **Benefício:** Melhora performance e experiência do usuário.

---

### 8.4 Decisão: Criptografar Credenciais no Banco
- **Motivo:** Credenciais em texto plano é vulnerabilidade crítica.
- **Impacto:** MÉDIO (implementar lógica de criptografia/descriptografia)
- **Benefício:** Atende padrões de segurança (LGPD, ISO 27001).

---

### 8.5 Decisão: Suportar Múltiplos Tipos de Integração
- **Motivo:** Legado só tinha HTTP. Modernizar exige suporte a SOAP, GraphQL, FTP, LDAP, etc.
- **Impacto:** ALTO (implementar múltiplos clientes/protocolos)
- **Benefício:** Sistema flexível para qualquer tipo de integração externa.

---

## 9. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Mitigação |
|------|---------|-----------|
| **Dependência de Integrações Hardcoded** | ALTO | Mapear todas as integrações hardcoded existentes e configurá-las no novo módulo antes de desativar o código legado. |
| **Credenciais Perdidas** | ALTO | Documentar todas as credenciais do Web.config e migrá-las de forma criptografada para o novo banco. |
| **Falta de Histórico de Execuções** | MÉDIO | Aceitar que logs antigos (arquivos .txt) não serão migrados. Novo sistema começa histórico do zero. |
| **Mudança de Comportamento (Retry/Timeout)** | BAIXO | Configurar novos valores de retry e timeout compatíveis com o legado (3 tentativas, 30 segundos). |
| **Falta de Testes de Integrações Externas** | ALTO | Criar ambiente de staging com APIs mock para testar integrações sem impactar sistemas externos reais. |

---

## 10. RASTREABILIDADE

| Elemento Legado | Destino | RF-087 Moderno |
|----------------|---------|----------------|
| `IntegracaoERP.vb` | SUBSTITUÍDO | UC01-criar-integracao (tipo REST_API) |
| `EmailService.vb` | SUBSTITUÍDO | UC01-criar-integracao (tipo SMTP - futuro) |
| `ImportacaoUsuarios.asmx` | SUBSTITUÍDO | UC01-criar-integracao (tipo LDAP) |
| `AppSettings` (credenciais) | SUBSTITUÍDO | Tabela Integracao (campo CredenciaisJson criptografado) |
| Logs em .txt | SUBSTITUÍDO | Tabela IntegracaoExecucao |
| Timeout hardcoded (30s) | ASSUMIDO | RN-RF087-005 (padrão 30 segundos configurável) |
| Retry manual (3 tentativas) | SUBSTITUÍDO | RN-RF087-008 (Polly com backoff exponencial) |
| Circuit Breaker | FUNCIONALIDADE NOVA | RN-RF087-006 |
| Rate Limiting | FUNCIONALIDADE NOVA | RN-RF087-007 |
| Webhooks | FUNCIONALIDADE NOVA | RN-RF087-013 |
| Filas | FUNCIONALIDADE NOVA | RN-RF087-014 |

---

## 11. PROBLEMAS LEGADO IDENTIFICADOS

### PROB-RF087-001: Credenciais em Texto Plano
**Severidade:** CRÍTICA
**Descrição:** Credenciais de APIs externas armazenadas em Web.config sem criptografia. Vulnerabilidade de segurança grave.
**Impacto:** Exposição de credenciais em caso de vazamento de código ou acesso ao servidor.
**Solução Moderna:** Campo CredenciaisJson criptografado com AES-256 no banco de dados. Nunca expor em logs ou APIs.

---

### PROB-RF087-002: Ausência de Resiliência
**Severidade:** ALTA
**Descrição:** Sem Circuit Breaker, Rate Limiting ou Retry inteligente. Falhas em APIs externas causavam falhas em cascata.
**Impacto:** Indisponibilidade do sistema quando APIs externas falhavam.
**Solução Moderna:** Biblioteca Polly com Circuit Breaker, Retry com backoff exponencial e Rate Limiting.

---

### PROB-RF087-003: Integrações Hardcoded
**Severidade:** ALTA
**Descrição:** Cada nova integração exigia alterar código VB.NET e fazer deploy.
**Impacto:** Alto custo de manutenção, risco de bugs, tempo de entrega longo.
**Solução Moderna:** Interface administrativa para configurar integrações dinamicamente sem deploy.

---

### PROB-RF087-004: Logs Não Estruturados
**Severidade:** MÉDIA
**Descrição:** Logs de integrações salvos em arquivos .txt sem estrutura, difícil análise e monitoramento.
**Impacto:** Dificulta debugging e análise de problemas. Sem métricas de performance.
**Solução Moderna:** Tabela IntegracaoExecucao com JSON estruturado + Dashboard com estatísticas.

---

### PROB-RF087-005: Ausência de Auditoria
**Severidade:** MÉDIA
**Descrição:** Não havia registro de quem/quando alterou configurações de integrações.
**Impacto:** Falta de rastreabilidade em caso de problemas ou auditorias.
**Solução Moderna:** AuditInterceptor automático em todas as operações (Created, CreatedBy, LastModified, LastModifiedBy).

---

### PROB-RF087-006: Multi-Tenancy Parcial
**Severidade:** MÉDIA
**Descrição:** Bancos de dados separados por cliente dificultava gestão centralizada de integrações.
**Impacto:** Cada cliente precisava ter configuração replicada manualmente.
**Solução Moderna:** Multi-tenancy com Row-Level Security (campo EmpresaId). Gestão centralizada por tenant.

---

## METADADOS

| Métrica | Valor |
|---------|-------|
| **Total de Itens Legado Rastreados** | 11 |
| **Itens ASSUMIDOS** | 1 |
| **Itens SUBSTITUÍDOS** | 7 |
| **Itens DESCARTADOS** | 1 |
| **Itens A_REVISAR** | 2 |
| **Cobertura de Destinos** | 100% |
| **Problemas Legado Identificados** | 6 |
| **Severidade Crítica** | 1 |
| **Severidade Alta** | 2 |
| **Severidade Média** | 3 |

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 1.0 | 2025-12-31 | Documentação inicial de referência ao legado (funcionalidade nova sem equivalente direto) | Agência ALC - alc.dev.br |
