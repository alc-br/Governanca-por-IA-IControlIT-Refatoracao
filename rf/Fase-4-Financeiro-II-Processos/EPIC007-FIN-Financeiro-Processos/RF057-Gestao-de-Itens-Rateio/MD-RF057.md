# Modelo de Dados - RF057 - Gestão de Itens de Rateio

**Versão:** 1.0 | **Data:** 2025-12-18 | **RF:** [RF057](./RF057.md) | **Banco:** SQL Server

## 1. Diagrama ER

```
Cliente (1) ───< (N) ItemRateio (1) ───< (N) AlocacaoItem
                                   │
                                   ├───< (N) HistoricoAlocacao
                                   ├───< (N) TransferenciaItem
                                   ├───< (N) CustoItem
                                   ├───< (N) AjusteItem
                                   └───< (N) AlertaItem

GrupoItens (1) ───< (N) ItemRateio
ExcecaoRateio ───> ItemRateio (1:1)
```

## 2. Tabelas

### 2.1 ItemRateio

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | PK |
| Numero | VARCHAR(50) | NÃO | - | Número do item (linha móvel, ID licença, etc) |
| Categoria | VARCHAR(50) | NÃO | - | LINHA_MOBILE, LICENCA_SOFTWARE, LINK_DADOS, EQUIPAMENTO |
| Tipo | VARCHAR(30) | NÃO | - | DEDICADO, COMPARTILHADO |
| Descricao | NVARCHAR(200) | SIM | NULL | Descrição do item |
| CustoMensal | DECIMAL(18,2) | NÃO | 0 | Custo mensal padrão |
| Status | VARCHAR(30) | NÃO | 'ATIVO' | ATIVO, INATIVO, CANCELADO, SUSPENSO |
| GrupoId | UNIQUEIDENTIFIER | SIM | NULL | FK GrupoItens (opcional) |
| DataAtivacao | DATE | NÃO | - | Data de ativação do item |
| DataCancelamento | DATE | SIM | NULL | Data de cancelamento |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK Cliente |
| Ativo | BIT | NÃO | 1 | Soft delete: false=ativo, true=excluído |
| CreatedAt/By/ModifiedAt/By | - | - | - | Auditoria |

**Índices:**
- PK_ItemRateio (Id)
- UK_ItemRateio_Numero (ClienteId, Numero)
- IX_ItemRateio_Categoria (Categoria, Status)
- IX_ItemRateio_Grupo (GrupoId) WHERE GrupoId IS NOT NULL

**Constraints:**
- CK_ItemRateio_Categoria: CHECK (Categoria IN ('LINHA_MOBILE', 'LICENCA_SOFTWARE', 'LINK_DADOS', 'EQUIPAMENTO'))
- CK_ItemRateio_Tipo: CHECK (Tipo IN ('DEDICADO', 'COMPARTILHADO'))
- CK_ItemRateio_Status: CHECK (Status IN ('ATIVO', 'INATIVO', 'CANCELADO', 'SUSPENSO'))

### 2.2 AlocacaoItem

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | PK |
| ItemId | UNIQUEIDENTIFIER | NÃO | - | FK ItemRateio |
| CentroCusto | VARCHAR(20) | NÃO | - | Centro de custo |
| NomeCentroCusto | NVARCHAR(100) | NÃO | - | Nome descritivo |
| Percentual | DECIMAL(5,2) | NÃO | 100.00 | Percentual alocado (0-100) |
| DataInicio | DATE | NÃO | - | Início da alocação |
| DataFim | DATE | SIM | NULL | Fim (NULL = permanente) |
| Ativa | BIT | NÃO | 1 | Alocação ativa |

**Índices:**
- PK_AlocacaoItem (Id)
- IX_AlocacaoItem_Item (ItemId, Ativa) WHERE Ativa=1
- IX_AlocacaoItem_CentroCusto (CentroCusto)
- IX_AlocacaoItem_Vigencia (DataInicio, DataFim)

**Constraints:**
- CK_AlocacaoItem_Percentual: CHECK (Percentual > 0 AND Percentual <= 100)

### 2.3 GrupoItens

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | PK |
| Codigo | VARCHAR(50) | NÃO | - | Código único |
| Nome | NVARCHAR(100) | NÃO | - | Nome do grupo |
| Descricao | NVARCHAR(500) | SIM | NULL | Descrição |
| RegraRateioId | UNIQUEIDENTIFIER | SIM | NULL | FK RegraRateio (opcional) |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK Cliente |
| Ativo | BIT | NÃO | 1 | Soft delete: false=ativo, true=excluído |
| CreatedAt/By/ModifiedAt/By | - | - | - | Auditoria |

**Índices:**
- PK_GrupoItens (Id)
- UK_GrupoItens_Codigo (ClienteId, Codigo)

### 2.4 HistoricoAlocacao

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | PK |
| ItemId | UNIQUEIDENTIFIER | NÃO | - | FK ItemRateio |
| CentroCusto | VARCHAR(20) | NÃO | - | Centro de custo |
| Percentual | DECIMAL(5,2) | NÃO | - | Percentual histórico |
| DataInicio | DATE | NÃO | - | Início vigência |
| DataFim | DATE | NÃO | - | Fim vigência |
| UsuarioAlteracaoId | UNIQUEIDENTIFIER | NÃO | - | Quem alterou |
| DataArquivamento | DATETIME2(7) | NÃO | SYSUTCDATETIME() | Data do arquivamento |

**Índices:**
- PK_HistoricoAlocacao (Id)
- IX_HistoricoAlocacao_Item (ItemId, DataFim DESC)

### 2.5 TransferenciaItem

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | PK |
| ItemId | UNIQUEIDENTIFIER | NÃO | - | FK ItemRateio |
| CentroCustoOrigem | VARCHAR(20) | NÃO | - | CC origem |
| CentroCustoDestino | VARCHAR(20) | NÃO | - | CC destino |
| Motivo | NVARCHAR(500) | NÃO | - | Motivo da transferência |
| DataTransferencia | DATETIME2(7) | NÃO | SYSUTCDATETIME() | Timestamp |
| UsuarioId | UNIQUEIDENTIFIER | NÃO | - | Quem transferiu |

**Índices:**
- PK_TransferenciaItem (Id)
- IX_TransferenciaItem_Item (ItemId, DataTransferencia DESC)

### 2.6 CustoItem

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | PK |
| ItemId | UNIQUEIDENTIFIER | NÃO | - | FK ItemRateio |
| Periodo | DATE | NÃO | - | Competência (mês/ano) |
| CustoFixo | DECIMAL(18,2) | NÃO | 0 | Franquia mensal |
| CustoVariavel | DECIMAL(18,2) | NÃO | 0 | Excedente |
| CustoTotal | AS (CustoFixo + CustoVariavel) PERSISTED | - | - | Total |
| Consumo | DECIMAL(18,2) | SIM | NULL | Consumo medido (minutos, MB, etc) |
| Unidade | VARCHAR(20) | SIM | NULL | MINUTOS, MEGABYTES, LICENCAS |
| FaturaId | UNIQUEIDENTIFIER | SIM | NULL | FK Fatura (origem) |

**Índices:**
- PK_CustoItem (Id)
- UK_CustoItem_Item_Periodo (ItemId, Periodo)
- IX_CustoItem_Periodo (Periodo DESC)

### 2.7 AjusteItem

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | PK |
| ItemId | UNIQUEIDENTIFIER | NÃO | - | FK ItemRateio |
| Periodo | DATE | NÃO | - | Competência |
| Tipo | VARCHAR(30) | NÃO | - | MULTA, CREDITO, DESCONTO, AJUSTE, CORRECAO |
| Valor | DECIMAL(18,2) | NÃO | - | Valor do ajuste |
| Justificativa | NVARCHAR(500) | NÃO | - | Justificativa obrigatória |
| DataAjuste | DATETIME2(7) | NÃO | SYSUTCDATETIME() | Timestamp |
| UsuarioId | UNIQUEIDENTIFIER | NÃO | - | Quem fez o ajuste |

**Índices:**
- PK_AjusteItem (Id)
- IX_AjusteItem_Item (ItemId, Periodo DESC)

**Constraints:**
- CK_AjusteItem_Tipo: CHECK (Tipo IN ('MULTA', 'CREDITO', 'DESCONTO', 'AJUSTE', 'CORRECAO'))

### 2.8 AlertaItem

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | PK |
| ItemId | UNIQUEIDENTIFIER | NÃO | - | FK ItemRateio |
| TipoAlerta | VARCHAR(50) | NÃO | - | SEM_USO_3_MESES, VARIACAO_ANORMAL, CUSTO_ALTO, OUTROS |
| Descricao | NVARCHAR(1000) | NÃO | - | Descrição do alerta |
| Gravidade | VARCHAR(20) | NÃO | 'MEDIA' | BAIXA, MEDIA, ALTA |
| SugestaoAcao | NVARCHAR(200) | SIM | NULL | Ação sugerida (ex: CANCELAR) |
| EconomiaPotencial | DECIMAL(18,2) | SIM | NULL | Economia se ação for tomada |
| DataDeteccao | DATETIME2(7) | NÃO | SYSUTCDATETIME() | Timestamp |
| Status | VARCHAR(30) | NÃO | 'PENDENTE' | PENDENTE, ANALISADO, RESOLVIDO, IGNORADO |
| Resolvido | BIT | NÃO | 0 | Se foi resolvido |
| DataResolucao | DATETIME2(7) | SIM | NULL | Data de resolução |
| ResolvidoPor | UNIQUEIDENTIFIER | SIM | NULL | FK Usuario |

**Índices:**
- PK_AlertaItem (Id)
- IX_AlertaItem_Item (ItemId, DataDeteccao DESC)
- IX_AlertaItem_Pendentes (Status) WHERE Status='PENDENTE'
- IX_AlertaItem_Gravidade (Gravidade, DataDeteccao DESC)

### 2.9 ExcecaoRateio

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | PK |
| ItemId | UNIQUEIDENTIFIER | NÃO | - | FK ItemRateio |
| Motivo | NVARCHAR(500) | NÃO | - | Motivo da exceção |
| ExcluirTotalmente | BIT | NÃO | 0 | Se true, não ratear esse item |
| DataInicio | DATE | SIM | NULL | Início (NULL = imediato) |
| DataFim | DATE | SIM | NULL | Fim (NULL = permanente) |
| UsuarioCriacaoId | UNIQUEIDENTIFIER | NÃO | - | Quem criou |
| DataCriacao | DATETIME2(7) | NÃO | SYSUTCDATETIME() | Timestamp |
| Ativa | BIT | NÃO | 1 | Ativa/Inativa |

**Índices:**
- PK_ExcecaoRateio (Id)
- UK_ExcecaoRateio_Item (ItemId) WHERE Ativa=1
- IX_ExcecaoRateio_Vigencia (DataInicio, DataFim)

## 3. DDL SQL Server

```sql
-- Tabela: ItemRateio
CREATE TABLE ItemRateio (
    Id UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    Numero VARCHAR(50) NOT NULL,
    Categoria VARCHAR(50) NOT NULL,
    Tipo VARCHAR(30) NOT NULL,
    Descricao NVARCHAR(200) NULL,
    CustoMensal DECIMAL(18,2) NOT NULL DEFAULT 0,
    Status VARCHAR(30) NOT NULL DEFAULT 'ATIVO',
    GrupoId UNIQUEIDENTIFIER NULL,
    DataAtivacao DATE NOT NULL,
    DataCancelamento DATE NULL,
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    FlExcluido BIT NOT NULL DEFAULT 0,
    CreatedAt DATETIME2(7) NOT NULL DEFAULT SYSUTCDATETIME(),
    CreatedBy UNIQUEIDENTIFIER NOT NULL,
    ModifiedAt DATETIME2(7) NULL,
    ModifiedBy UNIQUEIDENTIFIER NULL,
    CONSTRAINT PK_ItemRateio PRIMARY KEY CLUSTERED (Id),
    CONSTRAINT FK_ItemRateio_Cliente FOREIGN KEY (ClienteId) REFERENCES Cliente(Id),
    CONSTRAINT FK_ItemRateio_Grupo FOREIGN KEY (GrupoId) REFERENCES GrupoItens(Id),
    CONSTRAINT CK_ItemRateio_Categoria CHECK (Categoria IN ('LINHA_MOBILE', 'LICENCA_SOFTWARE', 'LINK_DADOS', 'EQUIPAMENTO')),
    CONSTRAINT CK_ItemRateio_Tipo CHECK (Tipo IN ('DEDICADO', 'COMPARTILHADO')),
    CONSTRAINT CK_ItemRateio_Status CHECK (Status IN ('ATIVO', 'INATIVO', 'CANCELADO', 'SUSPENSO'))
);
CREATE UNIQUE NONCLUSTERED INDEX UK_ItemRateio_Numero ON ItemRateio(ClienteId, Numero) WHERE FlExcluido = 0;
CREATE NONCLUSTERED INDEX IX_ItemRateio_Categoria ON ItemRateio(Categoria, Status);

-- Tabela: AlocacaoItem
CREATE TABLE AlocacaoItem (
    Id UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    ItemId UNIQUEIDENTIFIER NOT NULL,
    CentroCusto VARCHAR(20) NOT NULL,
    NomeCentroCusto NVARCHAR(100) NOT NULL,
    Percentual DECIMAL(5,2) NOT NULL DEFAULT 100.00,
    DataInicio DATE NOT NULL,
    DataFim DATE NULL,
    Ativa BIT NOT NULL DEFAULT 1,
    CONSTRAINT PK_AlocacaoItem PRIMARY KEY CLUSTERED (Id),
    CONSTRAINT FK_AlocacaoItem_Item FOREIGN KEY (ItemId) REFERENCES ItemRateio(Id) ON DELETE CASCADE,
    CONSTRAINT CK_AlocacaoItem_Percentual CHECK (Percentual > 0 AND Percentual <= 100)
);
CREATE NONCLUSTERED INDEX IX_AlocacaoItem_Item ON AlocacaoItem(ItemId, Ativa) WHERE Ativa=1;

-- Tabela: GrupoItens
CREATE TABLE GrupoItens (
    Id UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    Codigo VARCHAR(50) NOT NULL,
    Nome NVARCHAR(100) NOT NULL,
    Descricao NVARCHAR(500) NULL,
    RegraRateioId UNIQUEIDENTIFIER NULL,
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    FlExcluido BIT NOT NULL DEFAULT 0,
    CreatedAt DATETIME2(7) NOT NULL DEFAULT SYSUTCDATETIME(),
    CreatedBy UNIQUEIDENTIFIER NOT NULL,
    ModifiedAt DATETIME2(7) NULL,
    ModifiedBy UNIQUEIDENTIFIER NULL,
    CONSTRAINT PK_GrupoItens PRIMARY KEY CLUSTERED (Id),
    CONSTRAINT FK_GrupoItens_Cliente FOREIGN KEY (ClienteId) REFERENCES Cliente(Id),
    CONSTRAINT FK_GrupoItens_Regra FOREIGN KEY (RegraRateioId) REFERENCES RegraRateio(Id)
);
CREATE UNIQUE NONCLUSTERED INDEX UK_GrupoItens_Codigo ON GrupoItens(ClienteId, Codigo) WHERE FlExcluido = 0;

-- Tabela: HistoricoAlocacao
CREATE TABLE HistoricoAlocacao (
    Id UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    ItemId UNIQUEIDENTIFIER NOT NULL,
    CentroCusto VARCHAR(20) NOT NULL,
    Percentual DECIMAL(5,2) NOT NULL,
    DataInicio DATE NOT NULL,
    DataFim DATE NOT NULL,
    UsuarioAlteracaoId UNIQUEIDENTIFIER NOT NULL,
    DataArquivamento DATETIME2(7) NOT NULL DEFAULT SYSUTCDATETIME(),
    CONSTRAINT PK_HistoricoAlocacao PRIMARY KEY CLUSTERED (Id),
    CONSTRAINT FK_HistoricoAlocacao_Item FOREIGN KEY (ItemId) REFERENCES ItemRateio(Id),
    CONSTRAINT FK_HistoricoAlocacao_Usuario FOREIGN KEY (UsuarioAlteracaoId) REFERENCES Usuario(Id)
);

-- Tabela: TransferenciaItem
CREATE TABLE TransferenciaItem (
    Id UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    ItemId UNIQUEIDENTIFIER NOT NULL,
    CentroCustoOrigem VARCHAR(20) NOT NULL,
    CentroCustoDestino VARCHAR(20) NOT NULL,
    Motivo NVARCHAR(500) NOT NULL,
    DataTransferencia DATETIME2(7) NOT NULL DEFAULT SYSUTCDATETIME(),
    UsuarioId UNIQUEIDENTIFIER NOT NULL,
    CONSTRAINT PK_TransferenciaItem PRIMARY KEY CLUSTERED (Id),
    CONSTRAINT FK_TransferenciaItem_Item FOREIGN KEY (ItemId) REFERENCES ItemRateio(Id),
    CONSTRAINT FK_TransferenciaItem_Usuario FOREIGN KEY (UsuarioId) REFERENCES Usuario(Id)
);

-- Tabela: CustoItem
CREATE TABLE CustoItem (
    Id UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    ItemId UNIQUEIDENTIFIER NOT NULL,
    Periodo DATE NOT NULL,
    CustoFixo DECIMAL(18,2) NOT NULL DEFAULT 0,
    CustoVariavel DECIMAL(18,2) NOT NULL DEFAULT 0,
    CustoTotal AS (CustoFixo + CustoVariavel) PERSISTED,
    Consumo DECIMAL(18,2) NULL,
    Unidade VARCHAR(20) NULL,
    FaturaId UNIQUEIDENTIFIER NULL,
    CONSTRAINT PK_CustoItem PRIMARY KEY CLUSTERED (Id),
    CONSTRAINT FK_CustoItem_Item FOREIGN KEY (ItemId) REFERENCES ItemRateio(Id),
    CONSTRAINT FK_CustoItem_Fatura FOREIGN KEY (FaturaId) REFERENCES Fatura(Id)
);
CREATE UNIQUE NONCLUSTERED INDEX UK_CustoItem_Item_Periodo ON CustoItem(ItemId, Periodo);

-- Tabela: AjusteItem
CREATE TABLE AjusteItem (
    Id UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    ItemId UNIQUEIDENTIFIER NOT NULL,
    Periodo DATE NOT NULL,
    Tipo VARCHAR(30) NOT NULL,
    Valor DECIMAL(18,2) NOT NULL,
    Justificativa NVARCHAR(500) NOT NULL,
    DataAjuste DATETIME2(7) NOT NULL DEFAULT SYSUTCDATETIME(),
    UsuarioId UNIQUEIDENTIFIER NOT NULL,
    CONSTRAINT PK_AjusteItem PRIMARY KEY CLUSTERED (Id),
    CONSTRAINT FK_AjusteItem_Item FOREIGN KEY (ItemId) REFERENCES ItemRateio(Id),
    CONSTRAINT FK_AjusteItem_Usuario FOREIGN KEY (UsuarioId) REFERENCES Usuario(Id),
    CONSTRAINT CK_AjusteItem_Tipo CHECK (Tipo IN ('MULTA', 'CREDITO', 'DESCONTO', 'AJUSTE', 'CORRECAO'))
);

-- Tabela: AlertaItem
CREATE TABLE AlertaItem (
    Id UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    ItemId UNIQUEIDENTIFIER NOT NULL,
    TipoAlerta VARCHAR(50) NOT NULL,
    Descricao NVARCHAR(1000) NOT NULL,
    Gravidade VARCHAR(20) NOT NULL DEFAULT 'MEDIA',
    SugestaoAcao NVARCHAR(200) NULL,
    EconomiaPotencial DECIMAL(18,2) NULL,
    DataDeteccao DATETIME2(7) NOT NULL DEFAULT SYSUTCDATETIME(),
    Status VARCHAR(30) NOT NULL DEFAULT 'PENDENTE',
    Resolvido BIT NOT NULL DEFAULT 0,
    DataResolucao DATETIME2(7) NULL,
    ResolvidoPor UNIQUEIDENTIFIER NULL,
    CONSTRAINT PK_AlertaItem PRIMARY KEY CLUSTERED (Id),
    CONSTRAINT FK_AlertaItem_Item FOREIGN KEY (ItemId) REFERENCES ItemRateio(Id),
    CONSTRAINT FK_AlertaItem_Resolvido FOREIGN KEY (ResolvidoPor) REFERENCES Usuario(Id),
    CONSTRAINT CK_AlertaItem_Gravidade CHECK (Gravidade IN ('BAIXA', 'MEDIA', 'ALTA'))
);
CREATE NONCLUSTERED INDEX IX_AlertaItem_Pendentes ON AlertaItem(Status) WHERE Status='PENDENTE';

-- Tabela: ExcecaoRateio
CREATE TABLE ExcecaoRateio (
    Id UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    ItemId UNIQUEIDENTIFIER NOT NULL,
    Motivo NVARCHAR(500) NOT NULL,
    ExcluirTotalmente BIT NOT NULL DEFAULT 0,
    DataInicio DATE NULL,
    DataFim DATE NULL,
    UsuarioCriacaoId UNIQUEIDENTIFIER NOT NULL,
    DataCriacao DATETIME2(7) NOT NULL DEFAULT SYSUTCDATETIME(),
    Ativa BIT NOT NULL DEFAULT 1,
    CONSTRAINT PK_ExcecaoRateio PRIMARY KEY CLUSTERED (Id),
    CONSTRAINT FK_ExcecaoRateio_Item FOREIGN KEY (ItemId) REFERENCES ItemRateio(Id),
    CONSTRAINT FK_ExcecaoRateio_Usuario FOREIGN KEY (UsuarioCriacaoId) REFERENCES Usuario(Id)
);
CREATE UNIQUE NONCLUSTERED INDEX UK_ExcecaoRateio_Item ON ExcecaoRateio(ItemId) WHERE Ativa=1;
```

## 4. Stored Procedures

```sql
-- Validar se soma de alocações = 100%
CREATE PROCEDURE sp_ValidarAlocacoesItem
    @ItemId UNIQUEIDENTIFIER,
    @Valido BIT OUTPUT
AS
BEGIN
    DECLARE @Soma DECIMAL(5,2);
    SELECT @Soma = SUM(Percentual) FROM AlocacaoItem WHERE ItemId = @ItemId AND Ativa = 1;
    SET @Valido = CASE WHEN ABS(@Soma - 100.00) < 0.01 THEN 1 ELSE 0 END;
END;
GO

-- Detectar itens sem uso
CREATE PROCEDURE sp_DetectarItensSemUso
    @ClienteId UNIQUEIDENTIFIER,
    @Meses INT = 3
AS
BEGIN
    DECLARE @DataLimite DATE = DATEADD(MONTH, -@Meses, GETDATE());

    INSERT INTO AlertaItem (ItemId, TipoAlerta, Descricao, Gravidade, SugestaoAcao, EconomiaPotencial)
    SELECT
        i.Id,
        'SEM_USO_3_MESES',
        CONCAT('Item ', i.Numero, ' sem uso há ', @Meses, ' meses. Custo mensal: R$ ', CAST(i.CustoMensal AS VARCHAR(20))),
        'ALTA',
        'CANCELAR',
        i.CustoMensal
    FROM ItemRateio i
    WHERE i.ClienteId = @ClienteId
      AND i.Status = 'ATIVO'
      AND NOT EXISTS (
          SELECT 1 FROM CustoItem c
          WHERE c.ItemId = i.Id AND c.Periodo >= @DataLimite AND c.Consumo > 0
      );
END;
GO
```

## 5. Views

```sql
-- Itens com alertas ativos
CREATE VIEW vw_ItensComAlerta
AS
SELECT
    i.Id, i.Numero, i.Categoria, i.CustoMensal,
    a.TipoAlerta, a.Gravidade, a.SugestaoAcao, a.EconomiaPotencial
FROM ItemRateio i
INNER JOIN AlertaItem a ON i.Id = a.ItemId
WHERE a.Status = 'PENDENTE' AND a.Resolvido = 0;
GO

-- Custo total por centro de custo
CREATE VIEW vw_CustoTotalPorCentroCusto
AS
SELECT
    al.CentroCusto,
    al.NomeCentroCusto,
    c.Periodo,
    SUM(c.CustoTotal * (al.Percentual / 100.0)) AS CustoAlocado
FROM AlocacaoItem al
INNER JOIN ItemRateio i ON al.ItemId = i.Id
INNER JOIN CustoItem c ON i.Id = c.ItemId
WHERE al.Ativa = 1 AND i.Ativo = 1
GROUP BY al.CentroCusto, al.NomeCentroCusto, c.Periodo;
GO
```

## Observações

- **Granularidade:** Controle fino de rateio por item individual
- **Flexibilidade:** Suporta rateio dedicado e compartilhado
- **Exceções:** Permite exclusão de itens específicos do rateio
- **Histórico:** Rastreabilidade completa de alocações e transferências
- **Alertas:** Detecção automática de itens sem uso e anomalias
- **Grupos:** Permite agrupar itens para aplicação de regras em lote
- **Performance:** Índices otimizados para consultas por período e centro de custo

**Total de tabelas:** 9 | **Índices:** 25+ | **Constraints:** 15+
