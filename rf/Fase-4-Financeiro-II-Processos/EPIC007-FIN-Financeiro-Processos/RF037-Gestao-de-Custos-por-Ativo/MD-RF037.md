# Modelo de Dados - RF037

**Versão:** 1.0
**Data:** 2025-12-18
**RF Relacionado:** [RF037 - Gestão de Custos por Ativo (TCO)](./RF037.md)
**Banco de Dados:** SQL Server
**Padrões:** Clean Architecture, DDD, CQRS, Multi-tenancy, LGPD

---

## 1. Diagrama de Entidades

```
┌─────────────────────┐         ┌──────────────────────┐
│   Conglomerados     │◄────────┤   CustosAtivo        │
└─────────────────────┘         ├──────────────────────┤
                                │ Id (PK)              │
┌─────────────────────┐         │ ConglomeradoId (FK)  │──┐
│      Ativos         │◄────────┤ AtivoId (FK)         │  │
├─────────────────────┤         │ TipoCustoAtivoId (FK)│  │
│ Id (PK)             │         │ Categoria            │  │
│ Nome                │         │ Descricao            │  │
│ TCOTotal            │         │ Valor                │  │
│ TCOAquisicao        │         │ DataOcorrencia       │  │
│ TCOManutencao       │         │ OrdemServicoId (FK)  │  │
│ TCOLicencas         │         │ ContratoId (FK)      │  │
│ ...                 │         │ FornecedorId (FK)    │  │
└─────────────────────┘         │ FlDepreciacao...     │  │
        │                       └──────────────────────┘  │
        │                                    │            │
        │                       ┌────────────┴────────┐   │
        │                       │ TiposCustoAtivo     │   │
        │                       ├─────────────────────┤   │
        │                       │ Id (PK)             │◄──┘
        │                       │ Nome                │
        │                       │ Categoria           │
        │                       │ FlAtivo             │
        │                       └─────────────────────┘
        │
        │                       ┌──────────────────────┐
        └──────────────────────►│  BeneficiosAtivo     │
                                ├──────────────────────┤
                                │ Id (PK)              │
                                │ AtivoId (FK)         │
                                │ Descricao            │
                                │ TipoBeneficio        │
                                │ Valor                │
                                │ DataOcorrencia       │
                                └──────────────────────┘
```

---

## 2. Entidades

### 2.1 Tabela: CustosAtivo

**Descrição:** Registro individual de todos os custos associados a ativos (aquisição, manutenção, licenças, consumíveis, depreciação). Base para cálculo de TCO (Total Cost of Ownership).

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK para Cliente (multi-tenancy raiz)s (multi-tenancy) |
| AtivoId | UNIQUEIDENTIFIER | NÃO | - | FK para Ativos |
| TipoCustoAtivoId | UNIQUEIDENTIFIER | NÃO | - | FK para TiposCustoAtivo |
| Categoria | INT | NÃO | - | 1=Aquisição, 2=Manutenção, 3=Licenças, 4=Consumíveis, 5=Energia, 6=Depreciação, 7=Suporte, 8=Treinamento |
| Descricao | NVARCHAR(500) | NÃO | - | Descrição do custo |
| Valor | DECIMAL(18,2) | NÃO | - | Valor do custo em reais |
| DataOcorrencia | DATE | NÃO | - | Data em que o custo ocorreu |
| OrdemServicoId | UNIQUEIDENTIFIER | SIM | NULL | FK para OrdensServico (se manutenção) |
| ContratoId | UNIQUEIDENTIFIER | SIM | NULL | FK para Contratos (se licença recorrente) |
| FornecedorId | UNIQUEIDENTIFIER | SIM | NULL | FK para Fornecedores |
| FlDepreciacaoAutomatica | BIT | NÃO | 0 | Se TRUE, depreciação calculada automaticamente |
| NumeroDocumento | NVARCHAR(100) | SIM | NULL | Número da NF, recibo ou documento fiscal |
| Observacoes | NVARCHAR(MAX) | SIM | NULL | Observações adicionais |
| UsuarioCriacaoId | UNIQUEIDENTIFIER | NÃO | - | Usuário que criou o registro |
| DataCriacao | DATETIME2 | NÃO | GETDATE() | Data de criação |
| UsuarioAlteracaoId | UNIQUEIDENTIFIER | SIM | NULL | Usuário que alterou o registro |
| DataAlteracao | DATETIME2 | SIM | NULL | Data de última alteração |
| Ativo | BIT | NÃO | true | Soft delete: false=ativo, true=excluído |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_CustosAtivo | Id | PRIMARY KEY | Chave primária |
| IX_CustosAtivo_AtivoId | AtivoId | NONCLUSTERED | Performance em queries por ativo |
| IX_CustosAtivo_Categoria | Categoria | NONCLUSTERED | Performance em filtros por categoria |
| IX_CustosAtivo_DataOcorrencia | DataOcorrencia | NONCLUSTERED | Performance em filtros por período |
| IX_CustosAtivo_ContratoId | ContratoId | NONCLUSTERED | Queries de custos vinculados a contratos |
| IX_CustosAtivo_FornecedorId | FornecedorId | NONCLUSTERED | Queries de custos por fornecedor |
| IX_CustosAtivo_FlExcluido | FlExcluido, Id INCLUDE (AtivoId, Valor) | NONCLUSTERED | Performance em queries de custos ativos |

#### Constraints

| Nome | Tipo | Definição | Descrição |
|------|------|-----------|-----------|
| PK_CustosAtivo | PRIMARY KEY | Id | Chave primária |
| FK_CustosAtivo_Conglomerado | FOREIGN KEY | ConglomeradoId REFERENCES Conglomerados(Id) | Multi-tenancy |
| FK_CustosAtivo_Ativo | FOREIGN KEY | AtivoId REFERENCES Ativos(Id) | Vinculação ao ativo |
| FK_CustosAtivo_TipoCustoAtivo | FOREIGN KEY | TipoCustoAtivoId REFERENCES TiposCustoAtivo(Id) | Tipo do custo |
| FK_CustosAtivo_OrdemServico | FOREIGN KEY | OrdemServicoId REFERENCES OrdensServico(Id) | Vínculo com OS (se manutenção) |
| FK_CustosAtivo_Contrato | FOREIGN KEY | ContratoId REFERENCES Contratos(Id) | Vínculo com contrato (se licença) |
| FK_CustosAtivo_Fornecedor | FOREIGN KEY | FornecedorId REFERENCES Fornecedores(Id) | Vínculo com fornecedor |
| CHK_CustosAtivo_Valor | CHECK | Valor > 0 | Valor deve ser positivo |
| CHK_CustosAtivo_Categoria | CHECK | Categoria BETWEEN 1 AND 8 | Categoria válida |

---

### 2.2 Tabela: TiposCustoAtivo

**Descrição:** Tipos de custos aplicáveis a ativos (configurável por empresa). Ex: "Compra de Hardware", "Licença Microsoft 365", "Manutenção Preventiva".

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK para Cliente (multi-tenancy raiz)s |
| Nome | NVARCHAR(200) | NÃO | - | Nome do tipo de custo |
| Categoria | INT | NÃO | - | Categoria padrão (1=Aquisição, 2=Manutenção, etc.) |
| FlAtivo | BIT | NÃO | 1 | Se tipo de custo está ativo |
| Ordem | INT | NÃO | 0 | Ordem de exibição |
| UsuarioCriacaoId | UNIQUEIDENTIFIER | NÃO | - | Usuário que criou |
| DataCriacao | DATETIME2 | NÃO | GETDATE() | Data de criação |
| UsuarioAlteracaoId | UNIQUEIDENTIFIER | SIM | NULL | Usuário que alterou |
| DataAlteracao | DATETIME2 | SIM | NULL | Data de alteração |
| Ativo | BIT | NÃO | true | Soft delete: false=ativo, true=excluído |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_TiposCustoAtivo | Id | PRIMARY KEY | Chave primária |
| IX_TiposCustoAtivo_Conglomerado | ClienteId | NONCLUSTERED | Multi-tenancy |
| UQ_TiposCustoAtivo_Nome | ConglomeradoId, Nome | UNIQUE | Nome único por conglomerado |

#### Constraints

| Nome | Tipo | Definição | Descrição |
|------|------|-----------|-----------|
| PK_TiposCustoAtivo | PRIMARY KEY | Id | Chave primária |
| FK_TiposCustoAtivo_Conglomerado | FOREIGN KEY | ConglomeradoId REFERENCES Conglomerados(Id) | Multi-tenancy |
| UQ_TiposCustoAtivo_Nome | UNIQUE | (ConglomeradoId, Nome) WHERE FlExcluido = 0 | Nome único por conglomerado |

---

### 2.3 Tabela: BeneficiosAtivo

**Descrição:** Registro de benefícios financeiros gerados pelo ativo (receita, economia, produtividade). Usado para cálculo de ROI (Return on Investment).

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK para Cliente (multi-tenancy raiz)s |
| AtivoId | UNIQUEIDENTIFIER | NÃO | - | FK para Ativos |
| Descricao | NVARCHAR(500) | NÃO | - | Descrição do benefício |
| TipoBeneficio | INT | NÃO | - | 1=ReceitaGerada, 2=EconomiaObtida, 3=ProdutividadeGanha |
| Valor | DECIMAL(18,2) | NÃO | - | Valor monetário do benefício |
| DataOcorrencia | DATE | NÃO | - | Data em que benefício foi gerado |
| UsuarioCriacaoId | UNIQUEIDENTIFIER | NÃO | - | Usuário que criou |
| DataCriacao | DATETIME2 | NÃO | GETDATE() | Data de criação |
| Ativo | BIT | NÃO | true | Soft delete: false=ativo, true=excluído |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_BeneficiosAtivo | Id | PRIMARY KEY | Chave primária |
| IX_BeneficiosAtivo_AtivoId | AtivoId | NONCLUSTERED | Performance em queries por ativo |
| IX_BeneficiosAtivo_DataOcorrencia | DataOcorrencia | NONCLUSTERED | Filtros por período |

#### Constraints

| Nome | Tipo | Definição | Descrição |
|------|------|-----------|-----------|
| PK_BeneficiosAtivo | PRIMARY KEY | Id | Chave primária |
| FK_BeneficiosAtivo_Conglomerado | FOREIGN KEY | ConglomeradoId REFERENCES Conglomerados(Id) | Multi-tenancy |
| FK_BeneficiosAtivo_Ativo | FOREIGN KEY | AtivoId REFERENCES Ativos(Id) | Vinculação ao ativo |
| CHK_BeneficiosAtivo_Valor | CHECK | Valor >= 0 | Valor não negativo |
| CHK_BeneficiosAtivo_TipoBeneficio | CHECK | TipoBeneficio BETWEEN 1 AND 3 | Tipo válido |

---

### 2.4 Alterações na Tabela Ativos (existente)

**Descrição:** Adicionar colunas de cache de TCO para performance (atualizado via Domain Events).

#### Novas Colunas

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| TCOTotal | DECIMAL(18,2) | NÃO | 0 | TCO total do ativo (cache) |
| TCOAquisicao | DECIMAL(18,2) | NÃO | 0 | TCO de aquisição (CAPEX) |
| TCOManutencao | DECIMAL(18,2) | NÃO | 0 | TCO de manutenção (OPEX) |
| TCOLicencas | DECIMAL(18,2) | NÃO | 0 | TCO de licenças (OPEX) |
| TCOConsumiveis | DECIMAL(18,2) | NÃO | 0 | TCO de consumíveis (OPEX) |
| TCODepreciacao | DECIMAL(18,2) | NÃO | 0 | Depreciação acumulada |
| TCOOutros | DECIMAL(18,2) | NÃO | 0 | Outros custos (energia, suporte, treinamento) |
| DataUltimaAtualizacaoTCO | DATETIME2 | SIM | NULL | Data da última atualização do TCO |
| FlCustoAcimaDaMedia | BIT | NÃO | 0 | Se TRUE, ativo com custo >30% acima da média |
| PercentualAcimaMedia | DECIMAL(5,2) | NÃO | 0 | Percentual acima da média (se FlCustoAcimaDaMedia=TRUE) |
| FlDepreciavel | BIT | NÃO | 1 | Se ativo é depreciável |
| FlDepreciadoTotalmente | BIT | NÃO | 0 | Se ativo já foi totalmente depreciado |
| ValorResidual | DECIMAL(18,2) | NÃO | 0 | Valor residual após depreciação total |

---

## 3. Relacionamentos

| Tabela Origem | Cardinalidade | Tabela Destino | Descrição |
|---------------|---------------|----------------|-----------|
| Conglomerados | 1:N | CustosAtivo | Conglomerado possui muitos custos de ativos |
| Ativos | 1:N | CustosAtivo | Ativo possui muitos custos |
| TiposCustoAtivo | 1:N | CustosAtivo | Tipo de custo usado em muitos lançamentos |
| OrdensServico | 1:N | CustosAtivo | Ordem de serviço pode gerar múltiplos custos |
| Contratos | 1:N | CustosAtivo | Contrato pode ter múltiplos custos recorrentes |
| Fornecedores | 1:N | CustosAtivo | Fornecedor pode ter múltiplos custos |
| Ativos | 1:N | BeneficiosAtivo | Ativo pode gerar múltiplos benefícios |

---

## 4. DDL - SQL Server

```sql
-- =============================================
-- RF037 - Gestão de Custos por Ativo (TCO)
-- Modelo de Dados
-- Data: 2025-12-18
-- =============================================

-- ---------------------------------------------
-- Tabela: TiposCustoAtivo
-- ---------------------------------------------
CREATE TABLE TiposCustoAtivo (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    Nome NVARCHAR(200) NOT NULL,
    Categoria INT NOT NULL, -- 1=Aquisição, 2=Manutenção, 3=Licenças, 4=Consumíveis, 5=Energia, 6=Depreciação, 7=Suporte, 8=Treinamento
    FlFlExcluido BIT NOT NULL DEFAULT 0,
    Ordem INT NOT NULL DEFAULT 0,

    -- Auditoria
    UsuarioCriacaoId UNIQUEIDENTIFIER NOT NULL,
    DataCriacao DATETIME2 NOT NULL DEFAULT GETDATE(),
    UsuarioAlteracaoId UNIQUEIDENTIFIER NULL,
    DataAlteracao DATETIME2 NULL,
    FlExcluido BIT NOT NULL DEFAULT 0,

    -- Foreign Keys
    CONSTRAINT FK_TiposCustoAtivo_Conglomerado
        FOREIGN KEY (ConglomeradoId) REFERENCES Conglomerados(Id),

    -- Unique Constraints
    CONSTRAINT UQ_TiposCustoAtivo_Nome
        UNIQUE (ConglomeradoId, Nome)
);

-- Índices
CREATE NONCLUSTERED INDEX IX_TiposCustoAtivo_Conglomerado
    ON TiposCustoAtivo(ConglomeradoId)
    WHERE FlExcluido = 0;

-- Comentários
EXEC sp_addextendedproperty
    @name = N'MS_Description', @value = N'Tipos de custos aplicáveis a ativos (configurável por empresa)',
    @level0type = N'SCHEMA', @level0name = N'dbo',
    @level1type = N'TABLE', @level1name = N'TiposCustoAtivo';

-- ---------------------------------------------
-- Tabela: CustosAtivo
-- ---------------------------------------------
CREATE TABLE CustosAtivo (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    AtivoId UNIQUEIDENTIFIER NOT NULL,
    TipoCustoAtivoId UNIQUEIDENTIFIER NOT NULL,
    Categoria INT NOT NULL, -- 1=Aquisição, 2=Manutenção, 3=Licenças, 4=Consumíveis, 5=Energia, 6=Depreciação, 7=Suporte, 8=Treinamento
    Descricao NVARCHAR(500) NOT NULL,
    Valor DECIMAL(18,2) NOT NULL,
    DataOcorrencia DATE NOT NULL,
    OrdemServicoId UNIQUEIDENTIFIER NULL,
    ContratoId UNIQUEIDENTIFIER NULL,
    FornecedorId UNIQUEIDENTIFIER NULL,
    FlDepreciacaoAutomatica BIT NOT NULL DEFAULT 0,
    NumeroDocumento NVARCHAR(100) NULL,
    Observacoes NVARCHAR(MAX) NULL,

    -- Auditoria
    UsuarioCriacaoId UNIQUEIDENTIFIER NOT NULL,
    DataCriacao DATETIME2 NOT NULL DEFAULT GETDATE(),
    UsuarioAlteracaoId UNIQUEIDENTIFIER NULL,
    DataAlteracao DATETIME2 NULL,
    FlExcluido BIT NOT NULL DEFAULT 0,

    -- Foreign Keys
    CONSTRAINT FK_CustosAtivo_Conglomerado
        FOREIGN KEY (ConglomeradoId) REFERENCES Conglomerados(Id),
    CONSTRAINT FK_CustosAtivo_Ativo
        FOREIGN KEY (AtivoId) REFERENCES Ativos(Id),
    CONSTRAINT FK_CustosAtivo_TipoCustoAtivo
        FOREIGN KEY (TipoCustoAtivoId) REFERENCES TiposCustoAtivo(Id),
    CONSTRAINT FK_CustosAtivo_OrdemServico
        FOREIGN KEY (OrdemServicoId) REFERENCES OrdensServico(Id),
    CONSTRAINT FK_CustosAtivo_Contrato
        FOREIGN KEY (ContratoId) REFERENCES Contratos(Id),
    CONSTRAINT FK_CustosAtivo_Fornecedor
        FOREIGN KEY (FornecedorId) REFERENCES Fornecedores(Id),

    -- Check Constraints
    CONSTRAINT CHK_CustosAtivo_Valor
        CHECK (Valor > 0),
    CONSTRAINT CHK_CustosAtivo_Categoria
        CHECK (Categoria BETWEEN 1 AND 8)
);

-- Índices
CREATE NONCLUSTERED INDEX IX_CustosAtivo_AtivoId
    ON CustosAtivo(AtivoId)
    WHERE FlExcluido = 0;

CREATE NONCLUSTERED INDEX IX_CustosAtivo_Categoria
    ON CustosAtivo(Categoria)
    WHERE FlExcluido = 0;

CREATE NONCLUSTERED INDEX IX_CustosAtivo_DataOcorrencia
    ON CustosAtivo(DataOcorrencia DESC)
    WHERE FlExcluido = 0;

CREATE NONCLUSTERED INDEX IX_CustosAtivo_ContratoId
    ON CustosAtivo(ContratoId)
    WHERE FlExcluido = 0 AND ContratoId IS NOT NULL;

CREATE NONCLUSTERED INDEX IX_CustosAtivo_FornecedorId
    ON CustosAtivo(FornecedorId)
    WHERE FlExcluido = 0 AND FornecedorId IS NOT NULL;

CREATE NONCLUSTERED INDEX IX_CustosAtivo_FlExcluido
    ON CustosAtivo(FlExcluido, Id)
    INCLUDE (AtivoId, Valor, DataOcorrencia, Categoria);

-- Comentários
EXEC sp_addextendedproperty
    @name = N'MS_Description', @value = N'Registro de custos associados a ativos (base para cálculo de TCO)',
    @level0type = N'SCHEMA', @level0name = N'dbo',
    @level1type = N'TABLE', @level1name = N'CustosAtivo';

-- ---------------------------------------------
-- Tabela: BeneficiosAtivo
-- ---------------------------------------------
CREATE TABLE BeneficiosAtivo (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    AtivoId UNIQUEIDENTIFIER NOT NULL,
    Descricao NVARCHAR(500) NOT NULL,
    TipoBeneficio INT NOT NULL, -- 1=ReceitaGerada, 2=EconomiaObtida, 3=ProdutividadeGanha
    Valor DECIMAL(18,2) NOT NULL,
    DataOcorrencia DATE NOT NULL,

    -- Auditoria
    UsuarioCriacaoId UNIQUEIDENTIFIER NOT NULL,
    DataCriacao DATETIME2 NOT NULL DEFAULT GETDATE(),
    FlExcluido BIT NOT NULL DEFAULT 0,

    -- Foreign Keys
    CONSTRAINT FK_BeneficiosAtivo_Conglomerado
        FOREIGN KEY (ConglomeradoId) REFERENCES Conglomerados(Id),
    CONSTRAINT FK_BeneficiosAtivo_Ativo
        FOREIGN KEY (AtivoId) REFERENCES Ativos(Id),

    -- Check Constraints
    CONSTRAINT CHK_BeneficiosAtivo_Valor
        CHECK (Valor >= 0),
    CONSTRAINT CHK_BeneficiosAtivo_TipoBeneficio
        CHECK (TipoBeneficio BETWEEN 1 AND 3)
);

-- Índices
CREATE NONCLUSTERED INDEX IX_BeneficiosAtivo_AtivoId
    ON BeneficiosAtivo(AtivoId)
    WHERE FlExcluido = 0;

CREATE NONCLUSTERED INDEX IX_BeneficiosAtivo_DataOcorrencia
    ON BeneficiosAtivo(DataOcorrencia DESC)
    WHERE FlExcluido = 0;

-- Comentários
EXEC sp_addextendedproperty
    @name = N'MS_Description', @value = N'Registro de benefícios financeiros gerados por ativos (usado para cálculo de ROI)',
    @level0type = N'SCHEMA', @level0name = N'dbo',
    @level1type = N'TABLE', @level1name = N'BeneficiosAtivo';

-- ---------------------------------------------
-- Alterações na Tabela Ativos (adicionar colunas de TCO)
-- ---------------------------------------------
ALTER TABLE Ativos ADD
    TCOTotal DECIMAL(18,2) NOT NULL DEFAULT 0,
    TCOAquisicao DECIMAL(18,2) NOT NULL DEFAULT 0,
    TCOManutencao DECIMAL(18,2) NOT NULL DEFAULT 0,
    TCOLicencas DECIMAL(18,2) NOT NULL DEFAULT 0,
    TCOConsumiveis DECIMAL(18,2) NOT NULL DEFAULT 0,
    TCODepreciacao DECIMAL(18,2) NOT NULL DEFAULT 0,
    TCOOutros DECIMAL(18,2) NOT NULL DEFAULT 0,
    DataUltimaAtualizacaoTCO DATETIME2 NULL,
    FlCustoAcimaDaMedia BIT NOT NULL DEFAULT 0,
    PercentualAcimaMedia DECIMAL(5,2) NOT NULL DEFAULT 0,
    FlDepreciavel BIT NOT NULL DEFAULT 1,
    FlDepreciadoTotalmente BIT NOT NULL DEFAULT 0,
    ValorResidual DECIMAL(18,2) NOT NULL DEFAULT 0;

-- Índice para queries de análise de TCO
CREATE NONCLUSTERED INDEX IX_Ativos_TCO
    ON Ativos(TCOTotal DESC, FlCustoAcimaDaMedia)
    WHERE FlExcluido = 0;

-- Comentários
EXEC sp_addextendedproperty
    @name = N'MS_Description', @value = N'TCO total do ativo (cache, atualizado via Domain Events)',
    @level0type = N'SCHEMA', @level0name = N'dbo',
    @level1type = N'TABLE', @level1name = N'Ativos',
    @level2type = N'COLUMN', @level2name = N'TCOTotal';
```

---

## 5. Dados Iniciais (Seed)

```sql
-- =============================================
-- Seed: Tipos de Custo Padrão
-- =============================================

-- ATENÇÃO: Substituir @ConglomeradoId e @UsuarioSistemaId pelos valores reais

DECLARE @ClienteId UNIQUEIDENTIFIER = '00000000-0000-0000-0000-000000000001';
DECLARE @UsuarioSistemaId UNIQUEIDENTIFIER = '00000000-0000-0000-0000-000000000001';

INSERT INTO TiposCustoAtivo (Id, ConglomeradoId, Nome, Categoria, FlAtivo, Ordem, UsuarioCriacaoId, DataCriacao, Ativo)
VALUES
    (NEWID(), @ConglomeradoId, 'Aquisição de Hardware', 1, 1, 1, @UsuarioSistemaId, GETDATE(), 0),
    (NEWID(), @ConglomeradoId, 'Aquisição de Software', 1, 1, 2, @UsuarioSistemaId, GETDATE(), 0),
    (NEWID(), @ConglomeradoId, 'Manutenção Preventiva', 2, 1, 3, @UsuarioSistemaId, GETDATE(), 0),
    (NEWID(), @ConglomeradoId, 'Manutenção Corretiva', 2, 1, 4, @UsuarioSistemaId, GETDATE(), 0),
    (NEWID(), @ConglomeradoId, 'Licença Microsoft 365', 3, 1, 5, @UsuarioSistemaId, GETDATE(), 0),
    (NEWID(), @ConglomeradoId, 'Licença Antivírus', 3, 1, 6, @UsuarioSistemaId, GETDATE(), 0),
    (NEWID(), @ConglomeradoId, 'Toner / Tinta', 4, 1, 7, @UsuarioSistemaId, GETDATE(), 0),
    (NEWID(), @ConglomeradoId, 'Papel', 4, 1, 8, @UsuarioSistemaId, GETDATE(), 0),
    (NEWID(), @ConglomeradoId, 'Peças de Reposição', 4, 1, 9, @UsuarioSistemaId, GETDATE(), 0),
    (NEWID(), @ConglomeradoId, 'Energia Elétrica', 5, 1, 10, @UsuarioSistemaId, GETDATE(), 0),
    (NEWID(), @ConglomeradoId, 'Depreciação Mensal', 6, 1, 11, @UsuarioSistemaId, GETDATE(), 0),
    (NEWID(), @ConglomeradoId, 'Suporte Técnico', 7, 1, 12, @UsuarioSistemaId, GETDATE(), 0),
    (NEWID(), @ConglomeradoId, 'Treinamento de Usuários', 8, 1, 13, @UsuarioSistemaId, GETDATE(), 0),
    (NEWID(), @ConglomeradoId, 'Upgrade de Hardware', 2, 1, 14, @UsuarioSistemaId, GETDATE(), 0),
    (NEWID(), @ConglomeradoId, 'Upgrade de Software', 2, 1, 15, @UsuarioSistemaId, GETDATE(), 0);

-- Total: 15 tipos de custo padrão
```

---

## 6. Observações

### 6.1. Decisões de Modelagem

**Cache de TCO na Tabela Ativos:**
- Adicionadas colunas `TCOTotal`, `TCOAquisicao`, `TCOManutencao`, etc. diretamente na tabela `Ativos` para performance
- Atualização via Domain Events (`CustoAtivoCriadoDomainEvent`, `CustoAtivoAtualizadoDomainEvent`, `CustoAtivoExcluidoDomainEvent`)
- Evita necessidade de `SUM` em cada query de listagem de ativos

**Categoria Duplicada (Enum + Campo):**
- `TipoCustoAtivo.Categoria` define categoria padrão do tipo
- `CustoAtivo.Categoria` permite reclassificação manual se necessário
- Facilita análise de TCO por categoria sem JOIN

**Vinculação Opcional a OrdemServico/Contrato:**
- `CustosAtivo.OrdemServicoId` obrigatório apenas para custos de manutenção (validado no backend)
- `CustosAtivo.ContratoId` obrigatório apenas para custos de licenças recorrentes
- Permite rastreabilidade completa de origem dos custos

### 6.2. Performance

**Índices Filtrados:**
- Todos os índices usam `WHERE FlExcluido = 0` para ignorar registros excluídos
- Reduz tamanho do índice e melhora performance de queries ativas

**Agregação em Tempo Real:**
- Cálculo de TCO é disparado por Domain Events (MediatR)
- Hangfire job roda diariamente para recalcular TCO de todos os ativos (validação/correção)

**Queries de Análise:**
- `IX_Ativos_TCO` otimizado para dashboards e comparações
- `IX_CustosAtivo_FlExcluido` com `INCLUDE` para queries frequentes

### 6.3. Regras de Negócio Implementadas no Modelo

**RN-037-001:** Multi-tenancy via `ConglomeradoId` em todas as tabelas
**RN-037-002:** Custo de aquisição único validado no backend (não constraint DB)
**RN-037-003:** Depreciação automática via `FlDepreciacaoAutomatica = TRUE` e job Hangfire
**RN-037-006:** TCO indireto (energia, suporte) via categoria `TCOOutros`
**RN-037-011:** Soft delete: false=ativo, true=excluído em todas as entidades com `FlExcluido = BIT`

---

## 7. Migrações e Compatibilidade

**Impacto em Tabelas Existentes:**
- **Ativos:** Adiciona 13 novas colunas (TCO, depreciação, flags)
- **Migrations:** Requer migration para `ALTER TABLE Ativos` com valores default

**Script de Migração (EF Core):**
```csharp
public partial class AddTCOColumnsToAtivos : Migration
{
    protected override void Up(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.AddColumn<decimal>(
            name: "TCOTotal",
            table: "Ativos",
            type: "decimal(18,2)",
            nullable: false,
            defaultValue: 0m);

        // ... (adicionar demais colunas)

        // Recalcular TCO para ativos existentes
        migrationBuilder.Sql(@"
            UPDATE A SET
                A.TCOTotal = ISNULL(SUM(CA.Valor), 0)
            FROM Ativos A
            LEFT JOIN CustosAtivo CA ON CA.AtivoId = A.Id AND CA.FlExcluido = 0
            WHERE A.FlExcluido = 0
            GROUP BY A.Id
        ");
    }
}
```

---

## 8. Estatísticas do Modelo

**Total de Tabelas:** 3 novas (TiposCustoAtivo, CustosAtivo, BeneficiosAtivo) + 1 alterada (Ativos)
**Total de Campos:** 54 campos
**Total de Índices:** 11 índices (incluindo PKs)
**Total de FKs:** 9 foreign keys
**Total de Constraints:** 6 check constraints
**Estimativa de Linhas (1 ano):** ~50.000 custos/ano (empresa média com 500 ativos)

---

## Histórico de Alterações

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 1.0 | 2025-12-18 | Architect Agent | Versão inicial - 3 tabelas + alterações em Ativos |
