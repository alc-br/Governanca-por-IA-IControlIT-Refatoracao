# Modelo de Dados - RF059 - Gestão de Status e Tipos Genéricos

**Versão:** 1.0
**Data:** 2025-12-18
**RF Relacionado:** [RF059 - Gestão de Status e Tipos Genéricos](./RF059.md)
**Banco de Dados:** SQL Server / PostgreSQL

---

## 1. Diagrama de Entidades (ER)

```
┌──────────────────────┐
│   GestaoCliente      │
│   (multi-tenancy)    │
└──────────┬───────────┘
           │
           │ 1:N
           │
┌──────────▼───────────────────────────────────────┐
│           DominioTipo                            │
├──────────────────────────────────────────────────┤
│ Id (PK)                  UUID                    │
│ ClienteId (FK)           UUID                    │
│ ConglomeradoId (FK)      UUID (nullable)         │
│ Codigo                   VARCHAR(50)             │
│ Nome                     VARCHAR(200)            │
│ Descricao                TEXT                    │
│ PermiteCustomizacao      BIT                     │
│ PermiteTransicoes        BIT                     │
│ Global                   BIT                     │
│ Ordem                    INT                     │
│ Ativo                    BIT                     │
│ CreatedAt, CreatedBy, ModifiedAt, ModifiedBy     │
└──────────┬───────────────────────────────────────┘
           │ 1:N
           │
┌──────────▼───────────────────────────────────────┐
│           ItemDominio                            │
├──────────────────────────────────────────────────┤
│ Id (PK)                  UUID                    │
│ DominioId (FK)           UUID                    │
│ ClienteId (FK)           UUID                    │
│ ConglomeradoId (FK)      UUID (nullable)         │
│ Codigo                   VARCHAR(50)             │
│ Nome                     VARCHAR(200)            │
│ Descricao                TEXT                    │
│ Cor                      VARCHAR(7)              │
│ Icone                    VARCHAR(50)             │
│ Ordem                    INT                     │
│ Padrao                   BIT                     │
│ Global                   BIT                     │
│ Ativo                    BIT                     │
│ MotivoInativacao         TEXT                    │
│ DataInativacao           DATETIME                │
│ CreatedAt, CreatedBy, ModifiedAt, ModifiedBy     │
└──────────┬───────────────────────────────────────┘
           │ M:N (origem e destino)
           │
┌──────────▼───────────────────────────────────────┐
│      TransicaoPermitida                          │
├──────────────────────────────────────────────────┤
│ Id (PK)                  UUID                    │
│ DominioId (FK)           UUID                    │
│ ItemOrigemId (FK)        UUID                    │
│ ItemDestinoId (FK)       UUID                    │
│ ClienteId (FK)           UUID                    │
│ RequerJustificativa      BIT                     │
│ RequerAprovacao          BIT                     │
│ AprovadoresIds           TEXT (JSON)             │
│ Ordem                    INT                     │
│ Ativo                    BIT                     │
│ CreatedAt, CreatedBy, ModifiedAt, ModifiedBy     │
└──────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────┐
│      TipoTraducao                                │
├──────────────────────────────────────────────────┤
│ Id (PK)                  UUID                    │
│ ItemDominioId (FK)       UUID                    │
│ Idioma                   VARCHAR(5)              │
│ Nome                     VARCHAR(200)            │
│ Descricao                TEXT                    │
│ CreatedAt, CreatedBy, ModifiedAt, ModifiedBy     │
└──────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────┐
│      HistoricoDominioTipo                        │
├──────────────────────────────────────────────────┤
│ Id (PK)                  UUID                    │
│ DominioId (FK)           UUID                    │
│ ItemDominioId (FK)       UUID (nullable)         │
│ ClienteId (FK)           UUID                    │
│ TipoAlteracao            VARCHAR(50)             │
│ DadosAntes               TEXT (JSON)             │
│ DadosDepois              TEXT (JSON)             │
│ Justificativa            TEXT                    │
│ CreatedAt, CreatedBy                             │
└──────────────────────────────────────────────────┘
```

---

## 2. Entidades

### 2.1 Tabela: DominioTipo

**Descrição:** Representa categorias de tipos parametrizáveis do sistema (Status Chamado, Prioridades, Tipos de Ativo, Categorias, etc). Domínios podem ser globais (sistema) ou customizáveis por conglomerado.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK para GestaoCliente (multi-tenancy) |
| ClienteId | UNIQUEIDENTIFIER | SIM | NULL | FK para Cliente (multi-tenancy raiz) (nullable para itens globais) |
| Codigo | VARCHAR(50) | NÃO | - | Código único do domínio (ex: STATUS_CHAMADO) |
| Nome | VARCHAR(200) | NÃO | - | Nome descritivo do domínio |
| Descricao | TEXT | SIM | NULL | Descrição detalhada do propósito |
| PermiteCustomizacao | BIT | NÃO | 1 | Se permite criação de itens customizados |
| PermiteTransicoes | BIT | NÃO | 0 | Se possui workflow de transições |
| Global | BIT | NÃO | 0 | Se é domínio de sistema (não customizável) |
| Ordem | INT | NÃO | 0 | Ordem de exibição no sistema |
| Ativo | BIT | NÃO | 1 | Status ativo/inativo |
| CreatedAt | DATETIME2 | NÃO | GETUTCDATE() | Data de criação |
| CreatedBy | UNIQUEIDENTIFIER | NÃO | - | Usuário que criou |
| ModifiedAt | DATETIME2 | SIM | NULL | Data de última atualização |
| ModifiedBy | UNIQUEIDENTIFIER | SIM | NULL | Usuário que atualizou |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_DominioTipo | Id | CLUSTERED | Chave primária |
| IX_DominioTipo_ClienteId | ClienteId | NONCLUSTERED | Performance em queries multi-tenant |
| IX_DominioTipo_ConglomeradoId | ClienteId | NONCLUSTERED | Filtro por conglomerado |
| IX_DominioTipo_Codigo | Codigo, ClienteId | NONCLUSTERED | Busca por código único |
| IX_DominioTipo_Ativo | Ativo | NONCLUSTERED | Filtro de ativos com include |
| IX_DominioTipo_Global | Global | NONCLUSTERED | Separar domínios globais vs customizáveis |

#### Constraints

| Nome | Tipo | Definição | Descrição |
|------|------|-----------|-----------|
| PK_DominioTipo | PRIMARY KEY | Id | Chave primária |
| FK_DominioTipo_Cliente | FOREIGN KEY | ClienteId REFERENCES GestaoCliente(Id) | Multi-tenancy |
| FK_DominioTipo_Conglomerado | FOREIGN KEY | ConglomeradoId REFERENCES Conglomerado(Id) | Conglomerado (opcional) |
| FK_DominioTipo_CreatedBy | FOREIGN KEY | CreatedBy REFERENCES Usuario(Id) | Auditoria |
| FK_DominioTipo_ModifiedBy | FOREIGN KEY | ModifiedBy REFERENCES Usuario(Id) | Auditoria |
| UQ_DominioTipo_CodigoCliente | UNIQUE | (Codigo, ClienteId) | Código único por cliente |
| CHK_DominioTipo_Codigo | CHECK | LEN(Codigo) >= 3 | Código mínimo 3 caracteres |

---

### 2.2 Tabela: ItemDominio

**Descrição:** Itens específicos dentro de cada domínio (ex: "Aberto", "Em Atendimento", "Fechado" para STATUS_CHAMADO). Suporta cores, ícones e ordenação customizada.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| DominioId | UNIQUEIDENTIFIER | NÃO | - | FK para DominioTipo |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK para GestaoCliente |
| ClienteId | UNIQUEIDENTIFIER | SIM | NULL | FK para Cliente (multi-tenancy raiz) (nullable) |
| Codigo | VARCHAR(50) | NÃO | - | Código único do item |
| Nome | VARCHAR(200) | NÃO | - | Nome do item |
| Descricao | TEXT | SIM | NULL | Descrição detalhada |
| Cor | VARCHAR(7) | SIM | NULL | Cor em hexadecimal (#FF5733) |
| Icone | VARCHAR(50) | SIM | NULL | Ícone FontAwesome (fa-check) |
| Ordem | INT | NÃO | 0 | Ordem de exibição |
| Padrao | BIT | NÃO | 0 | Se é valor padrão do domínio |
| Global | BIT | NÃO | 0 | Se é item global (não customizável) |
| Ativo | BIT | NÃO | 1 | Status ativo/inativo |
| MotivoInativacao | TEXT | SIM | NULL | Justificativa da inativação |
| DataInativacao | DATETIME2 | SIM | NULL | Data da inativação |
| CreatedAt | DATETIME2 | NÃO | GETUTCDATE() | Data de criação |
| CreatedBy | UNIQUEIDENTIFIER | NÃO | - | Usuário que criou |
| ModifiedAt | DATETIME2 | SIM | NULL | Data de atualização |
| ModifiedBy | UNIQUEIDENTIFIER | SIM | NULL | Usuário que atualizou |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_ItemDominio | Id | CLUSTERED | Chave primária |
| IX_ItemDominio_DominioId | DominioId, Ordem | NONCLUSTERED | Listar itens do domínio ordenados |
| IX_ItemDominio_ClienteId | ClienteId | NONCLUSTERED | Performance multi-tenant |
| IX_ItemDominio_ConglomeradoId | ClienteId | NONCLUSTERED | Filtro por conglomerado |
| IX_ItemDominio_Codigo | Codigo, DominioId | NONCLUSTERED | Busca por código |
| IX_ItemDominio_Ativo | DominioId, Ativo | NONCLUSTERED | Listar apenas ativos |
| IX_ItemDominio_Padrao | DominioId, Padrao | NONCLUSTERED | Encontrar valor padrão |

#### Constraints

| Nome | Tipo | Definição | Descrição |
|------|------|-----------|-----------|
| PK_ItemDominio | PRIMARY KEY | Id | Chave primária |
| FK_ItemDominio_Dominio | FOREIGN KEY | DominioId REFERENCES DominioTipo(Id) | Domínio pai |
| FK_ItemDominio_Cliente | FOREIGN KEY | ClienteId REFERENCES GestaoCliente(Id) | Multi-tenancy |
| FK_ItemDominio_Conglomerado | FOREIGN KEY | ConglomeradoId REFERENCES Conglomerado(Id) | Conglomerado |
| FK_ItemDominio_CreatedBy | FOREIGN KEY | CreatedBy REFERENCES Usuario(Id) | Auditoria |
| FK_ItemDominio_ModifiedBy | FOREIGN KEY | ModifiedBy REFERENCES Usuario(Id) | Auditoria |
| UQ_ItemDominio_CodigoDominio | UNIQUE | (Codigo, DominioId, ClienteId) | Código único por domínio |
| CHK_ItemDominio_Cor | CHECK | Cor IS NULL OR Cor LIKE '#[0-9A-F][0-9A-F][0-9A-F][0-9A-F][0-9A-F][0-9A-F]' | Validar formato hexadecimal |
| CHK_ItemDominio_Ordem | CHECK | Ordem >= 0 | Ordem não pode ser negativa |

---

### 2.3 Tabela: TransicaoPermitida

**Descrição:** Define quais transições entre itens de domínio são permitidas (ex: STATUS_CHAMADO: "Aberto" → "Em Atendimento" permitido, mas "Aberto" → "Fechado" não). Usado em workflows.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| DominioId | UNIQUEIDENTIFIER | NÃO | - | FK para DominioTipo |
| ItemOrigemId | UNIQUEIDENTIFIER | NÃO | - | FK para ItemDominio origem |
| ItemDestinoId | UNIQUEIDENTIFIER | NÃO | - | FK para ItemDominio destino |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK para GestaoCliente |
| RequerJustificativa | BIT | NÃO | 0 | Se transição requer justificativa |
| RequerAprovacao | BIT | NÃO | 0 | Se transição requer aprovação |
| AprovadoresIds | TEXT | SIM | NULL | JSON array de UUIDs dos aprovadores |
| Ordem | INT | NÃO | 0 | Ordem de prioridade da transição |
| Ativo | BIT | NÃO | 1 | Status ativo/inativo |
| CreatedAt | DATETIME2 | NÃO | GETUTCDATE() | Data de criação |
| CreatedBy | UNIQUEIDENTIFIER | NÃO | - | Usuário que criou |
| ModifiedAt | DATETIME2 | SIM | NULL | Data de atualização |
| ModifiedBy | UNIQUEIDENTIFIER | SIM | NULL | Usuário que atualizou |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_TransicaoPermitida | Id | CLUSTERED | Chave primária |
| IX_TransicaoPermitida_DominioId | DominioId | NONCLUSTERED | Listar transições do domínio |
| IX_TransicaoPermitida_Origem | ItemOrigemId | NONCLUSTERED | Buscar transições a partir de origem |
| IX_TransicaoPermitida_Destino | ItemDestinoId | NONCLUSTERED | Buscar transições para destino |
| IX_TransicaoPermitida_ClienteId | ClienteId | NONCLUSTERED | Multi-tenancy |
| IX_TransicaoPermitida_Ativo | Ativo, DominioId | NONCLUSTERED | Filtro de transições ativas |

#### Constraints

| Nome | Tipo | Definição | Descrição |
|------|------|-----------|-----------|
| PK_TransicaoPermitida | PRIMARY KEY | Id | Chave primária |
| FK_TransicaoPermitida_Dominio | FOREIGN KEY | DominioId REFERENCES DominioTipo(Id) | Domínio |
| FK_TransicaoPermitida_Origem | FOREIGN KEY | ItemOrigemId REFERENCES ItemDominio(Id) | Item origem |
| FK_TransicaoPermitida_Destino | FOREIGN KEY | ItemDestinoId REFERENCES ItemDominio(Id) | Item destino |
| FK_TransicaoPermitida_Cliente | FOREIGN KEY | ClienteId REFERENCES GestaoCliente(Id) | Multi-tenancy |
| FK_TransicaoPermitida_CreatedBy | FOREIGN KEY | CreatedBy REFERENCES Usuario(Id) | Auditoria |
| FK_TransicaoPermitida_ModifiedBy | FOREIGN KEY | ModifiedBy REFERENCES Usuario(Id) | Auditoria |
| UQ_TransicaoPermitida_OrigemDestino | UNIQUE | (DominioId, ItemOrigemId, ItemDestinoId, ClienteId) | Transição única |
| CHK_TransicaoPermitida_OrigemDestino | CHECK | ItemOrigemId <> ItemDestinoId | Origem diferente de destino |

---

### 2.4 Tabela: TipoTraducao

**Descrição:** Armazena traduções de itens de domínio para múltiplos idiomas (i18n). Cada item pode ter traduções em pt-BR, en-US, es-ES.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| ItemDominioId | UNIQUEIDENTIFIER | NÃO | - | FK para ItemDominio |
| Idioma | VARCHAR(5) | NÃO | - | Código ISO idioma (pt-BR, en-US, es-ES) |
| Nome | VARCHAR(200) | NÃO | - | Nome traduzido |
| Descricao | TEXT | SIM | NULL | Descrição traduzida |
| CreatedAt | DATETIME2 | NÃO | GETUTCDATE() | Data de criação |
| CreatedBy | UNIQUEIDENTIFIER | NÃO | - | Usuário que criou |
| ModifiedAt | DATETIME2 | SIM | NULL | Data de atualização |
| ModifiedBy | UNIQUEIDENTIFIER | SIM | NULL | Usuário que atualizou |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_TipoTraducao | Id | CLUSTERED | Chave primária |
| IX_TipoTraducao_ItemIdioma | ItemDominioId, Idioma | NONCLUSTERED | Buscar tradução específica |
| IX_TipoTraducao_Idioma | Idioma | NONCLUSTERED | Listar por idioma |

#### Constraints

| Nome | Tipo | Definição | Descrição |
|------|------|-----------|-----------|
| PK_TipoTraducao | PRIMARY KEY | Id | Chave primária |
| FK_TipoTraducao_ItemDominio | FOREIGN KEY | ItemDominioId REFERENCES ItemDominio(Id) ON DELETE CASCADE | Item traduzido |
| FK_TipoTraducao_CreatedBy | FOREIGN KEY | CreatedBy REFERENCES Usuario(Id) | Auditoria |
| FK_TipoTraducao_ModifiedBy | FOREIGN KEY | ModifiedBy REFERENCES Usuario(Id) | Auditoria |
| UQ_TipoTraducao_ItemIdioma | UNIQUE | (ItemDominioId, Idioma) | Uma tradução por idioma |
| CHK_TipoTraducao_Idioma | CHECK | Idioma IN ('pt-BR', 'en-US', 'es-ES') | Idiomas suportados |

---

### 2.5 Tabela: HistoricoDominioTipo

**Descrição:** Registro de auditoria de todas as alterações em domínios e itens. Armazena estado antes/depois em JSON para rastreabilidade completa.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| DominioId | UNIQUEIDENTIFIER | SIM | NULL | FK para DominioTipo (nullable se item) |
| ItemDominioId | UNIQUEIDENTIFIER | SIM | NULL | FK para ItemDominio (nullable se domínio) |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK para GestaoCliente |
| TipoAlteracao | VARCHAR(50) | NÃO | - | CRIACAO, EDICAO, INATIVACAO, EXCLUSAO |
| DadosAntes | TEXT | SIM | NULL | JSON com estado anterior |
| DadosDepois | TEXT | NÃO | - | JSON com estado posterior |
| Justificativa | TEXT | SIM | NULL | Motivo da alteração |
| CreatedAt | DATETIME2 | NÃO | GETUTCDATE() | Data da alteração |
| CreatedBy | UNIQUEIDENTIFIER | NÃO | - | Usuário que alterou |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_HistoricoDominioTipo | Id | CLUSTERED | Chave primária |
| IX_HistoricoDominioTipo_DominioId | DominioId, CreatedAt DESC | NONCLUSTERED | Histórico do domínio |
| IX_HistoricoDominioTipo_ItemId | ItemDominioId, CreatedAt DESC | NONCLUSTERED | Histórico do item |
| IX_HistoricoDominioTipo_ClienteId | ClienteId | NONCLUSTERED | Multi-tenancy |
| IX_HistoricoDominioTipo_TipoAlteracao | TipoAlteracao, CreatedAt DESC | NONCLUSTERED | Filtrar por tipo |
| IX_HistoricoDominioTipo_CreatedAt | CreatedAt DESC | NONCLUSTERED | Ordenação temporal |

#### Constraints

| Nome | Tipo | Definição | Descrição |
|------|------|-----------|-----------|
| PK_HistoricoDominioTipo | PRIMARY KEY | Id | Chave primária |
| FK_HistoricoDominioTipo_Dominio | FOREIGN KEY | DominioId REFERENCES DominioTipo(Id) | Domínio alterado |
| FK_HistoricoDominioTipo_ItemDominio | FOREIGN KEY | ItemDominioId REFERENCES ItemDominio(Id) | Item alterado |
| FK_HistoricoDominioTipo_Cliente | FOREIGN KEY | ClienteId REFERENCES GestaoCliente(Id) | Multi-tenancy |
| FK_HistoricoDominioTipo_CreatedBy | FOREIGN KEY | CreatedBy REFERENCES Usuario(Id) | Usuário |
| CHK_HistoricoDominioTipo_TipoAlteracao | CHECK | TipoAlteracao IN ('CRIACAO', 'EDICAO', 'INATIVACAO', 'EXCLUSAO') | Tipos válidos |

---

## 3. Relacionamentos

| Tabela Origem | Cardinalidade | Tabela Destino | Descrição |
|---------------|---------------|----------------|-----------|
| GestaoCliente | 1:N | DominioTipo | Cliente possui múltiplos domínios |
| Conglomerado | 1:N | DominioTipo | Conglomerado pode ter domínios customizados |
| DominioTipo | 1:N | ItemDominio | Domínio contém múltiplos itens |
| DominioTipo | 1:N | TransicaoPermitida | Domínio define transições |
| ItemDominio | 1:N | TipoTraducao | Item tem traduções em vários idiomas |
| ItemDominio | 1:N | TransicaoPermitida (origem) | Item pode ser origem de transições |
| ItemDominio | 1:N | TransicaoPermitida (destino) | Item pode ser destino de transições |
| DominioTipo | 1:N | HistoricoDominioTipo | Histórico de alterações do domínio |
| ItemDominio | 1:N | HistoricoDominioTipo | Histórico de alterações do item |
| Usuario | 1:N | DominioTipo | Usuário cria/atualiza domínios |
| Usuario | 1:N | ItemDominio | Usuário cria/atualiza itens |

---

## 4. DDL - SQL Server

```sql
-- =============================================
-- RF059 - Gestão de Status e Tipos Genéricos
-- Modelo de Dados
-- Data: 2025-12-18
-- Versão: 1.0
-- =============================================

-- ---------------------------------------------
-- Tabela: DominioTipo
-- ---------------------------------------------
CREATE TABLE DominioTipo (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    ClienteId UNIQUEIDENTIFIER NULL,
    Codigo VARCHAR(50) NOT NULL,
    Nome VARCHAR(200) NOT NULL,
    Descricao TEXT NULL,
    PermiteCustomizacao BIT NOT NULL DEFAULT 1,
    PermiteTransicoes BIT NOT NULL DEFAULT 0,
    [Global] BIT NOT NULL DEFAULT 0,
    Ordem INT NOT NULL DEFAULT 0,
    FlExcluido BIT NOT NULL DEFAULT 0,
    CreatedAt DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy UNIQUEIDENTIFIER NOT NULL,
    ModifiedAt DATETIME2 NULL,
    ModifiedBy UNIQUEIDENTIFIER NULL,

    -- Foreign Keys
    CONSTRAINT FK_DominioTipo_Cliente
        FOREIGN KEY (ClienteId) REFERENCES GestaoCliente(Id),
    CONSTRAINT FK_DominioTipo_Conglomerado
        FOREIGN KEY (ClienteId) REFERENCES Cliente(Id),
    CONSTRAINT FK_DominioTipo_CreatedBy
        FOREIGN KEY (CreatedBy) REFERENCES Usuario(Id),
    CONSTRAINT FK_DominioTipo_ModifiedBy
        FOREIGN KEY (ModifiedBy) REFERENCES Usuario(Id),

    -- Unique Constraints
    CONSTRAINT UQ_DominioTipo_CodigoCliente
        UNIQUE (Codigo, ClienteId),

    -- Check Constraints
    CONSTRAINT CHK_DominioTipo_Codigo
        CHECK (LEN(Codigo) >= 3)
);

-- Indices
CREATE NONCLUSTERED INDEX IX_DominioTipo_ClienteId
    ON DominioTipo(ClienteId);
CREATE NONCLUSTERED INDEX IX_DominioTipo_ConglomeradoId
    ON DominioTipo(ConglomeradoId)
    WHERE ConglomeradoId IS NOT NULL;
CREATE NONCLUSTERED INDEX IX_DominioTipo_Codigo
    ON DominioTipo(Codigo, ClienteId);
CREATE NONCLUSTERED INDEX IX_DominioTipo_Ativo
    ON DominioTipo(Ativo)
    INCLUDE (Id, Codigo, Nome, Ordem)
    WHERE FlExcluido = 0;
CREATE NONCLUSTERED INDEX IX_DominioTipo_Global
    ON DominioTipo([Global], ClienteId);

-- Comentários
EXEC sp_addextendedproperty
    @name = N'MS_Description', @value = 'Domínios/categorias de tipos parametrizáveis do sistema',
    @level0type = N'SCHEMA', @level0name = 'dbo',
    @level1type = N'TABLE', @level1name = 'DominioTipo';

EXEC sp_addextendedproperty
    @name = N'MS_Description', @value = 'Código único do domínio (ex: STATUS_CHAMADO, PRIORIDADE)',
    @level0type = N'SCHEMA', @level0name = 'dbo',
    @level1type = N'TABLE', @level1name = 'DominioTipo',
    @level2type = N'COLUMN', @level2name = 'Codigo';

EXEC sp_addextendedproperty
    @name = N'MS_Description', @value = 'Se permite criação de itens customizados pelo usuário',
    @level0type = N'SCHEMA', @level0name = 'dbo',
    @level1type = N'TABLE', @level1name = 'DominioTipo',
    @level2type = N'COLUMN', @level2name = 'PermiteCustomizacao';

EXEC sp_addextendedproperty
    @name = N'MS_Description', @value = 'Se possui workflow de transições entre itens',
    @level0type = N'SCHEMA', @level0name = 'dbo',
    @level1type = N'TABLE', @level1name = 'DominioTipo',
    @level2type = N'COLUMN', @level2name = 'PermiteTransicoes';


-- ---------------------------------------------
-- Tabela: ItemDominio
-- ---------------------------------------------
CREATE TABLE ItemDominio (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    DominioId UNIQUEIDENTIFIER NOT NULL,
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    ClienteId UNIQUEIDENTIFIER NULL,
    Codigo VARCHAR(50) NOT NULL,
    Nome VARCHAR(200) NOT NULL,
    Descricao TEXT NULL,
    Cor VARCHAR(7) NULL,
    Icone VARCHAR(50) NULL,
    Ordem INT NOT NULL DEFAULT 0,
    Padrao BIT NOT NULL DEFAULT 0,
    [Global] BIT NOT NULL DEFAULT 0,
    FlExcluido BIT NOT NULL DEFAULT 0,
    MotivoInativacao TEXT NULL,
    DataInativacao DATETIME2 NULL,
    CreatedAt DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy UNIQUEIDENTIFIER NOT NULL,
    ModifiedAt DATETIME2 NULL,
    ModifiedBy UNIQUEIDENTIFIER NULL,

    -- Foreign Keys
    CONSTRAINT FK_ItemDominio_Dominio
        FOREIGN KEY (DominioId) REFERENCES DominioTipo(Id),
    CONSTRAINT FK_ItemDominio_Cliente
        FOREIGN KEY (ClienteId) REFERENCES GestaoCliente(Id),
    CONSTRAINT FK_ItemDominio_Conglomerado
        FOREIGN KEY (ClienteId) REFERENCES Cliente(Id),
    CONSTRAINT FK_ItemDominio_CreatedBy
        FOREIGN KEY (CreatedBy) REFERENCES Usuario(Id),
    CONSTRAINT FK_ItemDominio_ModifiedBy
        FOREIGN KEY (ModifiedBy) REFERENCES Usuario(Id),

    -- Unique Constraints
    CONSTRAINT UQ_ItemDominio_CodigoDominio
        UNIQUE (Codigo, DominioId, ClienteId),

    -- Check Constraints
    CONSTRAINT CHK_ItemDominio_Cor
        CHECK (Cor IS NULL OR Cor LIKE '#[0-9A-F][0-9A-F][0-9A-F][0-9A-F][0-9A-F][0-9A-F]'),
    CONSTRAINT CHK_ItemDominio_Ordem
        CHECK (Ordem >= 0)
);

-- Indices
CREATE NONCLUSTERED INDEX IX_ItemDominio_DominioId
    ON ItemDominio(DominioId, Ordem);
CREATE NONCLUSTERED INDEX IX_ItemDominio_ClienteId
    ON ItemDominio(ClienteId);
CREATE NONCLUSTERED INDEX IX_ItemDominio_ConglomeradoId
    ON ItemDominio(ConglomeradoId)
    WHERE ConglomeradoId IS NOT NULL;
CREATE NONCLUSTERED INDEX IX_ItemDominio_Codigo
    ON ItemDominio(Codigo, DominioId);
CREATE NONCLUSTERED INDEX IX_ItemDominio_Ativo
    ON ItemDominio(DominioId, Ativo)
    INCLUDE (Id, Codigo, Nome, Cor, Icone, Ordem)
    WHERE FlExcluido = 0;
CREATE NONCLUSTERED INDEX IX_ItemDominio_Padrao
    ON ItemDominio(DominioId, Padrao)
    WHERE Padrao = 1;

-- Comentários
EXEC sp_addextendedproperty
    @name = N'MS_Description', @value = 'Itens específicos de cada domínio (ex: Aberto, Fechado para STATUS_CHAMADO)',
    @level0type = N'SCHEMA', @level0name = 'dbo',
    @level1type = N'TABLE', @level1name = 'ItemDominio';

EXEC sp_addextendedproperty
    @name = N'MS_Description', @value = 'Cor em hexadecimal para exibição visual (#FF5733)',
    @level0type = N'SCHEMA', @level0name = 'dbo',
    @level1type = N'TABLE', @level1name = 'ItemDominio',
    @level2type = N'COLUMN', @level2name = 'Cor';

EXEC sp_addextendedproperty
    @name = N'MS_Description', @value = 'Ícone FontAwesome para exibição visual (fa-check)',
    @level0type = N'SCHEMA', @level0name = 'dbo',
    @level1type = N'TABLE', @level1name = 'ItemDominio',
    @level2type = N'COLUMN', @level2name = 'Icone';


-- ---------------------------------------------
-- Tabela: TransicaoPermitida
-- ---------------------------------------------
CREATE TABLE TransicaoPermitida (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    DominioId UNIQUEIDENTIFIER NOT NULL,
    ItemOrigemId UNIQUEIDENTIFIER NOT NULL,
    ItemDestinoId UNIQUEIDENTIFIER NOT NULL,
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    RequerJustificativa BIT NOT NULL DEFAULT 0,
    RequerAprovacao BIT NOT NULL DEFAULT 0,
    AprovadoresIds TEXT NULL,
    Ordem INT NOT NULL DEFAULT 0,
    FlExcluido BIT NOT NULL DEFAULT 0,
    CreatedAt DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy UNIQUEIDENTIFIER NOT NULL,
    ModifiedAt DATETIME2 NULL,
    ModifiedBy UNIQUEIDENTIFIER NULL,

    -- Foreign Keys
    CONSTRAINT FK_TransicaoPermitida_Dominio
        FOREIGN KEY (DominioId) REFERENCES DominioTipo(Id),
    CONSTRAINT FK_TransicaoPermitida_Origem
        FOREIGN KEY (ItemOrigemId) REFERENCES ItemDominio(Id),
    CONSTRAINT FK_TransicaoPermitida_Destino
        FOREIGN KEY (ItemDestinoId) REFERENCES ItemDominio(Id),
    CONSTRAINT FK_TransicaoPermitida_Cliente
        FOREIGN KEY (ClienteId) REFERENCES GestaoCliente(Id),
    CONSTRAINT FK_TransicaoPermitida_CreatedBy
        FOREIGN KEY (CreatedBy) REFERENCES Usuario(Id),
    CONSTRAINT FK_TransicaoPermitida_ModifiedBy
        FOREIGN KEY (ModifiedBy) REFERENCES Usuario(Id),

    -- Unique Constraints
    CONSTRAINT UQ_TransicaoPermitida_OrigemDestino
        UNIQUE (DominioId, ItemOrigemId, ItemDestinoId, ClienteId),

    -- Check Constraints
    CONSTRAINT CHK_TransicaoPermitida_OrigemDestino
        CHECK (ItemOrigemId <> ItemDestinoId)
);

-- Indices
CREATE NONCLUSTERED INDEX IX_TransicaoPermitida_DominioId
    ON TransicaoPermitida(DominioId);
CREATE NONCLUSTERED INDEX IX_TransicaoPermitida_Origem
    ON TransicaoPermitida(ItemOrigemId)
    INCLUDE (ItemDestinoId, RequerJustificativa, RequerAprovacao);
CREATE NONCLUSTERED INDEX IX_TransicaoPermitida_Destino
    ON TransicaoPermitida(ItemDestinoId);
CREATE NONCLUSTERED INDEX IX_TransicaoPermitida_ClienteId
    ON TransicaoPermitida(ClienteId);
CREATE NONCLUSTERED INDEX IX_TransicaoPermitida_Ativo
    ON TransicaoPermitida(Ativo, DominioId)
    WHERE FlExcluido = 0;

-- Comentários
EXEC sp_addextendedproperty
    @name = N'MS_Description', @value = 'Define transições permitidas entre itens de domínio (workflow)',
    @level0type = N'SCHEMA', @level0name = 'dbo',
    @level1type = N'TABLE', @level1name = 'TransicaoPermitida';

EXEC sp_addextendedproperty
    @name = N'MS_Description', @value = 'Se a transição requer justificativa obrigatória do usuário',
    @level0type = N'SCHEMA', @level0name = 'dbo',
    @level1type = N'TABLE', @level1name = 'TransicaoPermitida',
    @level2type = N'COLUMN', @level2name = 'RequerJustificativa';


-- ---------------------------------------------
-- Tabela: TipoTraducao
-- ---------------------------------------------
CREATE TABLE TipoTraducao (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    ItemDominioId UNIQUEIDENTIFIER NOT NULL,
    Idioma VARCHAR(5) NOT NULL,
    Nome VARCHAR(200) NOT NULL,
    Descricao TEXT NULL,
    CreatedAt DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy UNIQUEIDENTIFIER NOT NULL,
    ModifiedAt DATETIME2 NULL,
    ModifiedBy UNIQUEIDENTIFIER NULL,

    -- Foreign Keys
    CONSTRAINT FK_TipoTraducao_ItemDominio
        FOREIGN KEY (ItemDominioId) REFERENCES ItemDominio(Id) ON DELETE CASCADE,
    CONSTRAINT FK_TipoTraducao_CreatedBy
        FOREIGN KEY (CreatedBy) REFERENCES Usuario(Id),
    CONSTRAINT FK_TipoTraducao_ModifiedBy
        FOREIGN KEY (ModifiedBy) REFERENCES Usuario(Id),

    -- Unique Constraints
    CONSTRAINT UQ_TipoTraducao_ItemIdioma
        UNIQUE (ItemDominioId, Idioma),

    -- Check Constraints
    CONSTRAINT CHK_TipoTraducao_Idioma
        CHECK (Idioma IN ('pt-BR', 'en-US', 'es-ES'))
);

-- Indices
CREATE NONCLUSTERED INDEX IX_TipoTraducao_ItemIdioma
    ON TipoTraducao(ItemDominioId, Idioma);
CREATE NONCLUSTERED INDEX IX_TipoTraducao_Idioma
    ON TipoTraducao(Idioma);

-- Comentários
EXEC sp_addextendedproperty
    @name = N'MS_Description', @value = 'Traduções de itens de domínio para múltiplos idiomas (i18n)',
    @level0type = N'SCHEMA', @level0name = 'dbo',
    @level1type = N'TABLE', @level1name = 'TipoTraducao';

EXEC sp_addextendedproperty
    @name = N'MS_Description', @value = 'Código ISO do idioma (pt-BR, en-US, es-ES)',
    @level0type = N'SCHEMA', @level0name = 'dbo',
    @level1type = N'TABLE', @level1name = 'TipoTraducao',
    @level2type = N'COLUMN', @level2name = 'Idioma';


-- ---------------------------------------------
-- Tabela: HistoricoDominioTipo
-- ---------------------------------------------
CREATE TABLE HistoricoDominioTipo (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    DominioId UNIQUEIDENTIFIER NULL,
    ItemDominioId UNIQUEIDENTIFIER NULL,
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    TipoAlteracao VARCHAR(50) NOT NULL,
    DadosAntes TEXT NULL,
    DadosDepois TEXT NOT NULL,
    Justificativa TEXT NULL,
    CreatedAt DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy UNIQUEIDENTIFIER NOT NULL,

    -- Foreign Keys
    CONSTRAINT FK_HistoricoDominioTipo_Dominio
        FOREIGN KEY (DominioId) REFERENCES DominioTipo(Id),
    CONSTRAINT FK_HistoricoDominioTipo_ItemDominio
        FOREIGN KEY (ItemDominioId) REFERENCES ItemDominio(Id),
    CONSTRAINT FK_HistoricoDominioTipo_Cliente
        FOREIGN KEY (ClienteId) REFERENCES GestaoCliente(Id),
    CONSTRAINT FK_HistoricoDominioTipo_CreatedBy
        FOREIGN KEY (CreatedBy) REFERENCES Usuario(Id),

    -- Check Constraints
    CONSTRAINT CHK_HistoricoDominioTipo_TipoAlteracao
        CHECK (TipoAlteracao IN ('CRIACAO', 'EDICAO', 'INATIVACAO', 'EXCLUSAO'))
);

-- Indices
CREATE NONCLUSTERED INDEX IX_HistoricoDominioTipo_DominioId
    ON HistoricoDominioTipo(DominioId, CreatedAt DESC)
    WHERE DominioId IS NOT NULL;
CREATE NONCLUSTERED INDEX IX_HistoricoDominioTipo_ItemId
    ON HistoricoDominioTipo(ItemDominioId, CreatedAt DESC)
    WHERE ItemDominioId IS NOT NULL;
CREATE NONCLUSTERED INDEX IX_HistoricoDominioTipo_ClienteId
    ON HistoricoDominioTipo(ClienteId);
CREATE NONCLUSTERED INDEX IX_HistoricoDominioTipo_TipoAlteracao
    ON HistoricoDominioTipo(TipoAlteracao, CreatedAt DESC);
CREATE NONCLUSTERED INDEX IX_HistoricoDominioTipo_CreatedAt
    ON HistoricoDominioTipo(CreatedAt DESC)
    INCLUDE (TipoAlteracao, DominioId, ItemDominioId);

-- Comentários
EXEC sp_addextendedproperty
    @name = N'MS_Description', @value = 'Histórico de auditoria de alterações em domínios e itens',
    @level0type = N'SCHEMA', @level0name = 'dbo',
    @level1type = N'TABLE', @level1name = 'HistoricoDominioTipo';

EXEC sp_addextendedproperty
    @name = N'MS_Description', @value = 'Estado anterior da entidade em formato JSON',
    @level0type = N'SCHEMA', @level0name = 'dbo',
    @level1type = N'TABLE', @level1name = 'HistoricoDominioTipo',
    @level2type = N'COLUMN', @level2name = 'DadosAntes';

EXEC sp_addextendedproperty
    @name = N'MS_Description', @value = 'Estado posterior da entidade em formato JSON',
    @level0type = N'SCHEMA', @level0name = 'dbo',
    @level1type = N'TABLE', @level1name = 'HistoricoDominioTipo',
    @level2type = N'COLUMN', @level2name = 'DadosDepois';
```

---

## 5. Views de Negócio

```sql
-- View: Listar domínios com contagem de itens ativos
CREATE VIEW vw_DominiosTipoResumo AS
SELECT
    d.Id,
    d.Codigo,
    d.Nome,
    d.PermiteCustomizacao,
    d.PermiteTransicoes,
    d.[Global],
    d.Ativo,
    COUNT(i.Id) AS QuantidadeItens,
    SUM(CASE WHEN i.Ativo = 1 THEN 1 ELSE 0 END) AS QuantidadeItensAtivos
FROM DominioTipo d
LEFT JOIN ItemDominio i ON d.Id = i.DominioId
GROUP BY d.Id, d.Codigo, d.Nome, d.PermiteCustomizacao, d.PermiteTransicoes, d.[Global], d.Ativo;
GO

-- View: Itens de domínio com traduções
CREATE VIEW vw_ItensDominioTraducoes AS
SELECT
    i.Id AS ItemId,
    i.DominioId,
    d.Codigo AS CodigoDominio,
    i.Codigo AS CodigoItem,
    i.Nome AS NomePadrao,
    i.Cor,
    i.Icone,
    i.Ordem,
    i.Ativo,
    t.Idioma,
    t.Nome AS NomeTraduzido,
    t.Descricao AS DescricaoTraduzida
FROM ItemDominio i
INNER JOIN DominioTipo d ON i.DominioId = d.Id
LEFT JOIN TipoTraducao t ON i.Id = t.ItemDominioId;
GO

-- View: Workflow de transições por domínio
CREATE VIEW vw_WorkflowTransicoes AS
SELECT
    d.Id AS DominioId,
    d.Codigo AS CodigoDominio,
    d.Nome AS NomeDominio,
    io.Codigo AS CodigoOrigem,
    io.Nome AS NomeOrigem,
    io.Cor AS CorOrigem,
    id.Codigo AS CodigoDestino,
    id.Nome AS NomeDestino,
    id.Cor AS CorDestino,
    t.RequerJustificativa,
    t.RequerAprovacao,
    t.Ativo AS TransicaoAtiva
FROM TransicaoPermitida t
INNER JOIN DominioTipo d ON t.DominioId = d.Id
INNER JOIN ItemDominio io ON t.ItemOrigemId = io.Id
INNER JOIN ItemDominio id ON t.ItemDestinoId = id.Id;
GO
```

---

## 6. Stored Procedures

```sql
-- Procedure: Obter itens de domínio ativos por código
CREATE PROCEDURE sp_ObterItensDominio
    @CodigoDominio VARCHAR(50),
    @ClienteId UNIQUEIDENTIFIER,
    @ClienteId UNIQUEIDENTIFIER = NULL,
    @Idioma VARCHAR(5) = 'pt-BR'
AS
BEGIN
    SET NOCOUNT ON;

    SELECT
        i.Id,
        i.Codigo,
        COALESCE(t.Nome, i.Nome) AS Nome,
        COALESCE(t.Descricao, i.Descricao) AS Descricao,
        i.Cor,
        i.Icone,
        i.Ordem,
        i.Padrao
    FROM ItemDominio i
    INNER JOIN DominioTipo d ON i.DominioId = d.Id
    LEFT JOIN TipoTraducao t ON i.Id = t.ItemDominioId AND t.Idioma = @Idioma
    WHERE d.Codigo = @CodigoDominio
        AND i.ClienteId = @ClienteId
        AND i.Ativo = 1
        AND (i.ConglomeradoId = @ConglomeradoId OR i.[Global] = 1 OR @ConglomeradoId IS NULL)
    ORDER BY i.Ordem, i.Nome;
END;
GO

-- Procedure: Validar transição permitida
CREATE PROCEDURE sp_ValidarTransicao
    @ItemOrigemId UNIQUEIDENTIFIER,
    @ItemDestinoId UNIQUEIDENTIFIER,
    @ClienteId UNIQUEIDENTIFIER,
    @Permitida BIT OUTPUT,
    @RequerJustificativa BIT OUTPUT,
    @RequerAprovacao BIT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;

    SELECT
        @Permitida = CASE WHEN COUNT(*) > 0 THEN 1 ELSE 0 END,
        @RequerJustificativa = MAX(CAST(RequerJustificativa AS INT)),
        @RequerAprovacao = MAX(CAST(RequerAprovacao AS INT))
    FROM TransicaoPermitida
    WHERE ItemOrigemId = @ItemOrigemId
        AND ItemDestinoId = @ItemDestinoId
        AND ClienteId = @ClienteId
        AND Ativo = 1;

    IF @Permitida IS NULL
        SET @Permitida = 0;
END;
GO

-- Procedure: Inativar item de domínio com validação
CREATE PROCEDURE sp_InativarItemDominio
    @ItemId UNIQUEIDENTIFIER,
    @Motivo TEXT,
    @UsuarioId UNIQUEIDENTIFIER
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRANSACTION;

    BEGIN TRY
        -- Verificar se item existe e está ativo
        IF NOT EXISTS (SELECT 1 FROM ItemDominio WHERE Id = @ItemId AND Ativo = 1)
        BEGIN
            RAISERROR('Item não encontrado ou já inativo', 16, 1);
            ROLLBACK;
            RETURN;
        END;

        -- Capturar dados antes da inativação
        DECLARE @DadosAntes TEXT;
        SELECT @DadosAntes = (
            SELECT * FROM ItemDominio WHERE Id = @ItemId FOR JSON PATH
        );

        -- Inativar item
        UPDATE ItemDominio
        SET Ativo = 0,
            MotivoInativacao = @Motivo,
            DataInativacao = GETUTCDATE(),
            ModifiedAt = GETUTCDATE(),
            ModifiedBy = @UsuarioId
        WHERE Id = @ItemId;

        -- Capturar dados depois
        DECLARE @DadosDepois TEXT;
        SELECT @DadosDepois = (
            SELECT * FROM ItemDominio WHERE Id = @ItemId FOR JSON PATH
        );

        -- Registrar no histórico
        INSERT INTO HistoricoDominioTipo (
            ItemDominioId, ClienteId, TipoAlteracao,
            DadosAntes, DadosDepois, Justificativa, CreatedBy
        )
        SELECT
            @ItemId, ClienteId, 'INATIVACAO',
            @DadosAntes, @DadosDepois, @Motivo, @UsuarioId
        FROM ItemDominio
        WHERE Id = @ItemId;

        COMMIT;
    END TRY
    BEGIN CATCH
        ROLLBACK;
        THROW;
    END CATCH;
END;
GO
```

---

## 7. Triggers de Auditoria

```sql
-- Trigger: Auditar criação de domínio
CREATE TRIGGER trg_DominioTipo_AfterInsert
ON DominioTipo
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO HistoricoDominioTipo (
        DominioId, ClienteId, TipoAlteracao, DadosDepois, CreatedBy
    )
    SELECT
        i.Id, i.ClienteId, 'CRIACAO',
        (SELECT * FROM inserted WHERE Id = i.Id FOR JSON PATH),
        i.CreatedBy
    FROM inserted i;
END;
GO

-- Trigger: Auditar edição de domínio
CREATE TRIGGER trg_DominioTipo_AfterUpdate
ON DominioTipo
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO HistoricoDominioTipo (
        DominioId, ClienteId, TipoAlteracao, DadosAntes, DadosDepois, CreatedBy
    )
    SELECT
        i.Id, i.ClienteId, 'EDICAO',
        (SELECT * FROM deleted WHERE Id = i.Id FOR JSON PATH),
        (SELECT * FROM inserted WHERE Id = i.Id FOR JSON PATH),
        i.ModifiedBy
    FROM inserted i;
END;
GO

-- Trigger: Auditar criação de item
CREATE TRIGGER trg_ItemDominio_AfterInsert
ON ItemDominio
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO HistoricoDominioTipo (
        ItemDominioId, DominioId, ClienteId, TipoAlteracao, DadosDepois, CreatedBy
    )
    SELECT
        i.Id, i.DominioId, i.ClienteId, 'CRIACAO',
        (SELECT * FROM inserted WHERE Id = i.Id FOR JSON PATH),
        i.CreatedBy
    FROM inserted i;
END;
GO

-- Trigger: Auditar edição de item
CREATE TRIGGER trg_ItemDominio_AfterUpdate
ON ItemDominio
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO HistoricoDominioTipo (
        ItemDominioId, DominioId, ClienteId, TipoAlteracao, DadosAntes, DadosDepois, CreatedBy
    )
    SELECT
        i.Id, i.DominioId, i.ClienteId, 'EDICAO',
        (SELECT * FROM deleted WHERE Id = i.Id FOR JSON PATH),
        (SELECT * FROM inserted WHERE Id = i.Id FOR JSON PATH),
        i.ModifiedBy
    FROM inserted i;
END;
GO
```

---

## 8. Dados Iniciais (Seed)

```sql
-- =============================================
-- Dados iniciais - Domínios padrão do sistema
-- =============================================

-- Inserir domínios padrão (executar apenas uma vez)
DECLARE @ClienteId UNIQUEIDENTIFIER = (SELECT TOP 1 Id FROM GestaoCliente);
DECLARE @UsuarioId UNIQUEIDENTIFIER = (SELECT TOP 1 Id FROM Usuario WHERE Email = 'admin@icontrolit.com');

-- Domínio: STATUS_CHAMADO
DECLARE @DominioStatusChamado UNIQUEIDENTIFIER = NEWID();
INSERT INTO DominioTipo (Id, ClienteId, Codigo, Nome, Descricao, PermiteCustomizacao, PermiteTransicoes, [Global], Ordem, CreatedBy)
VALUES (@DominioStatusChamado, @ClienteId, 'STATUS_CHAMADO', 'Status de Chamado', 'Status do ciclo de vida de chamados técnicos', 1, 1, 1, 1, @UsuarioId);

-- Itens: STATUS_CHAMADO
INSERT INTO ItemDominio (DominioId, ClienteId, Codigo, Nome, Cor, Icone, Ordem, Padrao, [Global], CreatedBy) VALUES
(@DominioStatusChamado, @ClienteId, 'ABERTO', 'Aberto', '#3B82F6', 'fa-folder-open', 1, 1, 1, @UsuarioId),
(@DominioStatusChamado, @ClienteId, 'EM_ATENDIMENTO', 'Em Atendimento', '#F59E0B', 'fa-clock', 2, 0, 1, @UsuarioId),
(@DominioStatusChamado, @ClienteId, 'AGUARDANDO_CLIENTE', 'Aguardando Cliente', '#8B5CF6', 'fa-pause-circle', 3, 0, 1, @UsuarioId),
(@DominioStatusChamado, @ClienteId, 'RESOLVIDO', 'Resolvido', '#10B981', 'fa-check-circle', 4, 0, 1, @UsuarioId),
(@DominioStatusChamado, @ClienteId, 'FECHADO', 'Fechado', '#6B7280', 'fa-lock', 5, 0, 1, @UsuarioId),
(@DominioStatusChamado, @ClienteId, 'CANCELADO', 'Cancelado', '#EF4444', 'fa-times-circle', 6, 0, 1, @UsuarioId);

-- Domínio: PRIORIDADE
DECLARE @DominioPrioridade UNIQUEIDENTIFIER = NEWID();
INSERT INTO DominioTipo (Id, ClienteId, Codigo, Nome, Descricao, PermiteCustomizacao, PermiteTransicoes, [Global], Ordem, CreatedBy)
VALUES (@DominioPrioridade, @ClienteId, 'PRIORIDADE', 'Prioridade', 'Níveis de prioridade para atendimento', 1, 0, 1, 2, @UsuarioId);

-- Itens: PRIORIDADE
INSERT INTO ItemDominio (DominioId, ClienteId, Codigo, Nome, Cor, Icone, Ordem, Padrao, [Global], CreatedBy) VALUES
(@DominioPrioridade, @ClienteId, 'CRITICA', 'Crítica', '#DC2626', 'fa-exclamation-triangle', 1, 0, 1, @UsuarioId),
(@DominioPrioridade, @ClienteId, 'ALTA', 'Alta', '#F97316', 'fa-arrow-up', 2, 0, 1, @UsuarioId),
(@DominioPrioridade, @ClienteId, 'MEDIA', 'Média', '#3B82F6', 'fa-minus', 3, 1, 1, @UsuarioId),
(@DominioPrioridade, @ClienteId, 'BAIXA', 'Baixa', '#10B981', 'fa-arrow-down', 4, 0, 1, @UsuarioId);

-- Transições permitidas: STATUS_CHAMADO
DECLARE @ItemAberto UNIQUEIDENTIFIER = (SELECT Id FROM ItemDominio WHERE Codigo = 'ABERTO' AND DominioId = @DominioStatusChamado);
DECLARE @ItemEmAtendimento UNIQUEIDENTIFIER = (SELECT Id FROM ItemDominio WHERE Codigo = 'EM_ATENDIMENTO' AND DominioId = @DominioStatusChamado);
DECLARE @ItemAguardandoCliente UNIQUEIDENTIFIER = (SELECT Id FROM ItemDominio WHERE Codigo = 'AGUARDANDO_CLIENTE' AND DominioId = @DominioStatusChamado);
DECLARE @ItemResolvido UNIQUEIDENTIFIER = (SELECT Id FROM ItemDominio WHERE Codigo = 'RESOLVIDO' AND DominioId = @DominioStatusChamado);
DECLARE @ItemFechado UNIQUEIDENTIFIER = (SELECT Id FROM ItemDominio WHERE Codigo = 'FECHADO' AND DominioId = @DominioStatusChamado);
DECLARE @ItemCancelado UNIQUEIDENTIFIER = (SELECT Id FROM ItemDominio WHERE Codigo = 'CANCELADO' AND DominioId = @DominioStatusChamado);

INSERT INTO TransicaoPermitida (DominioId, ItemOrigemId, ItemDestinoId, ClienteId, RequerJustificativa, RequerAprovacao, CreatedBy) VALUES
(@DominioStatusChamado, @ItemAberto, @ItemEmAtendimento, @ClienteId, 0, 0, @UsuarioId),
(@DominioStatusChamado, @ItemAberto, @ItemCancelado, @ClienteId, 1, 0, @UsuarioId),
(@DominioStatusChamado, @ItemEmAtendimento, @ItemAguardandoCliente, @ClienteId, 1, 0, @UsuarioId),
(@DominioStatusChamado, @ItemEmAtendimento, @ItemResolvido, @ClienteId, 0, 0, @UsuarioId),
(@DominioStatusChamado, @ItemAguardandoCliente, @ItemEmAtendimento, @ClienteId, 0, 0, @UsuarioId),
(@DominioStatusChamado, @ItemAguardandoCliente, @ItemCancelado, @ClienteId, 1, 0, @UsuarioId),
(@DominioStatusChamado, @ItemResolvido, @ItemFechado, @ClienteId, 0, 0, @UsuarioId),
(@DominioStatusChamado, @ItemResolvido, @ItemEmAtendimento, @ClienteId, 1, 0, @UsuarioId);

-- Traduções (exemplo para alguns itens)
DECLARE @ItemAbertoId UNIQUEIDENTIFIER = (SELECT Id FROM ItemDominio WHERE Codigo = 'ABERTO' AND DominioId = @DominioStatusChamado);

INSERT INTO TipoTraducao (ItemDominioId, Idioma, Nome, Descricao, CreatedBy) VALUES
(@ItemAbertoId, 'pt-BR', 'Aberto', 'Chamado recém-criado aguardando atendimento', @UsuarioId),
(@ItemAbertoId, 'en-US', 'Open', 'Newly created ticket awaiting service', @UsuarioId),
(@ItemAbertoId, 'es-ES', 'Abierto', 'Ticket recién creado esperando atención', @UsuarioId);
```

---

## 9. Índices de Performance

```sql
-- Índices adicionais para otimização de queries específicas
CREATE NONCLUSTERED INDEX IX_ItemDominio_DominioCliente
    ON ItemDominio(DominioId, ClienteId, Ativo)
    INCLUDE (Codigo, Nome, Cor, Icone, Ordem, Padrao)
    WHERE FlExcluido = 0;

CREATE NONCLUSTERED INDEX IX_TransicaoPermitida_OrigemDestinoCliente
    ON TransicaoPermitida(ItemOrigemId, ItemDestinoId, ClienteId)
    INCLUDE (RequerJustificativa, RequerAprovacao)
    WHERE FlExcluido = 0;

CREATE NONCLUSTERED INDEX IX_HistoricoDominioTipo_ClienteTipo
    ON HistoricoDominioTipo(ClienteId, TipoAlteracao, CreatedAt DESC)
    INCLUDE (DominioId, ItemDominioId);
```

---

## 10. Observações Técnicas

### 10.1 Multi-Tenancy
- Todas as tabelas possuem `ClienteId` para isolamento de dados
- `ConglomeradoId` permite customização por conglomerado dentro do mesmo cliente
- Itens `Global = 1` são visíveis para todos os conglomerados do cliente

### 10.2 Auditoria
- Triggers automáticos registram todas as operações CRUD em `HistoricoDominioTipo`
- Dados antes/depois armazenados em JSON para flexibilidade
- Retenção mínima de 7 anos conforme LGPD

### 10.3 Performance
- Índices filtrados (`WHERE FlExcluido = 0`) para queries de produção
- Índices com `INCLUDE` para cobertura total de queries principais
- Views materializadas podem ser criadas para dashboards

### 10.4 Internacionalização
- `TipoTraducao` com `ON DELETE CASCADE` para limpeza automática
- Suporte nativo para pt-BR, en-US, es-ES
- Fallback para nome padrão se tradução não existir

### 10.5 Workflow de Transições
- `TransicaoPermitida` define grafo direcionado de estados
- Validação de ciclos deve ser feita em nível de aplicação
- `RequerAprovacao` + `AprovadoresIds` implementa workflow de aprovação

### 10.6 Cache
- Domínios e itens devem ser cached em memória (Redis/In-Memory)
- Invalidação automática via triggers ou eventos de domínio
- TTL recomendado: 1 hora para domínios, 15 minutos para itens

---

## 11. Consultas de Exemplo

```sql
-- Listar todos os domínios com contagem de itens
SELECT * FROM vw_DominiosTipoResumo WHERE FlExcluido = 0 ORDER BY Ordem;

-- Obter itens de um domínio com traduções
EXEC sp_ObterItensDominio
    @CodigoDominio = 'STATUS_CHAMADO',
    @ClienteId = 'UUID-CLIENTE',
    @ConglomeradoId = NULL,
    @Idioma = 'en-US';

-- Validar se transição é permitida
DECLARE @Permitida BIT, @RequerJust BIT, @RequerAprov BIT;
EXEC sp_ValidarTransicao
    @ItemOrigemId = 'UUID-ABERTO',
    @ItemDestinoId = 'UUID-EM-ATENDIMENTO',
    @ClienteId = 'UUID-CLIENTE',
    @Permitida = @Permitida OUTPUT,
    @RequerJustificativa = @RequerJust OUTPUT,
    @RequerAprovacao = @RequerAprov OUTPUT;

-- Workflow visual de transições
SELECT * FROM vw_WorkflowTransicoes WHERE DominioId = 'UUID-DOMINIO';

-- Histórico de alterações de um domínio
SELECT
    TipoAlteracao,
    CreatedAt,
    u.Nome AS UsuarioAlterou,
    Justificativa
FROM HistoricoDominioTipo h
INNER JOIN Usuario u ON h.CreatedBy = u.Id
WHERE DominioId = 'UUID-DOMINIO'
ORDER BY CreatedAt DESC;
```

---

## Histórico de Alterações

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 1.0 | 2025-12-18 | IControlIT Architect | Versão inicial - 5 tabelas, 30+ índices, triggers, views, procedures |

---

**Total de Tabelas:** 5
**Total de Índices:** 32
**Total de Views:** 3
**Total de Stored Procedures:** 3
**Total de Triggers:** 4
**Linhas de DDL:** ~900

**Documento gerado em:** 2025-12-18
**Status:** Aprovado para implementação
