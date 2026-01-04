# Modelo de Dados - RF056 - Gestão de Filas de Atendimento

**Versão:** 1.0 | **Data:** 2025-12-18 | **RF:** [RF056](./RF056.md) | **Banco:** SQL Server

## 1. Diagrama ER

```
Cliente (1) ───< (N) Fila (1) ───< (N) FilaAtendente
                      │
                      └───< (N) Solicitacao (com AtendenteId, FilaId)
FilaAtendente (N) ──> (1) Atendente (Usuario)
Atendente (1) ───< (N) AtendenteHistoricoStatus
Fila (1) ───< (N) MetricasFila
Solicitacao (1) ───< (N) TransferenciaSolicitacao
```

## 2. Tabelas

### 2.1 Fila

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | PK |
| Codigo | VARCHAR(50) | NÃO | - | Código único (FILA_MOBILE, FILA_DESKTOP) |
| Nome | NVARCHAR(100) | NÃO | - | Nome da fila |
| Categoria | VARCHAR(50) | NÃO | - | MOBILE, DESKTOP, REDE, LICENCAS, OUTROS |
| PrioridadePadrao | INT | NÃO | 2 | Prioridade padrão (1-5) |
| SLAPadraoHoras | INT | NÃO | 24 | SLA padrão em horas |
| EstrategiaDistribuicao | VARCHAR(30) | NÃO | 'ROUND_ROBIN' | ROUND_ROBIN, MENOR_CARGA, SKILL_MATCHING |
| AutoAtribuicao | BIT | NÃO | 1 | Atribuição automática |
| Ativa | BIT | NÃO | 1 | Fila ativa |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK Cliente |
| CreatedAt/By/ModifiedAt/By | - | - | - | Auditoria |

**Índices:**
- PK_Fila (Id)
- UK_Fila_Codigo (ClienteId, Codigo)
- IX_Fila_Categoria (Categoria, Ativa)

### 2.2 Atendente

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | PK |
| UsuarioId | UNIQUEIDENTIFIER | NÃO | - | FK Usuario |
| Status | VARCHAR(30) | NÃO | 'DISPONIVEL' | DISPONIVEL, OCUPADO, PAUSA, AUSENTE, PAUSA_ALMOCO |
| CargaAtual | INT | NÃO | 0 | Solicitações abertas atuais |
| LimiteSimultaneo | INT | NÃO | 5 | Máximo de solicitações simultâneas |
| SkillsJSON | NVARCHAR(MAX) | NÃO | '[]' | Array de skills: [{"categoria": "MOBILE", "nivel": 3}] |
| UltimaAtualizacaoStatus | DATETIME2(7) | NÃO | SYSUTCDATETIME() | Timestamp |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK Cliente |
| Ativo | BIT | NÃO | 1 | Ativo/Inativo |
| CreatedAt/By/ModifiedAt/By | - | - | - | Auditoria |

**Índices:**
- PK_Atendente (Id)
- UK_Atendente_Usuario (UsuarioId)
- IX_Atendente_Status (Status, CargaAtual) WHERE FlExcluido = 0

**Constraints:**
- CK_Atendente_Status: CHECK (Status IN ('DISPONIVEL', 'OCUPADO', 'PAUSA', 'AUSENTE', 'PAUSA_ALMOCO'))
- CK_Atendente_CargaAtual: CHECK (CargaAtual >= 0 AND CargaAtual <= LimiteSimultaneo)

### 2.3 FilaAtendente

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | PK |
| FilaId | UNIQUEIDENTIFIER | NÃO | - | FK Fila |
| AtendenteId | UNIQUEIDENTIFIER | NÃO | - | FK Atendente |
| DataVinculo | DATETIME2(7) | NÃO | SYSUTCDATETIME() | Data de inclusão na fila |
| Prioridade | INT | NÃO | 1 | Prioridade do atendente na fila |
| Ativo | BIT | NÃO | 1 | Vínculo ativo |

**Índices:**
- PK_FilaAtendente (Id)
- UK_FilaAtendente (FilaId, AtendenteId)
- IX_FilaAtendente_Atendente (AtendenteId)

### 2.4 AtendenteHistoricoStatus

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | PK |
| AtendenteId | UNIQUEIDENTIFIER | NÃO | - | FK Atendente |
| StatusAnterior | VARCHAR(30) | SIM | NULL | Status anterior |
| StatusNovo | VARCHAR(30) | NÃO | - | Novo status |
| Motivo | NVARCHAR(200) | SIM | NULL | Motivo da mudança |
| DataAlteracao | DATETIME2(7) | NÃO | SYSUTCDATETIME() | Timestamp |
| DuracaoSegundos | INT | SIM | NULL | Duração do status anterior (se aplicável) |

**Índices:**
- PK_AtendenteHistoricoStatus (Id)
- IX_AtendenteHistoricoStatus_Atendente (AtendenteId, DataAlteracao DESC)

### 2.5 TransferenciaSolicitacao

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | PK |
| SolicitacaoId | UNIQUEIDENTIFIER | NÃO | - | FK Solicitacao |
| AtendenteOrigemId | UNIQUEIDENTIFIER | NÃO | - | FK Atendente origem |
| AtendenteDestinoId | UNIQUEIDENTIFIER | NÃO | - | FK Atendente destino |
| FilaOrigemId | UNIQUEIDENTIFIER | SIM | NULL | FK Fila origem |
| FilaDestinoId | UNIQUEIDENTIFIER | SIM | NULL | FK Fila destino |
| Motivo | NVARCHAR(500) | NÃO | - | Motivo da transferência |
| DataTransferencia | DATETIME2(7) | NÃO | SYSUTCDATETIME() | Timestamp |
| UsuarioTransferenciaId | UNIQUEIDENTIFIER | NÃO | - | Quem fez a transferência |

**Índices:**
- PK_TransferenciaSolicitacao (Id)
- IX_TransferenciaSolicitacao_Solicitacao (SolicitacaoId, DataTransferencia DESC)
- IX_TransferenciaSolicitacao_Origem (AtendenteOrigemId)
- IX_TransferenciaSolicitacao_Destino (AtendenteDestinoId)

### 2.6 MetricasFila

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | PK |
| FilaId | UNIQUEIDENTIFIER | NÃO | - | FK Fila |
| DataHora | DATETIME2(7) | NÃO | SYSUTCDATETIME() | Timestamp da captura |
| TotalNaFila | INT | NÃO | 0 | Total aguardando atendimento |
| TotalEmAtendimento | INT | NÃO | 0 | Total em atendimento |
| TempoMedioEsperaMinutos | INT | NÃO | 0 | Tempo médio na fila |
| AtendentesDisponiveis | INT | NÃO | 0 | Atendentes disponíveis |
| TaxaSLAPercentual | DECIMAL(5,2) | NÃO | 0 | % atendidos dentro do SLA |

**Índices:**
- PK_MetricasFila (Id)
- IX_MetricasFila_Fila (FilaId, DataHora DESC)

## 3. DDL SQL Server

```sql
-- Tabela: Fila
CREATE TABLE Fila (
    Id UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    Codigo VARCHAR(50) NOT NULL,
    Nome NVARCHAR(100) NOT NULL,
    Categoria VARCHAR(50) NOT NULL,
    PrioridadePadrao INT NOT NULL DEFAULT 2,
    SLAPadraoHoras INT NOT NULL DEFAULT 24,
    EstrategiaDistribuicao VARCHAR(30) NOT NULL DEFAULT 'ROUND_ROBIN',
    AutoAtribuicao BIT NOT NULL DEFAULT 1,
    Ativa BIT NOT NULL DEFAULT 1,
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    CreatedAt DATETIME2(7) NOT NULL DEFAULT SYSUTCDATETIME(),
    CreatedBy UNIQUEIDENTIFIER NOT NULL,
    ModifiedAt DATETIME2(7) NULL,
    ModifiedBy UNIQUEIDENTIFIER NULL,
    CONSTRAINT PK_Fila PRIMARY KEY CLUSTERED (Id),
    CONSTRAINT FK_Fila_Cliente FOREIGN KEY (ClienteId) REFERENCES Cliente(Id),
    CONSTRAINT CK_Fila_Categoria CHECK (Categoria IN ('MOBILE', 'DESKTOP', 'REDE', 'LICENCAS', 'OUTROS')),
    CONSTRAINT CK_Fila_Estrategia CHECK (EstrategiaDistribuicao IN ('ROUND_ROBIN', 'MENOR_CARGA', 'SKILL_MATCHING'))
);
CREATE UNIQUE NONCLUSTERED INDEX UK_Fila_Codigo ON Fila(ClienteId, Codigo) WHERE Ativa=1;

-- Tabela: Atendente
CREATE TABLE Atendente (
    Id UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    UsuarioId UNIQUEIDENTIFIER NOT NULL,
    Status VARCHAR(30) NOT NULL DEFAULT 'DISPONIVEL',
    CargaAtual INT NOT NULL DEFAULT 0,
    LimiteSimultaneo INT NOT NULL DEFAULT 5,
    SkillsJSON NVARCHAR(MAX) NOT NULL DEFAULT '[]',
    UltimaAtualizacaoStatus DATETIME2(7) NOT NULL DEFAULT SYSUTCDATETIME(),
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    FlExcluido BIT NOT NULL DEFAULT 0,
    CreatedAt DATETIME2(7) NOT NULL DEFAULT SYSUTCDATETIME(),
    CreatedBy UNIQUEIDENTIFIER NOT NULL,
    ModifiedAt DATETIME2(7) NULL,
    ModifiedBy UNIQUEIDENTIFIER NULL,
    CONSTRAINT PK_Atendente PRIMARY KEY CLUSTERED (Id),
    CONSTRAINT FK_Atendente_Usuario FOREIGN KEY (UsuarioId) REFERENCES Usuario(Id),
    CONSTRAINT FK_Atendente_Cliente FOREIGN KEY (ClienteId) REFERENCES Cliente(Id),
    CONSTRAINT CK_Atendente_Status CHECK (Status IN ('DISPONIVEL', 'OCUPADO', 'PAUSA', 'AUSENTE', 'PAUSA_ALMOCO')),
    CONSTRAINT CK_Atendente_CargaAtual CHECK (CargaAtual >= 0 AND CargaAtual <= LimiteSimultaneo)
);
CREATE UNIQUE NONCLUSTERED INDEX UK_Atendente_Usuario ON Atendente(UsuarioId);
CREATE NONCLUSTERED INDEX IX_Atendente_Status ON Atendente(Status, CargaAtual) WHERE FlExcluido = 0;

-- Tabela: FilaAtendente
CREATE TABLE FilaAtendente (
    Id UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    FilaId UNIQUEIDENTIFIER NOT NULL,
    AtendenteId UNIQUEIDENTIFIER NOT NULL,
    DataVinculo DATETIME2(7) NOT NULL DEFAULT SYSUTCDATETIME(),
    Prioridade INT NOT NULL DEFAULT 1,
    FlExcluido BIT NOT NULL DEFAULT 0,
    CONSTRAINT PK_FilaAtendente PRIMARY KEY CLUSTERED (Id),
    CONSTRAINT FK_FilaAtendente_Fila FOREIGN KEY (FilaId) REFERENCES Fila(Id),
    CONSTRAINT FK_FilaAtendente_Atendente FOREIGN KEY (AtendenteId) REFERENCES Atendente(Id)
);
CREATE UNIQUE NONCLUSTERED INDEX UK_FilaAtendente ON FilaAtendente(FilaId, AtendenteId) WHERE FlExcluido = 0;

-- Tabela: AtendenteHistoricoStatus
CREATE TABLE AtendenteHistoricoStatus (
    Id UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    AtendenteId UNIQUEIDENTIFIER NOT NULL,
    StatusAnterior VARCHAR(30) NULL,
    StatusNovo VARCHAR(30) NOT NULL,
    Motivo NVARCHAR(200) NULL,
    DataAlteracao DATETIME2(7) NOT NULL DEFAULT SYSUTCDATETIME(),
    DuracaoSegundos INT NULL,
    CONSTRAINT PK_AtendenteHistoricoStatus PRIMARY KEY CLUSTERED (Id),
    CONSTRAINT FK_AtendenteHistoricoStatus_Atendente FOREIGN KEY (AtendenteId) REFERENCES Atendente(Id) ON DELETE CASCADE
);

-- Tabela: TransferenciaSolicitacao
CREATE TABLE TransferenciaSolicitacao (
    Id UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    SolicitacaoId UNIQUEIDENTIFIER NOT NULL,
    AtendenteOrigemId UNIQUEIDENTIFIER NOT NULL,
    AtendenteDestinoId UNIQUEIDENTIFIER NOT NULL,
    FilaOrigemId UNIQUEIDENTIFIER NULL,
    FilaDestinoId UNIQUEIDENTIFIER NULL,
    Motivo NVARCHAR(500) NOT NULL,
    DataTransferencia DATETIME2(7) NOT NULL DEFAULT SYSUTCDATETIME(),
    UsuarioTransferenciaId UNIQUEIDENTIFIER NOT NULL,
    CONSTRAINT PK_TransferenciaSolicitacao PRIMARY KEY CLUSTERED (Id),
    CONSTRAINT FK_TransferenciaSolicitacao_Solicitacao FOREIGN KEY (SolicitacaoId) REFERENCES Solicitacao(Id),
    CONSTRAINT FK_TransferenciaSolicitacao_Origem FOREIGN KEY (AtendenteOrigemId) REFERENCES Atendente(Id),
    CONSTRAINT FK_TransferenciaSolicitacao_Destino FOREIGN KEY (AtendenteDestinoId) REFERENCES Atendente(Id),
    CONSTRAINT FK_TransferenciaSolicitacao_Usuario FOREIGN KEY (UsuarioTransferenciaId) REFERENCES Usuario(Id)
);

-- Tabela: MetricasFila
CREATE TABLE MetricasFila (
    Id UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    FilaId UNIQUEIDENTIFIER NOT NULL,
    DataHora DATETIME2(7) NOT NULL DEFAULT SYSUTCDATETIME(),
    TotalNaFila INT NOT NULL DEFAULT 0,
    TotalEmAtendimento INT NOT NULL DEFAULT 0,
    TempoMedioEsperaMinutos INT NOT NULL DEFAULT 0,
    AtendentesDisponiveis INT NOT NULL DEFAULT 0,
    TaxaSLAPercentual DECIMAL(5,2) NOT NULL DEFAULT 0,
    CONSTRAINT PK_MetricasFila PRIMARY KEY CLUSTERED (Id),
    CONSTRAINT FK_MetricasFila_Fila FOREIGN KEY (FilaId) REFERENCES Fila(Id) ON DELETE CASCADE
);
CREATE NONCLUSTERED INDEX IX_MetricasFila_Fila ON MetricasFila(FilaId, DataHora DESC);

-- Adicionar campos em Solicitacao (se não existirem)
ALTER TABLE Solicitacao ADD FilaId UNIQUEIDENTIFIER NULL;
ALTER TABLE Solicitacao ADD CONSTRAINT FK_Solicitacao_Fila FOREIGN KEY (FilaId) REFERENCES Fila(Id);
CREATE NONCLUSTERED INDEX IX_Solicitacao_Fila ON Solicitacao(FilaId, Status) WHERE Status IN ('AGUARDANDO_ATENDIMENTO', 'EM_ATENDIMENTO');
```

## 4. Stored Procedures

```sql
-- Selecionar próximo atendente disponível
CREATE PROCEDURE sp_SelecionarProximoAtendente
    @FilaId UNIQUEIDENTIFIER,
    @CategoriaRequerida VARCHAR(50),
    @AtendenteId UNIQUEIDENTIFIER OUTPUT
AS
BEGIN
    SET NOCOUNT ON;

    -- Buscar atendente disponível com menor carga
    SELECT TOP 1 @AtendenteId = a.Id
    FROM Atendente a
    INNER JOIN FilaAtendente fa ON a.Id = fa.AtendenteId AND fa.FilaId = @FilaId
    WHERE a.Status = 'DISPONIVEL'
      AND a.CargaAtual < a.LimiteSimultaneo
      AND a.Ativo = 1
      AND fa.Ativo = 1
      AND JSON_VALUE(a.SkillsJSON, '$[0].categoria') = @CategoriaRequerida -- Simplificado
    ORDER BY a.CargaAtual ASC, fa.Prioridade ASC;
END;
GO

-- Atribuir solicitação automaticamente
CREATE PROCEDURE sp_AtribuirSolicitacaoAutomatica
    @SolicitacaoId UNIQUEIDENTIFIER
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRANSACTION;

    DECLARE @FilaId UNIQUEIDENTIFIER;
    DECLARE @Categoria VARCHAR(50);
    DECLARE @AtendenteId UNIQUEIDENTIFIER;

    -- Obter fila e categoria da solicitação
    SELECT @FilaId = FilaId, @Categoria = st.Categoria
    FROM Solicitacao s
    INNER JOIN SolicitacaoTipo st ON s.TipoId = st.Id
    WHERE s.Id = @SolicitacaoId;

    -- Selecionar atendente
    EXEC sp_SelecionarProximoAtendente @FilaId, @Categoria, @AtendenteId OUTPUT;

    IF @AtendenteId IS NOT NULL
    BEGIN
        -- Atribuir solicitação
        UPDATE Solicitacao SET AtendenteId = @AtendenteId, Status = 'EM_ATENDIMENTO', DataAtribuicao = SYSUTCDATETIME()
        WHERE Id = @SolicitacaoId;

        -- Incrementar carga do atendente
        UPDATE Atendente SET CargaAtual = CargaAtual + 1 WHERE Id = @AtendenteId;
    END

    COMMIT TRANSACTION;
END;
GO
```

## 5. Views

```sql
-- Visão de filas com estatísticas em tempo real
CREATE VIEW vw_FilasTempoReal
AS
SELECT
    f.Id, f.Nome, f.Categoria,
    COUNT(DISTINCT fa.AtendenteId) AS TotalAtendentes,
    SUM(CASE WHEN a.Status = 'DISPONIVEL' THEN 1 ELSE 0 END) AS AtendentesDisponiveis,
    (SELECT COUNT(*) FROM Solicitacao s WHERE s.FilaId = f.Id AND s.Status = 'AGUARDANDO_ATENDIMENTO') AS TotalNaFila,
    (SELECT COUNT(*) FROM Solicitacao s WHERE s.FilaId = f.Id AND s.Status = 'EM_ATENDIMENTO') AS TotalEmAtendimento
FROM Fila f
LEFT JOIN FilaAtendente fa ON f.Id = fa.FilaId AND fa.Ativo = 1
LEFT JOIN Atendente a ON fa.AtendenteId = a.Id AND a.Ativo = 1
WHERE f.Ativa = 1
GROUP BY f.Id, f.Nome, f.Categoria;
GO
```

## Observações

- **Multi-tenancy:** ClienteId em todas as tabelas principais
- **Real-time:** Métricas capturadas a cada 30 segundos via job
- **Escalabilidade:** Suporta 100 atendentes e 10.000 solicitações/dia
- **Skills:** JSON array para flexibilidade
- **Balanceamento:** Estratégias configuráveis por fila
- **Auditoria:** Histórico completo de status de atendentes

**Total de tabelas:** 6 | **Índices:** 15+ | **Constraints:** 12+
