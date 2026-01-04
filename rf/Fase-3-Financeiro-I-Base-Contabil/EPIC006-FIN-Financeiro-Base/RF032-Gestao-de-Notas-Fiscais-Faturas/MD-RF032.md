# Modelo de Dados - RF032: Gestão de Notas Fiscais em Faturas

**Versão:** 1.0
**Data:** 2025-12-18
**RF Relacionado:** [RF032 - Gestão de Notas Fiscais em Faturas](./RF032.md)
**Banco de Dados:** SQL Server / SQLite (dev)

---

## 1. Diagrama Entidade-Relacionamento (ER)

```
┌─────────────────────────────┐          ┌──────────────────────────────┐
│     Conglomerados           │          │         Faturas              │
├─────────────────────────────┤          ├──────────────────────────────┤
│ Id (PK)                     │◄────┐    │ Id (PK)                      │◄──┐
│ Nome                        │     │    │ ConglomeradoId (FK)          │   │
│ ...                         │     │    │ NumeroFatura                 │   │
└─────────────────────────────┘     │    │ Status                       │   │
                                    │    │ ...                          │   │
                                    │    └──────────────────────────────┘   │
                                    │                 ▲                     │
                                    │                 │                     │
                                    │                 │ 1:N                 │
                                    │                 │                     │
┌─────────────────────────────┐   │    ┌──────────────────────────────┐   │
│     CentrosCusto            │   │    │  NotasFiscaisFaturas         │   │
├─────────────────────────────┤   │    ├──────────────────────────────┤   │
│ Id (PK)                     │◄──┼────┤ Id (PK)                      │   │
│ ConglomeradoId (FK)         │   │    │ ConglomeradoId (FK)          ├───┘
│ Nome                        │   └────┤ FaturaId (FK)                │
│ Codigo                      │        │ NumeroNotaFiscal (UNIQUE)    │
│ ...                         │        │ PercentualRateio             │
└─────────────────────────────┘        │ CentroCustoId (FK) [NULL]    │
                                       │ FilialId (FK) [NULL]         ├──┐
┌─────────────────────────────┐        │ ValorCalculado               │  │
│        Filiais              │        │ DataEmissao                  │  │
├─────────────────────────────┤        │ DataRecebimento              │  │
│ Id (PK)                     │◄───────┤ Observacoes                  │  │
│ ConglomeradoId (FK)         │        │ FlExcluido                   │  │
│ Nome                        │        │ CreatedAt                    │  │
│ CNPJ                        │        │ CreatedBy                    │  │
│ ...                         │        │ UpdatedAt                    │  │
└─────────────────────────────┘        │ UpdatedBy                    │  │
                                       └──────────────────────────────┘  │
┌─────────────────────────────┐                     │                    │
│  NotasFiscaisFaturasHistory │                     │ 1:N                │
├─────────────────────────────┤                     │                    │
│ Id (PK)                     │                     ▼                    │
│ NotaFiscalFaturaId (FK)     │◄────────────────────┘                    │
│ ConglomeradoId (FK)         │◄─────────────────────────────────────────┘
│ Operation (INSERT/UPDATE)   │
│ OldValues (JSON)            │
│ NewValues (JSON)            │
│ ChangedBy                   │
│ ChangedAt                   │
└─────────────────────────────┘
```

---

## 2. Entidades

### 2.1 Tabela: NotasFiscaisFaturas

**Descrição:** Armazena notas fiscais vinculadas a faturas com percentual de rateio para centros de custo e filiais.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK para Cliente (multi-tenancy raiz)s (multi-tenancy) |
| FaturaId | UNIQUEIDENTIFIER | NÃO | - | FK para Faturas |
| NumeroNotaFiscal | NVARCHAR(200) | NÃO | - | Número da nota fiscal (único por conglomerado) |
| PercentualRateio | DECIMAL(10,4) | NÃO | - | Percentual de rateio (0.0001 a 100.0000) |
| CentroCustoId | UNIQUEIDENTIFIER | SIM | NULL | FK para CentrosCusto (opcional) |
| FilialId | NVARCHAR(50) | SIM | NULL | FK para Filiais (opcional) |
| ValorCalculado | DECIMAL(18,2) | NÃO | 0.00 | Valor calculado baseado no percentual |
| DataEmissao | DATETIME2 | SIM | NULL | Data de emissão da NF |
| DataRecebimento | DATETIME2 | SIM | NULL | Data de recebimento da NF |
| Observacoes | NVARCHAR(MAX) | SIM | NULL | Observações adicionais |
| Ativo | BIT | NÃO | true | Soft delete: false=ativo, true=excluído flag |
| CreatedAt | DATETIME2 | NÃO | GETDATE() | Data de criação |
| CreatedBy | UNIQUEIDENTIFIER | NÃO | - | Usuário que criou |
| UpdatedAt | DATETIME2 | SIM | NULL | Data de atualização |
| UpdatedBy | UNIQUEIDENTIFIER | SIM | NULL | Usuário que atualizou |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_NotasFiscaisFaturas | Id | CLUSTERED | Chave primária |
| IX_NotasFiscaisFaturas_ConglomeradoId | ClienteId | NONCLUSTERED | Performance multi-tenant |
| IX_NotasFiscaisFaturas_FaturaId | FaturaId | NONCLUSTERED | Busca por fatura |
| UQ_NotasFiscaisFaturas_NumeroNF | (ConglomeradoId, NumeroNotaFiscal) | UNIQUE FILTERED | Unicidade de NF por conglomerado (WHERE FlExcluido = 0) |
| IX_NotasFiscaisFaturas_CentroCustoId | CentroCustoId | NONCLUSTERED | Busca por centro de custo |
| IX_NotasFiscaisFaturas_FilialId | FilialId | NONCLUSTERED | Busca por filial |
| IX_NotasFiscaisFaturas_DataEmissao | DataEmissao | NONCLUSTERED | Ordenação por data |

#### Constraints

| Nome | Tipo | Definição | Descrição |
|------|------|-----------|-----------|
| PK_NotasFiscaisFaturas | PRIMARY KEY | Id | Chave primária |
| FK_NotasFiscaisFaturas_Conglomerado | FOREIGN KEY | ConglomeradoId REFERENCES Conglomerados(Id) | Multi-tenancy |
| FK_NotasFiscaisFaturas_Fatura | FOREIGN KEY | FaturaId REFERENCES Faturas(Id) | Vinculação com fatura |
| FK_NotasFiscaisFaturas_CentroCusto | FOREIGN KEY | CentroCustoId REFERENCES CentrosCusto(Id) | Rateio por centro de custo |
| FK_NotasFiscaisFaturas_Filial | FOREIGN KEY | FilialId REFERENCES Filiais(Id) | Rateio por filial |
| FK_NotasFiscaisFaturas_CreatedBy | FOREIGN KEY | CreatedBy REFERENCES Users(Id) | Auditoria criação |
| FK_NotasFiscaisFaturas_UpdatedBy | FOREIGN KEY | UpdatedBy REFERENCES Users(Id) | Auditoria atualização |
| CK_NotasFiscaisFaturas_PercentualRateio | CHECK | PercentualRateio > 0 AND PercentualRateio <= 100 | Percentual válido |
| CK_NotasFiscaisFaturas_ValorCalculado | CHECK | ValorCalculado >= 0 | Valor não negativo |
| CK_NotasFiscaisFaturas_DataRecebimento | CHECK | DataRecebimento IS NULL OR DataRecebimento >= DataEmissao | Data recebimento após emissão |

---

### 2.2 Tabela: NotasFiscaisFaturasHistory

**Descrição:** Tabela de histórico para auditoria completa de alterações em notas fiscais (7 anos LGPD).

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| NotaFiscalFaturaId | UNIQUEIDENTIFIER | NÃO | - | FK para NotasFiscaisFaturas |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK para Cliente (multi-tenancy raiz)s |
| Operation | NVARCHAR(20) | NÃO | - | INSERT, UPDATE, DELETE |
| OldValues | NVARCHAR(MAX) | SIM | NULL | JSON com valores anteriores |
| NewValues | NVARCHAR(MAX) | SIM | NULL | JSON com novos valores |
| ChangedBy | UNIQUEIDENTIFIER | NÃO | - | Usuário que fez a alteração |
| ChangedAt | DATETIME2 | NÃO | GETDATE() | Timestamp da alteração |
| IPAddress | NVARCHAR(50) | SIM | NULL | IP de origem da alteração |
| UserAgent | NVARCHAR(500) | SIM | NULL | User Agent da requisição |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_NotasFiscaisFaturasHistory | Id | CLUSTERED | Chave primária |
| IX_NotasFiscaisFaturasHistory_NotaFiscalFaturaId | NotaFiscalFaturaId | NONCLUSTERED | Busca por nota fiscal |
| IX_NotasFiscaisFaturasHistory_ConglomeradoId | ClienteId | NONCLUSTERED | Performance multi-tenant |
| IX_NotasFiscaisFaturasHistory_ChangedAt | ChangedAt | NONCLUSTERED | Ordenação cronológica |
| IX_NotasFiscaisFaturasHistory_ChangedBy | ChangedBy | NONCLUSTERED | Auditoria por usuário |

#### Constraints

| Nome | Tipo | Definição | Descrição |
|------|------|-----------|-----------|
| PK_NotasFiscaisFaturasHistory | PRIMARY KEY | Id | Chave primária |
| FK_NotasFiscaisFaturasHistory_NotaFiscalFatura | FOREIGN KEY | NotaFiscalFaturaId REFERENCES NotasFiscaisFaturas(Id) | Vínculo com registro original |
| FK_NotasFiscaisFaturasHistory_Conglomerado | FOREIGN KEY | ConglomeradoId REFERENCES Conglomerados(Id) | Multi-tenancy |
| FK_NotasFiscaisFaturasHistory_ChangedBy | FOREIGN KEY | ChangedBy REFERENCES Users(Id) | Auditoria |

---

## 3. Relacionamentos

| Tabela Origem | Cardinalidade | Tabela Destino | Descrição |
|---------------|---------------|----------------|-----------|
| Conglomerados | 1:N | NotasFiscaisFaturas | Conglomerado possui muitas notas fiscais |
| Faturas | 1:N | NotasFiscaisFaturas | Fatura pode ter múltiplas notas fiscais |
| CentrosCusto | 1:N | NotasFiscaisFaturas | Centro de custo pode estar em múltiplas notas |
| Filiais | 1:N | NotasFiscaisFaturas | Filial pode estar em múltiplas notas |
| Users | 1:N | NotasFiscaisFaturas (CreatedBy) | Usuário cria notas fiscais |
| Users | 1:N | NotasFiscaisFaturas (UpdatedBy) | Usuário atualiza notas fiscais |
| NotasFiscaisFaturas | 1:N | NotasFiscaisFaturasHistory | Nota fiscal possui histórico de alterações |

---

## 4. DDL - SQL Server

```sql
-- =============================================
-- RF032 - Gestão de Notas Fiscais em Faturas
-- Modelo de Dados
-- Data: 2025-12-18
-- =============================================

-- ---------------------------------------------
-- Tabela: NotasFiscaisFaturas
-- ---------------------------------------------
CREATE TABLE [dbo].[NotasFiscaisFaturas] (
    [Id] UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    [ConglomeradoId] UNIQUEIDENTIFIER NOT NULL,
    [FaturaId] UNIQUEIDENTIFIER NOT NULL,
    [NumeroNotaFiscal] NVARCHAR(200) NOT NULL,
    [PercentualRateio] DECIMAL(10,4) NOT NULL,
    [CentroCustoId] UNIQUEIDENTIFIER NULL,
    [FilialId] NVARCHAR(50) NULL,
    [ValorCalculado] DECIMAL(18,2) NOT NULL DEFAULT 0.00,
    [DataEmissao] DATETIME2 NULL,
    [DataRecebimento] DATETIME2 NULL,
    [Observacoes] NVARCHAR(MAX) NULL,
    [FlExcluido] BIT NOT NULL DEFAULT 0,
    [CreatedAt] DATETIME2 NOT NULL DEFAULT GETDATE(),
    [CreatedBy] UNIQUEIDENTIFIER NOT NULL,
    [UpdatedAt] DATETIME2 NULL,
    [UpdatedBy] UNIQUEIDENTIFIER NULL,

    -- Primary Key
    CONSTRAINT [PK_NotasFiscaisFaturas] PRIMARY KEY CLUSTERED ([Id] ASC),

    -- Foreign Keys
    CONSTRAINT [FK_NotasFiscaisFaturas_Conglomerado]
        FOREIGN KEY ([ConglomeradoId]) REFERENCES [dbo].[Conglomerados]([Id]),
    CONSTRAINT [FK_NotasFiscaisFaturas_Fatura]
        FOREIGN KEY ([FaturaId]) REFERENCES [dbo].[Faturas]([Id]),
    CONSTRAINT [FK_NotasFiscaisFaturas_CentroCusto]
        FOREIGN KEY ([CentroCustoId]) REFERENCES [dbo].[CentrosCusto]([Id]),
    CONSTRAINT [FK_NotasFiscaisFaturas_Filial]
        FOREIGN KEY ([FilialId]) REFERENCES [dbo].[Filiais]([Id]),
    CONSTRAINT [FK_NotasFiscaisFaturas_CreatedBy]
        FOREIGN KEY ([CreatedBy]) REFERENCES [dbo].[Users]([Id]),
    CONSTRAINT [FK_NotasFiscaisFaturas_UpdatedBy]
        FOREIGN KEY ([UpdatedBy]) REFERENCES [dbo].[Users]([Id]),

    -- Check Constraints
    CONSTRAINT [CK_NotasFiscaisFaturas_PercentualRateio]
        CHECK ([PercentualRateio] > 0 AND [PercentualRateio] <= 100),
    CONSTRAINT [CK_NotasFiscaisFaturas_ValorCalculado]
        CHECK ([ValorCalculado] >= 0),
    CONSTRAINT [CK_NotasFiscaisFaturas_DataRecebimento]
        CHECK ([DataRecebimento] IS NULL OR [DataRecebimento] >= [DataEmissao])
);
GO

-- Índices
CREATE NONCLUSTERED INDEX [IX_NotasFiscaisFaturas_ConglomeradoId]
    ON [dbo].[NotasFiscaisFaturas]([ConglomeradoId])
    WHERE [FlExcluido] = 0;
GO

CREATE NONCLUSTERED INDEX [IX_NotasFiscaisFaturas_FaturaId]
    ON [dbo].[NotasFiscaisFaturas]([FaturaId])
    INCLUDE ([NumeroNotaFiscal], [PercentualRateio], [ValorCalculado])
    WHERE [FlExcluido] = 0;
GO

CREATE UNIQUE NONCLUSTERED INDEX [UQ_NotasFiscaisFaturas_NumeroNF]
    ON [dbo].[NotasFiscaisFaturas]([ConglomeradoId], [NumeroNotaFiscal])
    WHERE [FlExcluido] = 0;
GO

CREATE NONCLUSTERED INDEX [IX_NotasFiscaisFaturas_CentroCustoId]
    ON [dbo].[NotasFiscaisFaturas]([CentroCustoId])
    WHERE [FlExcluido] = 0 AND [CentroCustoId] IS NOT NULL;
GO

CREATE NONCLUSTERED INDEX [IX_NotasFiscaisFaturas_FilialId]
    ON [dbo].[NotasFiscaisFaturas]([FilialId])
    WHERE [FlExcluido] = 0 AND [FilialId] IS NOT NULL;
GO

CREATE NONCLUSTERED INDEX [IX_NotasFiscaisFaturas_DataEmissao]
    ON [dbo].[NotasFiscaisFaturas]([DataEmissao] DESC)
    WHERE [FlExcluido] = 0 AND [DataEmissao] IS NOT NULL;
GO

-- Comentários
EXEC sys.sp_addextendedproperty
    @name=N'MS_Description',
    @value=N'Notas fiscais vinculadas a faturas com percentual de rateio',
    @level0type=N'SCHEMA', @level0name=N'dbo',
    @level1type=N'TABLE',  @level1name=N'NotasFiscaisFaturas';
GO

EXEC sys.sp_addextendedproperty
    @name=N'MS_Description',
    @value=N'Número da nota fiscal (único por conglomerado)',
    @level0type=N'SCHEMA', @level0name=N'dbo',
    @level1type=N'TABLE',  @level1name=N'NotasFiscaisFaturas',
    @level2type=N'COLUMN', @level2name=N'NumeroNotaFiscal';
GO

EXEC sys.sp_addextendedproperty
    @name=N'MS_Description',
    @value=N'Percentual de rateio (0.0001 a 100.0000). Soma por fatura deve ser 100%',
    @level0type=N'SCHEMA', @level0name=N'dbo',
    @level1type=N'TABLE',  @level1name=N'NotasFiscaisFaturas',
    @level2type=N'COLUMN', @level2name=N'PercentualRateio';
GO


-- ---------------------------------------------
-- Tabela: NotasFiscaisFaturasHistory
-- ---------------------------------------------
CREATE TABLE [dbo].[NotasFiscaisFaturasHistory] (
    [Id] UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    [NotaFiscalFaturaId] UNIQUEIDENTIFIER NOT NULL,
    [ConglomeradoId] UNIQUEIDENTIFIER NOT NULL,
    [Operation] NVARCHAR(20) NOT NULL,
    [OldValues] NVARCHAR(MAX) NULL,
    [NewValues] NVARCHAR(MAX) NULL,
    [ChangedBy] UNIQUEIDENTIFIER NOT NULL,
    [ChangedAt] DATETIME2 NOT NULL DEFAULT GETDATE(),
    [IPAddress] NVARCHAR(50) NULL,
    [UserAgent] NVARCHAR(500) NULL,

    -- Primary Key
    CONSTRAINT [PK_NotasFiscaisFaturasHistory] PRIMARY KEY CLUSTERED ([Id] ASC),

    -- Foreign Keys
    CONSTRAINT [FK_NotasFiscaisFaturasHistory_NotaFiscalFatura]
        FOREIGN KEY ([NotaFiscalFaturaId]) REFERENCES [dbo].[NotasFiscaisFaturas]([Id]),
    CONSTRAINT [FK_NotasFiscaisFaturasHistory_Conglomerado]
        FOREIGN KEY ([ConglomeradoId]) REFERENCES [dbo].[Conglomerados]([Id]),
    CONSTRAINT [FK_NotasFiscaisFaturasHistory_ChangedBy]
        FOREIGN KEY ([ChangedBy]) REFERENCES [dbo].[Users]([Id])
);
GO

-- Índices
CREATE NONCLUSTERED INDEX [IX_NotasFiscaisFaturasHistory_NotaFiscalFaturaId]
    ON [dbo].[NotasFiscaisFaturasHistory]([NotaFiscalFaturaId])
    INCLUDE ([Operation], [ChangedAt], [ChangedBy]);
GO

CREATE NONCLUSTERED INDEX [IX_NotasFiscaisFaturasHistory_ConglomeradoId]
    ON [dbo].[NotasFiscaisFaturasHistory]([ConglomeradoId]);
GO

CREATE NONCLUSTERED INDEX [IX_NotasFiscaisFaturasHistory_ChangedAt]
    ON [dbo].[NotasFiscaisFaturasHistory]([ChangedAt] DESC);
GO

CREATE NONCLUSTERED INDEX [IX_NotasFiscaisFaturasHistory_ChangedBy]
    ON [dbo].[NotasFiscaisFaturasHistory]([ChangedBy]);
GO

-- Comentários
EXEC sys.sp_addextendedproperty
    @name=N'MS_Description',
    @value=N'Histórico de alterações em notas fiscais (retenção 7 anos LGPD)',
    @level0type=N'SCHEMA', @level0name=N'dbo',
    @level1type=N'TABLE',  @level1name=N'NotasFiscaisFaturasHistory';
GO
```

---

## 5. Triggers de Auditoria

```sql
-- =============================================
-- Trigger: Auditoria de INSERT
-- =============================================
CREATE TRIGGER [dbo].[TRG_NotasFiscaisFaturas_AfterInsert]
ON [dbo].[NotasFiscaisFaturas]
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO [dbo].[NotasFiscaisFaturasHistory]
        ([NotaFiscalFaturaId], [ConglomeradoId], [Operation], [NewValues], [ChangedBy], [ChangedAt])
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
CREATE TRIGGER [dbo].[TRG_NotasFiscaisFaturas_AfterUpdate]
ON [dbo].[NotasFiscaisFaturas]
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO [dbo].[NotasFiscaisFaturasHistory]
        ([NotaFiscalFaturaId], [ConglomeradoId], [Operation], [OldValues], [NewValues], [ChangedBy], [ChangedAt])
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

-- =============================================
-- Trigger: Auditoria de DELETE (Soft Delete)
-- =============================================
CREATE TRIGGER [dbo].[TRG_NotasFiscaisFaturas_AfterDelete]
ON [dbo].[NotasFiscaisFaturas]
INSTEAD OF DELETE
AS
BEGIN
    SET NOCOUNT ON;

    UPDATE nf
    SET
        nf.[FlExcluido] = 1,
        nf.[UpdatedAt] = GETDATE(),
        nf.[UpdatedBy] = CAST(CONTEXT_INFO() AS UNIQUEIDENTIFIER) -- Usuário atual via CONTEXT_INFO
    FROM [dbo].[NotasFiscaisFaturas] nf
    INNER JOIN DELETED d ON nf.[Id] = d.[Id];

    INSERT INTO [dbo].[NotasFiscaisFaturasHistory]
        ([NotaFiscalFaturaId], [ConglomeradoId], [Operation], [OldValues], [ChangedBy], [ChangedAt])
    SELECT
        d.[Id],
        d.[ConglomeradoId],
        'DELETE',
        (SELECT * FROM DELETED d2 WHERE d2.Id = d.Id FOR JSON PATH, WITHOUT_ARRAY_WRAPPER),
        CAST(CONTEXT_INFO() AS UNIQUEIDENTIFIER),
        GETDATE()
    FROM DELETED d;
END;
GO
```

---

## 6. Views Úteis

```sql
-- =============================================
-- View: NotasFiscaisFaturas com Dados Denormalizados
-- =============================================
CREATE VIEW [dbo].[vw_NotasFiscaisFaturas_Detalhada]
AS
SELECT
    nf.[Id],
    nf.[ConglomeradoId],
    c.[Nome] AS ConglomeradoNome,
    nf.[FaturaId],
    f.[NumeroFatura],
    f.[ValorTotal] AS FaturaValorTotal,
    nf.[NumeroNotaFiscal],
    nf.[PercentualRateio],
    nf.[ValorCalculado],
    nf.[CentroCustoId],
    cc.[Nome] AS CentroCustoNome,
    cc.[Codigo] AS CentroCustoCodigo,
    nf.[FilialId],
    fil.[Nome] AS FilialNome,
    fil.[CNPJ] AS FilialCNPJ,
    nf.[DataEmissao],
    nf.[DataRecebimento],
    nf.[Observacoes],
    nf.[CreatedAt],
    u_created.[Nome] AS CriadoPor,
    nf.[UpdatedAt],
    u_updated.[Nome] AS AtualizadoPor
FROM [dbo].[NotasFiscaisFaturas] nf
INNER JOIN [dbo].[Conglomerados] c ON nf.[ConglomeradoId] = c.[Id]
INNER JOIN [dbo].[Faturas] f ON nf.[FaturaId] = f.[Id]
LEFT JOIN [dbo].[CentrosCusto] cc ON nf.[CentroCustoId] = cc.[Id]
LEFT JOIN [dbo].[Filiais] fil ON nf.[FilialId] = fil.[Id]
INNER JOIN [dbo].[Users] u_created ON nf.[CreatedBy] = u_created.[Id]
LEFT JOIN [dbo].[Users] u_updated ON nf.[UpdatedBy] = u_updated.[Id]
WHERE nf.[FlExcluido] = 0;
GO

-- =============================================
-- View: Validação de Soma de Percentuais por Fatura
-- =============================================
CREATE VIEW [dbo].[vw_NotasFiscaisFaturas_SomaPercentuais]
AS
SELECT
    nf.[FaturaId],
    f.[NumeroFatura],
    SUM(nf.[PercentualRateio]) AS SomaPercentuais,
    COUNT(*) AS QtdNotasFiscais,
    CASE
        WHEN SUM(nf.[PercentualRateio]) = 100.0000 THEN 'OK'
        WHEN SUM(nf.[PercentualRateio]) > 100.0000 THEN 'EXCEDEU'
        WHEN SUM(nf.[PercentualRateio]) < 100.0000 THEN 'INCOMPLETO'
    END AS StatusRateio
FROM [dbo].[NotasFiscaisFaturas] nf
INNER JOIN [dbo].[Faturas] f ON nf.[FaturaId] = f.[Id]
WHERE nf.[FlExcluido] = 0
GROUP BY nf.[FaturaId], f.[NumeroFatura];
GO
```

---

## 7. Stored Procedures

```sql
-- =============================================
-- SP: Recalcular Valores de Notas Fiscais de uma Fatura
-- =============================================
CREATE PROCEDURE [dbo].[sp_RecalcularValoresNotasFiscais]
    @FaturaId UNIQUEIDENTIFIER
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @ValorTotalFatura DECIMAL(18,2);

    SELECT @ValorTotalFatura = [ValorTotal]
    FROM [dbo].[Faturas]
    WHERE [Id] = @FaturaId;

    UPDATE nf
    SET
        nf.[ValorCalculado] = (@ValorTotalFatura * nf.[PercentualRateio]) / 100.0,
        nf.[UpdatedAt] = GETDATE()
    FROM [dbo].[NotasFiscaisFaturas] nf
    WHERE nf.[FaturaId] = @FaturaId
      AND nf.[FlExcluido] = 0;

    SELECT
        nf.[Id],
        nf.[NumeroNotaFiscal],
        nf.[PercentualRateio],
        nf.[ValorCalculado],
        @ValorTotalFatura AS ValorTotalFatura
    FROM [dbo].[NotasFiscaisFaturas] nf
    WHERE nf.[FaturaId] = @FaturaId
      AND nf.[FlExcluido] = 0;
END;
GO

-- =============================================
-- SP: Validar Soma de Percentuais de uma Fatura
-- =============================================
CREATE PROCEDURE [dbo].[sp_ValidarSomaPercentuaisFatura]
    @FaturaId UNIQUEIDENTIFIER,
    @SomaPercentuais DECIMAL(10,4) OUTPUT,
    @StatusRateio NVARCHAR(50) OUTPUT
AS
BEGIN
    SET NOCOUNT ON;

    SELECT @SomaPercentuais = SUM([PercentualRateio])
    FROM [dbo].[NotasFiscaisFaturas]
    WHERE [FaturaId] = @FaturaId
      AND [FlExcluido] = 0;

    SET @SomaPercentuais = ISNULL(@SomaPercentuais, 0);

    SET @StatusRateio = CASE
        WHEN @SomaPercentuais = 100.0000 THEN 'OK'
        WHEN @SomaPercentuais > 100.0000 THEN 'EXCEDEU'
        WHEN @SomaPercentuais < 100.0000 THEN 'INCOMPLETO'
        ELSE 'ERRO'
    END;

    SELECT @SomaPercentuais AS SomaPercentuais, @StatusRateio AS StatusRateio;
END;
GO
```

---

## 8. Dados Iniciais (Seed)

Nenhum dado inicial necessário. Notas fiscais são criadas sob demanda pelos usuários.

---

## 9. Observações

### Decisões de Modelagem

1. **Percentual com 4 casas decimais**: Permite rateios precisos (ex: 33.3333% para 3 centros de custo iguais).

2. **ValorCalculado armazenado**: Evita recálculos constantes, mas deve ser atualizado via SP quando valor da fatura mudar.

3. **CentroCustoId e FilialId opcionais**: Permite notas fiscais sem rateio específico.

4. **NumeroNotaFiscal único por conglomerado**: Evita duplicação fiscal dentro do mesmo tenant.

5. **Histórico completo em tabela separada**: Auditoria de 7 anos (LGPD) sem impactar performance da tabela principal.

6. **Triggers para auditoria automática**: Garante que nenhuma alteração passe sem registro.

### Considerações de Performance

- Índice filtrado em `FlExcluido = 0` melhora queries de listagem.
- Índice composto único (ConglomeradoId, NumeroNotaFiscal) garante unicidade sem full table scan.
- View `vw_NotasFiscaisFaturas_Detalhada` facilita relatórios, mas evite em queries de alta frequência.
- SP `sp_RecalcularValoresNotasFiscais` deve ser executado quando valor da fatura mudar.

### Migração de Dados do Legado

```sql
-- Script de migração da tabela legada Nota_Fiscal_Fatura
INSERT INTO [dbo].[NotasFiscaisFaturas]
    ([Id], [ConglomeradoId], [FaturaId], [NumeroNotaFiscal], [PercentualRateio],
     [CentroCustoId], [FilialId], [ValorCalculado], [FlExcluido],
     [CreatedAt], [CreatedBy])
SELECT
    NEWID(),
    @ConglomeradoId, -- Definir conglomerado padrão
    f.[Id], -- Mapear Id_Fatura legado para novo GUID
    nfl.[Nr_Nota_Fiscal],
    nfl.[Pct_Nota_Fiscal],
    cc.[Id], -- Mapear Id_Centro_Custo legado
    fil.[Id], -- Mapear id_Filial legado
    0.00, -- Recalcular depois
    0,
    GETDATE(),
    @UsuarioMigracao -- Usuário do sistema de migração
FROM [dbo_legacy].[Nota_Fiscal_Fatura] nfl
INNER JOIN [dbo].[Faturas] f ON f.[NumeroFaturaLegado] = nfl.[Id_Fatura]
LEFT JOIN [dbo].[CentrosCusto] cc ON cc.[CodigoLegado] = nfl.[Id_Centro_Custo]
LEFT JOIN [dbo].[Filiais] fil ON fil.[CodigoLegado] = nfl.[id_Filial];

-- Recalcular valores após migração
EXEC sp_MSforeachtable 'UPDATE nf SET nf.ValorCalculado = (f.ValorTotal * nf.PercentualRateio) / 100.0 FROM NotasFiscaisFaturas nf INNER JOIN Faturas f ON nf.FaturaId = f.Id';
```

---

## Histórico de Alterações

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 1.0 | 2025-12-18 | Architect Agent | Versão inicial - 2 tabelas, 14 índices, 3 triggers, 2 views, 2 SPs |
