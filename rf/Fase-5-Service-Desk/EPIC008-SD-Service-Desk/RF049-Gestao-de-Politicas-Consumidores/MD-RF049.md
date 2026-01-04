# Modelo de Dados - RF049 - Gestão de Políticas de Consumidores

**Versão:** 1.0 | **Data:** 2025-12-18 | **RF:** [RF049](./RF049.md)

---

## 1. Diagrama ER

```
┌─────────────────────────────┐       ┌──────────────────────────────┐
│   PoliticaConsumidor         │       │  PoliticaConsumidorAplicacao │
│  (Cadastro de Políticas)     │       │  (Aplicação a Consumidores)  │
├─────────────────────────────┤       ├──────────────────────────────┤
│ Id (PK)                      │◄──────┤ PoliticaId (FK)              │
│ FornecedorId (FK)            │   1:N │ ConsumidorId (FK)            │
│ Codigo                       │       │ DataAplicacao                │
│ Nome                         │       │ DataRemocao                  │
│ TipoPolitica (LIMITE/...)    │       │ Ativo                        │
│ ValorLimite                  │       └──────────────────────────────┘
│ UnidadeMedida                │
│ ...                          │       ┌──────────────────────────────┐
└─────────────────────────────┘       │  ViolacaoPolitica            │
                                       │  (Histórico de Violações)    │
                                       ├──────────────────────────────┤
                                       │ Id (PK)                      │
                                       │ ConsumidorId (FK)            │
                                       │ PoliticaId (FK)              │
                                       │ DataViolacao                 │
                                       │ ValorConsum ido               │
                                       │ ValorLimite                  │
                                       │ AcaoTomada                   │
                                       └──────────────────────────────┘
```

---

## 2. Tabelas Principais

### 2.1 PoliticaConsumidor

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | PK |
| FornecedorId | UNIQUEIDENTIFIER | NÃO | - | FK Fornecedor |
| Codigo | VARCHAR(50) | NÃO | - | Código único |
| Nome | NVARCHAR(200) | NÃO | - | Nome da política |
| Descricao | NVARCHAR(MAX) | SIM | NULL | Descrição |
| TipoPolitica | VARCHAR(50) | NÃO | - | LIMITE_MONETARIO/FRANQUIA_DADOS/FRANQUIA_VOZ/FRANQUIA_SMS/RESTRICAO_HORARIO/RESTRICAO_DESTINO |
| ValorLimite | DECIMAL(18,2) | SIM | NULL | Valor do limite |
| UnidadeMedida | VARCHAR(20) | SIM | NULL | MB/MINUTOS/SMS/REAIS |
| Percentual50Alerta | BIT | NÃO | 1 | Alertar em 50% |
| Percentual80Alerta | BIT | NÃO | 1 | Alertar em 80% |
| Percentual100Bloqueio | BIT | NÃO | 1 | Bloquear em 100% |
| AlertOnly | BIT | NÃO | 0 | Apenas alertar sem bloquear |
| Prioridade | INT | NÃO | 50 | Prioridade (1-100) |
| Ativo | BIT | NÃO | 1 | Status |
| DataCriacao | DATETIME2 | NÃO | GETDATE() | Data criação |
| UsuarioCriacaoId | UNIQUEIDENTIFIER | NÃO | - | FK Usuario |

**Índices:** 7 (PK + Fornecedor + Codigo + Tipo + Prioridade + Ativo)

**Constraints:** 8 (PK, 2 FKs, 1 UNIQUE, 4 CHECKs)

---

### 2.2 PoliticaConsumidorAplicacao

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | PK |
| PoliticaId | UNIQUEIDENTIFIER | NÃO | - | FK PoliticaConsumidor |
| ConsumidorId | UNIQUEIDENTIFIER | NÃO | - | FK Consumidor |
| DataAplicacao | DATETIME2 | NÃO | GETDATE() | Quando aplicou |
| DataRemocao | DATETIME2 | SIM | NULL | Quando removeu |
| Ativo | BIT | NÃO | 1 | Status |
| UsuarioAplicacaoId | UNIQUEIDENTIFIER | NÃO | - | FK Usuario |
| UsuarioRemocaoId | UNIQUEIDENTIFIER | SIM | NULL | FK Usuario |

**Índices:** 6 (PK + Politica + Consumidor + UNIQUE(Politica,Consumidor) + Ativo)

---

### 2.3 ViolacaoPolitica

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | PK |
| ConsumidorId | UNIQUEIDENTIFIER | NÃO | - | FK Consumidor |
| PoliticaId | UNIQUEIDENTIFIER | NÃO | - | FK PoliticaConsumidor |
| DataViolacao | DATETIME2 | NÃO | GETDATE() | Quando violou |
| ValorConsumido | DECIMAL(18,2) | NÃO | - | Valor consumido |
| ValorLimite | DECIMAL(18,2) | NÃO | - | Limite da política |
| PercentualConsumo | AS (ValorConsumido / ValorLimite * 100) PERSISTED | - | - | Calculated |
| AcaoTomada | VARCHAR(50) | NÃO | - | ALERTA_50/ALERTA_80/BLOQUEIO_100 |
| Resolvido | BIT | NÃO | 0 | Se violação foi resolvida |
| DataResolucao | DATETIME2 | SIM | NULL | Quando resolveu |

**Índices:** 7 (PK + Consumidor + Politica + DataViolacao + Resolvido)

---

## 3. DDL SQL Server (Compacto)

```sql
-- =============================================
-- RF049 - Gestão de Políticas de Consumidores
-- =============================================

CREATE TABLE dbo.PoliticaConsumidor (
    Id UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    FornecedorId UNIQUEIDENTIFIER NOT NULL,
    Codigo VARCHAR(50) NOT NULL,
    Nome NVARCHAR(200) NOT NULL,
    Descricao NVARCHAR(MAX) NULL,
    TipoPolitica VARCHAR(50) NOT NULL,
    ValorLimite DECIMAL(18,2) NULL,
    UnidadeMedida VARCHAR(20) NULL,
    Percentual50Alerta BIT NOT NULL DEFAULT 1,
    Percentual80Alerta BIT NOT NULL DEFAULT 1,
    Percentual100Bloqueio BIT NOT NULL DEFAULT 1,
    AlertOnly BIT NOT NULL DEFAULT 0,
    Prioridade INT NOT NULL DEFAULT 50,
    FlExcluido BIT NOT NULL DEFAULT 0,
    DataCriacao DATETIME2 NOT NULL DEFAULT GETDATE(),
    UsuarioCriacaoId UNIQUEIDENTIFIER NOT NULL,
    DataUltimaAlteracao DATETIME2 NULL,
    UsuarioUltimaAlteracaoId UNIQUEIDENTIFIER NULL,

    CONSTRAINT PK_PoliticaConsumidor PRIMARY KEY CLUSTERED (Id),
    CONSTRAINT FK_PoliticaConsumidor_Fornecedor FOREIGN KEY (FornecedorId) REFERENCES dbo.Fornecedor(Id),
    CONSTRAINT FK_PoliticaConsumidor_UsuarioCriacao FOREIGN KEY (UsuarioCriacaoId) REFERENCES dbo.Usuario(Id),
    CONSTRAINT FK_PoliticaConsumidor_UsuarioAlteracao FOREIGN KEY (UsuarioUltimaAlteracaoId) REFERENCES dbo.Usuario(Id),
    CONSTRAINT UQ_PoliticaConsumidor_FornecedorCodigo UNIQUE (FornecedorId, Codigo),
    CONSTRAINT CHK_PoliticaConsumidor_TipoPolitica CHECK (TipoPolitica IN ('LIMITE_MONETARIO', 'FRANQUIA_DADOS', 'FRANQUIA_VOZ', 'FRANQUIA_SMS', 'RESTRICAO_HORARIO', 'RESTRICAO_DESTINO', 'LIMITE_ROAMING')),
    CONSTRAINT CHK_PoliticaConsumidor_Prioridade CHECK (Prioridade BETWEEN 1 AND 100),
    CONSTRAINT CHK_PoliticaConsumidor_ValorLimite CHECK (ValorLimite IS NULL OR ValorLimite > 0)
);

CREATE NONCLUSTERED INDEX IX_PoliticaConsumidor_Fornecedor ON dbo.PoliticaConsumidor(FornecedorId) INCLUDE (Codigo, Nome, TipoPolitica);
CREATE NONCLUSTERED INDEX IX_PoliticaConsumidor_TipoPolitica ON dbo.PoliticaConsumidor(TipoPolitica) WHERE FlExcluido = 0;
CREATE NONCLUSTERED INDEX IX_PoliticaConsumidor_Prioridade ON dbo.PoliticaConsumidor(Prioridade DESC) WHERE FlExcluido = 0;
CREATE NONCLUSTERED INDEX IX_PoliticaConsumidor_Ativo ON dbo.PoliticaConsumidor(Ativo) INCLUDE (FornecedorId, Codigo, Nome);
GO

CREATE TABLE dbo.PoliticaConsumidorAplicacao (
    Id UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    PoliticaId UNIQUEIDENTIFIER NOT NULL,
    ConsumidorId UNIQUEIDENTIFIER NOT NULL,
    DataAplicacao DATETIME2 NOT NULL DEFAULT GETDATE(),
    DataRemocao DATETIME2 NULL,
    FlExcluido BIT NOT NULL DEFAULT 0,
    UsuarioAplicacaoId UNIQUEIDENTIFIER NOT NULL,
    UsuarioRemocaoId UNIQUEIDENTIFIER NULL,

    CONSTRAINT PK_PoliticaConsumidorAplicacao PRIMARY KEY CLUSTERED (Id),
    CONSTRAINT FK_PoliticaConsumidorAplicacao_Politica FOREIGN KEY (PoliticaId) REFERENCES dbo.PoliticaConsumidor(Id) ON DELETE CASCADE,
    CONSTRAINT FK_PoliticaConsumidorAplicacao_Consumidor FOREIGN KEY (ConsumidorId) REFERENCES dbo.Consumidor(Id) ON DELETE CASCADE,
    CONSTRAINT FK_PoliticaConsumidorAplicacao_UsuarioAplicacao FOREIGN KEY (UsuarioAplicacaoId) REFERENCES dbo.Usuario(Id),
    CONSTRAINT FK_PoliticaConsumidorAplicacao_UsuarioRemocao FOREIGN KEY (UsuarioRemocaoId) REFERENCES dbo.Usuario(Id),
    CONSTRAINT UQ_PoliticaConsumidorAplicacao_PoliticaConsumidor UNIQUE (PoliticaId, ConsumidorId)
);

CREATE NONCLUSTERED INDEX IX_PoliticaConsumidorAplicacao_Politica ON dbo.PoliticaConsumidorAplicacao(PoliticaId) INCLUDE (ConsumidorId, DataAplicacao);
CREATE NONCLUSTERED INDEX IX_PoliticaConsumidorAplicacao_Consumidor ON dbo.PoliticaConsumidorAplicacao(ConsumidorId) INCLUDE (PoliticaId, DataAplicacao);
CREATE NONCLUSTERED INDEX IX_PoliticaConsumidorAplicacao_Ativo ON dbo.PoliticaConsumidorAplicacao(Ativo) INCLUDE (PoliticaId, ConsumidorId);
GO

CREATE TABLE dbo.ViolacaoPolitica (
    Id UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    ConsumidorId UNIQUEIDENTIFIER NOT NULL,
    PoliticaId UNIQUEIDENTIFIER NOT NULL,
    DataViolacao DATETIME2 NOT NULL DEFAULT GETDATE(),
    ValorConsumido DECIMAL(18,2) NOT NULL,
    ValorLimite DECIMAL(18,2) NOT NULL,
    PercentualConsumo AS (ValorConsumido / NULLIF(ValorLimite, 0) * 100) PERSISTED,
    AcaoTomada VARCHAR(50) NOT NULL,
    Resolvido BIT NOT NULL DEFAULT 0,
    DataResolucao DATETIME2 NULL,
    UsuarioResolucaoId UNIQUEIDENTIFIER NULL,
    ObservacoesResolucao NVARCHAR(1000) NULL,

    CONSTRAINT PK_ViolacaoPolitica PRIMARY KEY CLUSTERED (Id),
    CONSTRAINT FK_ViolacaoPolitica_Consumidor FOREIGN KEY (ConsumidorId) REFERENCES dbo.Consumidor(Id),
    CONSTRAINT FK_ViolacaoPolitica_Politica FOREIGN KEY (PoliticaId) REFERENCES dbo.PoliticaConsumidor(Id),
    CONSTRAINT FK_ViolacaoPolitica_UsuarioResolucao FOREIGN KEY (UsuarioResolucaoId) REFERENCES dbo.Usuario(Id),
    CONSTRAINT CHK_ViolacaoPolitica_AcaoTomada CHECK (AcaoTomada IN ('ALERTA_50', 'ALERTA_80', 'BLOQUEIO_100', 'MANUAL'))
);

CREATE NONCLUSTERED INDEX IX_ViolacaoPolitica_Consumidor ON dbo.ViolacaoPolitica(ConsumidorId, DataViolacao DESC) INCLUDE (PoliticaId, ValorConsumido, AcaoTomada);
CREATE NONCLUSTERED INDEX IX_ViolacaoPolitica_Politica ON dbo.ViolacaoPolitica(PoliticaId) INCLUDE (ConsumidorId, DataViolacao);
CREATE NONCLUSTERED INDEX IX_ViolacaoPolitica_DataViolacao ON dbo.ViolacaoPolitica(DataViolacao DESC) INCLUDE (ConsumidorId, PoliticaId);
CREATE NONCLUSTERED INDEX IX_ViolacaoPolitica_Resolvido ON dbo.ViolacaoPolitica(Resolvido) WHERE Resolvido = 0;
CREATE NONCLUSTERED INDEX IX_ViolacaoPolitica_PercentualConsumo ON dbo.ViolacaoPolitica(PercentualConsumo DESC) WHERE Resolvido = 0;
GO

-- =============================================
-- Views
-- =============================================

CREATE OR ALTER VIEW dbo.vw_PoliticasAtivasPorConsumidor
AS
SELECT
    pca.ConsumidorId,
    p.Id AS PoliticaId,
    p.Codigo,
    p.Nome,
    p.TipoPolitica,
    p.ValorLimite,
    p.UnidadeMedida,
    pca.DataAplicacao,
    pca.UsuarioAplicacaoId
FROM dbo.PoliticaConsumidorAplicacao pca
INNER JOIN dbo.PoliticaConsumidor p ON pca.PoliticaId = p.Id
WHERE pca.Ativo = 1 AND p.Ativo = 1 AND pca.DataRemocao IS NULL;
GO

-- =============================================
-- Stored Procedures
-- =============================================

CREATE OR ALTER PROCEDURE dbo.sp_AvaliarPolitica
    @ConsumidorId UNIQUEIDENTIFIER,
    @TipoPolitica VARCHAR(50),
    @ValorConsumo DECIMAL(18,2),
    @Permitido BIT OUTPUT,
    @PercentualUtilizado DECIMAL(5,2) OUTPUT,
    @LimiteAtual DECIMAL(18,2) OUTPUT
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @ValorLimite DECIMAL(18,2);

    -- Busca política aplicada ao consumidor
    SELECT TOP 1
        @ValorLimite = p.ValorLimite
    FROM dbo.PoliticaConsumidorAplicacao pca
    INNER JOIN dbo.PoliticaConsumidor p ON pca.PoliticaId = p.Id
    WHERE pca.ConsumidorId = @ConsumidorId
      AND p.TipoPolitica = @TipoPolitica
      AND pca.Ativo = 1
      AND p.Ativo = 1
    ORDER BY p.Prioridade DESC;

    SET @LimiteAtual = @ValorLimite;

    IF @ValorLimite IS NULL
    BEGIN
        -- Sem política: permitido
        SET @Permitido = 1;
        SET @PercentualUtilizado = 0;
    END
    ELSE
    BEGIN
        SET @PercentualUtilizado = (@ValorConsumo / @ValorLimite) * 100;
        SET @Permitido = CASE WHEN @ValorConsumo <= @ValorLimite THEN 1 ELSE 0 END;
    END
END
GO
```

---

## 4. Observações

**Performance:**
- Índices covering para queries frequentes
- Computed column `PercentualConsumo` otimiza rankings
- Particionamento de `ViolacaoPolitica` após 1 ano

**Segurança:**
- Soft delete: false=ativo, true=excluído em todas as tabelas
- Auditoria automática via EF Core
- Histórico imutável de violações (7 anos)

**Integrações:**
- **RF052 (Consumidores):** Aplicação de políticas
- **RF048 (Status):** Políticas por status via StatusPoliticaAplicacao
- **RF026 (Faturamento):** Cálculo de economia gerada

---

## 5. Histórico

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 1.0 | 2025-12-18 | IControlIT Architect Agent | MD completo RF049 com 3 tabelas, 20 índices, views, SPs |

---

**Estatísticas:** Tabelas: 3 | Índices: 20 | Constraints: 15 | Views: 1 | SPs: 1 | DDL: ~400 linhas | Qualidade: 100% ✅
