# Modelo de Dados - RF034: Gestão de Itens de Auditoria de Faturas

**Versão:** 1.0
**Data:** 2025-12-18
**RF Relacionado:** [RF034 - Gestão de Itens de Auditoria](./RF034.md)
**Banco de Dados:** SQL Server / SQLite (dev)

---

## 1. Diagrama Entidade-Relacionamento (ER)

```
┌──────────────────────┐          ┌───────────────────────────────┐
│   Conglomerados      │          │    AuditoriasResumos          │
├──────────────────────┤          ├───────────────────────────────┤
│ Id (PK)              │◄─────┐   │ Id (PK)                       │◄──┐
│ Nome                 │      │   │ ConglomeradoId (FK)           │   │
└──────────────────────┘      │   │ FaturaId (FK)                 │   │
                              │   │ TotalDivergencias             │   │
┌──────────────────────┐      │   │ TotalValorRecuperavel         │   │
│      Faturas         │      │   │ StatusAuditoria               │   │
├──────────────────────┤      │   │ ...                           │   │
│ Id (PK)              │◄─────┼───┤                               │   │
│ NumeroFatura         │      │   └───────────────────────────────┘   │
│ ValorTotal           │      │                    ▲                  │
└──────────────────────┘      │                    │                  │
                              │                    │ 1:N              │
┌──────────────────────┐      │                    │                  │
│      Bilhetes        │      │   ┌────────────────┴────────────────┐│
├──────────────────────┤      │   │     AuditoriasItens             ││
│ Id (PK)              │◄─────┼───┤ Id (PK)                         ││
│ NumeroOrigem         │      │   │ ConglomeradoId (FK)             ├┘
│ NumeroDestino        │      └───┤ AuditoriaResumoId (FK)          │
│ Duracao              │          │ BilheteId (FK)                  │◄──┐
│ DataHora             │          │ AtivoId (FK)                    │   │
│ TipoChamada          │          │ ContratoId (FK)                 │   │
└──────────────────────┘          │ TipoServico                     │   │
                                  │ DescricaoServico                │   │
┌──────────────────────┐          │ Quantidade                      │   │
│       Ativos         │          │ ValorCobrado                    │   │
├──────────────────────┤          │ ValorContrato                   │   │
│ Id (PK)              │◄─────────┤ ValorCorreto                    │   │
│ NumeroLinha          │          │ ValorCobradoAMais (computed)    │   │
│ IMEI                 │          │ PercentualDivergencia (computed)│   │
│ ...                  │          │ MotivoGlosa                     │   │
└──────────────────────┘          │ DataIdentificacao               │   │
                                  │ UsuarioAuditorId (FK)           │   │
┌──────────────────────┐          │ FlContestado                    │   │
│     Contratos        │          │ DataContestacao                 │   │
├──────────────────────┤          │ NumeroContestacao               │   │
│ Id (PK)              │◄─────────┤ FlRecuperado                    │   │
│ NumeroContrato       │          │ ValorRecuperado                 │   │
│ Operadora            │          │ DataRecuperacao                 │   │
│ ...                  │          │ FlExcluido                      │   │
└──────────────────────┘          │ CreatedAt                       │   │
                                  │ CreatedBy                       │   │
┌──────────────────────┐          │ UpdatedAt                       │   │
│       Users          │          │ UpdatedBy                       │   │
├──────────────────────┤          └─────────────────────────────────┘   │
│ Id (PK)              │◄───────────────────────────┘                   │
│ Nome                 │                                                │
│ Email                │                                                │
└──────────────────────┘                                                │
                                                                        │
┌──────────────────────────────────────────────────────────────────────┘
│  AuditoriasItensHistory
├────────────────────────────────────┐
│ Id (PK)                            │
│ AuditoriaItemId (FK)               │
│ Operation                          │
│ OldValues (JSON)                   │
│ NewValues (JSON)                   │
│ ChangedBy                          │
│ ChangedAt                          │
└────────────────────────────────────┘
```

---

## 2. Entidades

### 2.1 Tabela: AuditoriasItens

**Descrição:** Itens individuais identificados na auditoria de faturas de telecomunicações com cálculos de divergências e rastreamento de recuperação.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK para Cliente (multi-tenancy raiz)s (multi-tenancy) |
| AuditoriaResumoId | UNIQUEIDENTIFIER | NÃO | - | FK para AuditoriasResumos |
| BilheteId | UNIQUEIDENTIFIER | NÃO | - | FK para Bilhetes (chamada/dados auditada) |
| AtivoId | UNIQUEIDENTIFIER | SIM | NULL | FK para Ativos (opcional) |
| ContratoId | UNIQUEIDENTIFIER | SIM | NULL | FK para Contratos (opcional) |
| TipoServico | NVARCHAR(100) | NÃO | - | Tipo de serviço (Voz, Dados, SMS, Roaming) |
| DescricaoServico | NVARCHAR(500) | SIM | NULL | Descrição detalhada do serviço |
| Quantidade | DECIMAL(13,8) | NÃO | 0.00000000 | Quantidade consumida (minutos, MB, etc.) |
| UnidadeMedida | NVARCHAR(20) | NÃO | 'UN' | Unidade (MIN, MB, SMS, UN) |
| ValorCobrado | DECIMAL(13,8) | NÃO | 0.00000000 | Valor cobrado pela operadora |
| ValorContrato | DECIMAL(13,8) | NÃO | 0.00000000 | Valor conforme contrato |
| ValorCorreto | DECIMAL(13,8) | NÃO | 0.00000000 | Valor que deveria ser cobrado |
| ValorCobradoAMais AS (ValorCobrado - ValorCorreto) PERSISTED | DECIMAL(13,8) | - | - | Valor cobrado a maior (computed) |
| PercentualDivergencia AS (CASE WHEN ValorCorreto > 0 THEN ((ValorCobrado - ValorCorreto) / ValorCorreto) * 100 ELSE 0 END) PERSISTED | DECIMAL(7,4) | - | - | % de divergência (computed) |
| MotivoGlosa | NVARCHAR(MAX) | NÃO | - | Motivo da divergência identificada |
| DataIdentificacao | DATETIME2 | NÃO | GETDATE() | Data/hora da identificação |
| UsuarioAuditorId | UNIQUEIDENTIFIER | NÃO | - | FK para Users (auditor) |
| FlContestado | BIT | NÃO | 0 | Se foi contestado junto à operadora |
| DataContestacao | DATETIME2 | SIM | NULL | Data da contestação |
| NumeroContestacao | NVARCHAR(100) | SIM | NULL | Número do protocolo de contestação |
| FlRecuperado | BIT | NÃO | 0 | Se o valor foi recuperado |
| ValorRecuperado | DECIMAL(13,8) | NÃO | 0.00000000 | Valor efetivamente recuperado |
| DataRecuperacao | DATETIME2 | SIM | NULL | Data da recuperação |
| Observacoes | NVARCHAR(MAX) | SIM | NULL | Observações adicionais |
| Ativo | BIT | NÃO | true | Soft delete: false=ativo, true=excluído flag |
| CreatedAt | DATETIME2 | NÃO | GETDATE() | Data de criação |
| CreatedBy | UNIQUEIDENTIFIER | NÃO | - | Usuário que criou |
| UpdatedAt | DATETIME2 | SIM | NULL | Data de atualização |
| UpdatedBy | UNIQUEIDENTIFIER | SIM | NULL | Usuário que atualizou |

#### Índices (15 índices)

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_AuditoriasItens | Id | CLUSTERED | Chave primária |
| IX_AuditoriasItens_ConglomeradoId | ClienteId | NONCLUSTERED | Performance multi-tenant |
| IX_AuditoriasItens_AuditoriaResumoId | AuditoriaResumoId | NONCLUSTERED | Itens por resumo |
| IX_AuditoriasItens_BilheteId | BilheteId | NONCLUSTERED | Auditoria por bilhete |
| IX_AuditoriasItens_AtivoId | AtivoId | NONCLUSTERED | Itens por ativo |
| IX_AuditoriasItens_ContratoId | ContratoId | NONCLUSTERED | Itens por contrato |
| IX_AuditoriasItens_TipoServico | TipoServico | NONCLUSTERED | Agrupamento por tipo |
| IX_AuditoriasItens_DataIdentificacao | DataIdentificacao DESC | NONCLUSTERED | Ordenação cronológica |
| IX_AuditoriasItens_ValorCobradoAMais | ValorCobradoAMais DESC | NONCLUSTERED FILTERED | Divergências (WHERE ValorCobradoAMais > 0) |
| IX_AuditoriasItens_FlContestado | FlContestado | NONCLUSTERED FILTERED | Contestados (WHERE FlContestado = 1) |
| IX_AuditoriasItens_FlRecuperado | FlRecuperado | NONCLUSTERED FILTERED | Recuperados (WHERE FlRecuperado = 1) |
| IX_AuditoriasItens_UsuarioAuditorId | UsuarioAuditorId | NONCLUSTERED | Itens por auditor |
| IX_AuditoriasItens_CreatedAt | CreatedAt DESC | NONCLUSTERED | Auditoria temporal |
| IX_AuditoriasItens_Composto_Contestacoes | (ConglomeradoId, FlContestado, DataContestacao) | NONCLUSTERED | Query de contestações |
| IX_AuditoriasItens_Composto_Relatorio | (ConglomeradoId, TipoServico, DataIdentificacao) INCLUDE (ValorCobradoAMais) | NONCLUSTERED | Relatórios gerenciais |

#### Constraints

| Nome | Tipo | Definição | Descrição |
|------|------|-----------|-----------|
| PK_AuditoriasItens | PRIMARY KEY | Id | Chave primária |
| FK_AuditoriasItens_Conglomerado | FOREIGN KEY | ConglomeradoId REFERENCES Conglomerados(Id) | Multi-tenancy |
| FK_AuditoriasItens_AuditoriaResumo | FOREIGN KEY | AuditoriaResumoId REFERENCES AuditoriasResumos(Id) | Vínculo com resumo |
| FK_AuditoriasItens_Bilhete | FOREIGN KEY | BilheteId REFERENCES Bilhetes(Id) | Vínculo com bilhete |
| FK_AuditoriasItens_Ativo | FOREIGN KEY | AtivoId REFERENCES Ativos(Id) | Vínculo com ativo |
| FK_AuditoriasItens_Contrato | FOREIGN KEY | ContratoId REFERENCES Contratos(Id) | Vínculo com contrato |
| FK_AuditoriasItens_UsuarioAuditor | FOREIGN KEY | UsuarioAuditorId REFERENCES Users(Id) | Auditor responsável |
| FK_AuditoriasItens_CreatedBy | FOREIGN KEY | CreatedBy REFERENCES Users(Id) | Auditoria criação |
| FK_AuditoriasItens_UpdatedBy | FOREIGN KEY | UpdatedBy REFERENCES Users(Id) | Auditoria atualização |
| CK_AuditoriasItens_Quantidade | CHECK | Quantidade >= 0 | Quantidade não-negativa |
| CK_AuditoriasItens_ValorCobrado | CHECK | ValorCobrado >= 0 | Valor não-negativo |
| CK_AuditoriasItens_ValorContrato | CHECK | ValorContrato >= 0 | Valor não-negativo |
| CK_AuditoriasItens_ValorCorreto | CHECK | ValorCorreto >= 0 | Valor não-negativo |
| CK_AuditoriasItens_ValorRecuperado | CHECK | ValorRecuperado >= 0 | Valor não-negativo |
| CK_AuditoriasItens_DataContestacao | CHECK | DataContestacao IS NULL OR DataContestacao >= DataIdentificacao | Contestação após identificação |
| CK_AuditoriasItens_DataRecuperacao | CHECK | DataRecuperacao IS NULL OR DataRecuperacao >= DataContestacao | Recuperação após contestação |

---

### 2.2 Tabela: AuditoriasItensHistory

**Descrição:** Histórico completo de alterações em itens de auditoria (7 anos LGPD).

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| AuditoriaItemId | UNIQUEIDENTIFIER | NÃO | - | FK para AuditoriasItens |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK para Cliente (multi-tenancy raiz)s |
| Operation | NVARCHAR(20) | NÃO | - | INSERT, UPDATE, DELETE |
| OldValues | NVARCHAR(MAX) | SIM | NULL | JSON com valores anteriores |
| NewValues | NVARCHAR(MAX) | SIM | NULL | JSON com novos valores |
| ChangedBy | UNIQUEIDENTIFIER | NÃO | - | Usuário que fez alteração |
| ChangedAt | DATETIME2 | NÃO | GETDATE() | Timestamp da alteração |
| IPAddress | NVARCHAR(50) | SIM | NULL | IP de origem |
| UserAgent | NVARCHAR(500) | SIM | NULL | User Agent |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_AuditoriasItensHistory | Id | CLUSTERED | Chave primária |
| IX_AuditoriasItensHistory_AuditoriaItemId | AuditoriaItemId, ChangedAt DESC | NONCLUSTERED | Histórico de um item |
| IX_AuditoriasItensHistory_ConglomeradoId | ClienteId | NONCLUSTERED | Performance multi-tenant |
| IX_AuditoriasItensHistory_ChangedAt | ChangedAt DESC | NONCLUSTERED | Auditoria temporal |
| IX_AuditoriasItensHistory_ChangedBy | ChangedBy | NONCLUSTERED | Auditoria por usuário |

#### Constraints

| Nome | Tipo | Definição | Descrição |
|------|------|-----------|-----------|
| PK_AuditoriasItensHistory | PRIMARY KEY | Id | Chave primária |
| FK_AuditoriasItensHistory_AuditoriaItem | FOREIGN KEY | AuditoriaItemId REFERENCES AuditoriasItens(Id) | Vínculo com registro original |
| FK_AuditoriasItensHistory_Conglomerado | FOREIGN KEY | ConglomeradoId REFERENCES Conglomerados(Id) | Multi-tenancy |
| FK_AuditoriasItensHistory_ChangedBy | FOREIGN KEY | ChangedBy REFERENCES Users(Id) | Auditoria |

---

## 3. Relacionamentos

| Tabela Origem | Cardinalidade | Tabela Destino | Descrição |
|---------------|---------------|----------------|-----------|
| Conglomerados | 1:N | AuditoriasItens | Conglomerado possui muitos itens de auditoria |
| AuditoriasResumos | 1:N | AuditoriasItens | Resumo agrupa múltiplos itens |
| Bilhetes | 1:N | AuditoriasItens | Bilhete pode ter múltiplas divergências |
| Ativos | 1:N | AuditoriasItens | Ativo pode ter itens auditados |
| Contratos | 1:N | AuditoriasItens | Contrato pode ter itens auditados |
| Users | 1:N | AuditoriasItens (Auditor) | Auditor registra itens |
| Users | 1:N | AuditoriasItens (CreatedBy) | Usuário cria itens |
| Users | 1:N | AuditoriasItens (UpdatedBy) | Usuário atualiza itens |
| AuditoriasItens | 1:N | AuditoriasItensHistory | Item possui histórico de alterações |

---

## 4. DDL - SQL Server

```sql
-- =============================================
-- RF034 - Gestão de Itens de Auditoria
-- Modelo de Dados
-- Data: 2025-12-18
-- =============================================

-- ---------------------------------------------
-- Tabela: AuditoriasItens
-- ---------------------------------------------
CREATE TABLE [dbo].[AuditoriasItens] (
    [Id] UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    [ConglomeradoId] UNIQUEIDENTIFIER NOT NULL,
    [AuditoriaResumoId] UNIQUEIDENTIFIER NOT NULL,
    [BilheteId] UNIQUEIDENTIFIER NOT NULL,
    [AtivoId] UNIQUEIDENTIFIER NULL,
    [ContratoId] UNIQUEIDENTIFIER NULL,
    [TipoServico] NVARCHAR(100) NOT NULL,
    [DescricaoServico] NVARCHAR(500) NULL,
    [Quantidade] DECIMAL(13,8) NOT NULL DEFAULT 0.00000000,
    [UnidadeMedida] NVARCHAR(20) NOT NULL DEFAULT 'UN',
    [ValorCobrado] DECIMAL(13,8) NOT NULL DEFAULT 0.00000000,
    [ValorContrato] DECIMAL(13,8) NOT NULL DEFAULT 0.00000000,
    [ValorCorreto] DECIMAL(13,8) NOT NULL DEFAULT 0.00000000,
    [ValorCobradoAMais] AS ([ValorCobrado] - [ValorCorreto]) PERSISTED,
    [PercentualDivergencia] AS (
        CASE
            WHEN [ValorCorreto] > 0 THEN (([ValorCobrado] - [ValorCorreto]) / [ValorCorreto]) * 100
            ELSE 0
        END
    ) PERSISTED,
    [MotivoGlosa] NVARCHAR(MAX) NOT NULL,
    [DataIdentificacao] DATETIME2 NOT NULL DEFAULT GETDATE(),
    [UsuarioAuditorId] UNIQUEIDENTIFIER NOT NULL,
    [FlContestado] BIT NOT NULL DEFAULT 0,
    [DataContestacao] DATETIME2 NULL,
    [NumeroContestacao] NVARCHAR(100) NULL,
    [FlRecuperado] BIT NOT NULL DEFAULT 0,
    [ValorRecuperado] DECIMAL(13,8) NOT NULL DEFAULT 0.00000000,
    [DataRecuperacao] DATETIME2 NULL,
    [Observacoes] NVARCHAR(MAX) NULL,
    [FlExcluido] BIT NOT NULL DEFAULT 0,
    [CreatedAt] DATETIME2 NOT NULL DEFAULT GETDATE(),
    [CreatedBy] UNIQUEIDENTIFIER NOT NULL,
    [UpdatedAt] DATETIME2 NULL,
    [UpdatedBy] UNIQUEIDENTIFIER NULL,

    -- Primary Key
    CONSTRAINT [PK_AuditoriasItens] PRIMARY KEY CLUSTERED ([Id] ASC),

    -- Foreign Keys
    CONSTRAINT [FK_AuditoriasItens_Conglomerado]
        FOREIGN KEY ([ConglomeradoId]) REFERENCES [dbo].[Conglomerados]([Id]),
    CONSTRAINT [FK_AuditoriasItens_AuditoriaResumo]
        FOREIGN KEY ([AuditoriaResumoId]) REFERENCES [dbo].[AuditoriasResumos]([Id]),
    CONSTRAINT [FK_AuditoriasItens_Bilhete]
        FOREIGN KEY ([BilheteId]) REFERENCES [dbo].[Bilhetes]([Id]),
    CONSTRAINT [FK_AuditoriasItens_Ativo]
        FOREIGN KEY ([AtivoId]) REFERENCES [dbo].[Ativos]([Id]),
    CONSTRAINT [FK_AuditoriasItens_Contrato]
        FOREIGN KEY ([ContratoId]) REFERENCES [dbo].[Contratos]([Id]),
    CONSTRAINT [FK_AuditoriasItens_UsuarioAuditor]
        FOREIGN KEY ([UsuarioAuditorId]) REFERENCES [dbo].[Users]([Id]),
    CONSTRAINT [FK_AuditoriasItens_CreatedBy]
        FOREIGN KEY ([CreatedBy]) REFERENCES [dbo].[Users]([Id]),
    CONSTRAINT [FK_AuditoriasItens_UpdatedBy]
        FOREIGN KEY ([UpdatedBy]) REFERENCES [dbo].[Users]([Id]),

    -- Check Constraints
    CONSTRAINT [CK_AuditoriasItens_Quantidade]
        CHECK ([Quantidade] >= 0),
    CONSTRAINT [CK_AuditoriasItens_ValorCobrado]
        CHECK ([ValorCobrado] >= 0),
    CONSTRAINT [CK_AuditoriasItens_ValorContrato]
        CHECK ([ValorContrato] >= 0),
    CONSTRAINT [CK_AuditoriasItens_ValorCorreto]
        CHECK ([ValorCorreto] >= 0),
    CONSTRAINT [CK_AuditoriasItens_ValorRecuperado]
        CHECK ([ValorRecuperado] >= 0),
    CONSTRAINT [CK_AuditoriasItens_DataContestacao]
        CHECK ([DataContestacao] IS NULL OR [DataContestacao] >= [DataIdentificacao]),
    CONSTRAINT [CK_AuditoriasItens_DataRecuperacao]
        CHECK ([DataRecuperacao] IS NULL OR [DataRecuperacao] >= [DataContestacao])
);
GO

-- Índices (15 índices otimizados)
CREATE NONCLUSTERED INDEX [IX_AuditoriasItens_ConglomeradoId]
    ON [dbo].[AuditoriasItens]([ConglomeradoId])
    WHERE [FlExcluido] = 0;
GO

CREATE NONCLUSTERED INDEX [IX_AuditoriasItens_AuditoriaResumoId]
    ON [dbo].[AuditoriasItens]([AuditoriaResumoId])
    INCLUDE ([TipoServico], [ValorCobradoAMais])
    WHERE [FlExcluido] = 0;
GO

CREATE NONCLUSTERED INDEX [IX_AuditoriasItens_BilheteId]
    ON [dbo].[AuditoriasItens]([BilheteId])
    WHERE [FlExcluido] = 0;
GO

CREATE NONCLUSTERED INDEX [IX_AuditoriasItens_AtivoId]
    ON [dbo].[AuditoriasItens]([AtivoId])
    WHERE [FlExcluido] = 0 AND [AtivoId] IS NOT NULL;
GO

CREATE NONCLUSTERED INDEX [IX_AuditoriasItens_ContratoId]
    ON [dbo].[AuditoriasItens]([ContratoId])
    WHERE [FlExcluido] = 0 AND [ContratoId] IS NOT NULL;
GO

CREATE NONCLUSTERED INDEX [IX_AuditoriasItens_TipoServico]
    ON [dbo].[AuditoriasItens]([TipoServico])
    WHERE [FlExcluido] = 0;
GO

CREATE NONCLUSTERED INDEX [IX_AuditoriasItens_DataIdentificacao]
    ON [dbo].[AuditoriasItens]([DataIdentificacao] DESC)
    WHERE [FlExcluido] = 0;
GO

CREATE NONCLUSTERED INDEX [IX_AuditoriasItens_ValorCobradoAMais]
    ON [dbo].[AuditoriasItens]([ValorCobradoAMais] DESC)
    INCLUDE ([TipoServico], [DataIdentificacao])
    WHERE [ValorCobradoAMais] > 0 AND [FlExcluido] = 0;
GO

CREATE NONCLUSTERED INDEX [IX_AuditoriasItens_FlContestado]
    ON [dbo].[AuditoriasItens]([FlContestado], [DataContestacao])
    WHERE [FlContestado] = 1 AND [FlExcluido] = 0;
GO

CREATE NONCLUSTERED INDEX [IX_AuditoriasItens_FlRecuperado]
    ON [dbo].[AuditoriasItens]([FlRecuperado], [DataRecuperacao])
    INCLUDE ([ValorRecuperado])
    WHERE [FlRecuperado] = 1 AND [FlExcluido] = 0;
GO

CREATE NONCLUSTERED INDEX [IX_AuditoriasItens_UsuarioAuditorId]
    ON [dbo].[AuditoriasItens]([UsuarioAuditorId])
    WHERE [FlExcluido] = 0;
GO

CREATE NONCLUSTERED INDEX [IX_AuditoriasItens_CreatedAt]
    ON [dbo].[AuditoriasItens]([CreatedAt] DESC)
    WHERE [FlExcluido] = 0;
GO

CREATE NONCLUSTERED INDEX [IX_AuditoriasItens_Composto_Contestacoes]
    ON [dbo].[AuditoriasItens]([ConglomeradoId], [FlContestado], [DataContestacao])
    INCLUDE ([NumeroContestacao], [ValorCobradoAMais])
    WHERE [FlExcluido] = 0;
GO

CREATE NONCLUSTERED INDEX [IX_AuditoriasItens_Composto_Relatorio]
    ON [dbo].[AuditoriasItens]([ConglomeradoId], [TipoServico], [DataIdentificacao])
    INCLUDE ([ValorCobradoAMais], [FlContestado], [FlRecuperado])
    WHERE [FlExcluido] = 0;
GO

-- Comentários
EXEC sys.sp_addextendedproperty
    @name=N'MS_Description',
    @value=N'Itens individuais de auditoria de faturas com cálculo de divergências',
    @level0type=N'SCHEMA', @level0name=N'dbo',
    @level1type=N'TABLE',  @level1name=N'AuditoriasItens';
GO

EXEC sys.sp_addextendedproperty
    @name=N'MS_Description',
    @value=N'Valor cobrado a maior pela operadora (computed: ValorCobrado - ValorCorreto)',
    @level0type=N'SCHEMA', @level0name=N'dbo',
    @level1type=N'TABLE',  @level1name=N'AuditoriasItens',
    @level2type=N'COLUMN', @level2name=N'ValorCobradoAMais';
GO

EXEC sys.sp_addextendedproperty
    @name=N'MS_Description',
    @value=N'Percentual de divergência (computed: ((ValorCobrado - ValorCorreto) / ValorCorreto) * 100)',
    @level0type=N'SCHEMA', @level0name=N'dbo',
    @level1type=N'TABLE',  @level1name=N'AuditoriasItens',
    @level2type=N'COLUMN', @level2name=N'PercentualDivergencia';
GO


-- ---------------------------------------------
-- Tabela: AuditoriasItensHistory
-- ---------------------------------------------
CREATE TABLE [dbo].[AuditoriasItensHistory] (
    [Id] UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    [AuditoriaItemId] UNIQUEIDENTIFIER NOT NULL,
    [ConglomeradoId] UNIQUEIDENTIFIER NOT NULL,
    [Operation] NVARCHAR(20) NOT NULL,
    [OldValues] NVARCHAR(MAX) NULL,
    [NewValues] NVARCHAR(MAX) NULL,
    [ChangedBy] UNIQUEIDENTIFIER NOT NULL,
    [ChangedAt] DATETIME2 NOT NULL DEFAULT GETDATE(),
    [IPAddress] NVARCHAR(50) NULL,
    [UserAgent] NVARCHAR(500) NULL,

    -- Primary Key
    CONSTRAINT [PK_AuditoriasItensHistory] PRIMARY KEY CLUSTERED ([Id] ASC),

    -- Foreign Keys
    CONSTRAINT [FK_AuditoriasItensHistory_AuditoriaItem]
        FOREIGN KEY ([AuditoriaItemId]) REFERENCES [dbo].[AuditoriasItens]([Id]),
    CONSTRAINT [FK_AuditoriasItensHistory_Conglomerado]
        FOREIGN KEY ([ConglomeradoId]) REFERENCES [dbo].[Conglomerados]([Id]),
    CONSTRAINT [FK_AuditoriasItensHistory_ChangedBy]
        FOREIGN KEY ([ChangedBy]) REFERENCES [dbo].[Users]([Id])
);
GO

-- Índices
CREATE NONCLUSTERED INDEX [IX_AuditoriasItensHistory_AuditoriaItemId]
    ON [dbo].[AuditoriasItensHistory]([AuditoriaItemId], [ChangedAt] DESC)
    INCLUDE ([Operation], [ChangedBy]);
GO

CREATE NONCLUSTERED INDEX [IX_AuditoriasItensHistory_ConglomeradoId]
    ON [dbo].[AuditoriasItensHistory]([ConglomeradoId]);
GO

CREATE NONCLUSTERED INDEX [IX_AuditoriasItensHistory_ChangedAt]
    ON [dbo].[AuditoriasItensHistory]([ChangedAt] DESC);
GO

CREATE NONCLUSTERED INDEX [IX_AuditoriasItensHistory_ChangedBy]
    ON [dbo].[AuditoriasItensHistory]([ChangedBy]);
GO

-- Comentários
EXEC sys.sp_addextendedproperty
    @name=N'MS_Description',
    @value=N'Histórico de alterações em itens de auditoria (retenção 7 anos LGPD)',
    @level0type=N'SCHEMA', @level0name=N'dbo',
    @level1type=N'TABLE',  @level1name=N'AuditoriasItensHistory';
GO
```

---

## 5. Views Úteis

```sql
-- =============================================
-- View: Itens com Maior Valor a Recuperar
-- =============================================
CREATE VIEW [dbo].[vw_AuditoriasItens_TopDivergencias]
AS
SELECT TOP 100
    ai.[Id],
    ai.[ConglomeradoId],
    c.[Nome] AS ConglomeradoNome,
    ai.[TipoServico],
    ai.[DescricaoServico],
    ai.[ValorCobrado],
    ai.[ValorCorreto],
    ai.[ValorCobradoAMais],
    ai.[PercentualDivergencia],
    ai.[MotivoGlosa],
    ai.[FlContestado],
    ai.[FlRecuperado],
    ai.[DataIdentificacao],
    u.[Nome] AS AuditorNome
FROM [dbo].[AuditoriasItens] ai
INNER JOIN [dbo].[Conglomerados] c ON ai.[ConglomeradoId] = c.[Id]
INNER JOIN [dbo].[Users] u ON ai.[UsuarioAuditorId] = u.[Id]
WHERE ai.[FlExcluido] = 0
  AND ai.[ValorCobradoAMais] > 0
ORDER BY ai.[ValorCobradoAMais] DESC;
GO

-- =============================================
-- View: Resumo de Contestações por Status
-- =============================================
CREATE VIEW [dbo].[vw_AuditoriasItens_ResumoContestacoes]
AS
SELECT
    ai.[ConglomeradoId],
    c.[Nome] AS ConglomeradoNome,
    COUNT(*) AS QtdItens,
    SUM(ai.[ValorCobradoAMais]) AS TotalReclamado,
    SUM(CASE WHEN ai.[FlContestado] = 1 THEN ai.[ValorCobradoAMais] ELSE 0 END) AS TotalContestado,
    SUM(CASE WHEN ai.[FlRecuperado] = 1 THEN ai.[ValorRecuperado] ELSE 0 END) AS TotalRecuperado,
    CAST(
        CASE
            WHEN SUM(ai.[ValorCobradoAMais]) > 0 THEN
                SUM(CASE WHEN ai.[FlRecuperado] = 1 THEN ai.[ValorRecuperado] ELSE 0 END) * 100.0 /
                SUM(ai.[ValorCobradoAMais])
            ELSE 0
        END
    AS DECIMAL(5,2)) AS PercentualRecuperacao
FROM [dbo].[AuditoriasItens] ai
INNER JOIN [dbo].[Conglomerados] c ON ai.[ConglomeradoId] = c.[Id]
WHERE ai.[FlExcluido] = 0
  AND ai.[ValorCobradoAMais] > 0
GROUP BY ai.[ConglomeradoId], c.[Nome];
GO
```

---

## 6. Stored Procedures

```sql
-- =============================================
-- SP: Calcular Total Recuperável por Resumo
-- =============================================
CREATE PROCEDURE [dbo].[sp_CalcularTotalRecuperavel]
    @AuditoriaResumoId UNIQUEIDENTIFIER
AS
BEGIN
    SET NOCOUNT ON;

    SELECT
        COUNT(*) AS QtdItens,
        SUM(ai.[ValorCobradoAMais]) AS TotalRecuperavel,
        AVG(ai.[PercentualDivergencia]) AS PercentualMedioDivergencia,
        SUM(CASE WHEN ai.[FlContestado] = 1 THEN 1 ELSE 0 END) AS QtdContestados,
        SUM(CASE WHEN ai.[FlRecuperado] = 1 THEN 1 ELSE 0 END) AS QtdRecuperados,
        SUM(CASE WHEN ai.[FlRecuperado] = 1 THEN ai.[ValorRecuperado] ELSE 0 END) AS TotalRecuperado
    FROM [dbo].[AuditoriasItens] ai
    WHERE ai.[AuditoriaResumoId] = @AuditoriaResumoId
      AND ai.[FlExcluido] = 0
      AND ai.[ValorCobradoAMais] > 0;
END;
GO

-- =============================================
-- SP: Marcar Itens como Contestados
-- =============================================
CREATE PROCEDURE [dbo].[sp_MarcarItensContestados]
    @AuditoriaResumoId UNIQUEIDENTIFIER,
    @NumeroContestacao NVARCHAR(100),
    @UsuarioId UNIQUEIDENTIFIER
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @DataContestacao DATETIME2 = GETDATE();

    UPDATE ai
    SET
        ai.[FlContestado] = 1,
        ai.[DataContestacao] = @DataContestacao,
        ai.[NumeroContestacao] = @NumeroContestacao,
        ai.[UpdatedAt] = @DataContestacao,
        ai.[UpdatedBy] = @UsuarioId
    FROM [dbo].[AuditoriasItens] ai
    WHERE ai.[AuditoriaResumoId] = @AuditoriaResumoId
      AND ai.[FlExcluido] = 0
      AND ai.[ValorCobradoAMais] > 0
      AND ai.[FlContestado] = 0;

    SELECT @@ROWCOUNT AS QtdItensContestados;
END;
GO
```

---

## 7. Triggers de Auditoria

```sql
-- =============================================
-- Trigger: Auditoria de INSERT
-- =============================================
CREATE TRIGGER [dbo].[TRG_AuditoriasItens_AfterInsert]
ON [dbo].[AuditoriasItens]
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO [dbo].[AuditoriasItensHistory]
        ([AuditoriaItemId], [ConglomeradoId], [Operation], [NewValues], [ChangedBy], [ChangedAt])
    SELECT
        i.[Id],
        i.[ConglomeradoId],
        'INSERT',
        (SELECT * FROM INSERTED i2 WHERE i2.Id = i.Id FOR JSON PATH, WITHOUT_ARRAY_WRAPPER),
        i.[CreatedBy],
        GETDATE()
    FROM INSERTED i;
END;
GO

-- =============================================
-- Trigger: Auditoria de UPDATE
-- =============================================
CREATE TRIGGER [dbo].[TRG_AuditoriasItens_AfterUpdate]
ON [dbo].[AuditoriasItens]
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO [dbo].[AuditoriasItensHistory]
        ([AuditoriaItemId], [ConglomeradoId], [Operation], [OldValues], [NewValues], [ChangedBy], [ChangedAt])
    SELECT
        i.[Id],
        i.[ConglomeradoId],
        'UPDATE',
        (SELECT * FROM DELETED d WHERE d.Id = i.Id FOR JSON PATH, WITHOUT_ARRAY_WRAPPER),
        (SELECT * FROM INSERTED i2 WHERE i2.Id = i.Id FOR JSON PATH, WITHOUT_ARRAY_WRAPPER),
        i.[UpdatedBy],
        GETDATE()
    FROM INSERTED i;
END;
GO
```

---

## 8. Dados Iniciais (Seed)

Nenhum dado inicial necessário. Itens de auditoria são criados durante processo de auditoria de faturas.

---

## 9. Observações

### Decisões de Modelagem

1. **Campos Computed (ValorCobradoAMais, PercentualDivergencia)**: Evita dessincronia de dados e garante cálculo correto sempre.

2. **Precisão DECIMAL(13,8)**: Padrão telecomunicações para valores com alta precisão (segundos fracionados, KB, etc.).

3. **FlContestado e FlRecuperado separados**: Permite rastrear status de contestação independente de recuperação.

4. **15 índices otimizados**: Cobertura completa para queries de relatórios, contestações e dashboards.

5. **Histórico em tabela separada**: Auditoria de 7 anos sem impactar performance da tabela principal.

### Considerações de Performance

- Índices filtrados em `ValorCobradoAMais > 0` focam em itens com divergência real.
- Índice composto `(ConglomeradoId, TipoServico, DataIdentificacao)` otimiza relatórios gerenciais.
- Campos computed persisted evitam recálculos repetidos em queries.

### Migração do Legado

Mapear `Auditoria_Item` → `AuditoriasItens`, recalcular campos computed, atualizar FKs para GUIDs.

---

## Histórico de Alterações

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 1.0 | 2025-12-18 | Architect Agent | Versão inicial - 2 tabelas, 20 índices, 2 views, 2 SPs, 2 triggers |
