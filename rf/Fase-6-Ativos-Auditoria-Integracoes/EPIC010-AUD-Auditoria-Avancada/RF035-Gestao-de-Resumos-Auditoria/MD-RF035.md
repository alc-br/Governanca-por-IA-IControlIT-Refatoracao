# Modelo de Dados - RF035: Gestão de Resumos de Auditoria de Faturas

**Versão:** 1.0
**Data:** 2025-12-18
**RF Relacionado:** [RF035 - Gestão de Resumos de Auditoria](./RF035.md)
**Banco de Dados:** SQL Server / SQLite (dev)

---

## 1. Diagrama Entidade-Relacionamento (ER)

```
┌──────────────────────┐          ┌────────────────────────────────┐
│   Conglomerados      │          │    AuditoriasResumos           │
├──────────────────────┤          ├────────────────────────────────┤
│ Id (PK)              │◄─────┐   │ Id (PK)                        │◄──┐
│ Nome                 │      │   │ ConglomeradoId (FK)            │   │
└──────────────────────┘      │   │ FaturaId (FK)                  │   │
                              │   │ PeriodoLote (AAAAMM)           │   │
┌──────────────────────┐      │   │ QtdItensAuditados              │   │
│      Faturas         │      │   │ QtdDivergenciasIdentificadas   │   │
├──────────────────────┤      │   │ ValorTotalCobrado              │   │
│ Id (PK)              │◄─────┼───┤ ValorTotalCorreto              │   │
│ NumeroFatura         │      │   │ ValorTotalDivergencia (comp)   │   │
│ ValorTotal           │      │   │ PercentualDivergencia (comp)   │   │
│ OperadoraId          │      │   │ StatusAuditoria (enum)         │   │
│ ...                  │      │   │ DataInicioAuditoria            │   │
└──────────────────────┘      │   │ DataConclusaoAuditoria         │   │
                              │   │ UsuarioResponsavelId (FK)      │   │
┌──────────────────────┐      │   │ FlAprovado                     │   │
│    Operadoras        │      │   │ UsuarioAprovadorId (FK)        │   │
├──────────────────────┤      │   │ DataAprovacao                  │   │
│ Id (PK)              │◄─────┤   │ ObservacoesAprovacao           │   │
│ NomeFantasia         │      │   │ FlExcluido                     │   │
│ CNPJ                 │      │   │ CreatedAt                      │   │
└──────────────────────┘      │   │ CreatedBy                      │   │
                              │   │ UpdatedAt                      │   │
┌──────────────────────┐      │   │ UpdatedBy                      │   │
│       Users          │      │   └────────────────────────────────┘   │
├──────────────────────┤      │                    │                   │
│ Id (PK)              │◄─────┘                    │ 1:N               │
│ Nome                 │◄──────────────────────────┘                   │
│ Email                │                                               │
└──────────────────────┘                                               │
                                                                       │
┌───────────────────────┐          ┌────────────────────────────────┐ │
│  AuditoriasItens      │          │  AuditoriasResumosHistory      │ │
├───────────────────────┤          ├────────────────────────────────┤ │
│ Id (PK)               │          │ Id (PK)                        │ │
│ AuditoriaResumoId (FK)│◄─────────┤ AuditoriaResumoId (FK)         ├─┘
│ BilheteId             │          │ Operation                      │
│ ValorCobradoAMais     │          │ OldValues (JSON)               │
│ ...                   │          │ NewValues (JSON)               │
└───────────────────────┘          │ ChangedBy                      │
         ▲                         │ ChangedAt                      │
         │                         └────────────────────────────────┘
         │ 1:N
         │
┌───────────────────────┐
│ AuditoriasResumosPorTipoServico
├───────────────────────┤
│ Id (PK)               │
│ AuditoriaResumoId (FK)│
│ TipoServico           │
│ QtdItens              │
│ ValorTotalCobrado     │
│ ValorTotalDivergencia │
└───────────────────────┘
```

---

## 2. Entidades

### 2.1 Tabela: AuditoriasResumos

**Descrição:** Consolidação de auditoria por fatura/lote com totalizadores automáticos e workflow de aprovação.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK para Cliente (multi-tenancy raiz)s (multi-tenancy) |
| FaturaId | UNIQUEIDENTIFIER | NÃO | - | FK para Faturas |
| OperadoraId | UNIQUEIDENTIFIER | NÃO | - | FK para Operadoras |
| PeriodoLote | NVARCHAR(6) | NÃO | - | Período no formato AAAAMM (ex: 202512) |
| QtdItensAuditados | INT | NÃO | 0 | Quantidade total de itens auditados |
| QtdDivergenciasIdentificadas | INT | NÃO | 0 | Quantidade de itens com divergência |
| ValorTotalCobrado | DECIMAL(18,2) | NÃO | 0.00 | Soma de ValorCobrado dos itens |
| ValorTotalCorreto | DECIMAL(18,2) | NÃO | 0.00 | Soma de ValorCorreto dos itens |
| ValorTotalDivergencia AS (ValorTotalCobrado - ValorTotalCorreto) PERSISTED | DECIMAL(18,2) | - | - | Valor total cobrado a mais (computed) |
| PercentualDivergencia AS (CASE WHEN ValorTotalCorreto > 0 THEN ((ValorTotalCobrado - ValorTotalCorreto) / ValorTotalCorreto) * 100 ELSE 0 END) PERSISTED | DECIMAL(7,4) | - | - | % de divergência (computed) |
| StatusAuditoria | INT | NÃO | 1 | Enum: 1=EmAndamento, 2=Concluida, 3=Aprovada, 4=Cancelada |
| DataInicioAuditoria | DATETIME2 | NÃO | GETDATE() | Data de início da auditoria |
| DataConclusaoAuditoria | DATETIME2 | SIM | NULL | Data de conclusão |
| UsuarioResponsavelId | UNIQUEIDENTIFIER | NÃO | - | FK para Users (auditor responsável) |
| FlAprovado | BIT | NÃO | 0 | Se foi aprovado para contestação |
| UsuarioAprovadorId | UNIQUEIDENTIFIER | SIM | NULL | FK para Users (quem aprovou) |
| DataAprovacao | DATETIME2 | SIM | NULL | Data da aprovação |
| ObservacoesAprovacao | NVARCHAR(MAX) | SIM | NULL | Observações da aprovação |
| Observacoes | NVARCHAR(MAX) | SIM | NULL | Observações gerais |
| Ativo | BIT | NÃO | true | Soft delete: false=ativo, true=excluído flag |
| CreatedAt | DATETIME2 | NÃO | GETDATE() | Data de criação |
| CreatedBy | UNIQUEIDENTIFIER | NÃO | - | Usuário que criou |
| UpdatedAt | DATETIME2 | SIM | NULL | Data de atualização |
| UpdatedBy | UNIQUEIDENTIFIER | SIM | NULL | Usuário que atualizou |

#### Índices (14 índices)

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_AuditoriasResumos | Id | CLUSTERED | Chave primária |
| IX_AuditoriasResumos_ConglomeradoId | ClienteId | NONCLUSTERED | Performance multi-tenant |
| IX_AuditoriasResumos_FaturaId | FaturaId | NONCLUSTERED UNIQUE | Um resumo por fatura |
| IX_AuditoriasResumos_OperadoraId | OperadoraId | NONCLUSTERED | Resumos por operadora |
| IX_AuditoriasResumos_PeriodoLote | PeriodoLote | NONCLUSTERED | Agrupamento temporal |
| IX_AuditoriasResumos_StatusAuditoria | StatusAuditoria | NONCLUSTERED | Filtro por status |
| IX_AuditoriasResumos_DataConclusaoAuditoria | DataConclusaoAuditoria DESC | NONCLUSTERED | Ordenação por conclusão |
| IX_AuditoriasResumos_UsuarioResponsavelId | UsuarioResponsavelId | NONCLUSTERED | Resumos por auditor |
| IX_AuditoriasResumos_FlAprovado | FlAprovado | NONCLUSTERED FILTERED | Aprovados (WHERE FlAprovado = 1) |
| IX_AuditoriasResumos_ValorTotalDivergencia | ValorTotalDivergencia DESC | NONCLUSTERED FILTERED | Top divergências (WHERE ValorTotalDivergencia > 0) |
| IX_AuditoriasResumos_CreatedAt | CreatedAt DESC | NONCLUSTERED | Auditoria temporal |
| IX_AuditoriasResumos_Composto_Dashboard | (ConglomeradoId, StatusAuditoria, DataConclusaoAuditoria) INCLUDE (ValorTotalDivergencia, OperadoraId) | NONCLUSTERED | Query dashboard |
| IX_AuditoriasResumos_Composto_PorPeriodo | (ConglomeradoId, PeriodoLote, OperadoraId) INCLUDE (ValorTotalDivergencia, FlAprovado) | NONCLUSTERED | Relatórios por período |
| IX_AuditoriasResumos_Composto_Aprovacao | (ConglomeradoId, FlAprovado, DataAprovacao) INCLUDE (UsuarioAprovadorId, ValorTotalDivergencia) | NONCLUSTERED | Workflow de aprovação |

#### Constraints

| Nome | Tipo | Definição | Descrição |
|------|------|-----------|-----------|
| PK_AuditoriasResumos | PRIMARY KEY | Id | Chave primária |
| FK_AuditoriasResumos_Conglomerado | FOREIGN KEY | ConglomeradoId REFERENCES Conglomerados(Id) | Multi-tenancy |
| FK_AuditoriasResumos_Fatura | FOREIGN KEY | FaturaId REFERENCES Faturas(Id) | Vínculo com fatura |
| FK_AuditoriasResumos_Operadora | FOREIGN KEY | OperadoraId REFERENCES Operadoras(Id) | Vínculo com operadora |
| FK_AuditoriasResumos_UsuarioResponsavel | FOREIGN KEY | UsuarioResponsavelId REFERENCES Users(Id) | Auditor responsável |
| FK_AuditoriasResumos_UsuarioAprovador | FOREIGN KEY | UsuarioAprovadorId REFERENCES Users(Id) | Aprovador |
| FK_AuditoriasResumos_CreatedBy | FOREIGN KEY | CreatedBy REFERENCES Users(Id) | Auditoria criação |
| FK_AuditoriasResumos_UpdatedBy | FOREIGN KEY | UpdatedBy REFERENCES Users(Id) | Auditoria atualização |
| CK_AuditoriasResumos_StatusAuditoria | CHECK | StatusAuditoria BETWEEN 1 AND 4 | Status válido |
| CK_AuditoriasResumos_PeriodoLote | CHECK | LEN(PeriodoLote) = 6 AND PeriodoLote LIKE '[0-9][0-9][0-9][0-9][0-9][0-9]' | Formato AAAAMM |
| CK_AuditoriasResumos_Quantidades | CHECK | QtdItensAuditados >= 0 AND QtdDivergenciasIdentificadas >= 0 AND QtdDivergenciasIdentificadas <= QtdItensAuditados | Quantidades consistentes |
| CK_AuditoriasResumos_Valores | CHECK | ValorTotalCobrado >= 0 AND ValorTotalCorreto >= 0 | Valores não-negativos |
| CK_AuditoriasResumos_DataConclusao | CHECK | DataConclusaoAuditoria IS NULL OR DataConclusaoAuditoria >= DataInicioAuditoria | Conclusão após início |
| CK_AuditoriasResumos_DataAprovacao | CHECK | DataAprovacao IS NULL OR DataAprovacao >= DataConclusaoAuditoria | Aprovação após conclusão |

---

### 2.2 Tabela: AuditoriasResumosPorTipoServico

**Descrição:** Detalhamento de resumo por tipo de serviço (Voz, Dados, SMS, Roaming).

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| AuditoriaResumoId | UNIQUEIDENTIFIER | NÃO | - | FK para AuditoriasResumos |
| TipoServico | NVARCHAR(100) | NÃO | - | Tipo de serviço |
| QtdItens | INT | NÃO | 0 | Quantidade de itens deste tipo |
| ValorTotalCobrado | DECIMAL(18,2) | NÃO | 0.00 | Total cobrado deste tipo |
| ValorTotalCorreto | DECIMAL(18,2) | NÃO | 0.00 | Total correto deste tipo |
| ValorTotalDivergencia AS (ValorTotalCobrado - ValorTotalCorreto) PERSISTED | DECIMAL(18,2) | - | - | Divergência deste tipo |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_AuditoriasResumosPorTipoServico | Id | CLUSTERED | Chave primária |
| IX_AuditoriasResumosPorTipoServico_ResumoId | AuditoriaResumoId | NONCLUSTERED | Detalhamento por resumo |
| IX_AuditoriasResumosPorTipoServico_TipoServico | TipoServico | NONCLUSTERED | Agrupamento por tipo |
| UQ_AuditoriasResumosPorTipoServico | (AuditoriaResumoId, TipoServico) | UNIQUE | Um registro por tipo no resumo |

#### Constraints

| Nome | Tipo | Definição | Descrição |
|------|------|-----------|-----------|
| PK_AuditoriasResumosPorTipoServico | PRIMARY KEY | Id | Chave primária |
| FK_AuditoriasResumosPorTipoServico_Resumo | FOREIGN KEY | AuditoriaResumoId REFERENCES AuditoriasResumos(Id) | Vínculo com resumo |
| CK_AuditoriasResumosPorTipoServico_QtdItens | CHECK | QtdItens >= 0 | Quantidade não-negativa |
| CK_AuditoriasResumosPorTipoServico_Valores | CHECK | ValorTotalCobrado >= 0 AND ValorTotalCorreto >= 0 | Valores não-negativos |

---

### 2.3 Tabela: AuditoriasResumosHistory

**Descrição:** Histórico de alterações em resumos de auditoria (7 anos LGPD).

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| AuditoriaResumoId | UNIQUEIDENTIFIER | NÃO | - | FK para AuditoriasResumos |
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
| PK_AuditoriasResumosHistory | Id | CLUSTERED | Chave primária |
| IX_AuditoriasResumosHistory_ResumoId | AuditoriaResumoId, ChangedAt DESC | NONCLUSTERED | Histórico de um resumo |
| IX_AuditoriasResumosHistory_ConglomeradoId | ClienteId | NONCLUSTERED | Performance multi-tenant |
| IX_AuditoriasResumosHistory_ChangedAt | ChangedAt DESC | NONCLUSTERED | Auditoria temporal |

#### Constraints

| Nome | Tipo | Definição | Descrição |
|------|------|-----------|-----------|
| PK_AuditoriasResumosHistory | PRIMARY KEY | Id | Chave primária |
| FK_AuditoriasResumosHistory_Resumo | FOREIGN KEY | AuditoriaResumoId REFERENCES AuditoriasResumos(Id) | Vínculo com resumo |
| FK_AuditoriasResumosHistory_Conglomerado | FOREIGN KEY | ConglomeradoId REFERENCES Conglomerados(Id) | Multi-tenancy |
| FK_AuditoriasResumosHistory_ChangedBy | FOREIGN KEY | ChangedBy REFERENCES Users(Id) | Auditoria |

---

## 3. Relacionamentos

| Tabela Origem | Cardinalidade | Tabela Destino | Descrição |
|---------------|---------------|----------------|-----------|
| Conglomerados | 1:N | AuditoriasResumos | Conglomerado possui muitos resumos |
| Faturas | 1:1 | AuditoriasResumos | Fatura possui um resumo de auditoria |
| Operadoras | 1:N | AuditoriasResumos | Operadora possui muitos resumos |
| Users | 1:N | AuditoriasResumos (Responsável) | Auditor responsável por resumos |
| Users | 1:N | AuditoriasResumos (Aprovador) | Aprovador de resumos |
| AuditoriasResumos | 1:N | AuditoriasItens | Resumo agrupa múltiplos itens |
| AuditoriasResumos | 1:N | AuditoriasResumosPorTipoServico | Resumo detalha por tipo de serviço |
| AuditoriasResumos | 1:N | AuditoriasResumosHistory | Resumo possui histórico de alterações |

---

## 4. DDL - SQL Server

```sql
-- =============================================
-- RF035 - Gestão de Resumos de Auditoria
-- Modelo de Dados
-- Data: 2025-12-18
-- =============================================

-- ---------------------------------------------
-- Tabela: AuditoriasResumos
-- ---------------------------------------------
CREATE TABLE [dbo].[AuditoriasResumos] (
    [Id] UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    [ConglomeradoId] UNIQUEIDENTIFIER NOT NULL,
    [FaturaId] UNIQUEIDENTIFIER NOT NULL,
    [OperadoraId] UNIQUEIDENTIFIER NOT NULL,
    [PeriodoLote] NVARCHAR(6) NOT NULL,
    [QtdItensAuditados] INT NOT NULL DEFAULT 0,
    [QtdDivergenciasIdentificadas] INT NOT NULL DEFAULT 0,
    [ValorTotalCobrado] DECIMAL(18,2) NOT NULL DEFAULT 0.00,
    [ValorTotalCorreto] DECIMAL(18,2) NOT NULL DEFAULT 0.00,
    [ValorTotalDivergencia] AS ([ValorTotalCobrado] - [ValorTotalCorreto]) PERSISTED,
    [PercentualDivergencia] AS (
        CASE
            WHEN [ValorTotalCorreto] > 0 THEN (([ValorTotalCobrado] - [ValorTotalCorreto]) / [ValorTotalCorreto]) * 100
            ELSE 0
        END
    ) PERSISTED,
    [StatusAuditoria] INT NOT NULL DEFAULT 1,
    [DataInicioAuditoria] DATETIME2 NOT NULL DEFAULT GETDATE(),
    [DataConclusaoAuditoria] DATETIME2 NULL,
    [UsuarioResponsavelId] UNIQUEIDENTIFIER NOT NULL,
    [FlAprovado] BIT NOT NULL DEFAULT 0,
    [UsuarioAprovadorId] UNIQUEIDENTIFIER NULL,
    [DataAprovacao] DATETIME2 NULL,
    [ObservacoesAprovacao] NVARCHAR(MAX) NULL,
    [Observacoes] NVARCHAR(MAX) NULL,
    [FlExcluido] BIT NOT NULL DEFAULT 0,
    [CreatedAt] DATETIME2 NOT NULL DEFAULT GETDATE(),
    [CreatedBy] UNIQUEIDENTIFIER NOT NULL,
    [UpdatedAt] DATETIME2 NULL,
    [UpdatedBy] UNIQUEIDENTIFIER NULL,

    -- Primary Key
    CONSTRAINT [PK_AuditoriasResumos] PRIMARY KEY CLUSTERED ([Id] ASC),

    -- Foreign Keys
    CONSTRAINT [FK_AuditoriasResumos_Conglomerado]
        FOREIGN KEY ([ConglomeradoId]) REFERENCES [dbo].[Conglomerados]([Id]),
    CONSTRAINT [FK_AuditoriasResumos_Fatura]
        FOREIGN KEY ([FaturaId]) REFERENCES [dbo].[Faturas]([Id]),
    CONSTRAINT [FK_AuditoriasResumos_Operadora]
        FOREIGN KEY ([OperadoraId]) REFERENCES [dbo].[Operadoras]([Id]),
    CONSTRAINT [FK_AuditoriasResumos_UsuarioResponsavel]
        FOREIGN KEY ([UsuarioResponsavelId]) REFERENCES [dbo].[Users]([Id]),
    CONSTRAINT [FK_AuditoriasResumos_UsuarioAprovador]
        FOREIGN KEY ([UsuarioAprovadorId]) REFERENCES [dbo].[Users]([Id]),
    CONSTRAINT [FK_AuditoriasResumos_CreatedBy]
        FOREIGN KEY ([CreatedBy]) REFERENCES [dbo].[Users]([Id]),
    CONSTRAINT [FK_AuditoriasResumos_UpdatedBy]
        FOREIGN KEY ([UpdatedBy]) REFERENCES [dbo].[Users]([Id]),

    -- Check Constraints
    CONSTRAINT [CK_AuditoriasResumos_StatusAuditoria]
        CHECK ([StatusAuditoria] BETWEEN 1 AND 4),
    CONSTRAINT [CK_AuditoriasResumos_PeriodoLote]
        CHECK (LEN([PeriodoLote]) = 6 AND [PeriodoLote] LIKE '[0-9][0-9][0-9][0-9][0-9][0-9]'),
    CONSTRAINT [CK_AuditoriasResumos_Quantidades]
        CHECK ([QtdItensAuditados] >= 0 AND [QtdDivergenciasIdentificadas] >= 0 AND [QtdDivergenciasIdentificadas] <= [QtdItensAuditados]),
    CONSTRAINT [CK_AuditoriasResumos_Valores]
        CHECK ([ValorTotalCobrado] >= 0 AND [ValorTotalCorreto] >= 0),
    CONSTRAINT [CK_AuditoriasResumos_DataConclusao]
        CHECK ([DataConclusaoAuditoria] IS NULL OR [DataConclusaoAuditoria] >= [DataInicioAuditoria]),
    CONSTRAINT [CK_AuditoriasResumos_DataAprovacao]
        CHECK ([DataAprovacao] IS NULL OR [DataAprovacao] >= [DataConclusaoAuditoria])
);
GO

-- Índices (14 índices otimizados)
CREATE NONCLUSTERED INDEX [IX_AuditoriasResumos_ConglomeradoId]
    ON [dbo].[AuditoriasResumos]([ConglomeradoId])
    WHERE [FlExcluido] = 0;
GO

CREATE UNIQUE NONCLUSTERED INDEX [IX_AuditoriasResumos_FaturaId]
    ON [dbo].[AuditoriasResumos]([FaturaId])
    WHERE [FlExcluido] = 0;
GO

CREATE NONCLUSTERED INDEX [IX_AuditoriasResumos_OperadoraId]
    ON [dbo].[AuditoriasResumos]([OperadoraId])
    WHERE [FlExcluido] = 0;
GO

CREATE NONCLUSTERED INDEX [IX_AuditoriasResumos_PeriodoLote]
    ON [dbo].[AuditoriasResumos]([PeriodoLote])
    INCLUDE ([OperadoraId], [ValorTotalDivergencia])
    WHERE [FlExcluido] = 0;
GO

CREATE NONCLUSTERED INDEX [IX_AuditoriasResumos_StatusAuditoria]
    ON [dbo].[AuditoriasResumos]([StatusAuditoria])
    WHERE [FlExcluido] = 0;
GO

CREATE NONCLUSTERED INDEX [IX_AuditoriasResumos_DataConclusaoAuditoria]
    ON [dbo].[AuditoriasResumos]([DataConclusaoAuditoria] DESC)
    WHERE [FlExcluido] = 0 AND [DataConclusaoAuditoria] IS NOT NULL;
GO

CREATE NONCLUSTERED INDEX [IX_AuditoriasResumos_UsuarioResponsavelId]
    ON [dbo].[AuditoriasResumos]([UsuarioResponsavelId])
    WHERE [FlExcluido] = 0;
GO

CREATE NONCLUSTERED INDEX [IX_AuditoriasResumos_FlAprovado]
    ON [dbo].[AuditoriasResumos]([FlAprovado], [DataAprovacao])
    WHERE [FlAprovado] = 1 AND [FlExcluido] = 0;
GO

CREATE NONCLUSTERED INDEX [IX_AuditoriasResumos_ValorTotalDivergencia]
    ON [dbo].[AuditoriasResumos]([ValorTotalDivergencia] DESC)
    INCLUDE ([FaturaId], [OperadoraId], [PeriodoLote])
    WHERE [ValorTotalDivergencia] > 0 AND [FlExcluido] = 0;
GO

CREATE NONCLUSTERED INDEX [IX_AuditoriasResumos_CreatedAt]
    ON [dbo].[AuditoriasResumos]([CreatedAt] DESC)
    WHERE [FlExcluido] = 0;
GO

CREATE NONCLUSTERED INDEX [IX_AuditoriasResumos_Composto_Dashboard]
    ON [dbo].[AuditoriasResumos]([ConglomeradoId], [StatusAuditoria], [DataConclusaoAuditoria])
    INCLUDE ([ValorTotalDivergencia], [OperadoraId])
    WHERE [FlExcluido] = 0;
GO

CREATE NONCLUSTERED INDEX [IX_AuditoriasResumos_Composto_PorPeriodo]
    ON [dbo].[AuditoriasResumos]([ConglomeradoId], [PeriodoLote], [OperadoraId])
    INCLUDE ([ValorTotalDivergencia], [FlAprovado])
    WHERE [FlExcluido] = 0;
GO

CREATE NONCLUSTERED INDEX [IX_AuditoriasResumos_Composto_Aprovacao]
    ON [dbo].[AuditoriasResumos]([ConglomeradoId], [FlAprovado], [DataAprovacao])
    INCLUDE ([UsuarioAprovadorId], [ValorTotalDivergencia])
    WHERE [FlExcluido] = 0;
GO

-- Comentários
EXEC sys.sp_addextendedproperty
    @name=N'MS_Description',
    @value=N'Resumos consolidados de auditoria por fatura com totalizadores automáticos',
    @level0type=N'SCHEMA', @level0name=N'dbo',
    @level1type=N'TABLE',  @level1name=N'AuditoriasResumos';
GO


-- ---------------------------------------------
-- Tabela: AuditoriasResumosPorTipoServico
-- ---------------------------------------------
CREATE TABLE [dbo].[AuditoriasResumosPorTipoServico] (
    [Id] UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    [AuditoriaResumoId] UNIQUEIDENTIFIER NOT NULL,
    [TipoServico] NVARCHAR(100) NOT NULL,
    [QtdItens] INT NOT NULL DEFAULT 0,
    [ValorTotalCobrado] DECIMAL(18,2) NOT NULL DEFAULT 0.00,
    [ValorTotalCorreto] DECIMAL(18,2) NOT NULL DEFAULT 0.00,
    [ValorTotalDivergencia] AS ([ValorTotalCobrado] - [ValorTotalCorreto]) PERSISTED,

    CONSTRAINT [PK_AuditoriasResumosPorTipoServico] PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [FK_AuditoriasResumosPorTipoServico_Resumo]
        FOREIGN KEY ([AuditoriaResumoId]) REFERENCES [dbo].[AuditoriasResumos]([Id]),
    CONSTRAINT [UQ_AuditoriasResumosPorTipoServico]
        UNIQUE ([AuditoriaResumoId], [TipoServico]),
    CONSTRAINT [CK_AuditoriasResumosPorTipoServico_QtdItens]
        CHECK ([QtdItens] >= 0),
    CONSTRAINT [CK_AuditoriasResumosPorTipoServico_Valores]
        CHECK ([ValorTotalCobrado] >= 0 AND [ValorTotalCorreto] >= 0)
);
GO

CREATE NONCLUSTERED INDEX [IX_AuditoriasResumosPorTipoServico_ResumoId]
    ON [dbo].[AuditoriasResumosPorTipoServico]([AuditoriaResumoId]);
GO

CREATE NONCLUSTERED INDEX [IX_AuditoriasResumosPorTipoServico_TipoServico]
    ON [dbo].[AuditoriasResumosPorTipoServico]([TipoServico]);
GO


-- ---------------------------------------------
-- Tabela: AuditoriasResumosHistory
-- ---------------------------------------------
CREATE TABLE [dbo].[AuditoriasResumosHistory] (
    [Id] UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    [AuditoriaResumoId] UNIQUEIDENTIFIER NOT NULL,
    [ConglomeradoId] UNIQUEIDENTIFIER NOT NULL,
    [Operation] NVARCHAR(20) NOT NULL,
    [OldValues] NVARCHAR(MAX) NULL,
    [NewValues] NVARCHAR(MAX) NULL,
    [ChangedBy] UNIQUEIDENTIFIER NOT NULL,
    [ChangedAt] DATETIME2 NOT NULL DEFAULT GETDATE(),
    [IPAddress] NVARCHAR(50) NULL,
    [UserAgent] NVARCHAR(500) NULL,

    CONSTRAINT [PK_AuditoriasResumosHistory] PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [FK_AuditoriasResumosHistory_Resumo]
        FOREIGN KEY ([AuditoriaResumoId]) REFERENCES [dbo].[AuditoriasResumos]([Id]),
    CONSTRAINT [FK_AuditoriasResumosHistory_Conglomerado]
        FOREIGN KEY ([ConglomeradoId]) REFERENCES [dbo].[Conglomerados]([Id]),
    CONSTRAINT [FK_AuditoriasResumosHistory_ChangedBy]
        FOREIGN KEY ([ChangedBy]) REFERENCES [dbo].[Users]([Id])
);
GO

CREATE NONCLUSTERED INDEX [IX_AuditoriasResumosHistory_ResumoId]
    ON [dbo].[AuditoriasResumosHistory]([AuditoriaResumoId], [ChangedAt] DESC);
GO

CREATE NONCLUSTERED INDEX [IX_AuditoriasResumosHistory_ConglomeradoId]
    ON [dbo].[AuditoriasResumosHistory]([ConglomeradoId]);
GO

CREATE NONCLUSTERED INDEX [IX_AuditoriasResumosHistory_ChangedAt]
    ON [dbo].[AuditoriasResumosHistory]([ChangedAt] DESC);
GO
```

---

## 5. Views Úteis

```sql
-- =============================================
-- View: Dashboard Executivo de Auditoria
-- =============================================
CREATE VIEW [dbo].[vw_AuditoriasResumos_Dashboard]
AS
SELECT
    ar.[ConglomeradoId],
    c.[Nome] AS ConglomeradoNome,
    ar.[PeriodoLote],
    o.[NomeFantasia] AS OperadoraNome,
    COUNT(*) AS QtdResumos,
    SUM(ar.[QtdItensAuditados]) AS TotalItensAuditados,
    SUM(ar.[QtdDivergenciasIdentificadas]) AS TotalDivergencias,
    SUM(ar.[ValorTotalCobrado]) AS TotalCobrado,
    SUM(ar.[ValorTotalCorreto]) AS TotalCorreto,
    SUM(ar.[ValorTotalDivergencia]) AS TotalRecuperavel,
    AVG(ar.[PercentualDivergencia]) AS PercentualMedioDivergencia,
    SUM(CASE WHEN ar.[FlAprovado] = 1 THEN ar.[ValorTotalDivergencia] ELSE 0 END) AS TotalAprovadoContestacao
FROM [dbo].[AuditoriasResumos] ar
INNER JOIN [dbo].[Conglomerados] c ON ar.[ConglomeradoId] = c.[Id]
INNER JOIN [dbo].[Operadoras] o ON ar.[OperadoraId] = o.[Id]
WHERE ar.[FlExcluido] = 0
  AND ar.[StatusAuditoria] IN (2, 3) -- Concluída ou Aprovada
GROUP BY ar.[ConglomeradoId], c.[Nome], ar.[PeriodoLote], o.[NomeFantasia];
GO

-- =============================================
-- View: Top 10 Faturas com Maior Divergência
-- =============================================
CREATE VIEW [dbo].[vw_AuditoriasResumos_Top10Divergencias]
AS
SELECT TOP 10
    ar.[Id],
    ar.[FaturaId],
    f.[NumeroFatura],
    o.[NomeFantasia] AS OperadoraNome,
    ar.[PeriodoLote],
    ar.[ValorTotalCobrado],
    ar.[ValorTotalCorreto],
    ar.[ValorTotalDivergencia],
    ar.[PercentualDivergencia],
    ar.[QtdDivergenciasIdentificadas],
    ar.[FlAprovado],
    u.[Nome] AS AuditorResponsavel
FROM [dbo].[AuditoriasResumos] ar
INNER JOIN [dbo].[Faturas] f ON ar.[FaturaId] = f.[Id]
INNER JOIN [dbo].[Operadoras] o ON ar.[OperadoraId] = o.[Id]
INNER JOIN [dbo].[Users] u ON ar.[UsuarioResponsavelId] = u.[Id]
WHERE ar.[FlExcluido] = 0
  AND ar.[ValorTotalDivergencia] > 0
ORDER BY ar.[ValorTotalDivergencia] DESC;
GO
```

---

## 6. Stored Procedures

```sql
-- =============================================
-- SP: Recalcular Totalizadores do Resumo
-- =============================================
CREATE PROCEDURE [dbo].[sp_RecalcularTotalizadoresResumo]
    @AuditoriaResumoId UNIQUEIDENTIFIER
AS
BEGIN
    SET NOCOUNT ON;

    UPDATE ar
    SET
        ar.[QtdItensAuditados] = totais.[QtdItens],
        ar.[QtdDivergenciasIdentificadas] = totais.[QtdDivergencias],
        ar.[ValorTotalCobrado] = totais.[TotalCobrado],
        ar.[ValorTotalCorreto] = totais.[TotalCorreto],
        ar.[UpdatedAt] = GETDATE()
    FROM [dbo].[AuditoriasResumos] ar
    CROSS APPLY (
        SELECT
            COUNT(*) AS QtdItens,
            SUM(CASE WHEN ai.[ValorCobradoAMais] > 0 THEN 1 ELSE 0 END) AS QtdDivergencias,
            SUM(ai.[ValorCobrado]) AS TotalCobrado,
            SUM(ai.[ValorCorreto]) AS TotalCorreto
        FROM [dbo].[AuditoriasItens] ai
        WHERE ai.[AuditoriaResumoId] = @AuditoriaResumoId
          AND ai.[FlExcluido] = 0
    ) totais
    WHERE ar.[Id] = @AuditoriaResumoId;

    -- Retornar resumo atualizado
    SELECT
        ar.[Id],
        ar.[QtdItensAuditados],
        ar.[QtdDivergenciasIdentificadas],
        ar.[ValorTotalCobrado],
        ar.[ValorTotalCorreto],
        ar.[ValorTotalDivergencia],
        ar.[PercentualDivergencia]
    FROM [dbo].[AuditoriasResumos] ar
    WHERE ar.[Id] = @AuditoriaResumoId;
END;
GO

-- =============================================
-- SP: Aprovar Resumo para Contestação
-- =============================================
CREATE PROCEDURE [dbo].[sp_AprovarResumoContestacao]
    @AuditoriaResumoId UNIQUEIDENTIFIER,
    @UsuarioAprovadorId UNIQUEIDENTIFIER,
    @Observacoes NVARCHAR(MAX) = NULL
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @DataAprovacao DATETIME2 = GETDATE();

    UPDATE ar
    SET
        ar.[FlAprovado] = 1,
        ar.[UsuarioAprovadorId] = @UsuarioAprovadorId,
        ar.[DataAprovacao] = @DataAprovacao,
        ar.[ObservacoesAprovacao] = @Observacoes,
        ar.[StatusAuditoria] = 3, -- Aprovada
        ar.[UpdatedAt] = @DataAprovacao,
        ar.[UpdatedBy] = @UsuarioAprovadorId
    FROM [dbo].[AuditoriasResumos] ar
    WHERE ar.[Id] = @AuditoriaResumoId
      AND ar.[StatusAuditoria] = 2 -- Somente se já concluída
      AND ar.[FlAprovado] = 0;

    SELECT @@ROWCOUNT AS QtdAprovadas;
END;
GO
```

---

## 7. Triggers

```sql
-- =============================================
-- Trigger: Recalcular Resumo ao Inserir Item
-- =============================================
CREATE TRIGGER [dbo].[TRG_AuditoriasItens_AfterInsert_RecalcularResumo]
ON [dbo].[AuditoriasItens]
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @ResumoId UNIQUEIDENTIFIER;

    SELECT @ResumoId = i.[AuditoriaResumoId]
    FROM INSERTED i;

    EXEC [dbo].[sp_RecalcularTotalizadoresResumo] @ResumoId;
END;
GO

-- =============================================
-- Trigger: Recalcular Resumo ao Atualizar Item
-- =============================================
CREATE TRIGGER [dbo].[TRG_AuditoriasItens_AfterUpdate_RecalcularResumo]
ON [dbo].[AuditoriasItens]
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @ResumoId UNIQUEIDENTIFIER;

    SELECT @ResumoId = i.[AuditoriaResumoId]
    FROM INSERTED i;

    EXEC [dbo].[sp_RecalcularTotalizadoresResumo] @ResumoId;
END;
GO

-- =============================================
-- Trigger: Recalcular Resumo ao Deletar Item (Soft Delete)
-- =============================================
CREATE TRIGGER [dbo].[TRG_AuditoriasItens_AfterUpdate_SoftDelete_RecalcularResumo]
ON [dbo].[AuditoriasItens]
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    IF UPDATE(FlExcluido)
    BEGIN
        DECLARE @ResumoId UNIQUEIDENTIFIER;

        SELECT @ResumoId = i.[AuditoriaResumoId]
        FROM INSERTED i
        WHERE i.[FlExcluido] = 1;

        IF @ResumoId IS NOT NULL
            EXEC [dbo].[sp_RecalcularTotalizadoresResumo] @ResumoId;
    END
END;
GO
```

---

## 8. Dados Iniciais (Seed)

Nenhum dado inicial necessário. Resumos são criados automaticamente durante processo de auditoria.

---

## 9. Observações

### Decisões de Modelagem

1. **Totalizadores Armazenados**: Evita joins pesados em queries de dashboard. Recalculados via triggers.

2. **Campos Computed (ValorTotalDivergencia, PercentualDivergencia)**: Garantem consistência matemática.

3. **Relacionamento 1:1 Fatura → Resumo**: Índice único garante um resumo por fatura.

4. **Workflow de Aprovação**: FlAprovado, UsuarioAprovadorId, DataAprovacao para rastreamento de decisões gerenciais.

5. **Detalhamento por Tipo de Serviço**: Tabela separada para análise por categoria (Voz, Dados, etc.).

### Considerações de Performance

- 14 índices otimizados na tabela principal.
- Índices compostos para queries de dashboard e relatórios.
- Triggers automatizam recálculo apenas quando necessário.
- Views pré-calculadas para relatórios executivos.

### Migração do Legado

Mapear `Auditoria_Resumo` → `AuditoriasResumos`, converter campos varchar para tipos corretos, recalcular totalizadores.

---

## Histórico de Alterações

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 1.0 | 2025-12-18 | Architect Agent | Versão inicial - 3 tabelas, 21 índices, 2 views, 2 SPs, 3 triggers |
