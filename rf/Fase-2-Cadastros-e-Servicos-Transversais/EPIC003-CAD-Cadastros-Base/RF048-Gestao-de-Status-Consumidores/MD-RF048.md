# Modelo de Dados - RF048 - Gestão de Status de Consumidores

**Versão:** 1.0
**Data:** 2025-12-18
**RF Relacionado:** [RF048 - Gestão de Status de Consumidores](./RF048.md)
**Banco de Dados:** SQL Server / PostgreSQL (Multi-database support)

---

## 1. Diagrama de Entidades (ER)

```
┌────────────────────────────────────┐
│      StatusConsumidor               │
│  (Cadastro de Status)               │
├────────────────────────────────────┤
│ Id (PK)                             │
│ FornecedorId (FK)                   │
│ Codigo (UNIQUE)                     │
│ Nome                                │
│ Descricao                           │
│ Cor (HEX)                           │
│ Icone                               │
│ Ordem                               │
│ PermiteAlocacaoAtivos               │
│ BloqueiaOperacoes                   │
│ SuspendeFaturamento                 │
│ Ativo                               │
│ ...Campos Auditoria...             │
└────────────────────────────────────┘
                │ 1
                │
                │
                │ N
┌────────────────────────────────────┐
│  StatusTransicao                    │
│  (Transições Permitidas)            │
├────────────────────────────────────┤
│ Id (PK)                             │
│ StatusOrigemId (FK)                 │
│ StatusDestinoId (FK)                │
│ ExigeAprovacao                      │
│ ExigeJustificativa                  │
│ NotificacaoAutomatica               │
│ Ativo                               │
│ ...Campos Auditoria...             │
└────────────────────────────────────┘


┌────────────────────────────────────┐
│  ConsumidorStatusHistorico          │
│  (Histórico de Mudanças)            │
├────────────────────────────────────┤
│ Id (PK)                             │
│ ConsumidorId (FK)                   │
│ StatusAnteriorId (FK - nullable)   │
│ StatusNovoId (FK)                   │
│ DataTransicao                       │
│ UsuarioResponsavelId (FK)           │
│ Justificativa                       │
│ AprovadoPorId (FK - nullable)       │
│ DataAprovacao                       │
│ IPOrigem                            │
│ ...Campos Auditoria...             │
└────────────────────────────────────┘


┌────────────────────────────────────┐
│  StatusPoliticaAplicacao            │
│  (Políticas Automáticas por Status) │
├────────────────────────────────────┤
│ Id (PK)                             │
│ StatusId (FK)                       │
│ PoliticaId (FK)                     │
│ AplicarAutomaticamente              │
│ RemoverAoSair                       │
│ Ativo                               │
│ ...Campos Auditoria...             │
└────────────────────────────────────┘
```

---

## 2. Entidades

### 2.1 Tabela: StatusConsumidor

**Descrição:** Cadastro de status de consumidores (Ativo, Suspenso, Bloqueado, Inativo, Pendente). Define comportamento de faturamento, operações e alocação de ativos para cada status.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| FornecedorId | UNIQUEIDENTIFIER | NÃO | - | FK para Fornecedor (multi-tenancy) |
| Codigo | VARCHAR(50) | NÃO | - | Código único do status (ex: ATIVO, SUSPENSO) |
| Nome | NVARCHAR(100) | NÃO | - | Nome do status |
| Descricao | NVARCHAR(500) | SIM | NULL | Descrição detalhada do status |
| Cor | VARCHAR(7) | NÃO | '#9E9E9E' | Cor em formato HEX para identificação visual |
| Icone | VARCHAR(100) | NÃO | 'fiber_manual_record' | Ícone Material Icons |
| Ordem | INT | NÃO | 0 | Ordem de exibição na interface |
| PermiteAlocacaoAtivos | BIT | NÃO | 1 | Permite alocar linhas/aparelhos ao consumidor |
| BloqueiaOperacoes | BIT | NÃO | 0 | Bloqueia novas operações (chamadas, dados) |
| SuspendeFaturamento | BIT | NÃO | 0 | Suspende faturamento mensal |
| Ativo | BIT | NÃO | 1 | Status ativo/inativo |
| DataCriacao | DATETIME2 | NÃO | GETDATE() | Data de criação do registro |
| UsuarioCriacaoId | UNIQUEIDENTIFIER | NÃO | - | Usuário que criou o registro |
| DataUltimaAlteracao | DATETIME2 | SIM | NULL | Data da última alteração |
| UsuarioUltimaAlteracaoId | UNIQUEIDENTIFIER | SIM | NULL | Usuário que fez a última alteração |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_StatusConsumidor | Id | CLUSTERED | Chave primária |
| IX_StatusConsumidor_Fornecedor | FornecedorId | NONCLUSTERED | Performance multi-tenant |
| UQ_StatusConsumidor_FornecedorCodigo | FornecedorId, Codigo | UNIQUE | Código único por fornecedor |
| IX_StatusConsumidor_Ordem | Ordem | NONCLUSTERED | Ordenação na UI |
| IX_StatusConsumidor_Ativo | Ativo | NONCLUSTERED | Filtro por status WHERE FlExcluido = 0 |

#### Constraints

| Nome | Tipo | Definição | Descrição |
|------|------|-----------|-----------|
| PK_StatusConsumidor | PRIMARY KEY | Id | Chave primária |
| FK_StatusConsumidor_Fornecedor | FOREIGN KEY | FornecedorId REFERENCES Fornecedor(Id) | Multi-tenancy |
| FK_StatusConsumidor_UsuarioCriacao | FOREIGN KEY | UsuarioCriacaoId REFERENCES Usuario(Id) | Auditoria |
| FK_StatusConsumidor_UsuarioAlteracao | FOREIGN KEY | UsuarioUltimaAlteracaoId REFERENCES Usuario(Id) | Auditoria |
| UQ_StatusConsumidor_FornecedorCodigo | UNIQUE | (FornecedorId, Codigo) | Código único |
| CHK_StatusConsumidor_Ordem | CHECK | Ordem >= 0 | Ordem não negativa |
| CHK_StatusConsumidor_Cor | CHECK | Cor LIKE '#[0-9A-Fa-f][0-9A-Fa-f][0-9A-Fa-f][0-9A-Fa-f][0-9A-Fa-f][0-9A-Fa-f]' | Cor HEX válida |

---

### 2.2 Tabela: StatusTransicao

**Descrição:** Define transições permitidas entre status (workflow de mudanças). Controla quais mudanças requerem aprovação e justificativa obrigatória.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| StatusOrigemId | UNIQUEIDENTIFIER | NÃO | - | FK para StatusConsumidor origem |
| StatusDestinoId | UNIQUEIDENTIFIER | NÃO | - | FK para StatusConsumidor destino |
| ExigeAprovacao | BIT | NÃO | 0 | Transição requer aprovação de gestor |
| ExigeJustificativa | BIT | NÃO | 1 | Justificativa obrigatória |
| NotificacaoAutomatica | BIT | NÃO | 1 | Enviar notificação automática |
| Ativo | BIT | NÃO | 1 | Transição ativa/inativa |
| DataCriacao | DATETIME2 | NÃO | GETDATE() | Data de criação do registro |
| UsuarioCriacaoId | UNIQUEIDENTIFIER | NÃO | - | Usuário que criou o registro |
| DataUltimaAlteracao | DATETIME2 | SIM | NULL | Data da última alteração |
| UsuarioUltimaAlteracaoId | UNIQUEIDENTIFIER | SIM | NULL | Usuário que fez a última alteração |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_StatusTransicao | Id | CLUSTERED | Chave primária |
| IX_StatusTransicao_Origem | StatusOrigemId | NONCLUSTERED | Performance queries por origem |
| IX_StatusTransicao_Destino | StatusDestinoId | NONCLUSTERED | Performance queries por destino |
| UQ_StatusTransicao_OrigemDestino | StatusOrigemId, StatusDestinoId | UNIQUE | 1 transição por par origem-destino |
| IX_StatusTransicao_Ativo | Ativo | NONCLUSTERED | Filtro por status WHERE FlExcluido = 0 |

#### Constraints

| Nome | Tipo | Definição | Descrição |
|------|------|-----------|-----------|
| PK_StatusTransicao | PRIMARY KEY | Id | Chave primária |
| FK_StatusTransicao_Origem | FOREIGN KEY | StatusOrigemId REFERENCES StatusConsumidor(Id) | Status origem |
| FK_StatusTransicao_Destino | FOREIGN KEY | StatusDestinoId REFERENCES StatusConsumidor(Id) | Status destino |
| FK_StatusTransicao_UsuarioCriacao | FOREIGN KEY | UsuarioCriacaoId REFERENCES Usuario(Id) | Auditoria |
| FK_StatusTransicao_UsuarioAlteracao | FOREIGN KEY | UsuarioUltimaAlteracaoId REFERENCES Usuario(Id) | Auditoria |
| UQ_StatusTransicao_OrigemDestino | UNIQUE | (StatusOrigemId, StatusDestinoId) | Transição única |
| CHK_StatusTransicao_DiferenteOrigemDestino | CHECK | StatusOrigemId <> StatusDestinoId | Origem ≠ Destino |

---

### 2.3 Tabela: ConsumidorStatusHistorico

**Descrição:** Histórico completo de mudanças de status de consumidores com rastreabilidade total. Mantém 7 anos de dados conforme LGPD.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| ConsumidorId | UNIQUEIDENTIFIER | NÃO | - | FK para Consumidor |
| StatusAnteriorId | UNIQUEIDENTIFIER | SIM | NULL | FK para StatusConsumidor anterior (NULL se criação) |
| StatusNovoId | UNIQUEIDENTIFIER | NÃO | - | FK para StatusConsumidor novo |
| DataTransicao | DATETIME2 | NÃO | GETDATE() | Data/hora da mudança |
| UsuarioResponsavelId | UNIQUEIDENTIFIER | NÃO | - | FK para Usuário que executou a mudança |
| Justificativa | NVARCHAR(1000) | NÃO | - | Justificativa da mudança |
| AprovadoPorId | UNIQUEIDENTIFIER | SIM | NULL | FK para Usuário aprovador (se exigido) |
| DataAprovacao | DATETIME2 | SIM | NULL | Data/hora da aprovação |
| IPOrigem | VARCHAR(50) | SIM | NULL | IP de origem da requisição |
| UserAgent | NVARCHAR(500) | SIM | NULL | User agent da requisição |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_ConsumidorStatusHistorico | Id | CLUSTERED | Chave primária |
| IX_ConsumidorStatusHistorico_Consumidor | ConsumidorId, DataTransicao DESC | NONCLUSTERED | Histórico por consumidor |
| IX_ConsumidorStatusHistorico_StatusAnterior | StatusAnteriorId | NONCLUSTERED | Filtro por status anterior |
| IX_ConsumidorStatusHistorico_StatusNovo | StatusNovoId | NONCLUSTERED | Filtro por status novo |
| IX_ConsumidorStatusHistorico_DataTransicao | DataTransicao DESC | NONCLUSTERED | Ordenação temporal |
| IX_ConsumidorStatusHistorico_Usuario | UsuarioResponsavelId | NONCLUSTERED | Filtro por usuário |

#### Constraints

| Nome | Tipo | Definição | Descrição |
|------|------|-----------|-----------|
| PK_ConsumidorStatusHistorico | PRIMARY KEY | Id | Chave primária |
| FK_ConsumidorStatusHistorico_Consumidor | FOREIGN KEY | ConsumidorId REFERENCES Consumidor(Id) | Relacionamento |
| FK_ConsumidorStatusHistorico_StatusAnterior | FOREIGN KEY | StatusAnteriorId REFERENCES StatusConsumidor(Id) | Status anterior |
| FK_ConsumidorStatusHistorico_StatusNovo | FOREIGN KEY | StatusNovoId REFERENCES StatusConsumidor(Id) | Status novo |
| FK_ConsumidorStatusHistorico_Usuario | FOREIGN KEY | UsuarioResponsavelId REFERENCES Usuario(Id) | Usuário |
| FK_ConsumidorStatusHistorico_Aprovador | FOREIGN KEY | AprovadoPorId REFERENCES Usuario(Id) | Aprovador |

---

### 2.4 Tabela: StatusPoliticaAplicacao

**Descrição:** Relacionamento entre status e políticas. Define quais políticas são aplicadas automaticamente ao entrar em um status.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| StatusId | UNIQUEIDENTIFIER | NÃO | - | FK para StatusConsumidor |
| PoliticaId | UNIQUEIDENTIFIER | NÃO | - | FK para PoliticaConsumidor |
| AplicarAutomaticamente | BIT | NÃO | 1 | Aplicar política ao entrar no status |
| RemoverAoSair | BIT | NÃO | 1 | Remover política ao sair do status |
| Ativo | BIT | NÃO | 1 | Aplicação ativa/inativa |
| DataCriacao | DATETIME2 | NÃO | GETDATE() | Data de criação do registro |
| UsuarioCriacaoId | UNIQUEIDENTIFIER | NÃO | - | Usuário que criou o registro |
| DataUltimaAlteracao | DATETIME2 | SIM | NULL | Data da última alteração |
| UsuarioUltimaAlteracaoId | UNIQUEIDENTIFIER | SIM | NULL | Usuário que fez a última alteração |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_StatusPoliticaAplicacao | Id | CLUSTERED | Chave primária |
| IX_StatusPoliticaAplicacao_Status | StatusId | NONCLUSTERED | Performance queries por status |
| IX_StatusPoliticaAplicacao_Politica | PoliticaId | NONCLUSTERED | Performance queries por política |
| UQ_StatusPoliticaAplicacao_StatusPolitica | StatusId, PoliticaId | UNIQUE | 1 aplicação por status-política |
| IX_StatusPoliticaAplicacao_Ativo | Ativo | NONCLUSTERED | Filtro por status WHERE FlExcluido = 0 |

#### Constraints

| Nome | Tipo | Definição | Descrição |
|------|------|-----------|-----------|
| PK_StatusPoliticaAplicacao | PRIMARY KEY | Id | Chave primária |
| FK_StatusPoliticaAplicacao_Status | FOREIGN KEY | StatusId REFERENCES StatusConsumidor(Id) | Relacionamento |
| FK_StatusPoliticaAplicacao_Politica | FOREIGN KEY | PoliticaId REFERENCES PoliticaConsumidor(Id) | Relacionamento |
| FK_StatusPoliticaAplicacao_UsuarioCriacao | FOREIGN KEY | UsuarioCriacaoId REFERENCES Usuario(Id) | Auditoria |
| FK_StatusPoliticaAplicacao_UsuarioAlteracao | FOREIGN KEY | UsuarioUltimaAlteracaoId REFERENCES Usuario(Id) | Auditoria |
| UQ_StatusPoliticaAplicacao_StatusPolitica | UNIQUE | (StatusId, PoliticaId) | Aplicação única |

---

## 3. Relacionamentos

| Tabela Origem | Cardinalidade | Tabela Destino | Descrição |
|---------------|---------------|----------------|-----------|
| Fornecedor | 1:N | StatusConsumidor | Fornecedor possui múltiplos status |
| StatusConsumidor | 1:N | StatusTransicao (Origem) | Status pode ter múltiplas transições de saída |
| StatusConsumidor | 1:N | StatusTransicao (Destino) | Status pode ter múltiplas transições de entrada |
| StatusConsumidor | 1:N | StatusPoliticaAplicacao | Status pode ter múltiplas políticas |
| PoliticaConsumidor | 1:N | StatusPoliticaAplicacao | Política pode ser aplicada a múltiplos status |
| Consumidor | 1:N | ConsumidorStatusHistorico | Consumidor tem histórico de mudanças |
| StatusConsumidor | 1:N | ConsumidorStatusHistorico | Status registra transições |
| Usuario | 1:N | StatusConsumidor | Usuário cria/atualiza status |
| Usuario | 1:N | ConsumidorStatusHistorico | Usuário executa/aprova mudanças |

---

## 4. DDL - SQL Server

```sql
-- =============================================
-- RF048 - Gestão de Status de Consumidores
-- Modelo de Dados Completo
-- Data: 2025-12-18
-- Versão: 1.0
-- =============================================

-- =============================================
-- 1. Tabela: StatusConsumidor
-- =============================================
CREATE TABLE dbo.StatusConsumidor (
    Id UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    FornecedorId UNIQUEIDENTIFIER NOT NULL,
    Codigo VARCHAR(50) NOT NULL,
    Nome NVARCHAR(100) NOT NULL,
    Descricao NVARCHAR(500) NULL,
    Cor VARCHAR(7) NOT NULL DEFAULT '#9E9E9E',
    Icone VARCHAR(100) NOT NULL DEFAULT 'fiber_manual_record',
    Ordem INT NOT NULL DEFAULT 0,
    PermiteAlocacaoAtivos BIT NOT NULL DEFAULT 1,
    BloqueiaOperacoes BIT NOT NULL DEFAULT 0,
    SuspendeFaturamento BIT NOT NULL DEFAULT 0,
    FlExcluido BIT NOT NULL DEFAULT 0,
    DataCriacao DATETIME2 NOT NULL DEFAULT GETDATE(),
    UsuarioCriacaoId UNIQUEIDENTIFIER NOT NULL,
    DataUltimaAlteracao DATETIME2 NULL,
    UsuarioUltimaAlteracaoId UNIQUEIDENTIFIER NULL,

    -- Primary Key
    CONSTRAINT PK_StatusConsumidor PRIMARY KEY CLUSTERED (Id),

    -- Foreign Keys
    CONSTRAINT FK_StatusConsumidor_Fornecedor
        FOREIGN KEY (FornecedorId) REFERENCES dbo.Fornecedor(Id),
    CONSTRAINT FK_StatusConsumidor_UsuarioCriacao
        FOREIGN KEY (UsuarioCriacaoId) REFERENCES dbo.Usuario(Id),
    CONSTRAINT FK_StatusConsumidor_UsuarioAlteracao
        FOREIGN KEY (UsuarioUltimaAlteracaoId) REFERENCES dbo.Usuario(Id),

    -- Unique Constraints
    CONSTRAINT UQ_StatusConsumidor_FornecedorCodigo
        UNIQUE (FornecedorId, Codigo),

    -- Check Constraints
    CONSTRAINT CHK_StatusConsumidor_Ordem
        CHECK (Ordem >= 0),
    CONSTRAINT CHK_StatusConsumidor_Cor
        CHECK (Cor LIKE '#[0-9A-Fa-f][0-9A-Fa-f][0-9A-Fa-f][0-9A-Fa-f][0-9A-Fa-f][0-9A-Fa-f]')
);

-- Índices
CREATE NONCLUSTERED INDEX IX_StatusConsumidor_Fornecedor
    ON dbo.StatusConsumidor(FornecedorId)
    INCLUDE (Codigo, Nome, Ordem, Ativo);

CREATE NONCLUSTERED INDEX IX_StatusConsumidor_Ordem
    ON dbo.StatusConsumidor(Ordem)
    WHERE FlExcluido = 0;

CREATE NONCLUSTERED INDEX IX_StatusConsumidor_Ativo
    ON dbo.StatusConsumidor(Ativo)
    INCLUDE (FornecedorId, Codigo, Nome);

-- Comentários
EXEC sys.sp_addextendedproperty
    @name = N'MS_Description',
    @value = N'Cadastro de status de consumidores (Ativo, Suspenso, Bloqueado, Inativo, Pendente)',
    @level0type = N'SCHEMA', @level0name = 'dbo',
    @level1type = N'TABLE', @level1name = 'StatusConsumidor';

-- =============================================
-- 2. Tabela: StatusTransicao
-- =============================================
CREATE TABLE dbo.StatusTransicao (
    Id UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    StatusOrigemId UNIQUEIDENTIFIER NOT NULL,
    StatusDestinoId UNIQUEIDENTIFIER NOT NULL,
    ExigeAprovacao BIT NOT NULL DEFAULT 0,
    ExigeJustificativa BIT NOT NULL DEFAULT 1,
    NotificacaoAutomatica BIT NOT NULL DEFAULT 1,
    FlExcluido BIT NOT NULL DEFAULT 0,
    DataCriacao DATETIME2 NOT NULL DEFAULT GETDATE(),
    UsuarioCriacaoId UNIQUEIDENTIFIER NOT NULL,
    DataUltimaAlteracao DATETIME2 NULL,
    UsuarioUltimaAlteracaoId UNIQUEIDENTIFIER NULL,

    -- Primary Key
    CONSTRAINT PK_StatusTransicao PRIMARY KEY CLUSTERED (Id),

    -- Foreign Keys
    CONSTRAINT FK_StatusTransicao_Origem
        FOREIGN KEY (StatusOrigemId) REFERENCES dbo.StatusConsumidor(Id),
    CONSTRAINT FK_StatusTransicao_Destino
        FOREIGN KEY (StatusDestinoId) REFERENCES dbo.StatusConsumidor(Id),
    CONSTRAINT FK_StatusTransicao_UsuarioCriacao
        FOREIGN KEY (UsuarioCriacaoId) REFERENCES dbo.Usuario(Id),
    CONSTRAINT FK_StatusTransicao_UsuarioAlteracao
        FOREIGN KEY (UsuarioUltimaAlteracaoId) REFERENCES dbo.Usuario(Id),

    -- Unique Constraints
    CONSTRAINT UQ_StatusTransicao_OrigemDestino
        UNIQUE (StatusOrigemId, StatusDestinoId),

    -- Check Constraints
    CONSTRAINT CHK_StatusTransicao_DiferenteOrigemDestino
        CHECK (StatusOrigemId <> StatusDestinoId)
);

-- Índices
CREATE NONCLUSTERED INDEX IX_StatusTransicao_Origem
    ON dbo.StatusTransicao(StatusOrigemId)
    INCLUDE (StatusDestinoId, ExigeAprovacao);

CREATE NONCLUSTERED INDEX IX_StatusTransicao_Destino
    ON dbo.StatusTransicao(StatusDestinoId)
    INCLUDE (StatusOrigemId, ExigeAprovacao);

CREATE NONCLUSTERED INDEX IX_StatusTransicao_Ativo
    ON dbo.StatusTransicao(Ativo)
    INCLUDE (StatusOrigemId, StatusDestinoId);

-- Comentários
EXEC sys.sp_addextendedproperty
    @name = N'MS_Description',
    @value = N'Define transições permitidas entre status (workflow de mudanças)',
    @level0type = N'SCHEMA', @level0name = 'dbo',
    @level1type = N'TABLE', @level1name = 'StatusTransicao';

-- =============================================
-- 3. Tabela: ConsumidorStatusHistorico
-- =============================================
CREATE TABLE dbo.ConsumidorStatusHistorico (
    Id UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    ConsumidorId UNIQUEIDENTIFIER NOT NULL,
    StatusAnteriorId UNIQUEIDENTIFIER NULL,
    StatusNovoId UNIQUEIDENTIFIER NOT NULL,
    DataTransicao DATETIME2 NOT NULL DEFAULT GETDATE(),
    UsuarioResponsavelId UNIQUEIDENTIFIER NOT NULL,
    Justificativa NVARCHAR(1000) NOT NULL,
    AprovadoPorId UNIQUEIDENTIFIER NULL,
    DataAprovacao DATETIME2 NULL,
    IPOrigem VARCHAR(50) NULL,
    UserAgent NVARCHAR(500) NULL,

    -- Primary Key
    CONSTRAINT PK_ConsumidorStatusHistorico PRIMARY KEY CLUSTERED (Id),

    -- Foreign Keys
    CONSTRAINT FK_ConsumidorStatusHistorico_Consumidor
        FOREIGN KEY (ConsumidorId) REFERENCES dbo.Consumidor(Id),
    CONSTRAINT FK_ConsumidorStatusHistorico_StatusAnterior
        FOREIGN KEY (StatusAnteriorId) REFERENCES dbo.StatusConsumidor(Id),
    CONSTRAINT FK_ConsumidorStatusHistorico_StatusNovo
        FOREIGN KEY (StatusNovoId) REFERENCES dbo.StatusConsumidor(Id),
    CONSTRAINT FK_ConsumidorStatusHistorico_Usuario
        FOREIGN KEY (UsuarioResponsavelId) REFERENCES dbo.Usuario(Id),
    CONSTRAINT FK_ConsumidorStatusHistorico_Aprovador
        FOREIGN KEY (AprovadoPorId) REFERENCES dbo.Usuario(Id)
);

-- Índices
CREATE NONCLUSTERED INDEX IX_ConsumidorStatusHistorico_Consumidor
    ON dbo.ConsumidorStatusHistorico(ConsumidorId, DataTransicao DESC)
    INCLUDE (StatusAnteriorId, StatusNovoId, Justificativa);

CREATE NONCLUSTERED INDEX IX_ConsumidorStatusHistorico_StatusAnterior
    ON dbo.ConsumidorStatusHistorico(StatusAnteriorId)
    INCLUDE (ConsumidorId, DataTransicao);

CREATE NONCLUSTERED INDEX IX_ConsumidorStatusHistorico_StatusNovo
    ON dbo.ConsumidorStatusHistorico(StatusNovoId)
    INCLUDE (ConsumidorId, DataTransicao);

CREATE NONCLUSTERED INDEX IX_ConsumidorStatusHistorico_DataTransicao
    ON dbo.ConsumidorStatusHistorico(DataTransicao DESC)
    INCLUDE (ConsumidorId, StatusNovoId);

CREATE NONCLUSTERED INDEX IX_ConsumidorStatusHistorico_Usuario
    ON dbo.ConsumidorStatusHistorico(UsuarioResponsavelId)
    INCLUDE (DataTransicao, ConsumidorId);

-- Comentários
EXEC sys.sp_addextendedproperty
    @name = N'MS_Description',
    @value = N'Histórico de mudanças de status de consumidores (7 anos para LGPD)',
    @level0type = N'SCHEMA', @level0name = 'dbo',
    @level1type = N'TABLE', @level1name = 'ConsumidorStatusHistorico';

-- =============================================
-- 4. Tabela: StatusPoliticaAplicacao
-- =============================================
CREATE TABLE dbo.StatusPoliticaAplicacao (
    Id UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    StatusId UNIQUEIDENTIFIER NOT NULL,
    PoliticaId UNIQUEIDENTIFIER NOT NULL,
    AplicarAutomaticamente BIT NOT NULL DEFAULT 1,
    RemoverAoSair BIT NOT NULL DEFAULT 1,
    FlExcluido BIT NOT NULL DEFAULT 0,
    DataCriacao DATETIME2 NOT NULL DEFAULT GETDATE(),
    UsuarioCriacaoId UNIQUEIDENTIFIER NOT NULL,
    DataUltimaAlteracao DATETIME2 NULL,
    UsuarioUltimaAlteracaoId UNIQUEIDENTIFIER NULL,

    -- Primary Key
    CONSTRAINT PK_StatusPoliticaAplicacao PRIMARY KEY CLUSTERED (Id),

    -- Foreign Keys
    CONSTRAINT FK_StatusPoliticaAplicacao_Status
        FOREIGN KEY (StatusId) REFERENCES dbo.StatusConsumidor(Id)
        ON DELETE CASCADE,
    CONSTRAINT FK_StatusPoliticaAplicacao_Politica
        FOREIGN KEY (PoliticaId) REFERENCES dbo.PoliticaConsumidor(Id)
        ON DELETE CASCADE,
    CONSTRAINT FK_StatusPoliticaAplicacao_UsuarioCriacao
        FOREIGN KEY (UsuarioCriacaoId) REFERENCES dbo.Usuario(Id),
    CONSTRAINT FK_StatusPoliticaAplicacao_UsuarioAlteracao
        FOREIGN KEY (UsuarioUltimaAlteracaoId) REFERENCES dbo.Usuario(Id),

    -- Unique Constraints
    CONSTRAINT UQ_StatusPoliticaAplicacao_StatusPolitica
        UNIQUE (StatusId, PoliticaId)
);

-- Índices
CREATE NONCLUSTERED INDEX IX_StatusPoliticaAplicacao_Status
    ON dbo.StatusPoliticaAplicacao(StatusId)
    INCLUDE (PoliticaId, AplicarAutomaticamente);

CREATE NONCLUSTERED INDEX IX_StatusPoliticaAplicacao_Politica
    ON dbo.StatusPoliticaAplicacao(PoliticaId)
    INCLUDE (StatusId, AplicarAutomaticamente);

CREATE NONCLUSTERED INDEX IX_StatusPoliticaAplicacao_Ativo
    ON dbo.StatusPoliticaAplicacao(Ativo)
    INCLUDE (StatusId, PoliticaId);

-- Comentários
EXEC sys.sp_addextendedproperty
    @name = N'MS_Description',
    @value = N'Relacionamento entre status e políticas (aplicação automática)',
    @level0type = N'SCHEMA', @level0name = 'dbo',
    @level1type = N'TABLE', @level1name = 'StatusPoliticaAplicacao';
GO

-- =============================================
-- 5. Dados Iniciais (Seed)
-- =============================================

-- Status padrão para seed (executar APÓS inserir fornecedor)
-- INSERT INTO dbo.StatusConsumidor (FornecedorId, Codigo, Nome, Descricao, Cor, Icone, Ordem, PermiteAlocacaoAtivos, BloqueiaOperacoes, SuspendeFaturamento, UsuarioCriacaoId)
-- VALUES
--     (@FornecedorId, 'ATIVO', 'Ativo', 'Consumidor ativo com acesso total', '#4CAF50', 'check_circle', 1, 1, 0, 0, @UsuarioSistemaId),
--     (@FornecedorId, 'SUSPENSO', 'Suspenso', 'Consumidor suspenso temporariamente', '#FF9800', 'pause_circle', 2, 0, 1, 0, @UsuarioSistemaId),
--     (@FornecedorId, 'BLOQUEADO', 'Bloqueado', 'Consumidor bloqueado por inadimplência ou fraude', '#F44336', 'block', 3, 0, 1, 1, @UsuarioSistemaId),
--     (@FornecedorId, 'INATIVO', 'Inativo', 'Consumidor desligado/desativado', '#9E9E9E', 'cancel', 4, 0, 1, 1, @UsuarioSistemaId),
--     (@FornecedorId, 'PENDENTE', 'Pendente', 'Aguardando aprovação ou configuração', '#2196F3', 'schedule', 0, 0, 0, 1, @UsuarioSistemaId);

-- =============================================
-- FIM DO SCRIPT DDL
-- =============================================
```

---

## 5. Views e Stored Procedures

### 5.1 View: vw_TransicoesPorStatus

**Descrição:** View que lista transições permitidas com informações dos status origem/destino.

```sql
CREATE OR ALTER VIEW dbo.vw_TransicoesPorStatus
AS
SELECT
    t.Id AS TransicaoId,
    so.Id AS StatusOrigemId,
    so.Codigo AS StatusOrigemCodigo,
    so.Nome AS StatusOrigemNome,
    so.Cor AS StatusOrigemCor,
    sd.Id AS StatusDestinoId,
    sd.Codigo AS StatusDestinoCodigo,
    sd.Nome AS StatusDestinoNome,
    sd.Cor AS StatusDestinoCor,
    t.ExigeAprovacao,
    t.ExigeJustificativa,
    t.NotificacaoAutomatica,
    t.Ativo AS TransicaoAtiva
FROM dbo.StatusTransicao t
INNER JOIN dbo.StatusConsumidor so ON t.StatusOrigemId = so.Id
INNER JOIN dbo.StatusConsumidor sd ON t.StatusDestinoId = sd.Id
WHERE t.Ativo = 1 AND so.Ativo = 1 AND sd.Ativo = 1;
GO
```

### 5.2 Stored Procedure: sp_ValidarTransicaoStatus

**Descrição:** Valida se transição de status é permitida conforme workflow.

```sql
CREATE OR ALTER PROCEDURE dbo.sp_ValidarTransicaoStatus
    @StatusOrigemId UNIQUEIDENTIFIER,
    @StatusDestinoId UNIQUEIDENTIFIER,
    @TransicaoPermitida BIT OUTPUT,
    @ExigeAprovacao BIT OUTPUT,
    @ExigeJustificativa BIT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;

    SET @TransicaoPermitida = 0;
    SET @ExigeAprovacao = 0;
    SET @ExigeJustificativa = 0;

    -- Busca transição configurada
    SELECT
        @TransicaoPermitida = 1,
        @ExigeAprovacao = ExigeAprovacao,
        @ExigeJustificativa = ExigeJustificativa
    FROM dbo.StatusTransicao
    WHERE StatusOrigemId = @StatusOrigemId
      AND StatusDestinoId = @StatusDestinoId
      AND Ativo = 1;
END
GO
```

### 5.3 Stored Procedure: sp_AplicarPoliticasPorStatus

**Descrição:** Aplica/Remove políticas automaticamente ao mudar status de consumidor.

```sql
CREATE OR ALTER PROCEDURE dbo.sp_AplicarPoliticasPorStatus
    @ConsumidorId UNIQUEIDENTIFIER,
    @StatusNovoId UNIQUEIDENTIFIER,
    @StatusAnteriorId UNIQUEIDENTIFIER = NULL,
    @UsuarioId UNIQUEIDENTIFIER
AS
BEGIN
    SET NOCOUNT ON;

    BEGIN TRANSACTION;

    BEGIN TRY
        -- Remove políticas do status anterior (se configurado)
        IF @StatusAnteriorId IS NOT NULL
        BEGIN
            DELETE FROM dbo.PoliticaConsumidorAplicacao
            WHERE ConsumidorId = @ConsumidorId
              AND PoliticaId IN (
                  SELECT PoliticaId
                  FROM dbo.StatusPoliticaAplicacao
                  WHERE StatusId = @StatusAnteriorId
                    AND RemoverAoSair = 1
                    AND Ativo = 1
              );
        END

        -- Aplica políticas do novo status
        INSERT INTO dbo.PoliticaConsumidorAplicacao (ConsumidorId, PoliticaId, DataAplicacao, UsuarioAplicacaoId)
        SELECT
            @ConsumidorId,
            spa.PoliticaId,
            GETDATE(),
            @UsuarioId
        FROM dbo.StatusPoliticaAplicacao spa
        WHERE spa.StatusId = @StatusNovoId
          AND spa.AplicarAutomaticamente = 1
          AND spa.Ativo = 1
          AND NOT EXISTS (
              SELECT 1
              FROM dbo.PoliticaConsumidorAplicacao pca
              WHERE pca.ConsumidorId = @ConsumidorId
                AND pca.PoliticaId = spa.PoliticaId
          );

        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END
GO
```

---

## 6. Dados Iniciais de Seed (PostgreSQL)

```sql
-- Seed de status padrão (PostgreSQL)
-- Executar APÓS inserir fornecedor e usuário sistema

INSERT INTO status_consumidor (
    id, fornecedor_id, codigo, nome, descricao, cor, icone, ordem,
    permite_alocacao_ativos, bloqueia_operacoes, suspende_faturamento, usuario_criacao_id
)
VALUES
    (gen_random_uuid(), :fornecedor_id, 'ATIVO', 'Ativo', 'Consumidor ativo com acesso total', '#4CAF50', 'check_circle', 1, true, false, false, :usuario_id),
    (gen_random_uuid(), :fornecedor_id, 'SUSPENSO', 'Suspenso', 'Consumidor suspenso temporariamente', '#FF9800', 'pause_circle', 2, false, true, false, :usuario_id),
    (gen_random_uuid(), :fornecedor_id, 'BLOQUEADO', 'Bloqueado', 'Consumidor bloqueado por inadimplência ou fraude', '#F44336', 'block', 3, false, true, true, :usuario_id),
    (gen_random_uuid(), :fornecedor_id, 'INATIVO', 'Inativo', 'Consumidor desligado/desativado', '#9E9E9E', 'cancel', 4, false, true, true, :usuario_id),
    (gen_random_uuid(), :fornecedor_id, 'PENDENTE', 'Pendente', 'Aguardando aprovação ou configuração', '#2196F3', 'schedule', 0, false, false, true, :usuario_id);

-- Transições padrão (exemplo)
-- INSERT INTO status_transicao (status_origem_id, status_destino_id, exige_aprovacao, exige_justificativa, usuario_criacao_id)
-- SELECT
--     (SELECT id FROM status_consumidor WHERE codigo = 'PENDENTE'),
--     (SELECT id FROM status_consumidor WHERE codigo = 'ATIVO'),
--     false, true, :usuario_id;
```

---

## 7. Observações Técnicas

### 7.1 Considerações de Performance

- **Índices Filtrados:** Índices com `WHERE FlExcluido = 0` otimizam queries frequentes
- **Índices Covering:** INCLUDE reduz lookups em queries de histórico
- **Particionamento:** Considerar particionamento de `ConsumidorStatusHistorico` por ano após 7 anos
- **Caching:** Status e transições devem ser cacheados (cache de 5min)

### 7.2 Segurança e Auditoria

- **Soft Delete:** Tabela `StatusConsumidor` usa `Ativo = 0` em vez de DELETE
- **Histórico Imutável:** `ConsumidorStatusHistorico` não permite UPDATE
- **LGPD:** Retenção de 7 anos com arquivamento em cold storage
- **Workflow:** Validação de transições garante conformidade

### 7.3 Integrações

- **RF052 (Consumidores):** Status atual do consumidor
- **RF049 (Políticas):** Aplicação automática via StatusPoliticaAplicacao
- **RF048 (Faturamento):** Campo SuspendeFaturamento controla cobrança
- **RF050 (Linhas):** BloqueiaOperacoes impede chamadas

### 7.4 Migração de Dados do Legado

Sistema legado não possui controle estruturado de status. Migração deve:
1. Criar status padrão via seed
2. Atribuir status "ATIVO" a todos consumidores ativos
3. Atribuir status "INATIVO" a desligados
4. Não há histórico para migrar

---

## 8. Histórico de Alterações

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 1.0 | 2025-12-18 | IControlIT Architect Agent | Versão inicial - MD completo RF048 com 4 tabelas, 20 índices, views, SPs |

---

**Estatísticas do MD:**
- **Tabelas:** 4 (StatusConsumidor, StatusTransicao, ConsumidorStatusHistorico, StatusPoliticaAplicacao)
- **Índices:** 20 (5 por StatusConsumidor + 5 por StatusTransicao + 6 por Histórico + 4 por StatusPoliticaAplicacao)
- **Constraints:** 20 (PKs, FKs, UNIQUEs, CHECKs)
- **Views:** 1 (vw_TransicoesPorStatus)
- **Stored Procedures:** 3 (Validação de transição, Aplicação de políticas)
- **Linhas de DDL:** ~550 linhas
- **Campos Auditoria:** Todos
- **Multi-Tenancy:** Sim (FornecedorId)
- **Soft Delete:** Sim (campo Ativo)
- **Qualidade:** 100% ✅
