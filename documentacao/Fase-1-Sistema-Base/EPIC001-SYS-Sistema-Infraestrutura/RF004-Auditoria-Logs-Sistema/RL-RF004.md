# RL-RF004 — Referência ao Legado: Sistema de Auditoria

**Versão:** 1.0
**Data:** 2025-12-29
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF-004 - Sistema de Auditoria e Logs do Sistema
**Sistema Legado:** Tabela Auditoria Simples (VB.NET + ASP.NET Web Forms)
**Objetivo:** Documentar o comportamento do sistema de auditoria legado que serve de base para a modernização com Sistema_Auditoria estruturado, garantindo rastreabilidade, entendimento histórico e mitigação de riscos. Diferente do RF-003 (logs técnicos), RF-004 audita ações de usuários e mudanças de dados de negócio.

---

## 1. CONTEXTO DO LEGADO

O sistema legado **possuía auditoria rudimentar** em tabela SQL simples, mas sem estrutura adequada para compliance (LGPD, SOX, ISO 27001).

- **Arquitetura:** Monolítica Web Forms (ASP.NET + VB.NET)
- **Linguagem / Stack:** VB.NET, ASP.NET Web Forms 4.x
- **Banco de Dados:** SQL Server (tabela `Auditoria`)
- **Multi-tenant:** Não (auditoria global sem segregação por empresa)
- **Auditoria:** Parcial (apenas texto livre sem snapshot/diff)
- **Configurações:** Não configurável (tudo logado, sem categorização ou retenção)

**Estrutura da Tabela Legada:**

```sql
CREATE TABLE Auditoria (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    Usuario VARCHAR(200),    -- Nome ou email do usuário
    Acao VARCHAR(500),       -- Descrição livre da ação
    Data DATETIME DEFAULT GETDATE()
);
```

**Características:**
- Tabela simples sem chave estrangeira (não relacionava com outras entidades)
- Sem índices otimizados (buscas lentas após milhares de registros)
- Sem particionamento (tabela única para todos os registros)
- Sem arquivamento (crescimento indefinido)

---

## 2. TELAS DO LEGADO

### Tela: ❌ NENHUMA INTERFACE ESPECÍFICA

O sistema legado **não possuía interface dedicada para visualizar auditoria**.

**Método de Acesso:**
- Administradores executavam **queries SQL diretas** via SQL Server Management Studio (SSMS)
- Buscas manuais com `WHERE Usuario LIKE '%admin%'` ou `WHERE CONVERT(DATE, Data) = '2023-10-15'`
- Sem filtros interativos, sem timeline, sem dashboards

**Problemas:**
1. ❌ Sem interface web (necessário acesso SSMS ao banco)
2. ❌ Sem autenticação específica (qualquer admin banco podia ler)
3. ❌ Sem auditoria de quem consultou auditoria (meta-auditoria zero)
4. ❌ Sem filtros amigáveis (data range, usuário, entidade)
5. ❌ Sem visualização de timeline de entidade
6. ❌ Sem export para CSV/JSON (copy/paste manual)

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

| Método | Local | Responsabilidade | Observações |
|--------|-------|------------------|-------------|
| `RegistrarAuditoria(usuario As String, acao As String)` | Code-behind (*.aspx.vb) | Inserir registro na tabela Auditoria | ❌ Sem snapshot antes/depois |
| ❌ Nenhum endpoint API | - | - | Auditoria não era acessível via API |
| ❌ Nenhum método de exportação | - | - | Sem compliance LGPD/SOX |

**Código VB.NET Legado:**

```vb.net
' Exemplo real de auditoria no sistema legado
Public Sub RegistrarAuditoria(usuario As String, acao As String)
    Dim sql As String = "INSERT INTO Auditoria (Usuario, Acao, Data) VALUES (@Usuario, @Acao, GETDATE())"
    Dim cmd As New SqlCommand(sql, connection)
    cmd.Parameters.AddWithValue("@Usuario", usuario)
    cmd.Parameters.AddWithValue("@Acao", acao)
    cmd.ExecuteNonQuery()
End Sub

' Uso típico (SEM SNAPSHOT!)
Try
    Dim empresaNome As String = txtNome.Text
    Dim sql As String = "UPDATE Empresa SET Nome = @Nome WHERE Id = @Id"
    ' ... executa UPDATE
    RegistrarAuditoria(Session("UserEmail"), "Empresa editada: " & empresaNome)
Catch ex As Exception
    ' ... erro
End Try
```

**Problemas Identificados:**

1. ❌ **Sem snapshot antes/depois** - Não armazenava estado da entidade
2. ❌ **Sem diff estruturado** - Impossível saber QUAIS campos foram alterados
3. ❌ **Sem IP/User-Agent** - Não rastreava origem do request
4. ❌ **Sem correlation ID** - Impossível correlacionar com logs técnicos
5. ❌ **Sem categorização** - Tudo era "Ação" genérica
6. ❌ **Sem retenção configurável** - Registros nunca eram deletados (compliance LGPD violado)
7. ❌ **Sem imutabilidade garantida** - Possível UPDATE/DELETE na tabela (adulteração)
8. ❌ **Sem assinatura digital** - Sem garantia de integridade

---

## 4. TABELAS LEGADAS

| Tabela | Finalidade | Problemas Identificados |
|--------|------------|-------------------------|
| `Auditoria` | Registrar ações de usuários em texto livre | ❌ Sem estrutura, sem snapshot, sem IP, sem retenção, sem imutabilidade, sem diff, sem categorização, sem compliance |

**DDL Legado Completo:**

```sql
CREATE TABLE Auditoria (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    Usuario VARCHAR(200),    -- Sem FK para tabela Usuario
    Acao VARCHAR(500),       -- Texto livre (não estruturado)
    Data DATETIME DEFAULT GETDATE()  -- Sem timezone
);

-- Sem índices otimizados!
-- Sem particionamento!
-- Sem trigger de imutabilidade!
```

**Observação:** Tabela permitia UPDATE e DELETE, violando princípio de auditoria imutável (append-only).

---

## 5. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

Regras que **não estavam documentadas**, apenas inferidas do código:

- **RL-RN-001:** Auditoria era registrada manualmente (cada tela chamava `RegistrarAuditoria` explicitamente) - alto risco de esquecer
- **RL-RN-002:** Formato de auditoria era fixo: `{Usuario} - {Acao} - {Data}`
- **RL-RN-003:** Não havia snapshot do estado anterior (impossível reconstruir histórico)
- **RL-RN-004:** Não havia diff (impossível saber QUAIS campos foram alterados)
- **RL-RN-005:** Não havia IP ou User-Agent (impossível rastrear origem de ações suspeitas)
- **RL-RN-006:** Não havia categorização (CRUD, AUTH, EXPORT, FINANCIAL, LGPD, etc.)
- **RL-RN-007:** Não havia retenção automática (registros nunca eram deletados)
- **RL-RN-008:** Não havia imutabilidade garantida (possível UPDATE/DELETE na tabela)
- **RL-RN-009:** Não havia assinatura digital (sem validação de integridade)
- **RL-RN-010:** Não havia auditoria de operações LGPD (acesso, exportação, consentimento, exclusão)
- **RL-RN-011:** Não havia timeline de entidade (impossível ver histórico cronológico)
- **RL-RN-012:** Não havia detecção de anomalias (exportações excessivas, acesso multi-tenant)
- **RL-RN-013:** Não havia segregação de funções (SOX violations não eram detectadas)
- **RL-RN-014:** Não havia arquivamento (custos crescentes com milhões de registros)
- **RL-RN-015:** Não havia alertas de retenção expirando (compliance reativa, não proativa)

---

## 6. GAP ANALYSIS (LEGADO x RF MODERNO)

| Item | Legado | RF Moderno | Observação |
|------|--------|------------|------------|
| **Estrutura** | ❌ Texto livre VARCHAR(500) | ✅ JSON estruturado (Before/After snapshots) | Permite reconstruir estado histórico |
| **Diff** | ❌ Inexistente | ✅ JSON Patch RFC 6902 | Saber exatamente quais campos mudaram |
| **IP/User-Agent** | ❌ Inexistente | ✅ Contexto completo (IP, User-Agent, Correlation ID) | Rastrear origem de ações |
| **Categorização** | ❌ Inexistente | ✅ 10 categorias (CRUD, AUTH, EXPORT, etc.) | Compliance LGPD/SOX/ISO |
| **Retenção** | ❌ Indefinida (nunca deletado) | ✅ Diferenciada (7 anos LGPD/SOX, 1 ano CRUD) | Compliance LGPD Art. 37/38 |
| **Imutabilidade** | ❌ Permitia UPDATE/DELETE | ✅ Append-only (trigger bloqueia UPDATE/DELETE) | Proteção contra adulteração |
| **Assinatura Digital** | ❌ Inexistente | ✅ Hash SHA-256 para registros críticos | Validação de integridade |
| **Timeline** | ❌ Inexistente | ✅ Timeline completa de entidade | Ver histórico cronológico |
| **Exportação** | ❌ Copy/paste manual SSMS | ✅ CSV/JSON via API | Auditoria externa (LGPD, SOX) |
| **Detecção Anomalias** | ❌ Inexistente | ✅ Alertas automáticos (>100 exports/h) | Segurança proativa |
| **Segregação Funções** | ❌ Inexistente | ✅ Detecção violações SOX | Compliance SOX Seção 404 |
| **Arquivamento** | ❌ Inexistente | ✅ Cold storage (Azure Blob > 1 ano) | Reduz custos 70%+ |
| **Multi-Tenancy** | ❌ Global | ✅ Tenant_Id/EmpresaId | Isolamento entre clientes |
| **Auditoria LGPD** | ❌ Inexistente | ✅ Tipos específicos (LGPD_ACCESS, LGPD_EXPORT, etc.) | Compliance LGPD Art. 37/38/46 |
| **Busca** | ❌ SQL manual SSMS | ✅ Full-text otimizada + interface web | Busca em milhões de registros |
| **Dashboards** | ❌ Inexistente | ✅ Compliance, Anomalias, Timeline, Analytics | Visibilidade executiva |
| **Alertas Retention** | ❌ Inexistente | ✅ Alerta 30 dias antes de expirar | Compliance proativo |

---

## 7. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Tabela Sistema_Auditoria Estruturada (JSON Snapshots + Diff)

**Justificativa:**
- **Compliance LGPD/SOX:** Necessário snapshot completo antes/depois para compliance
- **Diff Estruturado:** JSON Patch RFC 6902 permite queries "quem alterou o CPF?"
- **Timeline:** Reconstruir estado de entidade em qualquer momento do passado

**Impacto:** Alto (mudança radical de paradigma de auditoria)

**DDL Modernizado:**

```sql
CREATE TABLE Sistema_Auditoria (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    Timestamp DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    Tipo VARCHAR(50) NOT NULL,  -- CRUD, AUTH, EXPORT, LGPD, etc.
    Descricao NVARCHAR(500) NOT NULL,
    Entidade VARCHAR(100),
    EntidadeId UNIQUEIDENTIFIER,
    Usuario NVARCHAR(200),
    UserId UNIQUEIDENTIFIER,
    Tenant_Id UNIQUEIDENTIFIER NOT NULL,  -- Multi-tenancy
    IP VARCHAR(50),
    UserAgent NVARCHAR(500),
    CorrelationId UNIQUEIDENTIFIER,
    RequestId UNIQUEIDENTIFIER,
    SessionId UNIQUEIDENTIFIER,
    DadosAnteriores_JSON NVARCHAR(MAX),  -- Snapshot BEFORE
    DadosNovos_JSON NVARCHAR(MAX),       -- Snapshot AFTER
    Diff_JSON NVARCHAR(MAX),              -- JSON Patch RFC 6902
    Hash_SHA256 VARCHAR(64),              -- Assinatura digital
    Justificativa NVARCHAR(1000),         -- Obrigatória para CONFIG
    RetentionDate DATE,                    -- Data de expiração
    Arquivado BIT DEFAULT 0,
    AzureBlobUri VARCHAR(500)
);

-- Trigger de imutabilidade (bloqueia UPDATE/DELETE)
CREATE TRIGGER TR_Sistema_Auditoria_Immutable
ON Sistema_Auditoria
FOR UPDATE, DELETE
AS
BEGIN
    RAISERROR('Registros de auditoria são imutáveis (append-only). UPDATE/DELETE bloqueados.', 16, 1);
    ROLLBACK TRANSACTION;
END;
```

### Decisão 2: AuditingBehaviour<TRequest, TResponse> (MediatR Interceptor)

**Justificativa:**
- **Auditoria Automática:** Elimina risco de esquecer de auditar
- **Snapshot Automático:** Captura estado antes/depois sem código manual
- **DRY:** Lógica centralizada (não repetida em cada tela)

**Impacto:** Médio (requer refatoração para MediatR se não estiver implementado)

### Decisão 3: 10 Categorias de Auditoria (CRUD, AUTH, EXPORT, etc.)

**Justificativa:**
- **Retenção Diferenciada:** LGPD/SOX/Financial = 7 anos, CRUD/Admin = 1 ano
- **Compliance:** LGPD exige tipos específicos (LGPD_ACCESS, LGPD_EXPORT, etc.)
- **Dashboards:** Categorização permite relatórios executivos

**Impacto:** Baixo (enum simples)

### Decisão 4: Imutabilidade Garantida (Trigger SQL)

**Justificativa:**
- **Proteção Forense:** Auditoria não pode ser adulterada
- **Compliance ISO 27001:** Evidências devem ser imutáveis
- **SOX:** Registros financeiros não podem ser modificados

**Impacto:** Baixo (trigger SQL simples)

### Decisão 5: Assinatura Digital SHA-256

**Justificativa:**
- **Validação de Integridade:** Detectar adulteração de registros críticos
- **Compliance ISO 27001:** Evidências devem ter integridade verificável
- **Auditoria Forense:** Provar que registro não foi modificado

**Impacto:** Baixo (cálculo de hash em registros FINANCIAL/SECURITY/LGPD/CONFIG)

### Decisão 6: Arquivamento Automático (Azure Blob Cold Storage)

**Justificativa:**
- **Custos:** SQL Server caro para 50M+ registros (custo reduzido 70%+ com cold storage)
- **Performance:** Tabela menor = queries mais rápidas
- **Compliance:** Manter retenção 7 anos sem explodir custos

**Impacto:** Médio (job noturno + integração Azure Blob)

### Decisão 7: Detecção de Anomalias Automática

**Justificativa:**
- **Segurança Proativa:** Detectar exportações excessivas antes de vazamento
- **LGPD:** Monitorar acesso a dados pessoais (compliance Art. 46)
- **Fraude:** Detectar padrões suspeitos (acesso 50+ empresas/dia)

**Impacto:** Médio (regras de detecção + alertas)

### Decisão 8: Segregação de Funções (SOX)

**Justificativa:**
- **Compliance SOX Seção 404:** Mesmo usuário não pode criar E aprovar
- **Auditoria:** Detectar violações automaticamente
- **Governança:** Dashboard "Violações SOX" para compliance

**Impacto:** Médio (regras de validação + queries)

---

## 8. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Mitigação |
|-------|---------|-----------|
| **Migração de dados históricos** | Alto | Não migrar (legado mantido read-only para consulta histórica). Sistema novo começa limpo. |
| **Snapshots grandes (JSON) consumirem espaço** | Médio | Arquivamento automático > 1 ano (Azure Blob comprimido). Retenção diferenciada. |
| **Overhead performance (snapshot + diff)** | Médio | Auditoria assíncrona (fire-and-forget). Não bloqueia operação principal. |
| **Hash SHA-256 aumentar latência** | Baixo | Calcular hash apenas para categorias críticas (FINANCIAL, SECURITY, LGPD, CONFIG). |
| **Detecção anomalias gerar falsos positivos** | Baixo | Calibrar thresholds: >100 exports/h (não 10/h). Alertas configuráveis. |
| **Retenção 7 anos custar caro** | Médio | Cold storage (Azure Blob tier Cold) após 1 ano reduz custo 70%+. |
| **Falta de auditoria durante deploy** | Médio | Circuit breaker: se auditoria falhar, logar localmente + retry + alerta. |
| **Equipe não saber interpretar diff JSON** | Baixo | Interface web formata diff visualmente (campo: valor antigo → valor novo). |

---

## 9. RASTREABILIDADE

| Elemento Legado | Referência RF | Destino |
|-----------------|---------------|---------|
| Tabela `Auditoria` (Id, Usuario, Acao, Data) | RF-004 → Sistema_Auditoria (15+ campos) | **SUBSTITUÍDO** - Tabela moderna com snapshot, diff, IP, categorização |
| `RegistrarAuditoria(usuario, acao)` manual | RF-004 → RN-AUD-001 (AuditingBehaviour automático) | **SUBSTITUÍDO** - Interceptor MediatR (automático) |
| ❌ Sem snapshot antes/depois | RF-004 → RN-AUD-002 (snapshot completo) | **ASSUMIDO** - Snapshot obrigatório |
| ❌ Sem diff | RF-004 → RN-AUD-003 (JSON Patch RFC 6902) | **ASSUMIDO** - Diff estruturado |
| ❌ Sem IP/User-Agent | RF-004 → RN-AUD-010 (contexto enriquecido) | **ASSUMIDO** - Contexto completo |
| ❌ Sem categorização | RF-004 → 10 categorias (CRUD, AUTH, EXPORT, etc.) | **ASSUMIDO** - Categorização obrigatória |
| ❌ Sem retenção configurável | RF-004 → RN-AUD-004 (retenção diferenciada) | **ASSUMIDO** - 7 anos LGPD/SOX, 1 ano CRUD |
| ❌ Sem imutabilidade | RF-004 → RN-AUD-005 (append-only + trigger) | **ASSUMIDO** - Trigger bloqueia UPDATE/DELETE |
| ❌ Sem assinatura digital | RF-004 → RN-AUD-006 (hash SHA-256) | **ASSUMIDO** - Hash para registros críticos |
| ❌ Sem detecção anomalias | RF-004 → RN-AUD-007 (alertas automáticos) | **ASSUMIDO** - Detecção proativa |
| ❌ Sem auditoria LGPD | RF-004 → RN-AUD-008 (tipos LGPD_*) | **ASSUMIDO** - Compliance LGPD Art. 37/38/46 |
| ❌ Sem timeline | RF-004 → RN-AUD-009 (timeline de entidade) | **ASSUMIDO** - Timeline completa |
| ❌ Sem arquivamento | RF-004 → RN-AUD-011 (cold storage) | **ASSUMIDO** - Arquivamento automático > 1 ano |
| ❌ Sem segregação funções | RF-004 → RN-AUD-012 (SOX violations) | **ASSUMIDO** - Detecção violações SOX |
| ❌ Sem justificativa CONFIG | RF-004 → RN-AUD-013 (justificativa obrigatória) | **ASSUMIDO** - Compliance configurações críticas |
| ❌ Sem busca full-text | RF-004 → RN-AUD-014 (índice full-text) | **ASSUMIDO** - Busca otimizada milhões registros |
| ❌ Sem alertas retention | RF-004 → RN-AUD-015 (alertas 30 dias antes) | **ASSUMIDO** - Compliance proativo |

**IMPORTANTE - Destino Obrigatório:**
- **SUBSTITUÍDO:** Elemento legado foi completamente removido e substituído por solução moderna
- **ASSUMIDO:** Funcionalidade inexistente no legado, criada do zero no sistema moderno
- **DESCARTADO:** (não aplicável neste RF - toda funcionalidade legada foi modernizada)

---

## EXEMPLO REAL DE AUDITORIA LEGADA

**Query SQL Manual (SSMS):**

```sql
SELECT * FROM Auditoria
WHERE Usuario LIKE '%admin%'
  AND CONVERT(DATE, Data) = '2023-10-15'
ORDER BY Data DESC;
```

**Resultado Típico:**

| Id | Usuario | Acao | Data |
|----|---------|------|------|
| 1234 | admin@test.com | Empresa editada: Acme Corp | 2023-10-15 14:23:45 |
| 1235 | admin@test.com | Usuario criado: joao.silva | 2023-10-15 14:25:12 |
| 1236 | admin@test.com | Fatura aprovada: 12345 | 2023-10-15 14:27:33 |

**Problemas Identificados:**

1. ❌ **Sem snapshot** - Impossível saber QUAIS dados foram alterados em "Empresa editada"
2. ❌ **Sem diff** - Impossível responder "O CPF foi alterado nessa operação?"
3. ❌ **Sem IP** - Impossível rastrear origem da ação
4. ❌ **Sem contexto** - Qual navegador? Qual correlation ID? Qual tenant?
5. ❌ **Sem categorização** - "Fatura aprovada" deveria ser FINANCIAL (retenção 7 anos SOX)
6. ❌ **Sem retenção** - Registro nunca expira (compliance LGPD violado)
7. ❌ **Sem integridade** - Possível UPDATE manual (adulteração)
8. ❌ **Sem exportação** - Copy/paste manual (não atende compliance)

**Modernização (RF-004):**

```json
{
  "Id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "Timestamp": "2025-12-29T14:23:45.123Z",
  "Tipo": "CRUD",
  "Descricao": "Empresa editada: Acme Corp",
  "Entidade": "Empresa",
  "EntidadeId": "f1a2b3c4-d5e6-7890-abcd-123456789abc",
  "Usuario": "admin@test.com",
  "UserId": "u1s2e3r4-i5d6-7890-abcd-abcdef123456",
  "Tenant_Id": "tenant-123",
  "IP": "192.168.1.100",
  "UserAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
  "CorrelationId": "corr-123-456-789",
  "RequestId": "req-abc-def-ghi",
  "DadosAnteriores_JSON": "{\"Nome\":\"Acme Corporation\",\"CNPJ\":\"12.345.678/0001-90\",\"Email\":\"contato@acme.com\"}",
  "DadosNovos_JSON": "{\"Nome\":\"Acme Corp\",\"CNPJ\":\"12.345.678/0001-90\",\"Email\":\"comercial@acme.com\"}",
  "Diff_JSON": "[{\"op\":\"replace\",\"path\":\"/Nome\",\"value\":\"Acme Corp\"},{\"op\":\"replace\",\"path\":\"/Email\",\"value\":\"comercial@acme.com\"}]",
  "Hash_SHA256": null,
  "RetentionDate": "2032-12-29",
  "Arquivado": false
}
```

**Melhorias:**
- ✅ Snapshot completo antes/depois (pode reconstruir estado histórico)
- ✅ Diff estruturado (sabe exatamente QUAIS campos mudaram)
- ✅ Contexto completo (IP, User-Agent, Correlation ID, Tenant, Request ID)
- ✅ Categorização (CRUD = 7 anos retenção)
- ✅ Retenção automática (expira em 2032-12-29)
- ✅ Multi-tenancy (Tenant_Id)
- ✅ Imutabilidade garantida (trigger bloqueia UPDATE/DELETE)
- ✅ Timeline (pode buscar todas mudanças desta empresa)

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 1.0 | 2025-12-29 | Versão inicial - Referência ao Legado do RF-004 (Sistema de Auditoria). Documentação de 8 problemas críticos do legado (sem snapshot, sem diff, sem IP, sem categorização, sem retenção, sem imutabilidade, sem compliance LGPD/SOX/ISO). Rastreabilidade completa de 16 elementos legados com destino obrigatório (SUBSTITUÍDO/ASSUMIDO). | Agência ALC - alc.dev.br |
