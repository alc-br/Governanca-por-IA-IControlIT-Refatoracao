# RL-RF096 — Referência ao Legado

**Versão:** 1.0
**Data:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF096 - Auditoria de Mudanças de Dados
**Sistema Legado:** IControlIT v1.0 (ASP.NET Web Forms + VB.NET)
**Objetivo:** Documentar o comportamento do sistema legado de auditoria de mudanças para garantir rastreabilidade, entendimento histórico e mitigação de riscos na modernização para .NET 10 + Angular 19.

---

## 1. CONTEXTO DO LEGADO

### 1.1 Arquitetura Geral

- **Arquitetura:** Monolítica Cliente-Servidor (ASP.NET Web Forms 4.5)
- **Linguagem / Stack:** VB.NET, ASP.NET Web Forms, SQL Server 2016+
- **Banco de Dados:** SQL Server (banco `GUA`)
- **Multi-tenant:** Não implementado no legado (apenas filtro por cliente via `Id_Cliente`)
- **Auditoria:** Parcial - cada entidade tinha sua própria tabela `_log` separada
- **Configurações:** Web.config (connection strings, appSettings)

### 1.2 Características Principais do Legado

- **Abordagem de auditoria:** Cada entidade crítica tinha uma tabela `_log` separada (Ativo_log, Fatura_log, Centro_Custo_log, Consumidor_log)
- **Granularidade:** Registro completo da entidade (não granular campo a campo)
- **Trigger:** Sem uso de triggers, todas as operações eram manuais via WebService
- **Contexto de execução:** Apenas `Id_Usuario_Alteracao` e `Dt_Alteracao` (sem IP, sem user-agent)
- **Rastreamento de relacionamentos:** Inexistente
- **Soft delete:** Implementado manualmente com flag `Ativo = 0`
- **Rollback:** Inexistente (apenas consulta de histórico)
- **Exportação:** CSV simples via stored procedure
- **Performance:** Consultas lentas (sem índices otimizados em `Dt_Alteracao`)

---

## 2. TELAS DO LEGADO

### 2.1 Tela: Auditoria.aspx

- **Caminho:** `D:\IC2\ic1_legado\IControlIT\Financeiro\Auditoria.aspx`
- **Responsabilidade:** Tela principal de auditoria de faturas vs. operadora (auditoria contábil, não de mudanças de dados)
- **Tipo:** Auditoria contábil (conferência de valores faturados)

**IMPORTANTE:** Esta tela NÃO é equivalente ao RF096 moderno. É auditoria contábil (billing audit), não auditoria de mudanças de dados (data change audit).

#### Campos Principais

| Campo | Tipo | Obrigatório | Observações |
|------|------|-------------|-------------|
| `ddlPeriodo` | Dropdown | Sim | Seleção de mês/ano |
| `ddlOperadora` | Dropdown | Sim | Filtro por operadora |
| `gridFaturas` | GridView | - | Lista de faturas com divergências |

#### Comportamentos Implícitos

- Validação de valores ocorre lado servidor (code-behind VB.NET)
- Sem validação de permissões granulares (apenas IsAuthenticated)
- Sem auditoria das próprias alterações de auditoria

---

### 2.2 Tela: Auditoria_Acompanhamento.aspx

- **Caminho:** `D:\IC2\ic1_legado\IControlIT\Financeiro\Auditoria_Acompanhamento.aspx`
- **Responsabilidade:** Acompanhamento de aberturas/contestações de auditoria contábil

**IMPORTANTE:** Também não relacionada a RF096. É para acompanhamento de contestações de faturas.

---

### 2.3 Tela: Auditoria_Consulta.aspx

- **Caminho:** `D:\IC2\ic1_legado\IControlIT\Configuracao\Auditoria_Consulta.aspx`
- **Responsabilidade:** Consulta de histórico de mudanças (MAIS PRÓXIMO DO RF096 MODERNO)

#### Campos Principais

| Campo | Tipo | Obrigatório | Observações |
|------|------|-------------|-------------|
| `ddlEntidade` | Dropdown | Sim | Ativo, Fatura, Centro de Custo, Consumidor |
| `txtIdEntidade` | TextBox | Sim | ID da entidade para consultar histórico |
| `gridHistorico` | GridView | - | Histórico de alterações |
| `btnExportar` | Button | - | Exporta CSV via stored procedure |

#### Comportamentos Implícitos

- Consulta hardcoded para cada tipo de entidade (4 procedures diferentes)
- Sem filtro de data/hora (sempre traz TODO o histórico)
- Performance ruim com >1000 registros (sem paginação)
- Sem ordenação (sempre ordem de inserção)
- Sem comparação entre versões (diff)

---

### 2.4 Tela: Auditoria_Importa.aspx

- **Caminho:** `D:\IC2\ic1_legado\IControlIT\Financeiro\Auditoria_Importa.aspx`
- **Responsabilidade:** Upload de arquivo para auditoria contábil

**IMPORTANTE:** Upload de bilhetes de operadora, não auditoria de mudanças de dados.

---

### 2.5 Tela: Auditoria_Status.aspx

- **Caminho:** `D:\IC2\ic1_legado\IControlIT\Financeiro\Auditoria_Status.aspx`
- **Responsabilidade:** Status de lotes de auditoria contábil

**IMPORTANTE:** Status de lotes de auditoria contábil, não de mudanças de dados.

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

### 3.1 WSCadastro.Envia_Log()

- **Local:** `D:\IC2\ic1_legado\IControlIT\WS_IControlIT\WSCadastro.asmx.vb`
- **Responsabilidade:** Registra log de operação CRUD em tabela `_log` correspondente
- **Assinatura:** `Public Function Envia_Log(ByVal entidade As String, ByVal idEntidade As Integer, ByVal idUsuario As Integer) As Boolean`

#### Comportamento

1. Identifica qual tabela `_log` usar baseado em parâmetro `entidade`
2. Copia TODOS os campos da entidade original para `_log`
3. Insere com `Id_Usuario_Alteracao` e `Dt_Alteracao = GetDate()`
4. Retorna `True` se sucesso, `False` se erro

#### Problemas Identificados

- Chamada manual (não automática)
- Sem contexto de execução (IP, user-agent)
- Sem granularidade de campo (copia tudo)
- Sem rastreamento de valores antes/depois
- Sem CorrelationId para operações em lote
- Performance ruim (INSERT individual para cada alteração)

**DESTINO:** SUBSTITUÍDO por AuditInterceptor automático no EF Core

---

### 3.2 WSConsulta.Consulta_Log()

- **Local:** `D:\IC2\ic1_legado\IControlIT\WS_IControlIT\WSConsulta.asmx.vb`
- **Responsabilidade:** Consulta histórico de mudanças de uma entidade
- **Assinatura:** `Public Function Consulta_Log(ByVal entidade As String, ByVal idEntidade As Integer) As DataTable`

#### Comportamento

1. Executa stored procedure `pa_Consulta_Auditoria_Log` com parâmetros
2. Retorna DataTable com histórico completo (sem paginação)
3. Ordenação fixa por `Dt_Alteracao DESC`

#### Problemas Identificados

- Sem paginação (problemas com >1000 registros)
- Sem filtros avançados (data, usuário, campo)
- Sem cache (sempre consulta banco)
- Performance ruim com volume alto

**DESTINO:** SUBSTITUÍDO por endpoint `GET /api/auditoria/timeline/{entityType}/{entityId}`

---

## 4. TABELAS LEGADAS

### 4.1 Tabela: Ativo_log

**Finalidade:** Registrar histórico de alterações da tabela `Ativo`

**DDL:**

```sql
CREATE TABLE [dbo].[Ativo_log](
    [Id_Ativo_log] [int] IDENTITY(1,1) NOT NULL,
    [Id_Ativo] [int] NOT NULL,
    [Nm_Ativo] [varchar](150),
    [Cd_Patrimonio] [varchar](50),
    [Dt_Alteracao] [datetime] NOT NULL,
    [Id_Usuario_Alteracao] [int],
    CONSTRAINT [PK_Ativo_log] PRIMARY KEY CLUSTERED ([Id_Ativo_log] ASC)
)
```

**Problemas Identificados:**

- Sem índice em `Dt_Alteracao` (consultas lentas)
- Sem índice em `Id_Usuario_Alteracao` (filtro lento)
- Sem contexto de execução (IP, user-agent)
- Sem rastreamento de campos alterados (copia tudo)
- Sem rastreamento de valores antes/depois
- Sem CorrelationId

**DESTINO:** SUBSTITUÍDO por `AuditLog` + `AuditFieldChange` (modelo normalizado)

---

### 4.2 Tabela: Fatura_log

**Finalidade:** Registrar histórico de alterações da tabela `Fatura`

**DDL:**

```sql
CREATE TABLE [dbo].[Fatura_log](
    [Id_Fatura_log] [int] IDENTITY(1,1) NOT NULL,
    [Id_Fatura] [int] NOT NULL,
    [Valor_Fatura] [decimal](12, 2),
    [Status] [varchar](20),
    [Dt_Alteracao] [datetime] NOT NULL,
    [Id_Usuario_Alteracao] [int],
    CONSTRAINT [PK_Fatura_log] PRIMARY KEY CLUSTERED ([Id_Fatura_log] ASC)
)
```

**Problemas Identificados:** Mesmos problemas de `Ativo_log`

**DESTINO:** SUBSTITUÍDO por `AuditLog` + `AuditFieldChange`

---

### 4.3 Tabela: Centro_Custo_log

**Finalidade:** Registrar histórico de alterações da tabela `Centro_Custo`

**DDL:**

```sql
CREATE TABLE [dbo].[Centro_Custo_log](
    [Id_Centro_Custo_log] [int] IDENTITY(1,1) NOT NULL,
    [Id_Centro_Custo] [int] NOT NULL,
    [Nm_Centro_Custo] [varchar](150),
    [Cd_Centro_Custo] [varchar](50),
    [Dt_Alteracao] [datetime] NOT NULL,
    [Id_Usuario_Alteracao] [int],
    CONSTRAINT [PK_Centro_Custo_log] PRIMARY KEY CLUSTERED ([Id_Centro_Custo_log] ASC)
)
```

**Problemas Identificados:** Mesmos problemas de `Ativo_log`

**DESTINO:** SUBSTITUÍDO por `AuditLog` + `AuditFieldChange`

---

### 4.4 Tabela: Consumidor_log

**Finalidade:** Registrar histórico de alterações da tabela `Consumidor`

**DDL:**

```sql
CREATE TABLE [dbo].[Consumidor_log](
    [id_Consumidor_log] [int] IDENTITY(1,1) NOT NULL,
    [id_Consumidor] [int] NOT NULL,
    [Nm_Consumidor] [varchar](255),
    [Email_Consumidor] [varchar](255),
    [Dt_Alteracao] [datetime] NOT NULL,
    [Id_Usuario_Alteracao] [int],
    CONSTRAINT [PK_Consumidor_log] PRIMARY KEY CLUSTERED ([id_Consumidor_log] ASC)
)
```

**Problemas Identificados:** Mesmos problemas de `Ativo_log`

**DESTINO:** SUBSTITUÍDO por `AuditLog` + `AuditFieldChange`

---

### 4.5 Tabela: Resumo de Mapeamento

| Campo Legado | Descrição | Campo Moderno | Tipo Moderno |
|--------------|-----------|---------------|--------------|
| `[Id_*_log]` | Chave primária incremental | `[Id]` | `UNIQUEIDENTIFIER` (GUID) |
| `[Id_*]` | ID da entidade alterada | `[EntityId]` | `NVARCHAR(100)` (string/GUID) |
| `[Dt_Alteracao]` | Data/hora da alteração | `[Timestamp]` | `DATETIMEOFFSET` (UTC sempre) |
| `[Id_Usuario_Alteracao]` | ID do usuário que alterou | `[UserId]` + `[UserName]` | `UNIQUEIDENTIFIER` + `NVARCHAR(200)` |
| Campos de valor (vários) | Cópia de todos os campos da entidade | `[AuditFieldChange]` | Tabela normalizada |
| (inexistente) | IP de origem | `[IP]` | `NVARCHAR(45)` |
| (inexistente) | User-Agent | `[UserAgent]` | `NVARCHAR(500)` |
| (inexistente) | ClienteId (multi-tenancy) | `[ClienteId]` | `UNIQUEIDENTIFIER` |
| (inexistente) | CorrelationId (lote) | `[CorrelationId]` | `UNIQUEIDENTIFIER` |

---

## 5. STORED PROCEDURES LEGADAS

### 5.1 pa_Importa_Auditoria

**Local:** `D:\IC2\ic1_legado\BancoDados\Interno\Auditoria.sql` (linha ~150)

**Responsabilidade:** Importa bilhetes de operadora para auditoria contábil (billing audit)

**IMPORTANTE:** NÃO relacionado a auditoria de mudanças de dados (RF096)

**DESTINO:** DESCARTADO (não aplicável ao RF096)

---

### 5.2 pa_Auditoria_Lote_Monta

**Local:** `D:\IC2\ic1_legado\BancoDados\Interno\Auditoria.sql` (linha ~350)

**Responsabilidade:** Monta lote de auditoria contábil com validações

**IMPORTANTE:** NÃO relacionado a auditoria de mudanças de dados (RF096)

**DESTINO:** DESCARTADO (não aplicável ao RF096)

---

### 5.3 pa_Auditoria_Tipo

**Local:** `D:\IC2\ic1_legado\BancoDados\Interno\Auditoria.sql` (linha ~550)

**Responsabilidade:** Classifica tipo de alteração (fatura, consumidor, ativo)

**Comportamento:**

1. Recebe `@entidade` (varchar)
2. Retorna código do tipo (1=Ativo, 2=Fatura, 3=Centro de Custo, 4=Consumidor)
3. Usado por outras procedures para rotear para tabela `_log` correta

**DESTINO:** SUBSTITUÍDO por decorador `[Audited]` automático (detecção via Reflection)

---

### 5.4 pa_Consulta_Auditoria_Log

**Local:** `D:\IC2\ic1_legado\BancoDados\Interno\Auditoria.sql` (linha ~750)

**Responsabilidade:** Retorna histórico de alterações de uma entidade

**Assinatura:**

```sql
CREATE PROCEDURE [dbo].[pa_Consulta_Auditoria_Log]
    @entidade VARCHAR(50),
    @idEntidade INT
AS
BEGIN
    -- Switch case para cada tipo de entidade
    IF @entidade = 'Ativo'
        SELECT * FROM Ativo_log WHERE Id_Ativo = @idEntidade ORDER BY Dt_Alteracao DESC
    ELSE IF @entidade = 'Fatura'
        SELECT * FROM Fatura_log WHERE Id_Fatura = @idEntidade ORDER BY Dt_Alteracao DESC
    ELSE IF @entidade = 'Centro_Custo'
        SELECT * FROM Centro_Custo_log WHERE Id_Centro_Custo = @idEntidade ORDER BY Dt_Alteracao DESC
    ELSE IF @entidade = 'Consumidor'
        SELECT * FROM Consumidor_log WHERE id_Consumidor = @idEntidade ORDER BY Dt_Alteracao DESC
END
```

**Problemas Identificados:**

- Sem paginação (retorna tudo)
- Sem filtros de data/usuário
- Sem cache
- Sem índices otimizados
- Performance ruim com >1000 registros

**DESTINO:** SUBSTITUÍDO por endpoint `GET /api/auditoria/timeline/{entityType}/{entityId}` com paginação e filtros

---

## 6. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

### RL-RN-001: Auditoria Manual por WebService

**Descrição:** No legado, auditoria não era automática. Cada operação CRUD precisava chamar explicitamente `WSCadastro.Envia_Log()` após sucesso.

**Problemas:** Fácil esquecer de chamar, sem atomicidade (transação separada), sem rollback se falhar.

**DESTINO:** SUBSTITUÍDO por AuditInterceptor automático (SaveChanges hook do EF Core)

---

### RL-RN-002: Uma Tabela _log por Entidade

**Descrição:** Cada entidade crítica tinha sua própria tabela `_log` (Ativo_log, Fatura_log, etc.), copiando TODOS os campos da entidade original.

**Problemas:** Redundância, manutenção complexa, sem normalização, sem granularidade de campo.

**DESTINO:** SUBSTITUÍDO por modelo normalizado `AuditLog` + `AuditFieldChange`

---

### RL-RN-003: Sem Contexto de Execução

**Descrição:** Legado registrava apenas `Id_Usuario_Alteracao` e `Dt_Alteracao`, sem IP, sem user-agent, sem ClienteId.

**Problemas:** Impossível rastrear origem da alteração, impossível detectar acessos anômalos.

**DESTINO:** ASSUMIDO no RF096 - todos os campos de contexto são obrigatórios

---

### RL-RN-004: Sem Soft Delete Auditado

**Descrição:** Soft delete existia (flag `Ativo = 0`), mas não era auditado como operação separada.

**Problemas:** Impossível saber quem deletou, quando deletou, histórico de soft delete.

**DESTINO:** ASSUMIDO no RF096 - soft delete é auditado como operação específica (OperationType = Deleted)

---

### RL-RN-005: Sem Rollback

**Descrição:** Legado apenas consultava histórico, sem capacidade de restaurar versões anteriores.

**Problemas:** Impossível reverter alterações incorretas automaticamente.

**DESTINO:** ASSUMIDO no RF096 - rollback controlado com validação de integridade

---

### RL-RN-006: Sem Detecção de Operações em Lote

**Descrição:** Importações em massa geravam N registros separados em `_log`, sem agrupamento.

**Problemas:** Impossível saber quais alterações fazem parte do mesmo batch.

**DESTINO:** ASSUMIDO no RF096 - CorrelationId único por SaveChanges

---

### RL-RN-007: Sem Rastreamento de Relacionamentos

**Descrição:** Adições/remoções em collections não eram auditadas.

**Problemas:** Impossível rastrear quando um ativo foi vinculado a um centro de custo.

**DESTINO:** ASSUMIDO no RF096 - rastreamento de RelationshipAdded/RelationshipRemoved

---

### RL-RN-008: Sem Alertas de Dados Sensíveis

**Descrição:** Alterações em CPF, e-mail, telefone não geravam alertas.

**Problemas:** Não conformidade LGPD Art. 48 (comunicação de incidentes).

**DESTINO:** ASSUMIDO no RF096 - alertas automáticos ao DPO

---

### RL-RN-009: Sem Integração SIEM

**Descrição:** Logs ficavam apenas no banco, sem envio para SIEM.

**Problemas:** Impossível correlacionar eventos de auditoria com eventos de segurança.

**DESTINO:** ASSUMIDO no RF096 - integração automática com Azure Sentinel

---

### RL-RN-010: Sem Retenção Configurável

**Descrição:** Dados de auditoria ficavam indefinidamente no banco (sem arquivamento/purga).

**Problemas:** Crescimento descontrolado, performance degradada, custo de storage.

**DESTINO:** ASSUMIDO no RF096 - retenção configurável por tipo de entidade (LGPD/SOX)

---

## 7. GAP ANALYSIS (LEGADO x RF MODERNO)

| Item | Legado | RF Moderno (RF096) | Observação |
|-----|--------|-------------------|------------|
| **Granularidade** | Registro completo da entidade | Campo a campo (FieldChange) | Melhora rastreabilidade |
| **Automação** | Manual (WebService) | Automático (EF Interceptor) | Reduz erros humanos |
| **Contexto** | Usuário + Data | Usuário + Data + IP + UserAgent + ClienteId | Conformidade LGPD/SOX |
| **Multi-tenancy** | Não (filtro manual) | Sim (ClienteId obrigatório) | Isolamento garantido |
| **Soft Delete** | Não auditado | Auditado (OperationType = Deleted) | Rastreabilidade completa |
| **Rollback** | Inexistente | Sim (com validação integridade) | Reversão de erros |
| **Relacionamentos** | Não auditado | Auditado (RelationshipAdded/Removed) | Rastreamento completo |
| **Lote** | Não detectado | Detectado (CorrelationId) | Agrupamento automático |
| **Alertas LGPD** | Inexistente | Sim (automático ao DPO) | Conformidade LGPD Art. 48 |
| **SIEM** | Não integrado | Integrado (Azure Sentinel) | Segurança avançada |
| **Retenção** | Indefinida | Configurável (5-7 anos) | Conformidade LGPD/SOX |
| **Exportação** | CSV simples | CSV/Excel/JSON/PDF + hash forense | Uso judicial |
| **Performance** | Lenta (sem índices) | Otimizada (índices + cache) | Escalabilidade |
| **Imutabilidade** | Não garantida | Garantida (triggers) | Integridade |

---

## 8. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Modelo Normalizado AuditLog + AuditFieldChange

**Descrição:** Substituir N tabelas `_log` por 2 tabelas normalizadas (AuditLog + AuditFieldChange)

**Motivo:**
- Reduzir redundância
- Facilitar manutenção
- Permitir granularidade de campo
- Facilitar queries agregadas

**Impacto:** Alto - Requer migração de dados do legado

**Mitigação:** Script de migração com mapeamento `[Entidade]_log` → `AuditLog` + `AuditFieldChange`

---

### Decisão 2: EF Core Interceptor vs. Triggers

**Descrição:** Usar EF Core SaveChanges Interceptor em vez de triggers SQL

**Motivo:**
- Mais flexível (contexto completo disponível em C#)
- Mais testável (unit tests)
- Mais portável (funciona em SQLite, SQL Server, PostgreSQL)
- Performance (uma operação, não duas)

**Impacto:** Baixo - Padrão recomendado para Clean Architecture

**Mitigação:** Garantir que interceptor NUNCA falhe (try-catch + log de erro)

---

### Decisão 3: GUID vs. INT para IDs

**Descrição:** Usar GUID para `AuditLog.Id` em vez de INT IDENTITY

**Motivo:**
- Distribuído (funciona com múltiplos servidores)
- Mais seguro (não sequencial, dificulta ataques)
- Facilita merge de ambientes (HOM → PRD)

**Impacto:** Médio - Storage maior (16 bytes vs. 4 bytes)

**Mitigação:** Índices otimizados, compressão de dados

---

### Decisão 4: UTC vs. LocalDateTime

**Descrição:** Sempre usar UTC para `Timestamp` (DATETIMEOFFSET)

**Motivo:**
- Multi-timezone (clientes em diferentes fusos horários)
- Evita bugs de DST (horário de verão)
- Ordenação consistente

**Impacto:** Baixo - Conversão para timezone local no frontend

**Mitigação:** Helper de conversão automática na camada de apresentação

---

### Decisão 5: Imutabilidade Garantida

**Descrição:** Bloquear UPDATE/DELETE em `AuditLog` via triggers + validação DbContext

**Motivo:**
- Conformidade LGPD/SOX (trilha de auditoria imutável)
- Integridade forense (uso em processos judiciais)
- Segurança (impossível alterar histórico)

**Impacto:** Alto - Requer triggers no banco + validação em código

**Mitigação:** Testes automatizados de tentativa de violação

---

## 9. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Mitigação |
|------|---------|-----------|
| **Perda de dados de auditoria legada** | Alto | Script de migração com validação de integridade + backup completo antes de migrar |
| **Performance degradada durante migração** | Médio | Migração em horário de baixo uso + índices criados antes da migração |
| **Incompatibilidade de timezone** | Baixo | Conversão de `Dt_Alteracao` (DateTime local) → `Timestamp` (UTC) com offset configurável |
| **Campos customizados em tabelas _log** | Médio | Análise manual de cada tabela `_log` antes de migrar + mapeamento explícito |
| **Queries legadas quebradas** | Alto | Criar views de compatibilidade `Ativo_log` → `AuditLog` para queries legadas |
| **Volume de dados** | Alto | Arquivamento de dados >10 anos antes de migrar + purga de dados duplicados |

---

## 10. RASTREABILIDADE

| Elemento Legado | Referência RF096 |
|----------------|------------------|
| `Ativo_log` (tabela) | `AuditLog` + `AuditFieldChange` (EntityType = "Ativo") |
| `Fatura_log` (tabela) | `AuditLog` + `AuditFieldChange` (EntityType = "Fatura") |
| `Centro_Custo_log` (tabela) | `AuditLog` + `AuditFieldChange` (EntityType = "CentroCusto") |
| `Consumidor_log` (tabela) | `AuditLog` + `AuditFieldChange` (EntityType = "Consumidor") |
| `WSCadastro.Envia_Log()` | AuditInterceptor.SavingChangesAsync() |
| `WSConsulta.Consulta_Log()` | `GET /api/auditoria/timeline/{entityType}/{entityId}` |
| `pa_Auditoria_Tipo` | `[Audited]` decorator + Reflection |
| `pa_Consulta_Auditoria_Log` | `GET /api/auditoria/timeline/{entityType}/{entityId}` |
| `Auditoria_Consulta.aspx` | `/auditoria/timeline` (Angular) |
| `btnExportar` (Auditoria_Consulta.aspx) | `POST /api/auditoria/exportacao-forense` |

---

## 11. SCRIPT DE MIGRAÇÃO (EXEMPLO)

```sql
-- Migração de Ativo_log → AuditLog
INSERT INTO AuditLog (Id, EntityType, EntityId, OperationType, Timestamp, UserId, UserName, IP, UserAgent, ClienteId, CorrelationId)
SELECT
    NEWID() AS Id,
    'Ativo' AS EntityType,
    CAST(Id_Ativo AS NVARCHAR(100)) AS EntityId,
    'Updated' AS OperationType, -- Legado não diferenciava Created/Updated
    CAST(Dt_Alteracao AS DATETIMEOFFSET) AS Timestamp,
    (SELECT Id FROM Usuario WHERE LegacyId = al.Id_Usuario_Alteracao) AS UserId,
    (SELECT Nome FROM Usuario WHERE LegacyId = al.Id_Usuario_Alteracao) AS UserName,
    '0.0.0.0' AS IP, -- Legado não tinha IP
    'Legacy Migration' AS UserAgent,
    (SELECT TOP 1 Id FROM Cliente) AS ClienteId, -- Assumir cliente padrão se não houver
    NEWID() AS CorrelationId
FROM Ativo_log al
WHERE NOT EXISTS (
    SELECT 1 FROM AuditLog
    WHERE EntityType = 'Ativo'
      AND EntityId = CAST(al.Id_Ativo AS NVARCHAR(100))
      AND Timestamp = CAST(al.Dt_Alteracao AS DATETIMEOFFSET)
);

-- Migração de campos alterados (exemplo para Nm_Ativo)
INSERT INTO AuditFieldChange (Id, AuditLogId, FieldName, OldValue, NewValue)
SELECT
    NEWID() AS Id,
    audit.Id AS AuditLogId,
    'Nome' AS FieldName,
    LAG(al.Nm_Ativo) OVER (PARTITION BY al.Id_Ativo ORDER BY al.Dt_Alteracao) AS OldValue,
    al.Nm_Ativo AS NewValue
FROM Ativo_log al
INNER JOIN AuditLog audit ON audit.EntityType = 'Ativo'
    AND audit.EntityId = CAST(al.Id_Ativo AS NVARCHAR(100))
    AND audit.Timestamp = CAST(al.Dt_Alteracao AS DATETIMEOFFSET)
WHERE LAG(al.Nm_Ativo) OVER (PARTITION BY al.Id_Ativo ORDER BY al.Dt_Alteracao) IS NOT NULL
  AND LAG(al.Nm_Ativo) OVER (PARTITION BY al.Id_Ativo ORDER BY al.Dt_Alteracao) <> al.Nm_Ativo;
```

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|------|------|----------|------|
| 1.0 | 2025-12-31 | Versão inicial de referência ao legado - Migração de RF096 v1.0 (código misturado) para v2.0 (separação RF/RL) | Agência ALC - alc.dev.br |
