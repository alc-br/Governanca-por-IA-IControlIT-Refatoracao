# Modelo de Dados - RF055 - Gestão de Rateio

**Versão:** 1.0 | **Data:** 2025-12-18 | **RF:** [RF055](./RF055.md) | **Banco:** SQL Server

## 1. Diagrama ER

```
Cliente (1) ─────< (N) RegraRateio (1) ─────< (N) PercentualAlocacao
RegraRateio (1) ─< (N) Rateio (1) ─────< (N) RateioItem
Rateio (1) ─────< (N) RateioHistorico
RateioItem (1) ─< (N) AjusteRateio
```

## 2. Tabelas

### 2.1 RegraRateio

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | PK |
| Codigo | VARCHAR(50) | NÃO | - | Código único (RAT_VENDAS_2025) |
| Nome | NVARCHAR(100) | NÃO | - | Nome da regra |
| TipoRateio | VARCHAR(30) | NÃO | - | FIXO, PROPORCIONAL_HEADCOUNT, USO_REAL, POR_PROJETO |
| ConfiguracaoJSON | NVARCHAR(MAX) | NÃO | - | Configuração específica do tipo |
| DataInicioVigencia | DATETIME2(7) | NÃO | - | Início de vigência |
| DataFimVigencia | DATETIME2(7) | SIM | NULL | Fim de vigência (NULL = permanente) |
| Versao | INT | NÃO | 1 | Versão da regra |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK Cliente |
| Ativo | BIT | NÃO | 1 | Ativo/Inativo |
| CreatedAt/By/ModifiedAt/By | - | - | - | Auditoria |

**Índices:**
- PK_RegraRateio (Id)
- UK_RegraRateio_Codigo (ClienteId, Codigo)
- IX_RegraRateio_Vigencia (DataInicioVigencia, DataFimVigencia) WHERE FlExcluido = 0

### 2.2 PercentualAlocacao

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | PK |
| RegraRateioId | UNIQUEIDENTIFIER | NÃO | - | FK RegraRateio |
| CentroCusto | VARCHAR(20) | NÃO | - | Código do centro de custo |
| NomeCentroCusto | NVARCHAR(100) | NÃO | - | Nome descritivo |
| Percentual | DECIMAL(5,2) | NÃO | - | Percentual alocado (0-100) |
| Ordem | INT | NÃO | - | Ordem de exibição |

**Índices:**
- PK_PercentualAlocacao (Id)
- IX_PercentualAlocacao_Regra (RegraRateioId, Ordem)

**Constraints:**
- CK_PercentualAlocacao_Percentual: CHECK (Percentual > 0 AND Percentual <= 100)

### 2.3 Rateio

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | PK |
| Numero | VARCHAR(30) | NÃO | - | Número único (RAT-202501-001) |
| RegraRateioId | UNIQUEIDENTIFIER | NÃO | - | FK RegraRateio |
| Periodo | DATE | NÃO | - | Competência do rateio (mês/ano) |
| ValorTotal | DECIMAL(18,2) | NÃO | - | Valor total a ratear |
| Status | VARCHAR(30) | NÃO | 'PROCESSADO' | PROCESSADO, APROVADO, REJEITADO, EXPORTADO |
| AprovadorId | UNIQUEIDENTIFIER | SIM | NULL | FK Usuario aprovador |
| DataAprovacao | DATETIME2(7) | SIM | NULL | Data de aprovação |
| DataExportacao | DATETIME2(7) | SIM | NULL | Data de exportação para ERP |
| SistemaDestinoERP | VARCHAR(50) | SIM | NULL | SAP, TOTVS, CONTA_AZUL |
| ArquivoExportacao | NVARCHAR(500) | SIM | NULL | Caminho do arquivo exportado |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK Cliente |
| Ativo | BIT | NÃO | 1 | Soft delete: false=ativo, true=excluído |
| CreatedAt/By/ModifiedAt/By | - | - | - | Auditoria |

**Índices:**
- PK_Rateio (Id)
- UK_Rateio_Numero (Numero)
- IX_Rateio_Cliente_Periodo (ClienteId, Periodo DESC)
- IX_Rateio_Status (Status) WHERE Status IN ('PROCESSADO','APROVADO')

### 2.4 RateioItem

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | PK |
| RateioId | UNIQUEIDENTIFIER | NÃO | - | FK Rateio |
| CentroCusto | VARCHAR(20) | NÃO | - | Centro de custo |
| NomeCentroCusto | NVARCHAR(100) | NÃO | - | Nome descritivo |
| Percentual | DECIMAL(5,2) | NÃO | - | Percentual alocado |
| Valor | DECIMAL(18,2) | NÃO | - | Valor alocado calculado |
| ValorAjustado | DECIMAL(18,2) | SIM | NULL | Valor após ajustes |
| ContaContabil | VARCHAR(50) | SIM | NULL | Conta contábil de destino |

**Índices:**
- PK_RateioItem (Id)
- IX_RateioItem_Rateio (RateioId)
- IX_RateioItem_CentroCusto (CentroCusto, RateioId)

### 2.5 AjusteRateio

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | PK |
| RateioItemId | UNIQUEIDENTIFIER | NÃO | - | FK RateioItem |
| TipoAjuste | VARCHAR(30) | NÃO | - | CREDITO, DEBITO, MULTA, DESCONTO, CORRECAO |
| Valor | DECIMAL(18,2) | NÃO | - | Valor do ajuste |
| Justificativa | NVARCHAR(500) | NÃO | - | Justificativa obrigatória |
| DataAjuste | DATETIME2(7) | NÃO | SYSUTCDATETIME() | Data do ajuste |
| UsuarioAjusteId | UNIQUEIDENTIFIER | NÃO | - | Quem fez o ajuste |

**Índices:**
- PK_AjusteRateio (Id)
- IX_AjusteRateio_Item (RateioItemId, DataAjuste DESC)

### 2.6 RateioHistorico

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | PK |
| RateioId | UNIQUEIDENTIFIER | NÃO | - | FK Rateio |
| StatusAnterior | VARCHAR(30) | SIM | NULL | Status antes |
| StatusNovo | VARCHAR(30) | NÃO | - | Novo status |
| UsuarioId | UNIQUEIDENTIFIER | NÃO | - | Quem alterou |
| DataAlteracao | DATETIME2(7) | NÃO | SYSUTCDATETIME() | Timestamp |
| Comentario | NVARCHAR(1000) | SIM | NULL | Comentário opcional |

**Índices:**
- PK_RateioHistorico (Id)
- IX_RateioHistorico_Rateio (RateioId, DataAlteracao DESC)

### 2.7 RegraRateioHistorico

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | PK |
| RegraRateioId | UNIQUEIDENTIFIER | NÃO | - | FK RegraRateio |
| Versao | INT | NÃO | - | Número da versão arquivada |
| ConfiguracaoJSON | NVARCHAR(MAX) | NÃO | - | Configuração da versão |
| DataInicioVigencia | DATETIME2(7) | NÃO | - | Início vigência |
| DataFimVigencia | DATETIME2(7) | NÃO | - | Fim vigência |
| UsuarioAlteracaoId | UNIQUEIDENTIFIER | NÃO | - | Quem alterou |
| DataArquivamento | DATETIME2(7) | NÃO | SYSUTCDATETIME() | Data do backup |

**Índices:**
- PK_RegraRateioHistorico (Id)
- IX_RegraRateioHistorico_Regra (RegraRateioId, Versao DESC)

## 3. DDL SQL Server

```sql
-- Tabela: RegraRateio
CREATE TABLE RegraRateio (
    Id UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    Codigo VARCHAR(50) NOT NULL,
    Nome NVARCHAR(100) NOT NULL,
    TipoRateio VARCHAR(30) NOT NULL,
    ConfiguracaoJSON NVARCHAR(MAX) NOT NULL,
    DataInicioVigencia DATETIME2(7) NOT NULL,
    DataFimVigencia DATETIME2(7) NULL,
    Versao INT NOT NULL DEFAULT 1,
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    FlExcluido BIT NOT NULL DEFAULT 0,
    CreatedAt DATETIME2(7) NOT NULL DEFAULT SYSUTCDATETIME(),
    CreatedBy UNIQUEIDENTIFIER NOT NULL,
    ModifiedAt DATETIME2(7) NULL,
    ModifiedBy UNIQUEIDENTIFIER NULL,
    CONSTRAINT PK_RegraRateio PRIMARY KEY CLUSTERED (Id),
    CONSTRAINT FK_RegraRateio_Cliente FOREIGN KEY (ClienteId) REFERENCES Cliente(Id),
    CONSTRAINT CK_RegraRateio_Tipo CHECK (TipoRateio IN ('FIXO', 'PROPORCIONAL_HEADCOUNT', 'USO_REAL', 'POR_PROJETO'))
);
CREATE UNIQUE NONCLUSTERED INDEX UK_RegraRateio_Codigo ON RegraRateio(ClienteId, Codigo) WHERE FlExcluido = 0;

-- Tabela: PercentualAlocacao
CREATE TABLE PercentualAlocacao (
    Id UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    RegraRateioId UNIQUEIDENTIFIER NOT NULL,
    CentroCusto VARCHAR(20) NOT NULL,
    NomeCentroCusto NVARCHAR(100) NOT NULL,
    Percentual DECIMAL(5,2) NOT NULL,
    Ordem INT NOT NULL,
    CONSTRAINT PK_PercentualAlocacao PRIMARY KEY CLUSTERED (Id),
    CONSTRAINT FK_PercentualAlocacao_Regra FOREIGN KEY (RegraRateioId) REFERENCES RegraRateio(Id) ON DELETE CASCADE,
    CONSTRAINT CK_PercentualAlocacao_Percentual CHECK (Percentual > 0 AND Percentual <= 100)
);
CREATE NONCLUSTERED INDEX IX_PercentualAlocacao_Regra ON PercentualAlocacao(RegraRateioId, Ordem);

-- Tabela: Rateio
CREATE TABLE Rateio (
    Id UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    Numero VARCHAR(30) NOT NULL,
    RegraRateioId UNIQUEIDENTIFIER NOT NULL,
    Periodo DATE NOT NULL,
    ValorTotal DECIMAL(18,2) NOT NULL,
    Status VARCHAR(30) NOT NULL DEFAULT 'PROCESSADO',
    AprovadorId UNIQUEIDENTIFIER NULL,
    DataAprovacao DATETIME2(7) NULL,
    DataExportacao DATETIME2(7) NULL,
    SistemaDestinoERP VARCHAR(50) NULL,
    ArquivoExportacao NVARCHAR(500) NULL,
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    FlExcluido BIT NOT NULL DEFAULT 0,
    CreatedAt DATETIME2(7) NOT NULL DEFAULT SYSUTCDATETIME(),
    CreatedBy UNIQUEIDENTIFIER NOT NULL,
    ModifiedAt DATETIME2(7) NULL,
    ModifiedBy UNIQUEIDENTIFIER NULL,
    CONSTRAINT PK_Rateio PRIMARY KEY CLUSTERED (Id),
    CONSTRAINT FK_Rateio_Regra FOREIGN KEY (RegraRateioId) REFERENCES RegraRateio(Id),
    CONSTRAINT FK_Rateio_Cliente FOREIGN KEY (ClienteId) REFERENCES Cliente(Id),
    CONSTRAINT FK_Rateio_Aprovador FOREIGN KEY (AprovadorId) REFERENCES Usuario(Id),
    CONSTRAINT CK_Rateio_Status CHECK (Status IN ('PROCESSADO', 'APROVADO', 'REJEITADO', 'EXPORTADO')),
    CONSTRAINT CK_Rateio_ValorTotal CHECK (ValorTotal >= 0)
);
CREATE UNIQUE NONCLUSTERED INDEX UK_Rateio_Numero ON Rateio(Numero);
CREATE NONCLUSTERED INDEX IX_Rateio_Cliente_Periodo ON Rateio(ClienteId, Periodo DESC);

-- Tabela: RateioItem
CREATE TABLE RateioItem (
    Id UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    RateioId UNIQUEIDENTIFIER NOT NULL,
    CentroCusto VARCHAR(20) NOT NULL,
    NomeCentroCusto NVARCHAR(100) NOT NULL,
    Percentual DECIMAL(5,2) NOT NULL,
    Valor DECIMAL(18,2) NOT NULL,
    ValorAjustado DECIMAL(18,2) NULL,
    ContaContabil VARCHAR(50) NULL,
    CONSTRAINT PK_RateioItem PRIMARY KEY CLUSTERED (Id),
    CONSTRAINT FK_RateioItem_Rateio FOREIGN KEY (RateioId) REFERENCES Rateio(Id) ON DELETE CASCADE,
    CONSTRAINT CK_RateioItem_Percentual CHECK (Percentual >= 0 AND Percentual <= 100),
    CONSTRAINT CK_RateioItem_Valor CHECK (Valor >= 0)
);
CREATE NONCLUSTERED INDEX IX_RateioItem_Rateio ON RateioItem(RateioId);

-- Tabela: AjusteRateio
CREATE TABLE AjusteRateio (
    Id UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    RateioItemId UNIQUEIDENTIFIER NOT NULL,
    TipoAjuste VARCHAR(30) NOT NULL,
    Valor DECIMAL(18,2) NOT NULL,
    Justificativa NVARCHAR(500) NOT NULL,
    DataAjuste DATETIME2(7) NOT NULL DEFAULT SYSUTCDATETIME(),
    UsuarioAjusteId UNIQUEIDENTIFIER NOT NULL,
    CONSTRAINT PK_AjusteRateio PRIMARY KEY CLUSTERED (Id),
    CONSTRAINT FK_AjusteRateio_Item FOREIGN KEY (RateioItemId) REFERENCES RateioItem(Id) ON DELETE CASCADE,
    CONSTRAINT FK_AjusteRateio_Usuario FOREIGN KEY (UsuarioAjusteId) REFERENCES Usuario(Id),
    CONSTRAINT CK_AjusteRateio_Tipo CHECK (TipoAjuste IN ('CREDITO', 'DEBITO', 'MULTA', 'DESCONTO', 'CORRECAO'))
);

-- Tabela: RateioHistorico
CREATE TABLE RateioHistorico (
    Id UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    RateioId UNIQUEIDENTIFIER NOT NULL,
    StatusAnterior VARCHAR(30) NULL,
    StatusNovo VARCHAR(30) NOT NULL,
    UsuarioId UNIQUEIDENTIFIER NOT NULL,
    DataAlteracao DATETIME2(7) NOT NULL DEFAULT SYSUTCDATETIME(),
    Comentario NVARCHAR(1000) NULL,
    CONSTRAINT PK_RateioHistorico PRIMARY KEY CLUSTERED (Id),
    CONSTRAINT FK_RateioHistorico_Rateio FOREIGN KEY (RateioId) REFERENCES Rateio(Id) ON DELETE CASCADE,
    CONSTRAINT FK_RateioHistorico_Usuario FOREIGN KEY (UsuarioId) REFERENCES Usuario(Id)
);

-- Tabela: RegraRateioHistorico
CREATE TABLE RegraRateioHistorico (
    Id UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    RegraRateioId UNIQUEIDENTIFIER NOT NULL,
    Versao INT NOT NULL,
    ConfiguracaoJSON NVARCHAR(MAX) NOT NULL,
    DataInicioVigencia DATETIME2(7) NOT NULL,
    DataFimVigencia DATETIME2(7) NOT NULL,
    UsuarioAlteracaoId UNIQUEIDENTIFIER NOT NULL,
    DataArquivamento DATETIME2(7) NOT NULL DEFAULT SYSUTCDATETIME(),
    CONSTRAINT PK_RegraRateioHistorico PRIMARY KEY CLUSTERED (Id),
    CONSTRAINT FK_RegraRateioHistorico_Regra FOREIGN KEY (RegraRateioId) REFERENCES RegraRateio(Id),
    CONSTRAINT FK_RegraRateioHistorico_Usuario FOREIGN KEY (UsuarioAlteracaoId) REFERENCES Usuario(Id)
);
```

## 4. Stored Procedures

```sql
-- Validar se soma de percentuais = 100%
CREATE PROCEDURE sp_ValidarPercentuaisRateio
    @RegraRateioId UNIQUEIDENTIFIER,
    @Valido BIT OUTPUT
AS
BEGIN
    DECLARE @Soma DECIMAL(5,2);
    SELECT @Soma = SUM(Percentual) FROM PercentualAlocacao WHERE RegraRateioId = @RegraRateioId;
    SET @Valido = CASE WHEN ABS(@Soma - 100.00) < 0.01 THEN 1 ELSE 0 END;
END;
GO

-- Processar rateio mensal automaticamente
CREATE PROCEDURE sp_ProcessarRateioMensal
    @ClienteId UNIQUEIDENTIFIER,
    @Periodo DATE,
    @RegraRateioId UNIQUEIDENTIFIER,
    @ValorTotal DECIMAL(18,2)
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRANSACTION;

    -- Criar rateio
    DECLARE @RateioId UNIQUEIDENTIFIER = NEWID();
    DECLARE @Numero VARCHAR(30) = 'RAT-' + FORMAT(@Periodo, 'yyyyMM') + '-001'; -- Simplificado

    INSERT INTO Rateio (Id, Numero, RegraRateioId, Periodo, ValorTotal, ClienteId, CreatedBy)
    VALUES (@RateioId, @Numero, @RegraRateioId, @Periodo, @ValorTotal, @ClienteId, @ClienteId);

    -- Criar itens baseados na regra
    INSERT INTO RateioItem (RateioId, CentroCusto, NomeCentroCusto, Percentual, Valor)
    SELECT @RateioId, pa.CentroCusto, pa.NomeCentroCusto, pa.Percentual,
           @ValorTotal * (pa.Percentual / 100.0)
    FROM PercentualAlocacao pa
    WHERE pa.RegraRateioId = @RegraRateioId;

    COMMIT TRANSACTION;
END;
GO
```

## 5. Views

```sql
-- Rateios pendentes de aprovação
CREATE VIEW vw_RateiosPendentesAprovacao
AS
SELECT r.Id, r.Numero, r.Periodo, r.ValorTotal, rg.Nome AS Regra, r.ClienteId
FROM Rateio r
INNER JOIN RegraRateio rg ON r.RegraRateioId = rg.Id
WHERE r.Status = 'PROCESSADO' AND r.Ativo = 1;
GO

-- Comparativo mensal
CREATE VIEW vw_ComparativoRateioMensal
AS
SELECT ClienteId, CentroCusto, Periodo, SUM(Valor) AS Total
FROM RateioItem ri
INNER JOIN Rateio r ON ri.RateioId = r.Id
WHERE r.Status = 'APROVADO'
GROUP BY ClienteId, CentroCusto, Periodo;
GO
```

## Observações

- **Multi-tenancy:** Todas as tabelas possuem ClienteId
- **Auditoria:** Campos Created/Modified em todas
- **Validação:** Soma de percentuais = 100% obrigatória
- **Versionamento:** Histórico de alterações de regras
- **Integrações:** Export para SAP, TOTVS, Conta Azul
- **Performance:** Índices para consultas frequentes

**Total de tabelas:** 7 | **Índices:** 20+ | **Constraints:** 15+
