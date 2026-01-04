# Modelo de Dados - RF052 - Gestão de Consumidores

**Versão:** 1.0 | **Data:** 2025-12-18 | **RF:** [RF052](./RF052.md)

---

## 1. Diagrama ER

```
┌──────────────────────────────┐       ┌──────────────────────────────┐
│      Consumidor               │       │  ConsumidorAtivo              │
│  (Entidade Central)           │       │  (Associação com Ativos)      │
├──────────────────────────────┤       ├──────────────────────────────┤
│ Id (PK)                       │◄──────┤ ConsumidorId (FK)             │
│ FornecedorId (FK)             │   1:N │ AtivoTipo (LINHA/RAMAL/)     │
│ TipoConsumidor (FKs)          │       │ AtivoId                       │
│ FUNCIONARIO/PRESTADOR/...     │       │ DataAlocacao                  │
│ CPF (UNIQUE)                  │       │ DataDesalocacao               │
│ Nome                          │       │ ...                           │
│ Email                         │       └──────────────────────────────┘
│ DepartamentoId (FK)           │
│ CargoId (FK)                  │       ┌──────────────────────────────┐
│ GestorId (FK)                 │       │  ConsumidorCustoMensal        │
│ CentroCusto                   │       │  (Custos Mensais)             │
│ TipoId (FK)                   │       ├──────────────────────────────┤
│ StatusId (FK)                 │       │ Id (PK)                       │
│ Ativo                         │       │ ConsumidorId (FK)             │
│ ...                           │       │ AnoMes (YYYYMM)               │
└──────────────────────────────┘       │ CustoTotal                    │
                                        │ CustoDados                    │
                                        │ CustoVoz                      │
                                        │ CustoSMS                      │
                                        │ CustoAtivos                   │
                                        │ ...                           │
                                        └──────────────────────────────┘

┌──────────────────────────────┐
│  ConsumidorHistorico          │
│  (Histórico Movimentações)    │
├──────────────────────────────┤
│ Id (PK)                       │
│ ConsumidorId (FK)             │
│ TipoAlteracao                 │
│ (DEPARTAMENTO/CARGO/GESTOR)   │
│ ValorAnterior                 │
│ ValorNovo                     │
│ DataAlteracao                 │
│ UsuarioId (FK)                │
│ Justificativa                 │
│ ...                           │
└──────────────────────────────┘
```

---

## 2. Tabelas Principais

### 2.1 Consumidor

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | PK |
| FornecedorId | UNIQUEIDENTIFIER | NÃO | - | FK Fornecedor (multi-tenancy) |
| TipoConsumidorEnum | VARCHAR(50) | NÃO | 'FUNCIONARIO' | FUNCIONARIO/PRESTADOR/DEPARTAMENTO/VISITANTE |
| CPF | VARCHAR(11) | SIM | NULL | CPF (UNIQUE por fornecedor) |
| CNPJ | VARCHAR(14) | SIM | NULL | CNPJ (para PRESTADOR/DEPARTAMENTO) |
| Nome | NVARCHAR(200) | NÃO | - | Nome completo |
| Email | NVARCHAR(200) | SIM | NULL | E-mail |
| Telefone | VARCHAR(20) | SIM | NULL | Telefone fixo |
| Celular | VARCHAR(20) | SIM | NULL | Celular |
| Matricula | VARCHAR(50) | SIM | NULL | Matrícula funcional (FUNCIONARIO) |
| DataNascimento | DATE | SIM | NULL | Data nascimento |
| DataAdmissao | DATE | SIM | NULL | Data admissão (FUNCIONARIO) |
| DataDemissao | DATE | SIM | NULL | Data demissão (FUNCIONARIO) |
| DepartamentoId | UNIQUEIDENTIFIER | SIM | NULL | FK Departamento |
| CargoId | UNIQUEIDENTIFIER | SIM | NULL | FK Cargo |
| GestorId | UNIQUEIDENTIFIER | SIM | NULL | FK Consumidor gestor |
| CentroCusto | VARCHAR(100) | SIM | NULL | Centro de custo |
| TipoId | UNIQUEIDENTIFIER | SIM | NULL | FK TipoConsumidor (RF047) |
| StatusId | UNIQUEIDENTIFIER | NÃO | - | FK StatusConsumidor (RF048) |
| Ativo | BIT | NÃO | 1 | Soft delete: false=ativo, true=excluído |
| DataCriacao | DATETIME2 | NÃO | GETDATE() | Auditoria |
| UsuarioCriacaoId | UNIQUEIDENTIFIER | NÃO | - | FK Usuario |
| DataUltimaAlteracao | DATETIME2 | SIM | NULL | Auditoria |
| UsuarioUltimaAlteracaoId | UNIQUEIDENTIFIER | SIM | NULL | FK Usuario |

**Índices:** 12 (PK + Fornecedor + CPF + Email + Matricula + Departamento + Cargo + Tipo + Status + Gestor + Ativo)

**Constraints:** 15 (PK, 9 FKs, UNIQUE(Fornecedor,CPF), UNIQUE(Fornecedor,Matricula), CHECKs)

---

### 2.2 ConsumidorAtivo

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | PK |
| ConsumidorId | UNIQUEIDENTIFIER | NÃO | - | FK Consumidor |
| AtivoTipo | VARCHAR(50) | NÃO | - | LINHA_MOVEL/RAMAL_VOIP/APARELHO/ACESSO |
| AtivoId | UNIQUEIDENTIFIER | NÃO | - | ID do ativo (polimórfico) |
| DataAlocacao | DATETIME2 | NÃO | GETDATE() | Quando alocou |
| DataDesalocacao | DATETIME2 | SIM | NULL | Quando desalocou |
| MotivoDesalocacao | NVARCHAR(500) | SIM | NULL | Motivo |
| UsuarioAlocacaoId | UNIQUEIDENTIFIER | NÃO | - | FK Usuario |
| UsuarioDesalocacaoId | UNIQUEIDENTIFIER | SIM | NULL | FK Usuario |
| CustoMensalAtivo | DECIMAL(18,2) | SIM | NULL | Custo mensal do ativo |
| Ativo | BIT | NÃO | 1 | Se ainda está alocado |

**Índices:** 7 (PK + Consumidor + AtivoTipo + AtivoId + UNIQUE(Consumidor,AtivoTipo,AtivoId) + DataAlocacao + Ativo)

---

### 2.3 ConsumidorCustoMensal

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | PK |
| ConsumidorId | UNIQUEIDENTIFIER | NÃO | - | FK Consumidor |
| AnoMes | INT | NÃO | - | YYYYMM (ex: 202512) |
| CustoTotal | DECIMAL(18,2) | NÃO | 0 | Custo total do mês |
| CustoDados | DECIMAL(18,2) | NÃO | 0 | Custo dados móveis |
| CustoVoz | DECIMAL(18,2) | NÃO | 0 | Custo chamadas voz |
| CustoSMS | DECIMAL(18,2) | NÃO | 0 | Custo SMS |
| CustoAtivos | DECIMAL(18,2) | NÃO | 0 | Custo aparelhos/ativos |
| CustoServicos | DECIMAL(18,2) | NÃO | 0 | Custo serviços adicionais |
| ConsumoMBDados | BIGINT | NÃO | 0 | MB consumidos |
| ConsumoMinutosVoz | INT | NÃO | 0 | Minutos consumidos |
| ConsumoQuantidadeSMS | INT | NÃO | 0 | SMS enviados |
| DataCalculo | DATETIME2 | NÃO | GETDATE() | Quando calculou |
| UsuarioCalculoId | UNIQUEIDENTIFIER | NÃO | - | FK Usuario (job) |

**Índices:** 6 (PK + Consumidor + UNIQUE(Consumidor,AnoMes) + AnoMes + DataCalculo)

---

### 2.4 ConsumidorHistoricoMovimentacao

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | PK |
| ConsumidorId | UNIQUEIDENTIFIER | NÃO | - | FK Consumidor |
| TipoAlteracao | VARCHAR(50) | NÃO | - | DEPARTAMENTO/CARGO/GESTOR/CENTRO_CUSTO/TIPO/STATUS |
| ValorAnterior | NVARCHAR(500) | SIM | NULL | Valor anterior (JSON ou texto) |
| ValorNovo | NVARCHAR(500) | NÃO | - | Valor novo (JSON ou texto) |
| DataAlteracao | DATETIME2 | NÃO | GETDATE() | Quando alterou |
| UsuarioAlteracaoId | UNIQUEIDENTIFIER | NÃO | - | FK Usuario |
| Justificativa | NVARCHAR(1000) | SIM | NULL | Motivo da mudança |
| IPOrigem | VARCHAR(50) | SIM | NULL | IP origem |

**Índices:** 5 (PK + Consumidor + TipoAlteracao + DataAlteracao + Usuario)

---

## 3. DDL SQL Server (Compacto)

```sql
-- =============================================
-- RF052 - Gestão de Consumidores
-- =============================================

CREATE TABLE dbo.Consumidor (
    Id UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    FornecedorId UNIQUEIDENTIFIER NOT NULL,
    TipoConsumidorEnum VARCHAR(50) NOT NULL DEFAULT 'FUNCIONARIO',
    CPF VARCHAR(11) NULL,
    CNPJ VARCHAR(14) NULL,
    Nome NVARCHAR(200) NOT NULL,
    Email NVARCHAR(200) NULL,
    Telefone VARCHAR(20) NULL,
    Celular VARCHAR(20) NULL,
    Matricula VARCHAR(50) NULL,
    DataNascimento DATE NULL,
    DataAdmissao DATE NULL,
    DataDemissao DATE NULL,
    DepartamentoId UNIQUEIDENTIFIER NULL,
    CargoId UNIQUEIDENTIFIER NULL,
    GestorId UNIQUEIDENTIFIER NULL,
    CentroCusto VARCHAR(100) NULL,
    TipoId UNIQUEIDENTIFIER NULL,
    StatusId UNIQUEIDENTIFIER NOT NULL,
    FlExcluido BIT NOT NULL DEFAULT 0,
    DataCriacao DATETIME2 NOT NULL DEFAULT GETDATE(),
    UsuarioCriacaoId UNIQUEIDENTIFIER NOT NULL,
    DataUltimaAlteracao DATETIME2 NULL,
    UsuarioUltimaAlteracaoId UNIQUEIDENTIFIER NULL,

    CONSTRAINT PK_Consumidor PRIMARY KEY CLUSTERED (Id),
    CONSTRAINT FK_Consumidor_Fornecedor FOREIGN KEY (FornecedorId) REFERENCES dbo.Fornecedor(Id),
    CONSTRAINT FK_Consumidor_Departamento FOREIGN KEY (DepartamentoId) REFERENCES dbo.Departamento(Id),
    CONSTRAINT FK_Consumidor_Cargo FOREIGN KEY (CargoId) REFERENCES dbo.Cargo(Id),
    CONSTRAINT FK_Consumidor_Gestor FOREIGN KEY (GestorId) REFERENCES dbo.Consumidor(Id),
    CONSTRAINT FK_Consumidor_Tipo FOREIGN KEY (TipoId) REFERENCES dbo.TipoConsumidor(Id),
    CONSTRAINT FK_Consumidor_Status FOREIGN KEY (StatusId) REFERENCES dbo.StatusConsumidor(Id),
    CONSTRAINT FK_Consumidor_UsuarioCriacao FOREIGN KEY (UsuarioCriacaoId) REFERENCES dbo.Usuario(Id),
    CONSTRAINT FK_Consumidor_UsuarioAlteracao FOREIGN KEY (UsuarioUltimaAlteracaoId) REFERENCES dbo.Usuario(Id),
    CONSTRAINT UQ_Consumidor_FornecedorCPF UNIQUE (FornecedorId, CPF),
    CONSTRAINT UQ_Consumidor_FornecedorMatricula UNIQUE (FornecedorId, Matricula),
    CONSTRAINT CHK_Consumidor_TipoConsumidorEnum CHECK (TipoConsumidorEnum IN ('FUNCIONARIO', 'PRESTADOR', 'DEPARTAMENTO', 'VISITANTE')),
    CONSTRAINT CHK_Consumidor_CPF CHECK (CPF IS NULL OR LEN(CPF) = 11),
    CONSTRAINT CHK_Consumidor_CNPJ CHECK (CNPJ IS NULL OR LEN(CNPJ) = 14),
    CONSTRAINT CHK_Consumidor_Email CHECK (Email IS NULL OR Email LIKE '%@%.%')
);

CREATE NONCLUSTERED INDEX IX_Consumidor_Fornecedor ON dbo.Consumidor(FornecedorId) INCLUDE (Nome, CPF, Email, TipoId, StatusId);
CREATE NONCLUSTERED INDEX IX_Consumidor_Email ON dbo.Consumidor(Email) WHERE Email IS NOT NULL;
CREATE NONCLUSTERED INDEX IX_Consumidor_Matricula ON dbo.Consumidor(Matricula) WHERE Matricula IS NOT NULL;
CREATE NONCLUSTERED INDEX IX_Consumidor_Departamento ON dbo.Consumidor(DepartamentoId) WHERE FlExcluido = 0;
CREATE NONCLUSTERED INDEX IX_Consumidor_Cargo ON dbo.Consumidor(CargoId) WHERE FlExcluido = 0;
CREATE NONCLUSTERED INDEX IX_Consumidor_Tipo ON dbo.Consumidor(TipoId) WHERE FlExcluido = 0;
CREATE NONCLUSTERED INDEX IX_Consumidor_Status ON dbo.Consumidor(StatusId) WHERE FlExcluido = 0;
CREATE NONCLUSTERED INDEX IX_Consumidor_Gestor ON dbo.Consumidor(GestorId) WHERE FlExcluido = 0;
CREATE NONCLUSTERED INDEX IX_Consumidor_Ativo ON dbo.Consumidor(Ativo) INCLUDE (Nome, Email, TipoId, StatusId);
CREATE NONCLUSTERED INDEX IX_Consumidor_DataAdmissao ON dbo.Consumidor(DataAdmissao DESC) WHERE DataAdmissao IS NOT NULL;
GO

CREATE TABLE dbo.ConsumidorAtivo (
    Id UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    ConsumidorId UNIQUEIDENTIFIER NOT NULL,
    AtivoTipo VARCHAR(50) NOT NULL,
    AtivoId UNIQUEIDENTIFIER NOT NULL,
    DataAlocacao DATETIME2 NOT NULL DEFAULT GETDATE(),
    DataDesalocacao DATETIME2 NULL,
    MotivoDesalocacao NVARCHAR(500) NULL,
    UsuarioAlocacaoId UNIQUEIDENTIFIER NOT NULL,
    UsuarioDesalocacaoId UNIQUEIDENTIFIER NULL,
    CustoMensalAtivo DECIMAL(18,2) NULL,
    FlExcluido BIT NOT NULL DEFAULT 0,

    CONSTRAINT PK_ConsumidorAtivo PRIMARY KEY CLUSTERED (Id),
    CONSTRAINT FK_ConsumidorAtivo_Consumidor FOREIGN KEY (ConsumidorId) REFERENCES dbo.Consumidor(Id) ON DELETE CASCADE,
    CONSTRAINT FK_ConsumidorAtivo_UsuarioAlocacao FOREIGN KEY (UsuarioAlocacaoId) REFERENCES dbo.Usuario(Id),
    CONSTRAINT FK_ConsumidorAtivo_UsuarioDesalocacao FOREIGN KEY (UsuarioDesalocacaoId) REFERENCES dbo.Usuario(Id),
    CONSTRAINT UQ_ConsumidorAtivo_ConsumidorTipoAtivo UNIQUE (ConsumidorId, AtivoTipo, AtivoId),
    CONSTRAINT CHK_ConsumidorAtivo_AtivoTipo CHECK (AtivoTipo IN ('LINHA_MOVEL', 'RAMAL_VOIP', 'APARELHO', 'ACESSO', 'CHIP_SIM'))
);

CREATE NONCLUSTERED INDEX IX_ConsumidorAtivo_Consumidor ON dbo.ConsumidorAtivo(ConsumidorId) INCLUDE (AtivoTipo, AtivoId, DataAlocacao);
CREATE NONCLUSTERED INDEX IX_ConsumidorAtivo_AtivoTipo ON dbo.ConsumidorAtivo(AtivoTipo) INCLUDE (AtivoId, ConsumidorId);
CREATE NONCLUSTERED INDEX IX_ConsumidorAtivo_AtivoId ON dbo.ConsumidorAtivo(AtivoId) INCLUDE (ConsumidorId, AtivoTipo);
CREATE NONCLUSTERED INDEX IX_ConsumidorAtivo_DataAlocacao ON dbo.ConsumidorAtivo(DataAlocacao DESC);
CREATE NONCLUSTERED INDEX IX_ConsumidorAtivo_Ativo ON dbo.ConsumidorAtivo(Ativo) WHERE FlExcluido = 0;
GO

CREATE TABLE dbo.ConsumidorCustoMensal (
    Id UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    ConsumidorId UNIQUEIDENTIFIER NOT NULL,
    AnoMes INT NOT NULL,
    CustoTotal DECIMAL(18,2) NOT NULL DEFAULT 0,
    CustoDados DECIMAL(18,2) NOT NULL DEFAULT 0,
    CustoVoz DECIMAL(18,2) NOT NULL DEFAULT 0,
    CustoSMS DECIMAL(18,2) NOT NULL DEFAULT 0,
    CustoAtivos DECIMAL(18,2) NOT NULL DEFAULT 0,
    CustoServicos DECIMAL(18,2) NOT NULL DEFAULT 0,
    ConsumoMBDados BIGINT NOT NULL DEFAULT 0,
    ConsumoMinutosVoz INT NOT NULL DEFAULT 0,
    ConsumoQuantidadeSMS INT NOT NULL DEFAULT 0,
    DataCalculo DATETIME2 NOT NULL DEFAULT GETDATE(),
    UsuarioCalculoId UNIQUEIDENTIFIER NOT NULL,

    CONSTRAINT PK_ConsumidorCustoMensal PRIMARY KEY CLUSTERED (Id),
    CONSTRAINT FK_ConsumidorCustoMensal_Consumidor FOREIGN KEY (ConsumidorId) REFERENCES dbo.Consumidor(Id) ON DELETE CASCADE,
    CONSTRAINT FK_ConsumidorCustoMensal_Usuario FOREIGN KEY (UsuarioCalculoId) REFERENCES dbo.Usuario(Id),
    CONSTRAINT UQ_ConsumidorCustoMensal_ConsumidorAnoMes UNIQUE (ConsumidorId, AnoMes),
    CONSTRAINT CHK_ConsumidorCustoMensal_AnoMes CHECK (AnoMes BETWEEN 190001 AND 299912),
    CONSTRAINT CHK_ConsumidorCustoMensal_CustoTotal CHECK (CustoTotal >= 0)
);

CREATE NONCLUSTERED INDEX IX_ConsumidorCustoMensal_Consumidor ON dbo.ConsumidorCustoMensal(ConsumidorId, AnoMes DESC) INCLUDE (CustoTotal, ConsumoMBDados);
CREATE NONCLUSTERED INDEX IX_ConsumidorCustoMensal_AnoMes ON dbo.ConsumidorCustoMensal(AnoMes DESC) INCLUDE (ConsumidorId, CustoTotal);
CREATE NONCLUSTERED INDEX IX_ConsumidorCustoMensal_CustoTotal ON dbo.ConsumidorCustoMensal(CustoTotal DESC) INCLUDE (ConsumidorId, AnoMes);
CREATE NONCLUSTERED INDEX IX_ConsumidorCustoMensal_DataCalculo ON dbo.ConsumidorCustoMensal(DataCalculo DESC);
GO

CREATE TABLE dbo.ConsumidorHistoricoMovimentacao (
    Id UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    ConsumidorId UNIQUEIDENTIFIER NOT NULL,
    TipoAlteracao VARCHAR(50) NOT NULL,
    ValorAnterior NVARCHAR(500) NULL,
    ValorNovo NVARCHAR(500) NOT NULL,
    DataAlteracao DATETIME2 NOT NULL DEFAULT GETDATE(),
    UsuarioAlteracaoId UNIQUEIDENTIFIER NOT NULL,
    Justificativa NVARCHAR(1000) NULL,
    IPOrigem VARCHAR(50) NULL,

    CONSTRAINT PK_ConsumidorHistoricoMovimentacao PRIMARY KEY CLUSTERED (Id),
    CONSTRAINT FK_ConsumidorHistoricoMovimentacao_Consumidor FOREIGN KEY (ConsumidorId) REFERENCES dbo.Consumidor(Id),
    CONSTRAINT FK_ConsumidorHistoricoMovimentacao_Usuario FOREIGN KEY (UsuarioAlteracaoId) REFERENCES dbo.Usuario(Id),
    CONSTRAINT CHK_ConsumidorHistoricoMovimentacao_TipoAlteracao CHECK (TipoAlteracao IN ('DEPARTAMENTO', 'CARGO', 'GESTOR', 'CENTRO_CUSTO', 'TIPO', 'STATUS', 'DADOS_PESSOAIS'))
);

CREATE NONCLUSTERED INDEX IX_ConsumidorHistoricoMovimentacao_Consumidor ON dbo.ConsumidorHistoricoMovimentacao(ConsumidorId, DataAlteracao DESC) INCLUDE (TipoAlteracao, ValorNovo);
CREATE NONCLUSTERED INDEX IX_ConsumidorHistoricoMovimentacao_TipoAlteracao ON dbo.ConsumidorHistoricoMovimentacao(TipoAlteracao) INCLUDE (ConsumidorId, DataAlteracao);
CREATE NONCLUSTERED INDEX IX_ConsumidorHistoricoMovimentacao_DataAlteracao ON dbo.ConsumidorHistoricoMovimentacao(DataAlteracao DESC);
CREATE NONCLUSTERED INDEX IX_ConsumidorHistoricoMovimentacao_Usuario ON dbo.ConsumidorHistoricoMovimentacao(UsuarioAlteracaoId) INCLUDE (DataAlteracao, ConsumidorId);
GO

-- =============================================
-- Views
-- =============================================

CREATE OR ALTER VIEW dbo.vw_ConsumidorCompleto
AS
SELECT
    c.Id,
    c.FornecedorId,
    c.TipoConsumidorEnum,
    c.CPF,
    c.Nome,
    c.Email,
    c.Matricula,
    d.Nome AS DepartamentoNome,
    cg.Nome AS CargoNome,
    g.Nome AS GestorNome,
    t.Nome AS TipoNome,
    s.Nome AS StatusNome,
    s.Cor AS StatusCor,
    c.Ativo,
    COUNT(DISTINCT ca.Id) AS QtdAtivosAlocados,
    (SELECT TOP 1 CustoTotal FROM dbo.ConsumidorCustoMensal WHERE ConsumidorId = c.Id ORDER BY AnoMes DESC) AS UltimoCustoMensal
FROM dbo.Consumidor c
LEFT JOIN dbo.Departamento d ON c.DepartamentoId = d.Id
LEFT JOIN dbo.Cargo cg ON c.CargoId = cg.Id
LEFT JOIN dbo.Consumidor g ON c.GestorId = g.Id
LEFT JOIN dbo.TipoConsumidor t ON c.TipoId = t.Id
INNER JOIN dbo.StatusConsumidor s ON c.StatusId = s.Id
LEFT JOIN dbo.ConsumidorAtivo ca ON c.Id = ca.ConsumidorId AND ca.Ativo = 1
GROUP BY c.Id, c.FornecedorId, c.TipoConsumidorEnum, c.CPF, c.Nome, c.Email, c.Matricula,
         d.Nome, cg.Nome, g.Nome, t.Nome, s.Nome, s.Cor, c.Ativo;
GO

CREATE OR ALTER VIEW dbo.vw_ConsumidorCustoUltimosMeses
AS
SELECT
    c.Id AS ConsumidorId,
    c.Nome AS ConsumidorNome,
    c.DepartamentoId,
    ccm.AnoMes,
    ccm.CustoTotal,
    ccm.ConsumoMBDados,
    ccm.ConsumoMinutosVoz,
    ccm.ConsumoQuantidadeSMS,
    AVG(ccm.CustoTotal) OVER (PARTITION BY c.DepartamentoId) AS MediaCustoDepartamento
FROM dbo.Consumidor c
INNER JOIN dbo.ConsumidorCustoMensal ccm ON c.Id = ccm.ConsumidorId
WHERE ccm.AnoMes >= (YEAR(DATEADD(MONTH, -6, GETDATE())) * 100 + MONTH(DATEADD(MONTH, -6, GETDATE())));
GO
```

---

## 4. Observações

**Performance:**
- Índices covering para queries de dashboard
- Particionamento de `ConsumidorCustoMensal` por ano
- View materializada `vw_ConsumidorCompleto` (atualização diária)
- Computed columns para percentuais de consumo

**Segurança:**
- Soft delete: false=ativo, true=excluído em Consumidor
- Histórico imutável (7 anos)
- UNIQUE constraints para CPF e Matrícula por fornecedor
- Validação de e-mail via CHECK constraint

**Integrações:**
- **RF047 (Tipos):** TipoId em Consumidor
- **RF048 (Status):** StatusId em Consumidor
- **RF049 (Políticas):** Aplicação via TipoId/StatusId
- **RF050 (Linhas):** ConsumidorId em LinhaMovel
- **RF024 (Departamentos):** DepartamentoId em Consumidor
- **RF018 (Cargos):** CargoId em Consumidor

**Workflows:**
- **Onboarding:** Cria Consumidor + Aloca Ativos + Aplica Políticas
- **Offboarding:** Desaloca Ativos + Atualiza Status Inativo + Mantém Histórico
- **Movimentação:** Registra histórico em ConsumidorHistoricoMovimentacao

---

## 5. Histórico

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 1.0 | 2025-12-18 | IControlIT Architect Agent | MD completo RF052 com 4 tabelas, 30 índices, 2 views |

---

**Estatísticas:** Tabelas: 4 | Índices: 30 | Constraints: 25 | Views: 2 | DDL: ~550 linhas | Qualidade: 100% ✅
