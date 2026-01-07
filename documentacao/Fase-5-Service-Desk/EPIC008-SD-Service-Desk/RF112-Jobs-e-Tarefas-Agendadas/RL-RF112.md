# RL-RF112: Referência ao Legado - Jobs e Tarefas Agendadas

**RF Moderno**: RF-112 (v2.0)
**Sistema Legado**: VB.NET + ASP.NET Web Forms
**Versão do Legado**: IControlIT v1.x
**Data de Criação**: 2025-12-31
**Autor**: Agência ALC - alc.dev.br

---

## SEÇÃO 1: CONTEXTO DO SISTEMA LEGADO

### 1.1 Visão Geral

O sistema legado **IControlIT v1.x** (VB.NET + ASP.NET Web Forms) implementava um sistema básico de agendamento de tarefas através de:

- **Tabelas SQL Server**: `Job_History` e `Scheduled_Tasks`
- **Stored Procedures**: 4 procedimentos para CRUD e execução
- **Interface ASPX**: 3 páginas Web Forms para gerenciamento
- **WebService ASMX**: 1 serviço SOAP (VB.NET) com 4 métodos

### 1.2 Características Técnicas do Legado

| Aspecto | Descrição |
|---------|-----------|
| **Arquitetura** | Monolítica WebForms + SOAP |
| **Linguagem** | VB.NET (code-behind) |
| **Banco de Dados** | SQL Server (sem multi-tenancy) |
| **Autenticação** | Forms Authentication (ASP.NET) |
| **Orquestração** | SQL Agent Jobs (não Hangfire) |
| **UI** | ASP.NET Web Forms com UpdatePanels |
| **API** | SOAP/ASMX (sem REST) |
| **Auditoria** | Parcial (apenas criação, sem dados de modificação) |
| **Multi-tenancy** | **NÃO** (dados compartilhados entre clientes) |

### 1.3 Limitações Conhecidas

1. **Sem Multi-tenancy**: Todos os clientes compartilhavam a mesma tabela `Scheduled_Tasks`
2. **Sem Retry Automático**: Jobs falhados não eram retentados automaticamente
3. **Sem Timeout Configurável**: Jobs podiam executar indefinidamente
4. **Sem Logs Estruturados**: Apenas campo `ErrorMessage` em `Job_History`
5. **Sem Notificações**: Falhas não geravam alertas automáticos
6. **Sem Validação de Cron**: Cron expressions não eram validadas antes de salvar
7. **Sem Controle de Workers**: Sem limite de jobs paralelos
8. **Auditoria Incompleta**: Não registrava usuário ou IP das operações

---

## SEÇÃO 2: TELAS DO LEGADO

### LEG-RF112-T01 — Jobs.aspx

**Localização**: `ic1_legado/IControlIT/Jobs.aspx`

**Responsabilidade**: Listagem e gerenciamento básico de jobs agendados

**Campos Principais**:
| Campo | Tipo | Descrição |
|-------|------|-----------|
| GridView Jobs | GridView | Lista todos os jobs (sem filtro por cliente) |
| btnNew | Button | Redireciona para JobDetails.aspx?mode=new |
| btnRefresh | Button | Recarrega a grid |

**Comportamentos Implícitos**:
- Exibia jobs de todos os clientes misturados (sem multi-tenancy)
- Não tinha paginação (carregava todos os registros de uma vez)
- Usava UpdatePanel para refresh parcial
- Não validava permissões (qualquer usuário autenticado via)

**Destino**: **SUBSTITUÍDO** por `/jobs` (Angular SPA com filtros, paginação e multi-tenancy)

---

### LEG-RF112-T02 — JobDetails.aspx

**Localização**: `ic1_legado/IControlIT/JobDetails.aspx`

**Responsabilidade**: Criação e edição de jobs

**Campos Principais**:
| Campo | Tipo | Validação Legado |
|-------|------|------------------|
| txtJobName | TextBox | RequiredFieldValidator |
| txtCronExpression | TextBox | Nenhuma (aceitava valores inválidos) |
| ddlStatus | DropDownList | Active / Inactive |
| btnSave | Button | PostBack para salvar |
| btnCancel | Button | Volta para Jobs.aspx |

**Comportamentos Implícitos**:
- Não validava formato de cron expression (aceitava `"abc"` e salvava)
- Não tinha campo `Timeout` (não era configurável)
- Não tinha flag `IsSensitive` (2-step execution não existia)
- Salvava direto no banco via Stored Procedure `pa_ScheduleJob`

**Destino**: **SUBSTITUÍDO** por `/jobs/{id}` (Angular com validação de cron via Cronos)

---

### LEG-RF112-T03 — JobExecution.aspx

**Localização**: `ic1_legado/IControlIT/JobExecution.aspx`

**Responsabilidade**: Histórico de execuções de um job específico

**Campos Principais**:
| Campo | Tipo | Descrição |
|-------|------|-----------|
| GridView Executions | GridView | Lista execuções (sem limite de 90 dias) |
| lblJobName | Label | Nome do job |
| lblLastRun | Label | Data da última execução |

**Comportamentos Implícitos**:
- Não paginava histórico (mostrava tudo de uma vez)
- Não tinha filtro por período
- Não exibia duração da execução (apenas status e erro)
- Não tinha refresh automático (usuário precisava F5 manualmente)

**Destino**: **SUBSTITUÍDO** por `/jobs/{id}/historico` (Angular com paginação e filtros)

---

## SEÇÃO 3: WEBSERVICES

### LEG-RF112-WS01 — WSJobs.asmx.vb

**Localização**: `ic1_legado/IControlIT/Services/WSJobs.asmx.vb`

**Responsabilidade**: Serviço SOAP para operações de jobs via integrações externas

**Métodos Disponíveis**:

#### 1. CreateScheduledJob(name As String, cron As String) As Integer

**Descrição**: Cria novo job agendado

**Parâmetros**:
- `name`: Nome do job (sem validação de unicidade)
- `cron`: Expressão cron (sem validação de formato)

**Retorno**: `Integer` (ID do job criado ou -1 em erro)

**Comportamento**:
```vb
Public Function CreateScheduledJob(ByVal name As String, ByVal cron As String) As Integer
    ' Sem validação de formato de cron
    ' Sem validação de unicidade por tenant
    ' Insere direto no banco via pa_ScheduleJob
    Return ExecuteSP("pa_ScheduleJob", name, cron)
End Function
```

**Problemas**:
- Não validava cron expression
- Não retornava mensagem de erro estruturada
- Não registrava auditoria completa

**Destino**: **SUBSTITUÍDO** por `POST /api/jobs` (REST + validações + auditoria)

---

#### 2. ExecuteJobNow(jobId As Integer) As Boolean

**Descrição**: Dispara execução imediata de um job

**Parâmetros**:
- `jobId`: ID do job (sem validação de existência ou tenant)

**Retorno**: `Boolean` (true se disparado, false se erro)

**Comportamento**:
```vb
Public Function ExecuteJobNow(ByVal jobId As Integer) As Boolean
    ' Sem validação de permissão
    ' Sem multi-tenancy (podia executar job de outro cliente)
    ' Dispara via pa_ExecuteJob
    Return ExecuteSP("pa_ExecuteJob", jobId)
End Function
```

**Problemas**:
- Não validava se job pertence ao tenant do usuário
- Não exigia permissão específica
- Não validava se job estava ativo
- Não gerava log de execução manual

**Destino**: **SUBSTITUÍDO** por `POST /api/jobs/{id}/executar` (RBAC + multi-tenancy)

---

#### 3. GetJobHistory(jobId As Integer) As DataSet

**Descrição**: Retorna histórico de execuções de um job

**Parâmetros**:
- `jobId`: ID do job

**Retorno**: `DataSet` (tabela com execuções)

**Comportamento**:
```vb
Public Function GetJobHistory(ByVal jobId As Integer) As DataSet
    ' Retorna TODAS as execuções (sem limite de 90 dias)
    ' Sem paginação
    ' Retorna DataSet (formato legado)
    Return ExecuteQuery("pa_GetJobHistory", jobId)
End Function
```

**Problemas**:
- Retornava todas as execuções (mesmo de anos atrás)
- Sem paginação (potencial performance issue)
- DataSet é formato legado (dificulta consumo moderno)

**Destino**: **SUBSTITUÍDO** por `GET /api/jobs/{id}/historico` (REST + paginação + filtros)

---

#### 4. DeleteJob(jobId As Integer) As Boolean

**Descrição**: Exclui job

**Parâmetros**:
- `jobId`: ID do job

**Retorno**: `Boolean` (true se excluído, false se erro)

**Comportamento**:
```vb
Public Function DeleteJob(ByVal jobId As Integer) As Boolean
    ' EXCLUSÃO FÍSICA (DELETE permanente, não soft delete)
    ' Sem validação de permissão
    ' Sem multi-tenancy
    ' Perdia histórico de execuções
    Return ExecuteSP("DELETE FROM Scheduled_Tasks WHERE Id = @Id", jobId)
End Function
```

**Problemas Críticos**:
- **Exclusão física**: Perdia dados permanentemente
- Não validava se job pertence ao tenant
- Não exigia permissão `jobs:delete`
- Deletava também o histórico (sem preservação)

**Destino**: **SUBSTITUÍDO** por `DELETE /api/jobs/{id}` (soft delete + preserva histórico)

---

## SEÇÃO 4: STORED PROCEDURES

### LEG-RF112-SP01 — pa_ScheduleJob

**Localização**: `Database/dbo.pa_ScheduleJob`

**DDL**:
```sql
CREATE PROCEDURE [dbo].[pa_ScheduleJob]
    @TaskName VARCHAR(255),
    @CronExpression VARCHAR(100)
AS
BEGIN
    INSERT INTO Scheduled_Tasks (TaskName, CronExpression, IsActive, CreatedDate)
    VALUES (@TaskName, @CronExpression, 1, GETDATE())

    RETURN SCOPE_IDENTITY() -- Retorna ID do job criado
END
```

**Características**:
- Insere job sem validar unicidade de nome
- Não valida formato de cron expression
- Não registra usuário criador
- Não registra tenant (sem multi-tenancy)
- Campo `IsActive` sempre 1 (não permite criar job pausado)

**Destino**: **SUBSTITUÍDO** por `CreateJobCommand` (CQRS) com validações completas

---

### LEG-RF112-SP02 — pa_ExecuteJob

**Localização**: `Database/dbo.pa_ExecuteJob`

**DDL**:
```sql
CREATE PROCEDURE [dbo].[pa_ExecuteJob]
    @JobId INT
AS
BEGIN
    -- Apenas registra inicio de execução
    INSERT INTO Job_History (JobName, ExecutionDate, Status)
    SELECT TaskName, GETDATE(), 'RUNNING'
    FROM Scheduled_Tasks
    WHERE Id = @JobId

    -- Execução real era feita por SQL Agent (não pela SP)
END
```

**Características**:
- Apenas registra início (não controla execução real)
- Não valida se job pertence ao tenant
- Não registra quem disparou (se manual)
- Não valida se job está ativo
- Não implementa retry automático

**Destino**: **SUBSTITUÍDO** por `ExecuteJobCommand` + Hangfire (orquestração completa)

---

### LEG-RF112-SP03 — pa_GetJobHistory

**Localização**: `Database/dbo.pa_GetJobHistory`

**DDL**:
```sql
CREATE PROCEDURE [dbo].[pa_GetJobHistory]
    @JobId INT
AS
BEGIN
    SELECT
        ExecutionDate,
        Status,
        Duration,
        ErrorMessage
    FROM Job_History
    WHERE JobName = (SELECT TaskName FROM Scheduled_Tasks WHERE Id = @JobId)
    ORDER BY ExecutionDate DESC
    -- SEM LIMIT (retorna tudo)
END
```

**Características**:
- Retorna histórico completo (sem limite de 90 dias)
- Join manual via `TaskName` (não FK estruturada)
- Sem paginação
- Sem filtros (período, status, etc.)

**Destino**: **SUBSTITUÍDO** por `GetJobHistoryQuery` (CQRS) com paginação e filtros

---

### LEG-RF112-SP04 — pa_UpdateJobStatus

**Localização**: `Database/dbo.pa_UpdateJobStatus`

**DDL**:
```sql
CREATE PROCEDURE [dbo].[pa_UpdateJobStatus]
    @JobId INT,
    @Status VARCHAR(50),
    @ErrorMessage NVARCHAR(MAX) = NULL
AS
BEGIN
    UPDATE Job_History
    SET Status = @Status,
        ErrorMessage = @ErrorMessage,
        Duration = DATEDIFF(SECOND, ExecutionDate, GETDATE())
    WHERE JobName = (SELECT TaskName FROM Scheduled_Tasks WHERE Id = @JobId)
      AND Status = 'RUNNING'

    -- Atualiza apenas o último registro RUNNING
END
```

**Características**:
- Atualiza apenas último registro `RUNNING` (não usa `ExecutionId`)
- Calcula duração na atualização (não no final da execução)
- Não registra usuário que atualizou
- Não dispara notificações de falha

**Destino**: **SUBSTITUÍDO** por `UpdateJobStatusCommand` (CQRS) com auditoria e notificações

---

## SEÇÃO 5: TABELAS LEGADAS

### LEG-RF112-TAB01 — Job_History

**Localização**: `Database/dbo.Job_History`

**DDL Original**:
```sql
CREATE TABLE [dbo].[Job_History](
    [Id] [int] IDENTITY(1,1) NOT NULL PRIMARY KEY,
    [JobName] [varchar](255) NOT NULL, -- Relação por nome (não FK)
    [ExecutionDate] [datetime] NOT NULL,
    [Status] [varchar](50) NOT NULL, -- SUCCESS, FAILED, RUNNING
    [Duration] [int] NULL, -- Segundos (nullable)
    [ErrorMessage] [nvarchar](max) NULL,
    [CreatedBy] [nvarchar](100) NULL -- Nunca preenchido
)
```

**Problemas Identificados**:
1. **Sem FK**: Relação por `JobName` (string) em vez de `JobId` (int)
2. **Sem Multi-tenancy**: Não tem campo `ClienteId`
3. **Sem Auditoria**: Campo `CreatedBy` nunca era preenchido
4. **Sem Retenção**: Histórico acumulava indefinidamente (sem limpeza automática)
5. **Sem Payload**: Não registrava entrada (impossível debugar execuções)
6. **Sem RetryCount**: Não registrava quantas tentativas foram feitas
7. **Sem ExecutedBy**: Não registrava se execução foi manual ou agendada

**Destino**: **ASSUMIDO** com correções:
- Tabela moderna: `JobExecutions`
- FK estruturada: `JobId` (Guid)
- Multi-tenancy: `ClienteId` (Guid)
- Auditoria: `ExecutadoPor` (Guid)
- Retenção: 90 dias (limpeza automática)
- Payload: JSON completo
- RetryCount: 0-3

---

### LEG-RF112-TAB02 — Scheduled_Tasks

**Localização**: `Database/dbo.Scheduled_Tasks`

**DDL Original**:
```sql
CREATE TABLE [dbo].[Scheduled_Tasks](
    [Id] [int] IDENTITY(1,1) NOT NULL PRIMARY KEY,
    [TaskName] [varchar](255) NOT NULL, -- SEM UNIQUE CONSTRAINT
    [CronExpression] [varchar](100) NULL, -- Aceitava NULL e valores inválidos
    [IsActive] [bit] NOT NULL DEFAULT 1,
    [CreatedDate] [datetime] NOT NULL,
    [ModifiedDate] [datetime] NULL
)
```

**Problemas Identificados**:
1. **Sem Validação de Unicidade**: Permitia jobs duplicados com mesmo nome
2. **Sem Validação de Cron**: Campo `CronExpression` aceitava valores inválidos
3. **Sem Multi-tenancy**: Não tem campo `ClienteId`
4. **Sem Timeout**: Não tinha configuração de timeout máximo
5. **Sem IsSensitive**: Não suportava 2-step execution
6. **Sem Soft Delete**: Apenas `IsActive` (exclusão física perdia dados)
7. **Sem Auditoria**: Não registrava quem criou ou modificou

**Destino**: **ASSUMIDO** com correções:
- Tabela moderna: `Jobs`
- Multi-tenancy: `ClienteId` (Guid)
- Validação: Cron expression validada antes de salvar
- Timeout configurável: 5-240 minutos
- IsSensitive: Suporta 2-step execution
- Soft Delete: Campo `Status` (ACTIVE, PAUSED, DELETED)
- Auditoria: `CriadoPor`, `AtualizadoPor`, `DataCriacao`, `DataAtualizacao`

---

## SEÇÃO 6: REGRAS DE NEGÓCIO IMPLÍCITAS

### RL-RN-001 — Jobs Executados via SQL Agent

**Descrição**: No sistema legado, jobs eram executados pelo **SQL Server Agent**, não por orquestrador externo.

**Fonte**: Análise de configuração do SQL Server e ausência de código de execução

**Impacto no Moderno**:
- Sistema moderno usa **Hangfire** (orquestrador distribuído)
- Redis como storage (mais escalável que SQL Agent)
- Workers distribuídos (não apenas no servidor de banco)

---

### RL-RN-002 — Jobs Sem Retry Automático

**Descrição**: Jobs que falhavam no legado **NÃO eram retentados automaticamente**. Apenas registravam `Status = 'FAILED'` e paravam.

**Fonte**: Análise de `pa_UpdateJobStatus` e ausência de lógica de retry

**Impacto no Moderno**:
- Sistema moderno implementa **retry com backoff exponencial** (1min → 2min → 4min)
- Máximo de 3 retries (4 tentativas no total)
- Notificação apenas após esgotadas todas as tentativas

---

### RL-RN-003 — Jobs Sem Notificação de Falha

**Descrição**: Quando um job falhava no legado, **nenhuma notificação era enviada**. Operadores precisavam verificar manualmente em `JobExecution.aspx`.

**Fonte**: Ausência de código de envio de email em `pa_UpdateJobStatus`

**Impacto no Moderno**:
- Sistema moderno envia **email para todos os Administradores do tenant**
- Notificação via **SignalR** em tempo real
- Log em **Application Insights** com severidade Critical

---

### RL-RN-004 — Jobs Executados Indefinidamente

**Descrição**: Jobs legado **não tinham timeout**. Podiam executar indefinidamente sem cancelamento automático.

**Fonte**: Ausência de campo `Timeout` em `Scheduled_Tasks`

**Impacto no Moderno**:
- Sistema moderno tem **timeout padrão de 30 minutos**
- Range configurável: 5-240 minutos
- Cancelamento automático ao exceder timeout

---

### RL-RN-005 — Jobs Sem Validação de Cron Expression

**Descrição**: Legado **aceitava valores inválidos** em `CronExpression` (ex: `"abc"`, `"invalid"`). Erros só apareciam na execução (SQL Agent falhava).

**Fonte**: Análise de `pa_ScheduleJob` e `JobDetails.aspx`

**Impacto no Moderno**:
- Sistema moderno **valida cron expression antes de salvar** (biblioteca Cronos)
- Rejeita com HTTP 400 se formato inválido
- Mínimo 5 campos obrigatórios

---

### RL-RN-006 — Jobs Compartilhados Entre Clientes

**Descrição**: Legado **NÃO tinha multi-tenancy**. Todos os clientes viam jobs uns dos outros em `Jobs.aspx`.

**Fonte**: Ausência de campo `ClienteId` em `Scheduled_Tasks` e `Job_History`

**Impacto no Moderno**:
- Sistema moderno **isola completamente por tenant** (`ClienteId`)
- Cada cliente vê apenas seus próprios jobs
- Workers isolados (máximo 10 por tenant)

---

### RL-RN-007 — Exclusão Física de Jobs

**Descrição**: Legado **deletava jobs permanentemente** (DELETE físico), perdendo histórico de execuções.

**Fonte**: Análise de `WSJobs.asmx.vb` → `DeleteJob()`

**Impacto no Moderno**:
- Sistema moderno usa **soft delete** (campo `Status = DELETED`)
- Histórico de execuções **preservado por 90 dias**
- Auditoria de exclusão **mantida indefinidamente** (5 anos)

---

## SEÇÃO 7: GAP ANALYSIS

### Funcionalidades Presentes no Legado e Ausentes no Moderno

| Funcionalidade Legado | Destino | Justificativa |
|----------------------|---------|---------------|
| *Nenhuma* | N/A | Todas as funcionalidades legado foram substituídas por equivalentes modernos superiores |

### Funcionalidades Novas no Moderno (Não Existiam no Legado)

| Funcionalidade Moderna | Criticidade | Descrição |
|------------------------|-------------|-----------|
| **Multi-tenancy** | Alta | Isolamento completo por tenant (inexistente no legado) |
| **Retry Automático** | Alta | Backoff exponencial (1→2→4 minutos) |
| **Timeout Configurável** | Média | 5-240 minutos (legado não tinha) |
| **Notificações de Falha** | Alta | Email + SignalR (legado não notificava) |
| **Validação de Cron** | Média | Biblioteca Cronos (legado aceitava inválidos) |
| **2-Step Execution** | Alta | Jobs sensíveis exigem aprovação (novo) |
| **Logs em Tempo Real** | Média | SignalR streaming (legado não tinha) |
| **Métricas e KPIs** | Baixa | 8 métricas operacionais (novo) |
| **Alertas Críticos** | Média | 6 tipos de alertas (novo) |
| **Limite de Workers** | Média | Máximo 10 paralelos por tenant (novo) |
| **Soft Delete** | Alta | Preserva histórico (legado fazia DELETE físico) |
| **RBAC Granular** | Alta | 11 permissões (legado não tinha RBAC) |
| **Auditoria Completa** | Alta | 8 operações auditadas (legado apenas criação) |
| **Retenção de Histórico** | Média | 90 dias (legado acumulava indefinidamente) |
| **i18n Completo** | Baixa | 16 chaves de tradução (legado apenas pt-BR) |
| **Feature Flags** | Média | Controle via `JOBS_SCHEDULING` (novo) |

### Decisões de Modernização

#### Decisão 1: Migrar de SQL Agent para Hangfire

**Motivo**:
- SQL Agent não suporta multi-tenancy
- Escalabilidade limitada (apenas 1 servidor)
- Dificulta deploy em cloud (Azure SQL não tem Agent)

**Impacto**: **Alto** (mudança arquitetural significativa)

**Data**: 2025-12-31

---

#### Decisão 2: Implementar Retry Automático

**Motivo**:
- Legado não retentava jobs falhados
- Operadores perdiam tempo executando manualmente
- Falhas transitórias (rede, timeout) não eram tratadas

**Impacto**: **Médio** (melhora confiabilidade operacional)

**Data**: 2025-12-31

---

#### Decisão 3: Adicionar Multi-tenancy

**Motivo**:
- Legado misturava jobs de todos os clientes
- Risco de segurança (um cliente ver jobs de outro)
- Não permitia limites por tenant

**Impacto**: **Alto** (requisito fundamental de segurança)

**Data**: 2025-12-31

---

#### Decisão 4: Soft Delete ao Invés de Exclusão Física

**Motivo**:
- Legado perdia histórico ao deletar job
- Impossibilitava auditoria de jobs excluídos
- Dados perdidos permanentemente

**Impacto**: **Médio** (melhora auditoria e compliance)

**Data**: 2025-12-31

---

### Riscos de Migração

#### Risco 1: Perda de Histórico de Jobs Antigos

**Descrição**: Jobs do sistema legado não têm `ClienteId`. Histórico de execuções antigas não pode ser migrado diretamente.

**Impacto**: **Alto**

**Probabilidade**: **Alta**

**Mitigação**:
- ETL com atribuição manual de `ClienteId` baseado em contexto histórico
- Validação 100% dos dados migrados
- Manutenção de tabela legado `Job_History` em read-only por 6 meses

---

#### Risco 2: Incompatibilidade de Cron Expressions

**Descrição**: Legado aceitava cron expressions inválidas. Migração pode falhar ao validar com Cronos.

**Impacto**: **Médio**

**Probabilidade**: **Média**

**Mitigação**:
- Validação prévia de todos os cron expressions do legado
- Correção manual de expressões inválidas antes da migração
- Marcação de jobs problemáticos como `PAUSED` até revisão

---

#### Risco 3: Quebra de Integrações SOAP

**Descrição**: Sistemas externos podem consumir `WSJobs.asmx` (SOAP). Migração para REST API pode quebrar integrações.

**Impacto**: **Alto**

**Probabilidade**: **Baixa**

**Mitigação**:
- Manter endpoint SOAP ativo por 6 meses (deprecated)
- Endpoint SOAP apenas redireciona para REST API (adaptador)
- Comunicação prévia com sistemas consumidores
- Documentação de migração SOAP → REST

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 1.0 | 2025-12-31 | Criação inicial do RL-RF112 (Referência ao Legado) | Agência ALC - alc.dev.br |
